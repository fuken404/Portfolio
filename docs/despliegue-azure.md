# Despliegue en Azure

Guía paso a paso para publicar el portafolio en `fuken404.dev`. Marca cada casilla al completarla.

## Arquitectura

```
fuken404.dev / www ──► Azure Static Web Apps (Free)     React compilado
api.fuken404.dev ────► Azure Container Apps (consumo)   Django + gunicorn, escala a cero
                           ├──► PostgreSQL Flexible Server (B1ms)
                           └──► Blob Storage            certificados e imágenes

DNS: Cloudflare (el dominio se compró ahí; Cloudflare Registrar exige usar su DNS)
Código: GitHub · Imagen del backend: GitHub Container Registry · CI/CD: GitHub Actions
```

| Recurso | Plan | Costo esperado |
| --- | --- | --- |
| Static Web Apps | Free | USD 0 |
| Container Apps | Consumo, mín. 0 réplicas | USD 0 dentro de la cuota gratis mensual |
| PostgreSQL Flexible Server | Burstable B1ms, 32 GB | USD 0 los primeros 12 meses con cuenta gratuita; después, pago mensual |
| Blob Storage | Estándar LRS | Centavos al mes |
| Log Analytics | Retención mínima | USD 0 con pocos registros |
| GitHub Container Registry | Gratis | USD 0 |
| Dominio `fuken404.dev` | Cloudflare | Ya pagado (anual) |

Nombres sugeridos (ajústalos si alguno está tomado, los de Postgres y Storage son globales):

| Variable | Valor |
| --- | --- |
| Región | `eastus2` (todo en la misma región) |
| Grupo de recursos | `rg-portafolio` |
| PostgreSQL | `pg-fuken404` · base `portafolio` |
| Storage | `stfuken404` · contenedor `media` |
| Entorno de Container Apps | `cae-portafolio` |
| Container App | `api-portafolio` |
| Static Web App | `swa-portafolio` |

---

## Fase 0 · Cuentas y herramientas

- [ ] Crear la **cuenta gratuita de Azure** (pide tarjeta; es la que incluye PostgreSQL B1ms gratis 12 meses).
- [ ] Instalar Azure CLI: `brew install azure-cli` y luego `az login`.
- [ ] Instalar GitHub CLI: `brew install gh` y luego `gh auth login`.
- [ ] Docker Desktop corriendo (ya lo tienes).
- [ ] Crear un **presupuesto con alerta** en Cost Management (por ejemplo USD 5/mes) para enterarte de cualquier cobro.

## Fase 1 · Preparar el código para producción

Backend:
- [ ] `Dockerfile` + `.dockerignore` (Python slim, gunicorn, usuario sin privilegios).
- [ ] Script de arranque: `migrate` y `collectstatic` antes de iniciar gunicorn.
- [ ] WhiteNoise para servir los archivos estáticos del admin.
- [ ] `django-storages[azure]` para guardar `media/` en Blob Storage cuando haya credenciales.
- [ ] Ajustes de producción por variables de entorno: `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `CORS_ALLOWED_ORIGINS`, HTTPS (`SECURE_PROXY_SSL_HEADER`, HSTS, cookies seguras), conexión a Postgres con `sslmode=require`.
- [ ] Endpoint `/api/health/` para las sondas de Container Apps.
- [ ] Probar la imagen en local contra el Postgres de Docker.

Frontend:
- [ ] Usar `VITE_API_URL=https://api.fuken404.dev/api` en el build de producción.
- [ ] `staticwebapp.config.json`: fallback de la SPA, cabeceras de seguridad y caché de assets.
- [ ] Regenerar `fallback.json` después de cargar la base de producción (para que las URLs de certificados apunten a Blob).

Repositorio:
- [ ] `git init`, revisar `.gitignore` (nada de `.env`, `media/`, `_originales/`), primer commit.
- [ ] Crear el repo en GitHub y hacer push. Idea: reutilizar el nombre `Portfolio` después de borrar el viejo.

## Fase 2 · Infraestructura en Azure

Los comandos se ejecutan con `az` después de `az login`. Los valores entre `<>` se completan en el momento.

1. Grupo de recursos
   - [ ] `az group create --name rg-portafolio --location eastus2`

2. PostgreSQL Flexible Server
   - [ ] Crear el servidor B1ms, versión 17, 32 GB, acceso público:
     `az postgres flexible-server create --resource-group rg-portafolio --name pg-fuken404 --location eastus2 --tier Burstable --sku-name Standard_B1ms --storage-size 32 --version 17 --admin-user <usuario> --admin-password <clave> --public-access 0.0.0.0`
     (`0.0.0.0` permite solo servicios de Azure.)
   - [ ] Crear la base: `az postgres flexible-server db create --resource-group rg-portafolio --server-name pg-fuken404 --database-name portafolio`
   - [ ] Agregar tu IP al firewall solo mientras cargas datos desde tu Mac.

3. Blob Storage
   - [ ] Crear la cuenta: `az storage account create --name stfuken404 --resource-group rg-portafolio --location eastus2 --sku Standard_LRS --allow-blob-public-access true`
   - [ ] Crear el contenedor `media` con lectura pública de blobs (los certificados ya tienen el documento tapado).

4. Container Apps
   - [ ] Crear el entorno de consumo (con Log Analytics de retención mínima).
   - [ ] Publicar la imagen en `ghcr.io/fuken404/portafolio-api` (primero a mano, luego por CI).
   - [ ] Crear la app con ingreso externo en el puerto 8000, `min-replicas 0`, `max-replicas 1`, y los secretos como variables: `SECRET_KEY`, `DATABASE_URL`, credenciales de Storage, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`.
   - [ ] Configurar sondas de salud contra `/api/health/`.

5. Static Web Apps
   - [ ] Crear `swa-portafolio` (plan Free) conectada al repo de GitHub, con `app_location: frontend` y `output_location: dist`. Azure agrega el workflow de GitHub Actions al repo.
   - [ ] Agregar `VITE_API_URL` al workflow.

6. Datos de producción
   - [ ] `migrate`, `seed`, `attach_certificates` (sube los certificados a Blob) y `createsuperuser`, ejecutados contra la base de Azure.
   - [ ] Quitar tu IP del firewall de Postgres al terminar.

## Fase 3 · Dominio en Cloudflare

Todos los registros que apuntan a Azure van en modo **DNS only (nube gris)**: con el proxy de Cloudflare activo, Azure no puede validar el dominio ni emitir los certificados. `.dev` exige HTTPS siempre, y ambos servicios emiten certificados gratis.

- [ ] **`fuken404.dev` → Static Web Apps.** En la SWA, agregar dominio personalizado (apex) con validación por TXT. En Cloudflare: el registro `TXT` que indique Azure y un `CNAME @` hacia `<swa>.azurestaticapps.net` (Cloudflare lo "aplana" en el apex).
- [ ] **`www.fuken404.dev` → Static Web Apps.** `CNAME www` hacia la misma SWA y agregarlo como segundo dominio (el plan Free permite 2).
- [ ] **`api.fuken404.dev` → Container Apps.** En la Container App, agregar dominio con certificado administrado. En Cloudflare: `CNAME api` hacia `<app>.<entorno>.azurecontainerapps.io` y el `TXT asuid.api` con el ID de verificación.
- [ ] Actualizar `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` y `CSRF_TRUSTED_ORIGINS` con los dominios finales.

## Fase 4 · CI/CD

- [ ] Frontend: el workflow de Static Web Apps compila y publica en cada push a `main` (y crea entornos de prueba por pull request).
- [ ] Backend: workflow que construye la imagen, la sube a GHCR y ejecuta `az containerapp update` con la nueva etiqueta. Autenticación con Azure por OIDC (identidad federada), sin guardar contraseñas en GitHub.
- [ ] Solo despliega el backend cuando cambian archivos en `backend/`, y el frontend cuando cambian en `frontend/`.

## Fase 5 · Verificación

- [ ] `https://fuken404.dev` carga en ES y EN, modo claro y oscuro, y en móvil.
- [ ] Las etiquetas de endpoint muestran `200` contra `api.fuken404.dev`.
- [ ] Los certificados abren en el modal desde Blob Storage.
- [ ] El formulario de contacto guarda el mensaje (revisar en el admin).
- [ ] `https://api.fuken404.dev/admin/` funciona y exige login.
- [ ] Revisar Cost Management a los pocos días para confirmar que todo está en USD 0.

## Pendientes después del primer despliegue

- Infraestructura como código en Bicep (recrear todo con un comando).
- Notificación por correo al recibir mensajes de contacto.
- Antes de que termine el año gratis de PostgreSQL: decidir si seguir pagando o migrar.
