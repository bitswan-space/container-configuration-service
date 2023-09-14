import bspump
import bspump.trigger
import bspump.common

from ..generators import ContainerConfigGenerator


class WifiscanPipeline(bspump.Pipeline):
    def __init__(self, app, pipeline_id):
        super().__init__(app, pipeline_id)

        # web trigger
        self.Trigger = bspump.trigger.WebTrigger(app, self)

        # Pretty print sink
        self.Sink = bspump.common.PPrintSink(app, self)

        self.build(
            self.Source,
            ContainerConfigGenerator(app, self),
            self.Sink,
        )
