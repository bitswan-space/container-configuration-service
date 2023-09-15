import logging
import asab.web.rest
import json.decoder
import os


L = logging.getLogger(__name__)


class Handler:
    def __init__(self, app, svc):
        self.Service = svc
        web_app = app.WebContainer.WebApp
        self.ConfigKey = os.environ.get("CCS_CONFIG_KEY", "ccs")

        web_app.router.add_post("/trigger", self.trigger)

    async def trigger(self, request):
        try:
            body = await request.json()
        except json.decoder.JSONDecodeError:
            L.warning("Invalid JSON format")
            return asab.web.rest.json_response(request, {"result": "ERROR", "reason": "Invalid JSON format"}, status=400)

        trigger_key = body.get("trigger-key", None)
        if trigger_key != self.ConfigKey:
            L.warning("Invalid trigger key")
            return asab.web.rest.json_response(request, {"result": "ERROR", "reason": "Invalid trigger key"}, status=400)

        await self.Service.trigger()

        return asab.web.rest.json_response(request, {"result": "OK"}, status=200)
