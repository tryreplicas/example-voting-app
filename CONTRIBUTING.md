# Contributing

## Running the app with Docker Compose

From the repository root, run:

```shell
docker compose up
```

- Vote: http://localhost:8080
- Results: http://localhost:8081

Changes in `vote` and `result` are picked up automatically through volume mounts. To also seed sample votes, run `docker compose --profile seed up -d`.

To stop the app, run `docker compose down` (add `-v` to delete the database volume).
