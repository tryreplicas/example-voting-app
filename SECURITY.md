# Security Policy

## Supported Versions

This repository is a demo/sample application for learning Docker, Docker
Compose, Swarm, and Kubernetes. It is **not intended for production use**.

There are no tagged releases. Only the latest commit on the `main` branch is
supported, and security fixes are applied there only.

| Version         | Supported          |
| --------------- | ------------------ |
| latest `main`   | :white_check_mark: |
| anything else   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues,
pull requests, or any other public channel.**

Instead, contact the maintainers listed in the [MAINTAINERS](MAINTAINERS)
file privately and describe the issue there.

## What to Include

To help us understand and reproduce the issue, please include as much of the
following as you can:

- **Affected service(s):** `vote`, `result`, `worker`, `redis`, and/or `db`
- **Deployment method:** e.g. `docker compose`, Docker Swarm
  (`docker-stack.yml`), or Kubernetes (`k8s-specifications/`), plus relevant
  versions
- **Steps to reproduce:** a minimal, step-by-step description or
  proof-of-concept
- **Impact:** what an attacker could achieve and under what conditions

## What to Expect

After you report a vulnerability, the maintainers will review it and may
follow up with questions. If the issue is confirmed, a fix will be made on
`main`, and you'll be kept informed of progress where possible. Because this is
a sample project maintained on a best-effort basis, we can't commit to
specific response or fix timelines.

Please give the maintainers a reasonable chance to address the issue before
disclosing it publicly.
