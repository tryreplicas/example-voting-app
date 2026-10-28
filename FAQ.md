# FAQ

**What do I need to run the app locally?**
Just Docker with Docker Compose. Run `docker compose up` from the repository root and it builds and starts every service (vote, result, worker, Redis, and Postgres) for you.

**Where can I see the app once it's running?**
The vote app is at [http://localhost:8080](http://localhost:8080) and the results are at [http://localhost:8081](http://localhost:8081). If you deploy to Kubernetes instead, they're on ports 31000 and 31001 of each cluster node.
