# Sử dụng Python 3.10 để đồng nhất với yêu cầu của TensorFlow 2.10
FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-postgres.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements-postgres.txt

# Copy toàn bộ mã nguồn VÀ thư mục AI (chứa model .h5) vào trong container
COPY . .

# Chỉ định đường dẫn tới model NẰM BÊN TRONG container (không dùng /data nữa)
# Giả sử thư mục AI của bạn nằm ngang hàng với thư mục project
ENV AI_MODEL_PATH=/app/AI/third_genre_classification_model.h5
ENV AI_PREPROCESSING_CONFIG_PATH=/app/AI/preprocessing_config.json
ENV DJANGO_SECRET_KEY=build-only-not-for-production

RUN chmod +x docker-entrypoint.sh
RUN python manage.py collectstatic --noinput

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]

# GIẢM SỐ LƯỢNG WORKER xuống 1 để cứu RAM trên Render Free
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "2", "--timeout", "120"]