# Use official slim Python base
FROM python:3.11-slim

LABEL maintainer="samariddin"

# Set working directory
WORKDIR /app

# Install OS dependencies for Python (required for psycopg2, Pillow, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn noter2web.wsgi:application --bind 0.0.0.0:8000"]