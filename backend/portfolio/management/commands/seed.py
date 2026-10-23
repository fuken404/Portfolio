"""
Contenido base del portafolio, en español e inglés.

Fuentes: hoja de vida (enfoque de desarrollador), LinkedIn (habilidades,
certificaciones y experiencia que no están en el CV) y repositorios públicos
de github.com/fuken404 (proyectos).

Los niveles (1-5) de las habilidades son un borrador para ajustar desde el admin.
"""

from datetime import date

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from portfolio.models import Certification, Education, Experience, Profile, Project, Skill

PROFILE = dict(
    name='Maycol Fuquene',
    role_es='Ingeniero de Software · Backend / Full Stack',
    role_en='Software Engineer · Backend / Full Stack',
    tagline_es=(
        'Construyo servicios backend e integraciones entre sistemas con Python y Django, '
        'y llevo modelos de lenguaje a soluciones reales de automatización.'
    ),
    tagline_en=(
        'I build backend services and system integrations with Python and Django, '
        'and bring language models into real automation solutions.'
    ),
    bio_es=(
        'Ingeniero de Software enfocado en backend con Python. Construyo servicios y APIs REST con '
        'Django y Django REST Framework, conecto sistemas entre sí y proceso datos con SQL y Pandas '
        'sobre bases de datos relacionales. Integro modelos de lenguaje en soluciones reales: '
        'desarrollo agentes de IA con OpenAI que automatizan procesos de negocio. Trabajo de la mano '
        'de los clientes para convertir requerimientos en software que funciona, y complemento mi '
        'stack con React en el frontend y una base sólida en Java y Spring Boot.'
    ),
    bio_en=(
        'Software Engineer focused on backend development with Python. I build services and REST '
        'APIs with Django and Django REST Framework, connect systems to each other, and process data '
        'with SQL and Pandas on relational databases. I bring language models into real solutions, '
        'building OpenAI-powered AI agents that automate business processes. I work closely with '
        'clients to turn requirements into software that works, and I round out my stack with React '
        'on the frontend and a solid foundation in Java and Spring Boot.'
    ),
    focus_es='Backend, integraciones e IA aplicada',
    focus_en='Backend, integrations and applied AI',
    languages_es='Español nativo · Inglés avanzado',
    languages_en='Native Spanish · Advanced English',
    location='Bogotá, Colombia',
    email='maycolfuquene.dev@outlook.com',
    github='https://github.com/fuken404',
    linkedin='https://www.linkedin.com/in/maycol-fuquene/',
    available=True,
)

# (nombre ES, nombre EN o '', nivel o None, principal)
# Dentro de cada categoría, en orden de relevancia para reclutadores
# (las principales se muestran primero de todas formas, ver Skill.Meta.ordering).
SKILLS = {
    'languages': [
        ('Python', '', 4, True),
        ('SQL', '', 4, True),
        ('JavaScript', '', 4, False),
        ('TypeScript', '', 3, False),
        ('Java', '', 4, False),
        ('PHP', '', 3, False),
        ('C#', '', 3, False),
        ('HTML5', '', 4, False),
        ('CSS3', '', 4, False),
        ('C++', '', 3, False),
        ('Visual Basic', '', 4, False),
    ],
    'backend': [
        ('Django', '', 4, True),
        ('FastAPI', '', 4, True),
        ('Django REST Framework', '', 4, False),
        ('APIs REST', 'REST APIs', 4, False),
        ('Node.js', '', 4, False),
        ('Spring Boot', '', 4, False),
        ('GraphQL', '', 2, False),
        ('Celery', '', 3, False),
        ('JWT', '', 4, False),
        ('Symfony', '', 3, False),
    ],
    'frontend': [
        ('React', '', 4, True),
        ('Angular', '', 4, False),
        ('React Native', '', 2, False),
        ('Flutter', '', 2, False),
        ('Sass / SCSS', '', 4, False),
        ('Bootstrap', '', 3, False),
        ('AJAX', '', 3, False),
    ],
    'data': [
        ('PostgreSQL', '', 4, True),
        ('MySQL', '', 4, False),
        ('MongoDB', '', 4, False),
        ('Redis', '', 2, False),
        ('Pandas', '', 3, False),
        ('SQLite', '', 4, False),
        ('Firebase', '', 4, False),
        ('MariaDB', '', 3, False),
        ('Power BI', '', 2, False),
        ('Streamlit', '', 3, False),
    ],
    'ai': [
        ('Agentes de IA', 'AI agents', None, True),
        ('Integración de LLMs', 'LLM integration', None, False),
        ('OpenAI API', '', None, False),
        ('LangChain', '', None, False),
        ('Machine learning', '', None, False),
        ('Claude', '', None, False),
        ('ChatGPT', '', None, False),
    ],
    'tools': [
        ('Docker', '', 4, False),
        ('Git', '', 4, False),
        ('AWS', '', 4, False),
        ('Linux', '', 4, False),
        ('GitHub', '', 4, False),
        ('Azure', '', 2, False),
        ('GCP', '', 2, False),
        ('Nginx', '', 3, False),
        ('Jira', '', 4, False),
        ('Certificados SSL', 'SSL certificates', 3, False),
        ('Notion', '', 4, False),
    ],
    'practices': [
        ('Pruebas de software', 'Software testing', None, False),
        ('Scrum', '', None, False),
        ('Principios SOLID', 'SOLID principles', None, False),
        ('Código limpio', 'Clean code', None, False),
        ('Programación orientada a objetos', 'Object-oriented programming', None, False),
        ('Sistemas distribuidos', 'Distributed systems', None, False),
        ('Desarrollo seguro', 'Secure coding', None, False),
        ('Revisión de código', 'Code review', None, False),
        ('Patrón MVC', 'MVC pattern', None, False),
        ('Kanban', '', None, False),
        ('Design Thinking', '', None, False),
    ],
}

# Tecnologías que aparecen en proyectos pero no en la sección Stack.
PROJECT_ONLY_SKILLS = [
    ('SQLAlchemy', 'data'), ('Alembic', 'data'),
    ('Express', 'backend'), ('Prisma', 'data'), ('Socket.io', 'backend'), ('Sequelize', 'data'),
 ('Groq', 'ai'), ('Telegram Bot API', 'backend'),
    ('Vercel', 'tools'), ('Fly.io', 'tools'),
]

PROJECTS = [
    dict(
        slug='habitare', year=2026, featured=True,
        repo_url='https://github.com/fuken404/Habitare',
        title_es='Habitare', title_en='Habitare',
        summary_es=(
            'Plataforma para administrar conjuntos residenciales: visitas, paquetes, PQRS, reservas de '
            'zonas comunes, sorteo de parqueaderos y facturación, con varios conjuntos en una sola '
            'instalación.'
        ),
        summary_en=(
            'Platform for managing residential complexes: visitors, packages, requests and complaints, '
            'common-area bookings, parking lotteries and billing, serving multiple complexes from a '
            'single deployment.'
        ),
        description_es=(
            'API en FastAPI asíncrono con SQLAlchemy y Alembic, organizada en 19 módulos con control de '
            'acceso por roles, aislamiento de datos por conjunto y eventos con patrón outbox. Incluye un '
            'panel web en React + TypeScript para administración y portería, y apps móviles para '
            'residentes en Flutter y React Native.'
        ),
        description_en=(
            'Async FastAPI API with SQLAlchemy and Alembic, organized into 19 modules with role-based '
            'access control, per-complex data isolation and outbox-pattern events. Includes a React + '
            'TypeScript web panel for management and front desk, and resident mobile apps in Flutter '
            'and React Native.'
        ),
        stack=['Python', 'FastAPI', 'SQLAlchemy', 'Alembic', 'PostgreSQL', 'React', 'TypeScript',
               'Flutter', 'React Native', 'Docker'],
    ),
    dict(
        slug='brickbybrick', year=2026, featured=True,
        repo_url='https://github.com/fuken404/BrickByBrick',
        title_es='BrickByBrick', title_en='BrickByBrick',
        summary_es=(
            'Plataforma para donar materiales de construcción excedentes en Bogotá: conecta '
            'constructoras con familias y emprendimientos, con trazabilidad de entregas y constancias '
            'tributarias en PDF.'
        ),
        summary_en=(
            'Platform for donating surplus construction materials in Bogotá: it connects builders '
            'with families and small businesses, with delivery tracking and PDF tax certificates.'
        ),
        description_es=(
            'Microservicios (autenticación, usuarios, materiales, eventos, publicaciones y '
            'notificaciones) detrás de un API Gateway; JWT con refresh tokens rotativos, chat y '
            'notificaciones en tiempo real con Socket.io, tareas programadas y panel de administración '
            'con métricas.'
        ),
        description_en=(
            'Microservices (auth, users, materials, events, posts and notifications) behind an API '
            'Gateway; JWT with rotating refresh tokens, real-time chat and notifications with '
            'Socket.io, scheduled jobs and an admin dashboard with metrics.'
        ),
        stack=['Angular', 'TypeScript', 'Node.js', 'Express', 'PostgreSQL', 'Prisma', 'Socket.io', 'JWT', 'Docker'],
    ),
    dict(
        slug='dante-ai', year=2026, featured=True,
        repo_url='https://github.com/fuken404/DanteAI',
        title_es='DanteAI', title_en='DanteAI',
        summary_es=(
            'Asistente personal en Telegram con memoria persistente: conversa por texto, notas de voz '
            'e imágenes usando Claude y Groq, y lee los enlaces que se le envían.'
        ),
        summary_en=(
            'Personal Telegram assistant with persistent memory: it chats through text, voice notes '
            'and images using Claude and Groq, and reads the links it is sent.'
        ),
        description_es='Bot asíncrono con webhooks, memoria en PostgreSQL y despliegue en Fly.io con Docker.',
        description_en='Async bot with webhooks, memory stored in PostgreSQL and deployed on Fly.io with Docker.',
        stack=['Python', 'Claude', 'Groq', 'Telegram Bot API', 'PostgreSQL', 'Docker', 'Fly.io'],
    ),
    dict(
        slug='sorora', year=2025,
        repo_url='https://github.com/fuken404/Sorora',
        title_es='Sorora', title_en='Sorora',
        summary_es=(
            'Plataforma web de alerta y protección para mujeres basada en microservicios, con módulos '
            'de albergues y alertas en tiempo real.'
        ),
        summary_en=(
            'Alert and protection web platform for women built on microservices, with shelter and '
            'real-time alert modules.'
        ),
        stack=['Python', 'FastAPI', 'MongoDB', 'Docker'],
    ),
    dict(
        slug='sistema-experto-diagnostico', year=2025,
        repo_url='https://github.com/fuken404/DiagnosticoMantenimientoEquiposComputo',
        title_es='Sistema experto de diagnóstico', title_en='Hardware diagnosis expert system',
        summary_es=(
            'Sistema experto que diagnostica fallas de hardware en equipos de cómputo a partir de '
            'reglas, con autenticación por roles y un panel para crear nuevas reglas.'
        ),
        summary_en=(
            'Rule-based expert system that diagnoses computer hardware faults, with role-based '
            'authentication and a panel for creating new rules.'
        ),
        stack=['Node.js', 'Express', 'JavaScript', 'PostgreSQL', 'Sequelize', 'JWT'],
    ),
    dict(
        slug='plantia', year=2025,
        repo_url='https://github.com/fuken404/PlantIA',
        title_es='PlantIA', title_en='PlantIA',
        summary_es=(
            'API serverless que lee la humedad y temperatura de una planta desde Firestore y genera '
            'recomendaciones de cuidado con IA.'
        ),
        summary_en=(
            'Serverless API that reads a plant\'s humidity and temperature from Firestore and '
            'generates AI care recommendations.'
        ),
        stack=['Python', 'FastAPI', 'Firebase', 'Vercel'],
    ),
    dict(
        slug='app-recordatorios', year=2026,
        repo_url='https://github.com/fuken404/AppRecordatorios',
        title_es='App de recordatorios', title_en='Reminders app',
        summary_es=(
            'App para iOS de recordatorios recurrentes con categorías y notificaciones locales, sin '
            'servidor ni cuenta.'
        ),
        summary_en='iOS app for recurring reminders with categories and local notifications, no server or account needed.',
        stack=['React Native', 'TypeScript'],
    ),
]

EXPERIENCE = [
    dict(
        order=0,
        company='Talent Advisor Consulting',
        position_es='Consultor de Implementación', position_en='Implementation Consultant',
        location_es='Bogotá, Colombia · Híbrido', location_en='Bogotá, Colombia · Hybrid',
        start=date(2025, 11, 1),
        description_es=(
            'Desarrollo de servicios backend e integraciones a partir de requerimientos de negocio, '
            'acompañando a clientes en la implementación de sistemas ERP/CRM.'
        ),
        description_en=(
            'Backend services and integrations built from business requirements, supporting clients '
            'through ERP/CRM implementations.'
        ),
        highlights_es=[
            'Desarrollo y mantengo servicios backend con Python y Django.',
            'Integré la plataforma web de la compañía (PHP/Symfony) con el ERP interno (Python/Django) mediante APIs REST.',
            'Construyo procesos de extracción, transformación y carga de datos con SQL y Pandas.',
            'Desarrollé agentes de IA con OpenAI que automatizan la elaboración de descriptivos de cargos.',
            'Implementé un modelo de regresión lineal para la proyección salarial del sistema de gestión salarial.',
            'Uso Claude y ChatGPT en el flujo de desarrollo para acelerar implementación, depuración y documentación.',
            'Trabajo con Scrum en sprints de dos semanas: defino criterios de aceptación y gestiono el trabajo en Jira.',
        ],
        highlights_en=[
            'I build and maintain backend services with Python and Django.',
            'Integrated the company web platform (PHP/Symfony) with the internal ERP (Python/Django) through REST APIs.',
            'I build extract, transform and load processes with SQL and Pandas.',
            'Built OpenAI-powered AI agents that automate writing job descriptions.',
            'Implemented a linear regression model for salary projection in the compensation system.',
            'I use Claude and ChatGPT in my development workflow to speed up implementation, debugging and documentation.',
            'I work in two-week Scrum sprints, defining acceptance criteria and managing work in Jira.',
        ],
    ),
    dict(
        order=1,
        company='Freelance',
        position_es='Desarrollador Backend', position_en='Backend Developer',
        location_es='Remoto', location_en='Remote',
        start=date(2021, 2, 1),
        description_es=(
            'Diseño e implementación de arquitecturas, APIs y sistemas seguros para aplicaciones web y '
            'móviles, con soluciones a la medida que priorizan escalabilidad, rendimiento y mantenimiento.'
        ),
        description_en=(
            'Design and implementation of architectures, APIs and secure systems for web and mobile '
            'apps, with custom solutions focused on scalability, performance and maintainability.'
        ),
        highlights_es=[
            'APIs REST y GraphQL con autenticación JWT.',
            'Backends con FastAPI, Spring Boot y Node.js sobre PostgreSQL, MySQL, MongoDB y Firebase.',
            'Despliegue de servicios en contenedores con Docker.',
        ],
        highlights_en=[
            'REST and GraphQL APIs with JWT authentication.',
            'Backends with FastAPI, Spring Boot and Node.js on PostgreSQL, MySQL, MongoDB and Firebase.',
            'Containerized service deployment with Docker.',
        ],
    ),
    dict(
        order=2,
        company='AR Construcciones',
        position_es='Promotor de Ventas', position_en='Sales Promoter',
        location_es='Cajicá y Sopó, Colombia', location_en='Cajicá and Sopó, Colombia',
        start=date(2022, 5, 1), end=date(2025, 10, 1),
        description_es='Asesoría comercial en proyectos de vivienda y administración de los sistemas que los soportan.',
        description_en='Sales advisory for housing projects and administration of the systems behind them.',
        highlights_es=[
            'Administré sistemas CRM y ERP (SINCO, SmartHome) y las plataformas fiduciarias de los proyectos inmobiliarios.',
            'Coordiné entre clientes, gerencia y entidades financieras durante el ciclo completo de venta.',
        ],
        highlights_en=[
            'Administered CRM and ERP systems (SINCO, SmartHome) and the fiduciary platforms of the real estate projects.',
            'Coordinated clients, management and financial institutions across the full sales cycle.',
        ],
    ),
    dict(
        order=3,
        company='D&M Soltec',
        position_es='Técnico en Sistemas', position_en='Systems Technician',
        location_es='Cajicá, Colombia', location_en='Cajicá, Colombia',
        start=date(2020, 11, 1), end=date(2022, 2, 1),
        description_es=(
            'Mantenimiento preventivo y correctivo de equipos de cómputo, servicio técnico y asesoría '
            'comercial en productos tecnológicos.'
        ),
        description_en=(
            'Preventive and corrective computer maintenance, technical support and sales advice on '
            'technology products.'
        ),
    ),
]

EDUCATION = [
    dict(
        institution='Universidad Manuela Beltrán',
        degree_es='Ingeniería de Software', degree_en='Software Engineering',
        location='Bogotá, Colombia', start=date(2021, 1, 1), end=date(2026, 1, 1),
    ),
    dict(
        institution='SENA',
        degree_es='Técnico en Sistemas', degree_en='Systems Technician',
        start=date(2019, 2, 1), end=date(2020, 12, 1),
    ),
]

# (slug, nombre ES, nombre EN o '', entidad, categoría, año, mes, horas, ID de credencial)
# El slug es el nombre del archivo en content/certificates/<categoría>/ (ver attach_certificates).
CERTIFICATIONS = [
    ('enterprise-full-stack-spring-angular',
     'Enterprise Full Stack — Spring Boot 4 y Angular 21', 'Enterprise Full Stack — Spring Boot 4 & Angular 21',
     'Dev Senior Code', 'development', 2026, 3, None, '01KM8NF7W981TG00725NTPYKGM'),
    ('mision-tic-2022-ruta-completa',
     'Misión TIC 2022 — Ruta completa', 'Misión TIC 2022 — Full track',
     'MinTIC / Universidad Sergio Arboleda', 'development', 2021, 12, 800, ''),
    ('mision-tic-java',
     'Misión TIC — Desarrollo de Software con Java', 'Misión TIC — Software Development with Java',
     'MinTIC / Universidad Sergio Arboleda', 'development', 2021, 11, 200, ''),
    ('mintic-android',
     'Desarrollo de Aplicaciones Móviles Android', 'Android Mobile App Development',
     'MinTIC', 'development', 2021, 12, None, ''),
    ('mintic-python',
     'Desarrollo de Software con Python', 'Software Development with Python',
     'MinTIC', 'development', 2021, 8, None, ''),
    ('cisco-pcap-python',
     'PCAP — Fundamentos de Programación en Python', 'PCAP — Programming Essentials in Python',
     'Cisco Networking Academy', 'development', 2021, 12, None, ''),
    ('lfd121-developing-secure-software',
     'Developing Secure Software (LFD121)', '',
     'Linux Foundation & OpenSSF', 'security', 2026, 5, None, 'LF-rvet3v32qn'),
    ('cisco-gestion-amenazas-ciberneticas',
     'Gestión de Amenazas Cibernéticas', 'Cyber Threat Management',
     'Cisco Networking Academy', 'security', 2026, 3, None, ''),
    ('ibm-enterprise-design-thinking',
     'Enterprise Design Thinking Practitioner', '',
     'IBM SkillsBuild', 'agile', 2025, 8, None, ''),
    ('scrum-fundamentals-certified',
     'Scrum Fundamentals Certified (SFC™)', '',
     'SCRUMstudy', 'agile', 2024, 3, None, '1021290'),
    ('cisco-ccna-switching-routing-wireless',
     'CCNAv7: Switching, Routing y Wireless Essentials', 'CCNAv7: Switching, Routing, and Wireless Essentials',
     'Cisco Networking Academy', 'infra', 2023, 11, None, ''),
    ('cisco-ccna-introduction-to-networks',
     'CCNAv7: Introduction to Networks', '',
     'Cisco Networking Academy', 'infra', 2023, 6, None, ''),
    ('cisco-ndg-linux-unhatched',
     'NDG Linux Unhatched', '',
     'Cisco Networking Academy', 'infra', 2022, 4, None, ''),
]

def skill_slug(name):
    """slugify pierde los símbolos: C# y C++ quedarían ambos como 'c'."""
    return slugify(name.replace('#', 'sharp').replace('+', 'plus'))


class Command(BaseCommand):
    help = 'Carga el contenido base del portafolio (ES + EN). Usa --force para reemplazar el existente.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='Borra el contenido actual (incluido lo editado en el admin) y lo vuelve a cargar.',
        )

    @transaction.atomic
    def handle(self, *args, force=False, **options):
        if Profile.objects.exists() and not force:
            raise CommandError(
                'Ya hay contenido cargado. Usa --force para reemplazarlo '
                '(se pierde lo editado en el admin).'
            )

        for model in (Profile, Project, Skill, Experience, Education, Certification):
            model.objects.all().delete()

        Profile.objects.create(**PROFILE)

        skills = {}
        order = 0
        for category, items in SKILLS.items():
            for name_es, name_en, level, core in items:
                skills[name_es] = Skill.objects.create(
                    name_es=name_es, name_en=name_en, slug=skill_slug(name_es), category=category,
                    level=level, is_core=core, order=order,
                )
                order += 1
        for name, category in PROJECT_ONLY_SKILLS:
            skills[name] = Skill.objects.create(
                name_es=name, slug=skill_slug(name), category=category, show_in_stack=False, order=order,
            )
            order += 1

        for i, data in enumerate(PROJECTS):
            data = dict(data)
            stack = data.pop('stack')
            project = Project.objects.create(order=i, **data)
            project.skills.set(skills[name] for name in stack)

        for data in EXPERIENCE:
            Experience.objects.create(**data)

        for data in EDUCATION:
            Education.objects.create(**data)

        for slug, name_es, name_en, issuer, category, year, month, hours, credential in CERTIFICATIONS:
            Certification.objects.create(
                slug=slug, name_es=name_es, name_en=name_en, issuer=issuer, category=category,
                issued=date(year, month, 1), hours=hours, credential_id=credential,
            )
        call_command('attach_certificates', stdout=self.stdout)

        self.stdout.write(self.style.SUCCESS(
            f'Contenido cargado: {len(PROJECTS)} proyectos, {Skill.objects.filter(show_in_stack=True).count()} '
            f'habilidades, {len(EXPERIENCE)} experiencias, {len(CERTIFICATIONS)} certificaciones.'
        ))
