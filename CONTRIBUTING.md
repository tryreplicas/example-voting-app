# Contributing

## Setup

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (or Docker Engine with the [Compose plugin](https://docs.docker.com/compose/install/) on Linux).
2. Clone the repository and `cd` into it.
3. Run `docker compose up` from the repository root to build and start all services (vote, result, worker, Redis, and Postgres).
4. Open the vote app at [http://localhost:8080](http://localhost:8080) and the results at [http://localhost:8081](http://localhost:8081) to confirm a vote shows up.
5. Stop everything with `docker compose down`. If something won't start, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
