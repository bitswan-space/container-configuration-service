import bspump
import bspump.trigger
import bspump.common

from ..generators import ContainerConfigGenerator


class NullSource(bspump.TriggerSource):
    def __init__(self, app, pipeline, id=None, config=None):
        super().__init__(app, pipeline, id, config)

    async def cycle(self):
        print("NullSource cycle")
        await self.process({})


class ContainerConfigPipeline(bspump.Pipeline):
    def __init__(self, app, pipeline_id):
        super().__init__(app, pipeline_id)

        self.Source = NullSource(app, self)

        # web trigger
        self.Trigger = bspump.trigger.PeriodicTrigger(app, 10)

        # Pretty print sink
        self.Sink = bspump.common.PPrintSink(app, self)

        self.build(
            self.Source.on(self.Trigger),
            ContainerConfigGenerator(app, self),
            self.Sink,
        )
