#!/bin/sh
# Healthcheck for the `redis` service in docker-compose.yml and
# docker-compose.images.yml. Sends PING via redis-cli to the container's own
# IP and exits 0 only if the reply is PONG.
set -eo pipefail

host="$(hostname -i || echo '127.0.0.1')"

if ping="$(redis-cli -h "$host" ping)" && [ "$ping" = 'PONG' ]; then
	exit 0
fi

exit 1
