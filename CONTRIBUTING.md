# Contributing

## Running the app locally

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (or Docker Engine with the [Compose plugin](https://docs.docker.com/compose/install/) on Linux).
- From the repository root, run `docker compose up` to build and start all services (vote, result, worker, Redis, and Postgres).
- Open the vote app at [http://localhost:8080](http://localhost:8080) and the results at [http://localhost:8081](http://localhost:8081); stop everything with `docker compose down`.
- To run prebuilt images instead of building locally, use `docker compose -f docker-compose.images.yml up`.
- To load sample votes, run `docker compose --profile seed up` (this starts the `seed` service).

## Branch and pull request workflow

1. Start from an up-to-date `main`: `git checkout main && git pull`.
2. Create a descriptive branch, e.g. `git checkout -b docs/fix-typo` or `fix/worker-reconnect`.
3. Commit your changes with clear messages, then push the branch:
   `git push -u origin <branch-name>`.
4. Open a pull request against `main` describing what changed and why.
5. Address review feedback by pushing more commits to the same branch.

## Keep changes small and focused

- One logical change per pull request; split unrelated fixes into separate PRs.
- Avoid drive-by reformatting or refactors outside the scope of your change.
- Before opening a PR, run `docker compose up --build` and check that the vote and result apps still work.
