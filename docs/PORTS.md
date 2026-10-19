# Ports

Ports used by each service. Host ports apply to `docker-compose.yml`; NodePorts apply to `k8s-specifications/`.

| Service  | Container port | Host port (Compose) | Kubernetes                     | Notes                                |
|----------|----------------|---------------------|--------------------------------|--------------------------------------|
| vote     | 80             | 8080                | NodePort 31000                 | Flask voting UI                      |
| result   | 80             | 8081                | NodePort 31001                 | Node.js results UI                   |
| result   | 9229           | 127.0.0.1:9229      | —                              | Node.js debugger (dev only)          |
| redis    | 6379           | not published       | ClusterIP (internal)           | Vote queue                           |
| db       | 5432           | not published       | ClusterIP (internal)           | Postgres storage                     |
