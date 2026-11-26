# Troubleshooting

**`docker compose up` fails with "port is already allocated"**
Another process is using port 8080 or 8081. Stop that process, or change the host side of the port mapping in `docker-compose.yml` (for example `"8090:80"` for the vote service) and open the new port instead.

**Votes don't show up on the results page**
The worker may have started before Redis or Postgres was ready. Check its logs with `docker compose logs worker`, then restart it with `docker compose restart worker`. If that doesn't help, reset everything with `docker compose down -v` followed by `docker compose up`.
