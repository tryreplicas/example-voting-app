# Ports

Each app listens on port 80 inside its container. The compose files publish those to host ports:

| Service | Container port | Host port (published) | URL |
|---------|----------------|-----------------------|-----|
| vote    | 80             | 8080                  | http://localhost:8080 |
| result  | 80             | 8081                  | http://localhost:8081 |

The mappings are `"8080:80"` (vote) and `"8081:80"` (result), in `docker-compose.yml`, `docker-compose.images.yml`, and `docker-stack.yml`.

The dev compose file (`docker-compose.yml`) also publishes the result service's Node debugger on `127.0.0.1:9229`.
