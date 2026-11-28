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

## Running tests

- `vote`: `cd vote && pip install -r requirements.txt pytest && python -m pytest tests`
- `result` unit tests: `cd result && npm install && npm test`
- `result` end-to-end test (votes through `vote` and checks `result`): `cd result && docker compose -f docker-compose.test.yml up --build --exit-code-from sut`

GitHub Actions builds the `vote`, `result`, and `worker` images on every pull request that touches their folders, so make sure `docker compose build` succeeds before you push.

## Branches and pull requests

- Branch from `main` with a short, descriptive kebab-case name, such as `add-healthz-endpoint` or `docs/readme-run-locally`.
- Keep each pull request to one change. Don't bundle unrelated fixes.
- Write commit messages and PR titles in the imperative mood ("Add index to votes table"). A conventional prefix like `docs:`, `fix:`, or `feat(result):` is welcome but not required.
- In the PR description, say what changed, why, and how you tested it. Add a screenshot for visible UI changes.
- Open pull requests against `main`. They are squash-merged once CI passes and a maintainer (see `MAINTAINERS`) approves.

## Code style

- Follow each service's existing conventions: PEP 8 for Python in `vote/`, the current JavaScript style in `result/` (CommonJS, `var`/callbacks as in `server.js`), and standard .NET conventions in `worker/`.
- Keep the app simple. It's a teaching example, so prefer clear code over clever abstractions, and don't add new services or dependencies without a good reason.
- If you change ports, service names, or credentials, update `docker-compose.yml`, `docker-stack.yml`, and `k8s-specifications/` together so they stay in sync.
- Shell scripts use LF line endings (enforced by `.gitattributes`).
