FROM python:3.9-slim

# Installer les dépendances système nécessaires pour mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    iputils-ping \
    cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .

CMD sh -c "mkdir -p media/cron_logs && \
    touch media/cron_logs/cron.log && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py createsuperuser --no-input || true && \
    python manage.py init_data && \
    python manage.py runserver 0.0.0.0:8000"
