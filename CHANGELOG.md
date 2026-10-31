# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project does not yet use versioned releases, so changes are listed under Unreleased.

## [Unreleased]

### Changed

- The `vote` and `result` apps are now published on ports 8080 and 8081 instead of 5000 and 5001.
- The `vote` service uses Python 3.11.
- The `result` app's dependencies are updated to the latest versions, which also resolves a socket.io CVE.
- The .NET worker uses a simplified multi-platform Dockerfile.
- The Redis port is no longer exposed on the host.

### Added

- Debug port support for the `result` (Node.js) app.
- A `.gitattributes` file to avoid line-ending issues across platforms.

### Fixed

- Python `vote` app reloads correctly in development, and file mounts follow the working directory.
- The worker no longer loses a vote when it is found in Redis and the database connection was closed.

### Removed

- Duplicate .NET `vote` and `result` apps.
- Unused Jenkins configuration.
