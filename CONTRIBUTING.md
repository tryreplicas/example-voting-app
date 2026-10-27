# Contributing

Thanks for helping improve the Example Voting App! This is a small demo, so contributions should stay simple.

## Project layout

* [`vote`](/vote) - Python front-end where users cast votes
* [`result`](/result) - Node.js app that shows results in real time
* [`worker`](/worker) - .NET worker that moves votes from Redis into Postgres
* [`k8s-specifications`](/k8s-specifications) - Kubernetes manifests
* [`seed-data`](/seed-data) and [`healthchecks`](/healthchecks) - helper scripts

## Running locally

You need Docker with [Docker Compose](https://docs.docker.com/compose). From the repo root, run:

```shell
docker compose up --build
```

The `vote` app runs at [http://localhost:8080](http://localhost:8080) and `result` at [http://localhost:8081](http://localhost:8081). See the [README](README.md) for Swarm and Kubernetes instructions.

## Submitting changes

1. Create a branch off `main`.
2. Keep each pull request focused on one change.
3. Make sure `docker compose up --build` still works and that votes show up in the results app.
4. In the pull request, explain what you changed and how you tested it.

For questions, open an issue or contact one of the [maintainers](MAINTAINERS).
