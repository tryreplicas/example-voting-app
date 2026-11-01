# Voting App

A simple distributed application running across multiple Docker containers.

## Getting started

Download [Docker Desktop](https://www.docker.com/products/docker-desktop) for Mac or Windows. [Docker Compose](https://docs.docker.com/compose) will be automatically installed. On Linux, make sure you have the latest version of [Compose](https://docs.docker.com/compose/install/).

This solution uses Python, Node.js, .NET, with Redis for messaging and Postgres for storage.

Run in this directory to build and run the app:

```shell
docker compose up
```

The `vote` app will be running at [http://localhost:8080](http://localhost:8080), and the `results` will be at [http://localhost:8081](http://localhost:8081).

Health check: GET /healthz on the vote app.

Alternately, if you want to run it on a [Docker Swarm](https://docs.docker.com/engine/swarm/), first make sure you have a swarm. If you don't, run:

```shell
docker swarm init
```

Once you have your swarm, in this directory run:

```shell
docker stack deploy --compose-file docker-stack.yml vote
```

## Run locally

You need [Docker](https://docs.docker.com/get-docker/) with the Compose plugin (`docker compose version` should print v2 or later). Ports 8080 and 8081 must be free.

From the repository root, build the images and start every service:

```shell
docker compose up --build
```

Compose waits for Redis and Postgres to pass their health checks before starting the `vote`, `worker`, and `result` services. Once they're up:

* Vote at [http://localhost:8080](http://localhost:8080)
* See results at [http://localhost:8081](http://localhost:8081)

The `vote` and `result` source folders are mounted into their containers, so edits to those apps show up without a rebuild. The `result` service also exposes a Node.js debugger on `127.0.0.1:9229`.

Other useful commands:

```shell
# Run in the background, then follow the logs
docker compose up -d
docker compose logs -f

# Fill the database with sample votes (runs once, then exits)
docker compose --profile seed up -d

# Use the prebuilt images from Docker Hub instead of building locally
docker compose -f docker-compose.images.yml up

# Stop the app
docker compose down

# Stop the app and delete the Postgres volume to start fresh
docker compose down -v
```

If something doesn't start, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Run the app in Kubernetes

The folder k8s-specifications contains the YAML specifications of the Voting App's services.

Run the following command to create the deployments and services. Note it will create these resources in your current namespace (`default` if you haven't changed it.)

```shell
kubectl create -f k8s-specifications/
```

The `vote` web app is then available on port 31000 on each host of the cluster, the `result` web app is available on port 31001.

To remove them, run:

```shell
kubectl delete -f k8s-specifications/
```

## Architecture

![Architecture diagram](architecture.excalidraw.png)

* A front-end web app in [Python](/vote) which lets you vote between two options
* A [Redis](https://hub.docker.com/_/redis/) which collects new votes
* A [.NET](/worker/) worker which consumes votes and stores them in…
* A [Postgres](https://hub.docker.com/_/postgres/) database backed by a Docker volume
* A [Node.js](/result) web app which shows the results of the voting in real time

## Notes

The voting application only accepts one vote per client browser. It does not register additional votes if a vote has already been submitted from a client.

This isn't an example of a properly architected perfectly designed distributed app... it's just a simple
example of the various types of pieces and languages you might see (queues, persistent data, etc), and how to
deal with them in Docker at a basic level.
Demo change for REP-1072 status sync.
Edited from the phone
Android regression test
hello from the suite
