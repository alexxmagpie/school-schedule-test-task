# School Schedule Test Task

This is a Django REST Framework application with an API for a school schedule.
The application is built using a cache backend, asynchronous views, and database indexes to ensure better performance.

### Setup instruction

 - Pull the repository.
 - Run `docker-compose build` and `docker-compose up`
 - Test endpoint is accessible at `localhost:8888/api/schedule/` with `for_today=true` or `class_name=example_name` as optional query parameters.

### What does the Docker configuration do?

- Start three containers: `application itself, Postgres, Redis`.
- Install dependencies.
- Run Django migrations.
- Populate the database with sample Schedule records.
- Run pytest.

The Dockerfile and entrypoint script are located in the /docker/backend folder.
The docker-compose.yml is in the root of the project.

### What I would love to do if I had more time?

At least...

- Clean Django settings.
- Hide sensible configuration values properly.
- Improve pytest coverage.
- Clean requiremets.txt.
- Split settings and Docker configurations into different environments.
- Separate Locust into its own Docker container
- Add type annotations to the code and add Pylint to improve adherence to standards.
- Setup Jenkis to automate build processes.
