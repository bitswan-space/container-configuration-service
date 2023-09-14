import bspump
import logging

from .pipelines.container_config_pipeline import ContainerConfigPipeline

L = logging.getLogger(__name__)


class ContainerConfigServiceApp(bspump.BSPumpApplication):
    def __init__(self):
        super().__init__()
        svc.add_pipeline(ContainerConfigPipeline(self, "ContainerConfigPipeline"))
