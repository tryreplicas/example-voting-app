# Contributing

## Running the app locally

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (or Docker Engine with the [Compose plugin](https://docs.docker.com/compose/install/) on Linux).
- From the repository root, run `docker compose up` to build and start all services (vote, result, worker, Redis, and Postgres).
- Open the vote app at [http://localhost:8080](http://localhost:8080) and the results at [http://localhost:8081](http://localhost:8081); stop everything with `docker compose down`.
