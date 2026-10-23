# API del portafolio (Django + gunicorn) para Azure Container Apps.
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependencias primero para aprovechar la caché de capas
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Los estáticos del admin se generan en la imagen. collectstatic solo
# necesita que los ajustes carguen, así que basta con valores ficticios.
RUN SECRET_KEY=build-only DATABASE_URL=sqlite:////tmp/build.db \
    python manage.py collectstatic --noinput

# Usuario sin privilegios
RUN useradd --create-home --uid 1000 app && chown -R app:app /app
USER app

EXPOSE 8000
CMD ["./docker-entrypoint.sh"]
