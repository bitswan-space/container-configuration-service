Container Configuration Service
-------------------------------------

This is a very simple service that when triggers searches through running containers using the Portainer API and again using the Portainer API injects a file with the container_id into the container. This exists solely to work around the fact that this is [otherwise impossible](https://github.com/opencontainers/runtime-spec/issues/1105).
