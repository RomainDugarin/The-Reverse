from discord.ext import commands, tasks
import asyncio
from urllib import parse
from discord import Embed

from reverse.core._service import SqliteService, TaskService, loop
from reverse.core._models import Context, Role
from reverse.core import utils

class Debugger(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		try:
			self.config = utils.load_custom_config('config.json', __file__, path='')
		except:
			self.config = None
		self.task = TaskService('Debugger')
		
	@commands.command()
	async def debugdb(self, ctx):
		print('{} asked for debug info on database'.format(ctx.author.name))
		server = SqliteService()
		embed=Embed(title="Debugger Database SQLITE", color=0xe80005)
		embed.set_author(name="The reverse")
		embed.add_field(name="env value", value=server.getEnvSqlite(), inline=False)
		embed.add_field(name="fullpath", value=server.getDBFullpath(), inline=False)
		embed.add_field(name="database name", value=server.getDBName(), inline=False)
		embed.add_field(name="database path", value=server.getDBPath(), inline=False)
		embed.add_field(name="in transaction", value=server.getInstance().in_transaction, inline=False)
		embed.add_field(name="isolation level", value=server.getInstance().in_transaction, inline=False)
		embed.add_field(name="Configuration Debugger", value=self.config, inline=False)
		embed.set_footer(text="Asked by {}".format(ctx.author.name))
		message = await ctx.send(embed=embed)
		self.lastEmbed = message

	@commands.command()
	async def showModules(self, ctx):
		ctx = Context(ctx)
		embed=Embed(title="Loaded Modules", color=0xe80005)
		embed.set_author(name="The reverse")
		for key, value in utils.listCogs().items():
			embed.add_field(name=key, value=value, inline=False)
		embed.set_footer(text="Asked by {}".format(ctx.author.name))
		message = await ctx.send(embed=embed)
		self.lastEmbed = message
	
	@commands.command()
	async def updateEmbed(self, ctx):
		if self.lastEmbed is not None:
			embed = self.lastEmbed.embeds[0]
			timestamp = None
			modifier = "Timestamps"
			for index, field in enumerate(embed.fields):
				if modifier == field.name:
					timestamp = index
					break
			import time
			if timestamp is not None:
				embed.set_field_at(timestamp, name=modifier, value=time.time())
			else:
				embed.add_field(name=modifier, value=time.time(), inline=False)
			await self.lastEmbed.edit(embed = embed)
	
	@commands.command()
	async def debugloop(self, ctx, *args):
		_kwargs, _args = utils.parse_args(args)
		data = {
			"index": 0,
			"loop": 5,
			"seconds":0,
			"minutes":0,
			"hours":0,
			"message": ""
		}
		try:
			for index, value in _kwargs.items():
				data[index] = value
		except:
			pass
		print(data)
		_loop = self.task.createLoop(self.loop_for_debug, seconds=float(data["seconds"]), minutes=float(data["minutes"]), hours=float(data["hours"]), count=int(data["loop"]), ctx=Context(ctx), data=data)
		self._debugloop = _loop
		_loop.start(ctx=_loop.ctx, data=_loop.data)
	
	async def testloop(self, ctx, message):
		await ctx.send(message)

	async def loop_for_debug(self, **kwargs):
		data = kwargs['data']
		ctx = kwargs['ctx']

		data['index'] += 1
		await self.testloop(ctx, data['message'])

	@commands.command()
	async def testargs(self, ctx, *args):
		_kwargs, _args = utils.parse_args(args)
		embed=Embed(title="Debugger args parser", color=0xe80005)
		embed.set_author(name="The reverse")
		embed.add_field(name="command", value=args, inline=False)
		embed.add_field(name="args", value=_args, inline=False)
		embed.add_field(name="kwargs", value=_kwargs, inline=False)
		embed.set_footer(text="Asked by {}".format(ctx.author.name))
		message = await ctx.send(embed=embed)
		self.lastEmbed = message

	@commands.command()
	async def debugRole(self, ctx, *args):
		ctx = Context(ctx)
		guild = ctx.guild
		_kwargs, _args = utils.parse_args(args)
		if("role" in _kwargs.keys()):
			try:
				r_id = int(_kwargs["role"][3:-1])
			except:
				await ctx.send("404 - Role not found")
				return
			if( (r := Role(r_id, guild)) != None): 
				await ctx.send("Find role with id={} and name={} ({} - {})".format(r.id, r.name, r, r.role))
			else:
				await ctx.send("404 - Role not found")
			return
		await ctx.send("You need to specify a role. --role @x")
	
	@commands.command()
	async def tenstop(self, ctx):
		await asyncio.sleep(10)
		await ctx.send("End tenstop")

	@commands.command()
	async def debugNextCall(self, ctx, *args):
		"""Generate 10 datetime from generate_next_call, by default, addition is off, day = 1"""
		_kwargs, _args = utils.parse_args(args)
		_t = utils.now()
		_adding = "adding" in _args
		await ctx.send("0: {}".format(_t))
		for i in range(1, 10):
			_tminus = _t
			_t = utils.generate_next_call(startDate=_t ,days=int(_kwargs.get('day', 1)), hours=int(_kwargs.get('hour', 0)), minutes=int(_kwargs.get('minute', 0)), seconds=int(_kwargs.get('second', 0)), adding=_adding)
			await ctx.send("{}: {} - {}s".format(i,_t,utils.time_until(_t, startDate=_tminus)))

def setup(bot):
	bot.add_cog(Debugger(bot))