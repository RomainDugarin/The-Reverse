from reverse.client.reverse import Reverse
from reverse.core._models import Server, Message, Context

class Bot(Reverse):
    
    def __init__(self, command_prefix, description=None, **kwargs):
        super().__init__(command_prefix=command_prefix, description=description, kwargs=kwargs)
        self.registerEvents()

    def registerEvents(self):
        self.getClient().event(self.on_ready)
        #self.getClient().event(self.on_message)
        self.addCommand(self.ping, pass_context=True)

    async def on_ready(self, ctx=None):
        print('We have logged in as {0.user} using Bot implementation'.format(self.getClient()))

    async def ping(self, ctx: Context):
        ctx = Context(ctx)
        await ctx.send("Hello")
    
    def run(self, token: str):
        super().run(token=token)