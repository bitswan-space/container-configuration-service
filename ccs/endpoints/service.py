import logging


L = logging.getLogger(__name__)


class Service:
    def __init__(self, app, pipeline):
        self.ContainerConfigPipeline = pipeline

    async def trigger(self):
        self.ContainerConfigPipeline.Source.put(self, {})
