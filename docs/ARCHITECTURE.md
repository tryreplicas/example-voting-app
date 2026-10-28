# Architecture

The voting app is made of five services that run as containers.

- **vote** (Python/Flask, port 8080): the front end where users cast a vote. Each vote is pushed onto a Redis list named `votes`.
- **redis** (Redis): a queue that buffers incoming votes between the vote app and the worker.
- **worker** (.NET): pops votes off the Redis `votes` list and writes each one into the Postgres `db` service, updating the running totals.
- **db** (PostgreSQL): the persistent store for votes and their counts.
- **result** (Node.js, port 8081): reads the totals from Postgres and pushes live updates to the browser over Socket.IO.

Data flows one way: vote → redis → worker → db → result.
