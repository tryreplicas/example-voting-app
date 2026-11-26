# Contributing

Thanks for helping out! This guide covers running the voting app locally with Docker Compose.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) on macOS or Windows, or Docker Engine with the [Compose plugin](https://docs.docker.com/compose/install/) on Linux.
- No environment variables or `.env` file are needed. The Postgres credentials are set in `docker-compose.yml`.

## Running the app

From the repository root:

```shell
docker compose up
```

This builds the images and starts five services: `vote`, `result`, `worker`, `redis`, and `db`. Add `-d` to run them in the background.

- Vote: [http://localhost:8080](http://localhost:8080)
- Results: [http://localhost:8081](http://localhost:8081)

To load sample votes, start the optional `seed` service with its profile:

```shell
docker compose --profile seed up -d
```

## Stopping and rebuilding

- Stop the services: `docker compose down`
- Stop and delete the Postgres data volume (`db-data`), which clears all votes: `docker compose down -v`
- Rebuild the images after changing a Dockerfile or the `worker` code: `docker compose up --build`
- `vote` and `result` mount their source folders, so restarting them (`docker compose restart vote result`) picks up code changes without a rebuild

## Where things live

- `vote/`: Python web app for casting votes (Redis is its queue).
- `worker/`: .NET worker that moves votes from Redis into Postgres.
- `result/`: Node.js web app that shows results in real time from Postgres.
- Redis and Postgres run from public images, and Postgres stores its data in the `db-data` volume.
