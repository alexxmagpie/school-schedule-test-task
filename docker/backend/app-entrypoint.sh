#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python manage.py populate_schedules 20

echo "--------------------STARTING TO RUN PROJECT TESTS-----------------------------"
coverage run -m pytest
coverage report -m

uvicorn school_schedule.asgi:application --host 0.0.0.0 --port 8888 --workers 4
