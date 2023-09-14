import bspump
import logging

from .pipelines import ContainerConfigPipeline

L = logging.getLogger(__name__)


class ContainerConfigServiceApp(bspump.BSPumpApplication):
    def __init__(self):
        super().__init__()
        svc = self.get_service("bspump.PumpService")
        svc.add_pipeline(ContainerConfigPipeline(self, "ContainerConfigPipeline"))
