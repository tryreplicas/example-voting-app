# Contributing

Thanks for helping out! This guide covers running the voting app locally with Docker Compose. For an overview of the app, its architecture, and other ways to run it (Docker Swarm, Kubernetes), see the [README](README.md).

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

## Opening a pull request

1. Create a branch from `main` and make your change.
2. Run the app with `docker compose up --build` and check your change at the URLs above.
3. Open a pull request against `main` with a short description of what changed and why, and link the related issue if there is one.

Pull requests that change `vote/`, `result/`, or `worker/` trigger a GitHub Actions workflow that builds that service's Docker image (the image isn't pushed), so keep it passing.
