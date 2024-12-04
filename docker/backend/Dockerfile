FROM python:3.10.15-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./backend/ /app/

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./docker /app/docker

RUN chmod +x /app/docker/backend/app-entrypoint.sh
ENTRYPOINT ["/app/docker/backend/app-entrypoint.sh"]

EXPOSE 8888

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=school_schedule.settings
