# BettingTestAssigment

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

Simple betting service and basic data providing service with PostgreSQL database. Rules in /rules folder

---

## How to spin it for the first time:
0. Copy `/Deploy/.env.example`, save it as `/Deploy/.env`, and tweak envs if you wish.
    ```shell
    cp Deploy/.env.example Deploy/.env
    ```
----
1. Build the Docker image:
    ```shell
    docker-compose -f Deploy/dev_compose.yml build
    ```

2. Run migrations:
    ```shell
    docker compose -f Deploy/dev_compose.yml run --rm bet_maker_api alembic revision --autogenerate -m "init" ; docker compose -f Deploy/dev_compose.yml run --rm bet_maker_api alembic upgrade head ; docker compose -f Deploy/dev_compose.yml stop
    ```

3. Start the services:
    ```shell
    docker-compose -f Deploy/dev_compose.yml up -d
    ```
   
#### Now you can call bet_service and line_provider at localhost:{port} from .env

----
## Tests:
Tests combined for CI usage.
```shell
docker compose -f Deploy/dev_compose.yml run --rm bet_maker_api /bin/sh tests/all_tests_comm.sh
```
All tests artifacts are located at /bet-maker/reports

---
## Explanations of Choices:

- **PostgreSQL for storing bet data:**
  - Standardized data, so there's no need to use MongoDB.
  - Data doesn't expire, so there's no need for Redis.
  - Offers reasonably fast read and write operations.

- **Regular API requests for exchanging information between services:**
  - The preferred methods for information exchange in the task don't mention direct database queries.
  - Adding a message queue as an additional service would complicate the system without clear advantages.
  - The task allows for a slight delay in data updates.
  - Implementing a callback endpoint to update bet status would require minimal authentication, which would add complexity and increase time to make this assigment.

- **Three simple endpoints are separated into three distinct routers:**
  - Primarily for demonstrating my preferred way of organizing files and modules.
  - Convenient for larger and more complex endpoint schemas.
  - As a bonus, it allows for separation by tags in the Swagger documentation.

- **Formatting:**
  - Type hints are used sufficiently to assist with development in IDEs.
  - Adherence to PEP8 with slightly modified rules, including increased line length. A full list of ignored formatting rules can be found in /tests/.flake8.

## Steps to make this service good
#### In a world where I have all the time in it.

- Database requests from both services as main source of truth
- Main compose file for use in production. Mainly closing line-provider from outside and adding images.
- Negative and more complicated/parametrised tests
- Enums got a little out of control I think
