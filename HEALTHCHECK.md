# Health checks

How to confirm the `vote`, `result`, and `worker` services are up and healthy when running with Docker Compose.

Commands assume you started the stack from the repo root with `docker compose up -d` (uses `docker-compose.yml`). If you used the prebuilt images, add `-f docker-compose.images.yml` to each `docker compose` command.

## Built-in health checks

| Service  | Health check                                                                 |
|----------|-------------------------------------------------------------------------------|
| `vote`   | `curl -f http://localhost` inside the container every 15s (`docker-compose.yml` only) |
| `result` | None                                                                          |
| `worker` | None                                                                          |
| `redis`  | `healthchecks/redis.sh` (`redis-cli ping` returns `PONG`)                     |
| `db`     | `healthchecks/postgres.sh` (`SELECT 1` via `psql`)                            |

`vote` and `worker` wait for `redis` to be healthy before starting; `result` and `worker` wait for `db`.

## Quick overview

```sh
docker compose ps
```

All services should show `running` (or `Up`). `vote`, `redis`, and `db` should also show `(healthy)`. `result` and `worker` have no health check, so they only show as running.

## vote

The Python/Flask voting app. Published on host port **8080** (container port 80).

Check it's running:

```sh
docker compose ps vote
docker compose logs --tail=50 vote
docker inspect --format '{{.State.Health.Status}}' $(docker compose ps -q vote)   # expect "healthy"
```

Check it's responding:

```sh
curl -fsS -o /dev/null -w '%{http_code}\n' http://localhost:8080/   # expect 200
```

Cast a test vote (`a` = Cats, `b` = Dogs by default):

```sh
curl -fsS -o /dev/null -X POST -d 'vote=a' http://localhost:8080/
docker compose logs --tail=5 vote   # expect "Received vote for a"
```

The vote is pushed onto the `votes` list in Redis for the worker to pick up.

## result

The Node.js results app. Published on host port **8081** (container port 80). In `docker-compose.yml` it also exposes the Node debugger on `127.0.0.1:9229`.

Check it's running:

```sh
docker compose ps result
docker compose logs --tail=50 result   # expect "App running on port 80" and "Connected to db"
```

Check it's responding:

```sh
curl -fsS -o /dev/null -w '%{http_code}\n' http://localhost:8081/   # expect 200
```

Open http://localhost:8081 in a browser to see live vote totals.

## worker

The .NET worker. It has no published ports. It pops votes from Redis and writes them to the `votes` table in Postgres.

Check it's running:

```sh
docker compose ps worker
docker compose logs --tail=50 worker   # expect "Found redis at ...", "Connected to db"
```

The logs should not keep repeating `Waiting for db` or `Waiting for redis`.

Confirm it's processing votes:

1. Cast a vote (see [vote](#vote)).
2. The worker logs should show it:

   ```sh
   docker compose logs --tail=5 worker   # expect "Processing vote for 'a' by '<voter_id>'"
   ```

3. The vote should be in the database:

   ```sh
   docker compose exec db psql -U postgres -c 'SELECT vote, COUNT(id) FROM votes GROUP BY vote;'
   ```

4. The Redis queue should be empty, meaning votes aren't piling up:

   ```sh
   docker compose exec redis redis-cli LLEN votes   # expect 0
   ```

5. The totals at http://localhost:8081 should update.

Each voter (identified by the `voter_id` cookie) has one row. Voting again with the same cookie updates that row instead of adding a new one. Repeated `curl` calls without a cookie each count as a new voter.

To generate a lot of traffic at once, run the seed job: `docker compose --profile seed up -d`. It sends 3000 votes to `vote`.
