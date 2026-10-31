# Support

Thanks for using the Example Voting App! This page explains where to get help and how to report problems.

## Getting help

GitHub Issues and Discussions are not enabled on this repository (a fork of [dockersamples/example-voting-app](https://github.com/dockersamples/example-voting-app)).

* For problems with the sample app itself, check whether it also happens upstream and, if so, open an issue on the [upstream issue tracker](https://github.com/dockersamples/example-voting-app/issues).
* For general questions about Docker, Compose, or Swarm, use the [Docker Forums](https://forums.docker.com/).
* For bugs in Docker itself, please report them to the relevant Docker project rather than here.

## Reporting bugs

Please include:

* **Which service** is affected: `vote` (Python), `result` (Node.js), `worker` (.NET), `redis`, `db` (Postgres), or `seed` (the `seed-data` loader).
* **How you are running it**: Docker Compose (`docker-compose.yml` or `docker-compose.images.yml`), Docker Swarm (`docker-stack.yml`), or Kubernetes (`k8s-specifications/`).
* **Steps to reproduce**, plus what you expected and what happened instead.
* **Logs** from the affected service, e.g. `docker compose logs <service>` or `kubectl logs <pod>`.
* **Environment details**: output of `docker version` and `docker info` (or `kubectl version`), and your OS / platform (Docker Desktop, cloud, VM, etc.).

## Security issues

This repository does not have a security policy. **Please do not report security vulnerabilities in public issues.** Contact the maintainers listed in [MAINTAINERS](MAINTAINERS) privately instead.

## Documentation

* [README](README.md): getting started, running with Compose, Swarm, and Kubernetes, and the architecture overview
* [Architecture diagram](architecture.excalidraw.png)
* Service source: [`vote/`](vote), [`result/`](result), [`worker/`](worker), [`seed-data/`](seed-data)
* Deployment files: [`docker-compose.yml`](docker-compose.yml), [`docker-stack.yml`](docker-stack.yml), [`k8s-specifications/`](k8s-specifications)
