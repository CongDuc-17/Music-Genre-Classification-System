FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-postgres.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements-postgres.txt

COPY . .

# Mount model + config at runtime (see docker-compose) — defaults for local image run:
ENV AI_MODEL_PATH=/data/third_genre_classification_model.h5
ENV AI_PREPROCESSING_CONFIG_PATH=/data/preprocessing_config.json
ENV DJANGO_SECRET_KEY=build-only-not-for-production

RUN chmod +x docker-entrypoint.sh
RUN python manage.py collectstatic --noinput

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--timeout", "120"]
