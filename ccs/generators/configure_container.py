import bspump
import logging
import requests
import os
import json

L = logging.getLogger(__name__)


class ContainerConfigGenerator(bspump.Generator):
    def __init__(self, app, pipeline, id=None, config=None):
        super().__init__(app, pipeline, id, config)
        self.portainer_url = self.Config["portainer_url"]
        print(self.portainer_url)
        self.portainer_access_token = os.environ.get("PORTAINER_ACCESS_TOKEN")
        self.next_public_portainer_access_token = os.environ.get("NEXT_PUBLIC_PORTAINER_ACCESS_TOKEN")
        self.configured_contianers = set()

    async def generate(self, context, event, depth):
        # First we get the list of hosts from the portainer API
        hosts = []
        url = f"{self.portainer_url}/api/endpoints"
        headers = {
            "X-API-Key": f"{self.portainer_access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for host in response.json():
                hosts.append(host["Id"])
        else:
            L.error(f"Error while getting the list of hosts from the portainer API.\n Status code: {response.status_code}\n\n{response.text}")
            return
        for host in hosts:
            # Then we get the list of containers
            containers = []
            url = f"{self.portainer_url}/api/endpoints/{host}/docker/containers/json"

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                for container in response.json():
                    containers.append(container["Id"])
            else:
                L.error(f"Error while getting the list of containers from the portainer API.\n Status code: {response.status_code}\n\n{response.text}")
                return

            for container_id in containers:
                if container_id in self.configured_contianers:
                    continue
                self.configured_contianers.add(container_id)
                # Then we use http://localhost:9000/api/endpoints/2/docker/containers/49cb064cac428e3033a23ed32820a9366c4e7cda95793e600d72900f88c78716/exec to put the container id in /container_id
                exec_cmd = {
                    "id": container_id,
                    "AttachStdin": False,
                    "AttachStdout": False,
                    "AttachStderr": False,
                    "Tty": False,
                    "Cmd": ["/bin/bash", "-c", f"echo {container_id} > /container_id"]
                }

                url = f"{self.portainer_url}/api/endpoints/{host}/docker/containers/{container_id}/exec"
                response = requests.post(url, headers=headers, data=json.dumps(exec_cmd))
                if response.status_code == 201:
                    exec_id = response.json()["Id"]
                    exec_start = {
                        "Detach": False,
                        "Tty": False
                    }
                    url = f"{self.portainer_url}/api/endpoints/{host}/docker/exec/{exec_id}/start"
                    response = requests.post(url, headers=headers, data=json.dumps(exec_start))
                    if response.status_code == 200:
                        self.Pipeline.inject(context, f"Configured {container_id}", depth)
                    else:
                        self.Pipeline.inject(context, f"Error while starting the exec command.\n Status code: {response.status_code}\n\n{response.text}", depth)
                else:
                    L.error("Error while creating command")
