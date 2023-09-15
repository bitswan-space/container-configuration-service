import bspump
import bspump.trigger
import bspump.common

from ..generators import ContainerConfigGenerator


class ContainerConfigPipeline(bspump.Pipeline):
    def __init__(self, app, pipeline_id):
        super().__init__(app, pipeline_id)

        self.Source = bspump.common.DirectSource(app, self)

        # Pretty print sink
        self.Sink = bspump.common.PPrintSink(app, self)

        self.build(
            self.Source,
            ContainerConfigGenerator(app, self),
            self.Sink,
        )
