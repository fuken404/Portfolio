# Portafolio

Portafolio personal con **Django** (API REST), **PostgreSQL** y **React** (Vite), en español e inglés.

La idea de diseño: el sitio es su propio caso de estudio. Cada sección muestra el endpoint
de Django del que sale su contenido, con el código de respuesta y la latencia reales.

## Estructura

```
Portafolio/
├── docker-compose.yml       PostgreSQL local (puerto 5435)
├── backend/                 Django 6 + Django REST Framework
│   ├── .env.example         variables de entorno (copiar como .env)
│   ├── content/certificates/  certificados por categoría (ver su README)
│   ├── config/              settings, urls raíz
│   └── portfolio/           app principal
│       ├── models.py        Profile, Skill, Project, Experience, Education, Certification, ContactMessage
│       ├── i18n.py          campos `_es` / `_en` y respaldo en español
│       ├── serializers.py
│       ├── views.py         endpoints de solo lectura + POST de contacto
│       ├── urls.py          /api/...
│       ├── admin.py         todo el contenido se edita desde /admin
│       └── management/commands/
│           ├── seed.py              contenido base (CV + LinkedIn + GitHub)
│           ├── attach_certificates.py  adjunta los archivos de content/certificates
│           └── export_fallback.py   genera frontend/src/data/fallback.json
└── frontend/                React 19 + Vite
    └── src/
        ├── api/client.js    fetch con medición de latencia
        ├── hooks/           useApi, useTheme, useActiveSection
        ├── i18n/            textos de la interfaz (ES/EN) y selector de idioma
        ├── components/      una pieza por sección
        ├── data/            fallback.json: copia local de la API (ES/EN) si no responde
        └── styles/
            ├── tokens.css   las dos paletas (Musgo / Arcilla)
            └── app.css      maquetación
```

## API

| Método | Ruta                       | Uso                     |
| ------ | -------------------------- | ----------------------- |
| GET    | `/api/profile/`            | datos del perfil        |
| GET    | `/api/skills/`             | stack                   |
| GET    | `/api/projects/`           | proyectos (`?skill=react` filtra por tecnología) |
| GET    | `/api/projects/<slug>/`    | detalle de un proyecto  |
| GET    | `/api/experience/`         | experiencia             |
| GET    | `/api/education/`          | educación               |
| GET    | `/api/certifications/`     | certificaciones         |
| POST   | `/api/contact/`            | formulario de contacto  |

Todas las respuestas salen en el idioma del encabezado `Accept-Language` (`es` o `en`),
incluidos los errores de validación.

## Idiomas

- **Contenido** (perfil, proyectos, experiencia): cada campo traducible tiene dos columnas,
  `campo_es` y `campo_en`. En el admin aparecen agrupadas en *Español* / *English*.
  El español es obligatorio; si el inglés queda vacío, la página en inglés muestra el español.
- **Interfaz** (menú, botones, etiquetas): `frontend/src/i18n/strings.js`.
- **Idioma inicial**: el que la persona eligió antes; si no, español para navegadores en
  español e inglés para el resto.

## Desarrollo

Base de datos (PostgreSQL en Docker, puerto 5435):

```bash
docker compose up -d
```

Backend (puerto 8010, porque el 8000 lo usa Docker en esta máquina):

```bash
cd backend
cp .env.example .env             # solo la primera vez; cambia SECRET_KEY
source .venv/bin/activate
python manage.py migrate
python manage.py seed            # contenido base (ES + EN); --force para reemplazar
python manage.py createsuperuser # para entrar a /admin
python manage.py runserver 127.0.0.1:8010
```

Frontend (Vite redirige `/api` y `/media` a Django):

```bash
cd frontend
npm install
npm run dev
```

Abrir http://localhost:5173. El contenido se edita en http://127.0.0.1:8010/admin.

Para agregar certificados, copia el archivo a `backend/content/certificates/<categoría>/<slug>.pdf`
(los nombres esperados están en el README de esa carpeta) y ejecuta `python manage.py attach_certificates`.

Después de editar contenido en el admin, regenera la copia local del frontend:

```bash
python manage.py export_fallback
```

## Paletas

El sitio tiene modo oscuro y claro (botón sol/luna en la barra superior). Por defecto sigue
la preferencia del sistema; si la persona elige uno, se recuerda en el navegador.

- **Oscuro · Musgo**: grafito con verde salvia.
- **Claro · Arcilla**: papel beige, tinta azul marino y acentos café.

Todas las variables están en `frontend/src/styles/tokens.css`.

## Despliegue

Producción en Azure (`fuken404.dev`): Static Web Apps para el frontend, Container Apps para la API,
PostgreSQL Flexible Server y Blob Storage. Paso a paso en [docs/despliegue-azure.md](docs/despliegue-azure.md).
