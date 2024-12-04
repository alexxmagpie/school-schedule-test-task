# Use the Python 3.10.15 image as the base image
FROM python:3.10.15-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (optional but often needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./backend/ /app/

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Copy docker configs.
COPY ./docker /app/docker

RUN chmod +x /app/docker/backend/app-entrypoint.sh
ENTRYPOINT ["/app/docker/backend/app-entrypoint.sh"]

# Expose port 8000 for Django
EXPOSE 8888

# Set environment variables for Django settings
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=school_schedule.settings
