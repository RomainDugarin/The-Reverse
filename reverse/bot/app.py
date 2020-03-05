from reverse.client.reverse import Reverse
from reverse.core._models import Server, Message, Context
import asyncio

class Bot(Reverse):
    
    def __init__(self, command_prefix, description=None, **kwargs):
        super().__init__(command_prefix=command_prefix, description=description, kwargs=kwargs)
        self.registerEvents()
        self.isShutingdown = False

    def registerEvents(self):
        self.getClient().event(self.on_ready)
        self.getClient().event(self.on_message)
        self.addCommand(self.hey, pass_context=True)
        self.addCommand(self.heyo, pass_context=True)
        self.addCommand(self.reload, pass_context=True)

    async def on_ready(self, ctx=None):
        print('We have logged in as {0.user} using Bot implementation'.format(self.getClient()))

    async def hey(self, ctx: Context):
        ctx = Context(ctx)
        await ctx.send("Hello!")

    async def heyo(self, ctx: Context, time: int, message: str):
        ctx = Context(ctx)
        await ctx.send("I will now wait {} seconds.".format(time))
        await asyncio.sleep(time)
        await ctx.send("Hey I didn't forget you! ;)\n Here your message : {}".format(message))
    
    def run(self, token: str, status: str = "starting"):
        super().run(token=token)
        print("{} successfully".format(status))
    
    async def reload(self, ctx, time: int = 0):
        ctx = Context(ctx)
        self.isShutingdown = True
        if(time > 0):
            await ctx.send("Reload in {} seconds".format(time))
            await asyncio.sleep(time)
        await ctx.send("Reloading now")
        await self.getClient().logout()