FROM python:3.11-slim

LABEL maintainer="samariddin"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

# Optional: collectstatic if static files should be ready at build time
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "noter2web.wsgi:application", "--bind", "0.0.0.0:8000"]
