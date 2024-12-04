# School Schedule Test Task

This is a Django REST Framework application with an API for a school schedule.

### Setup instruction

 - pull the repository
 - run `docker-compose build` and `docker-compose up`
 - test endpoint accessible at `localhost:8888/api/schedule/` with `for_today=true` or `class_name=example_name` as optional query parameters

### What does docker configuration do?

- starts three containers with: `application itself, postgres, redis`
- runs Django migrations
- populates database with sample Schedule records
- runs pytest

Dockerfile and entrypoint script located in /docker/backend folder.
docker-compose.yml in root of a project.
