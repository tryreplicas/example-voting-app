# Contributing

## Running the app locally

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (or Docker Engine with the [Compose plugin](https://docs.docker.com/compose/install/) on Linux).
- From the repository root, run `docker compose up` to build and start all services (vote, result, worker, Redis, and Postgres).
- Open the vote app at [http://localhost:8080](http://localhost:8080) and the results at [http://localhost:8081](http://localhost:8081); stop everything with `docker compose down`.

## Running tests

- The result app has a Node.js test suite. From `result/`, run `npm test` (it runs `node --test tests/*.test.js`).

## Pull requests and CI

- Pull requests to `main` run the GitHub Actions image build for each component they change (`vote/**`, `result/**`, `worker/**`); see [`.github/workflows/`](.github/workflows/). No workflow runs the test suites.

## Reporting issues

- Report problems with this app in this repository's issue tracker. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first. The issue template asks for a description, reproduction steps, expected and actual results, and the output of `docker version` and `docker info`.
- Bugs in Docker itself belong in the [docker/docker](https://github.com/docker/docker) repository. For general Docker help, the template points to the [Docker Forums](https://forums.docker.com/).
- Maintainers are listed in [MAINTAINERS](MAINTAINERS).
