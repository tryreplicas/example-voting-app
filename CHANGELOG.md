# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

This project has no tagged releases yet, so all changes are listed under
"Unreleased". The entries below summarize notable recent changes from the git
history.

## [Unreleased]

### Added

- Debug port support for the `result` (Node.js) app, with the debugger bound
  only to localhost and a renamed VS Code debug launch configuration.
- `.gitattributes` file to avoid line-ending (EOL) issues across platforms.
- GitHub Actions workflows to build the `vote`, `result` and `worker` images
  and push them to Docker Hub.
- `before` and `after` image tags for the `vote` and `result` images, for
  use in demos.

### Changed

- Default ports for the `vote` and `result` services changed from 5000/5001
  to 8080/8081.
- Dockerfiles updated to satisfy Docker build lint checks (`FromAsCasing`,
  `LegacyKeyValueFormat`, `JSONArgsRecommended`, `InvalidDefinitionDescription`).
- `vote` service updated to Python 3.11.
- `result` app libraries updated to their latest versions, resolving a
  socket.io CVE.
- Simplified the .NET multi-platform Dockerfile for the `worker` service.
- Cleaned up the Compose and Kubernetes files, removed the namespace from the
  Kubernetes example, and updated the architecture diagram.

### Fixed

- File mounts after the working-directory change, and Python auto-reloading
  for the `vote` service.
- The .NET `worker` build.
- A vote could be lost when it was found in Redis but the database connection
  had been closed.

### Removed

- Duplicate .NET voting and result apps.
- Exposed Redis port from the Compose setup.

[Unreleased]: https://github.com/tryreplicas/example-voting-app/commits/main
