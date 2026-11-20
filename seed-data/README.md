# Seed data

Generates 3,000 sample votes for load tests by sending HTTP requests to the
`vote` service, the same way a browser does.

## What it seeds

The seed container sends 3,000 `POST` requests to `http://vote/` (the `vote`
service's form endpoint, on port 80 inside the Compose network):

| Batch | Payload  | Requests |
|-------|----------|----------|
| 1     | `vote=a` | 1,000    |
| 2     | `vote=b` | 1,000    |
| 3     | `vote=a` | 1,000    |

That gives **2,000 votes for option A and 1,000 for option B**. By default
option A is "Cats" and option B is "Dogs" (`OPTION_A` / `OPTION_B` in the
`vote` service).

The requests do not send a `voter_id` cookie, so the `vote` app gives each
request a new random voter ID. Each vote then follows the normal path: `vote`
pushes it onto the Redis `votes` list, `worker` writes it to the `votes` table
in Postgres (`db`), and `result` shows the totals.

## Files

- `make-data.py` runs at image build time. It writes the URL-encoded form
  bodies `posta` (`vote=a`) and `postb` (`vote=b`) with no trailing newline,
  so `ab` can post them as is.
- `generate-votes.sh` is the container's default command. It runs
  [ApacheBench](https://httpd.apache.org/docs/current/programs/ab.html)
  (`ab`) three times. Each run is `-n 1000` requests at `-c 50` concurrency,
  with `-T "application/x-www-form-urlencoded"`.
- `Dockerfile` uses `python:3.9-slim` as the base image, installs
  `apache2-utils` (which provides `ab`), copies this directory to `/seed`,
  runs `make-data.py`, and sets `/seed/generate-votes.sh` as the command.

## How to run it

The `seed` service in the root `docker-compose.yml` has the `seed` profile,
so it only starts when you enable that profile:

```shell
docker compose --profile seed up -d
```

It waits until the `vote` service is healthy, runs once (`restart: "no"`), and
then exits. It is on the `front-tier` network, which is how it reaches `vote`
by hostname. To add another 3,000 votes, run the service again:

```shell
docker compose --profile seed run --rm seed
```

## Parameters

There are no environment variables or command-line options. To change the
number of votes, concurrency, or split between options, edit the `-n` and
`-c` values or the number of `ab` lines in `generate-votes.sh`. Then rebuild
the image (for example, `docker compose --profile seed build seed`).

The target URL `http://vote/` is hard-coded, so the script only works on a
network where the `vote` service resolves by that name.
