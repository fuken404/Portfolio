from django.db import models

# Los campos traducibles van en pares `<campo>_es` (obligatorio) y `<campo>_en`
# (opcional: si está vacío, la API devuelve el español). Ver i18n.py.


class Profile(models.Model):
    """Datos principales del portafolio. Se espera un único registro."""

    name = models.CharField('nombre', max_length=120)
    role_es = models.CharField('rol (ES)', max_length=120)
    role_en = models.CharField('rol (EN)', max_length=120, blank=True)
    tagline_es = models.CharField('frase corta (ES)', max_length=240)
    tagline_en = models.CharField('frase corta (EN)', max_length=240, blank=True)
    bio_es = models.TextField('biografía (ES)')
    bio_en = models.TextField('biografía (EN)', blank=True)
    focus_es = models.CharField('enfoque (ES)', max_length=120, blank=True)
    focus_en = models.CharField('enfoque (EN)', max_length=120, blank=True)
    languages_es = models.CharField('idiomas (ES)', max_length=120, blank=True, help_text='Ej. Español nativo · Inglés avanzado')
    languages_en = models.CharField('idiomas (EN)', max_length=120, blank=True)
    location = models.CharField('ubicación', max_length=120, blank=True)
    email = models.EmailField('correo', blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    available = models.BooleanField('disponible para proyectos', default=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfil'

    def __str__(self):
        return self.name


class Skill(models.Model):
    class Category(models.TextChoices):
        LANGUAGES = 'languages', 'Lenguajes'
        BACKEND = 'backend', 'Backend'
        FRONTEND = 'frontend', 'Frontend y móvil'
        DATA = 'data', 'Datos'
        AI = 'ai', 'IA aplicada'
        TOOLS = 'tools', 'Herramientas'
        PRACTICES = 'practices', 'Prácticas'

    # Las tecnologías suelen llamarse igual en ambos idiomas (Django, React...);
    # name_en solo hace falta para prácticas como "Código limpio".
    name_es = models.CharField('nombre (ES)', max_length=60, unique=True)
    name_en = models.CharField('nombre (EN)', max_length=60, blank=True)
    slug = models.SlugField(unique=True)
    category = models.CharField('categoría', max_length=20, choices=Category.choices)
    level = models.PositiveSmallIntegerField(
        'nivel (1-5)', null=True, blank=True,
        help_text='Vacío para no mostrar el medidor (útil en prácticas y metodologías).',
    )
    is_core = models.BooleanField('tecnología principal', default=False)
    show_in_stack = models.BooleanField(
        'mostrar en Stack', default=True,
        help_text='Desmarcar para tecnologías que solo aparecen en proyectos.',
    )
    order = models.PositiveSmallIntegerField('orden', default=0)

    class Meta:
        # Las principales van primero en cada categoría; luego el orden manual.
        ordering = ['-is_core', 'order', 'name_es']
        verbose_name = 'habilidad'
        verbose_name_plural = 'habilidades'

    def __str__(self):
        return self.name_es


class Project(models.Model):
    slug = models.SlugField(unique=True)
    title_es = models.CharField('título (ES)', max_length=120)
    title_en = models.CharField('título (EN)', max_length=120, blank=True)
    summary_es = models.CharField('resumen (ES)', max_length=280)
    summary_en = models.CharField('resumen (EN)', max_length=280, blank=True)
    description_es = models.TextField('descripción (ES)', blank=True)
    description_en = models.TextField('descripción (EN)', blank=True)
    skills = models.ManyToManyField(Skill, related_name='projects', verbose_name='tecnologías', blank=True)
    year = models.PositiveSmallIntegerField('año')
    repo_url = models.URLField('repositorio', blank=True)
    live_url = models.URLField('demo', blank=True)
    image = models.ImageField('imagen', upload_to='projects/', blank=True)
    featured = models.BooleanField('destacado', default=False)
    order = models.PositiveSmallIntegerField('orden', default=0)

    class Meta:
        ordering = ['order', '-year']
        verbose_name = 'proyecto'
        verbose_name_plural = 'proyectos'

    def __str__(self):
        return self.title_es


class Experience(models.Model):
    company = models.CharField('empresa', max_length=120)
    position_es = models.CharField('cargo (ES)', max_length=120)
    position_en = models.CharField('cargo (EN)', max_length=120, blank=True)
    location_es = models.CharField('lugar (ES)', max_length=120, blank=True, help_text='Ej. Bogotá, Colombia · Híbrido')
    location_en = models.CharField('lugar (EN)', max_length=120, blank=True)
    start = models.DateField('inicio')
    end = models.DateField('fin', null=True, blank=True, help_text='Vacío si es el trabajo actual')
    description_es = models.TextField('descripción (ES)')
    description_en = models.TextField('descripción (EN)', blank=True)
    highlights_es = models.JSONField('logros (ES)', default=list, blank=True, help_text='Lista de textos')
    highlights_en = models.JSONField('logros (EN)', default=list, blank=True, help_text='Lista de textos')
    order = models.PositiveSmallIntegerField('orden', default=0, help_text='Menor aparece primero')

    class Meta:
        ordering = ['order', '-start']
        verbose_name = 'experiencia'
        verbose_name_plural = 'experiencia'

    def __str__(self):
        return f'{self.position_es} · {self.company}'


class Education(models.Model):
    institution = models.CharField('institución', max_length=120)
    degree_es = models.CharField('título (ES)', max_length=120)
    degree_en = models.CharField('título (EN)', max_length=120, blank=True)
    location = models.CharField('ubicación', max_length=120, blank=True)
    start = models.DateField('inicio')
    end = models.DateField('fin', null=True, blank=True, help_text='Vacío si está en curso')

    class Meta:
        ordering = ['-start']
        verbose_name = 'educación'
        verbose_name_plural = 'educación'

    def __str__(self):
        return f'{self.degree_es} · {self.institution}'


class Certification(models.Model):
    class Category(models.TextChoices):
        DEVELOPMENT = 'development', 'Desarrollo de software'
        SECURITY = 'security', 'Desarrollo seguro y ciberseguridad'
        AGILE = 'agile', 'Metodologías ágiles y diseño'
        INFRA = 'infra', 'Redes e infraestructura'

    name_es = models.CharField('nombre (ES)', max_length=160)
    name_en = models.CharField('nombre (EN)', max_length=160, blank=True)
    slug = models.SlugField(
        unique=True,
        help_text='Nombre del archivo en content/certificates/<categoría>/ (ver attach_certificates).',
    )
    issuer = models.CharField('entidad', max_length=120)
    category = models.CharField('categoría', max_length=20, choices=Category.choices)
    issued = models.DateField('fecha de expedición', help_text='Se muestra solo mes y año')
    hours = models.PositiveSmallIntegerField('horas', null=True, blank=True)
    credential_id = models.CharField('ID de credencial', max_length=80, blank=True)
    credential_url = models.URLField('enlace de verificación', blank=True)
    file = models.FileField('certificado', upload_to='certificates/', blank=True, help_text='PDF o imagen')

    class Meta:
        ordering = ['-issued']
        verbose_name = 'certificación'
        verbose_name_plural = 'certificaciones'

    def __str__(self):
        return self.name_es


class ContactMessage(models.Model):
    name = models.CharField('nombre', max_length=120)
    email = models.EmailField('correo')
    message = models.TextField('mensaje')
    lang = models.CharField('idioma', max_length=5, blank=True, help_text='Idioma en que se vio la página')
    created_at = models.DateTimeField('recibido', auto_now_add=True)
    read = models.BooleanField('leído', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'mensaje'
        verbose_name_plural = 'mensajes'

    def __str__(self):
        return f'{self.name} <{self.email}>'
