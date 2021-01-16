from reverse.client.reverse import Reverse
from reverse.core._models import Server, Message, Context
from reverse.core import utils
import asyncio
import sys

class Bot(Reverse):
    
    def __new__(cls, command_prefix, description=None, **kwargs):
        return super(Bot, cls).__new__(cls)

    def __init__(self, command_prefix, description=None, **kwargs):
        super().__init__(command_prefix, description, **kwargs)
        sys.tracebacklimit = 1
        self.prefix = command_prefix
        self.description = description
        self.initKwargs = kwargs
        self.registerEvents()
        self.isShutingdown = False

    def registerEvents(self):
        self.getClient().event(self.on_ready)
        self.getClient().event(self.on_message)
        self.addCommand(self.hey, pass_context=True)
        self.addCommand(self.remindme, pass_context=True)
        self.addCommand(self.reload, pass_context=True)

    async def on_ready(self, ctx=None):
        print('We have logged in as {0.user} using Bot implementation'.format(self.getClient()))

    async def hey(self, ctx: Context):
        await ctx.send("Hello!")

    async def remindme(self, ctx: Context, time: int, message: str):
        ctx = Context(ctx)
        await ctx.send("I will now wait {} seconds.".format(time))
        await asyncio.sleep(time)
        await ctx.send("Hey I didn't forget you! ;)\n Here your message : {}".format(message))
    
    def run(self, token: str, status: str = "starting"):
        super().run(token=token)
        print("{} successfully".format(status))
    
    async def isShutingdown(self):
        return self.isShutingdown
    
    async def reload(self, ctx, *args):
        ctx = Context(ctx)
        _kwargs, _args = utils.parse_args(args)
        data = {}
        if('time' in _kwargs):
            time = int(_kwargs['time'])
        else:
            time = 0
        
        import json
        for cog in self.cogs:
            data[cog] = 'on'
        with open('cogs.json', 'w') as outfile:
            json.dump({**data, **_kwargs}, outfile)

        if(time > 0):
            await ctx.send(embed=utils.formatEmbed("Reload in {} seconds".format(time), ctx.author.name, **{**data, **_kwargs}))
            await asyncio.sleep(time)
        self.isShutingdown = True
        sys.tracebacklimit = 0
        raise SystemExit('Restarting The-Reverse')
        