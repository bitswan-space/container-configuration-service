import bspump
import logging

from .pipelines import ContainerConfigPipeline

L = logging.getLogger(__name__)


class ContainerConfigServiceApp(bspump.BSPumpApplication):
    def __init__(self):
        super().__init__()
        svc = self.get_service("bspump.PumpService")
        self.ContainerConfigPipeline = ContainerConfigPipeline(self, "ContainerConfigPipeline")
        svc.add_pipeline(self.ContainerConfigPipeline)

        from .endpoints.handler import Handler
        from .endpoints.service import Service
        self.Service = Service(self, self.ContainerConfigPipeline)
        self.Handler = Handler(self, self.Service)

