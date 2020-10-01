from discord.ext import commands
from discord import Embed
import datetime

from reverse.core._service.betaseries import *
from reverse.core._service import TaskService
from reverse.core._models import Context
from reverse.core import utils


class Series(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.b = BetaSeries('c62c2adcf1dc', '84998d383001')
		self.task = TaskService('Series')
		self.LOGO = "https://www.betaseries.com/images/site/betaseries.svg"
		
	@commands.command()
	async def recreate(self, token, user):
		"""Reset connection

		Parameters
		----------
		token : str
			API Token
		user : str
			User ID
		"""
		self.b = BetaSeries(token, user)

	@commands.command(aliases=['bstart'])
	async def betastart(self, ctx, *args):
		"""Start coroutine that trigger every day at 7am to display Planning of specified day released

		Parameters
		----------
		ctx : :class:`reverse.core._models.Context`
			Context
		"""
		ctx = Context(ctx)
		_kwargs, _args = utils.parse_args(args)
		hour = _kwargs.get('hour', 7)

		next_call = utils.now() + datetime.timedelta(days=1)
		next_call = next_call.replace(hour=hour, minute=0, second=0)

		delta = utils.time_until(next_call)
		data = {
			"Hour": 7,
			"Timer": delta,
			"Date": next_call
		}

		_task = _kwargs.get("task", self.release_today.__name__)
		try:
			callable(getattr(Series,_task))
			if((_loop := self.task.findTaskByName(self.release_today.__name__)) != None):
				_loop.stop()
				self.task.remove(_loop)
				await ctx.send("Overwrite betaseries task.")
			_loop = self.task.createLoop(self.release_today, seconds=delta, ctx=ctx, data=data)
			self.task.start(_loop, ctx=_loop.ctx, data=_loop.data)
			print("Betaseries task started. Delta : {} - Date : {}".format(delta, next_call))
		except:
			await ctx.send("Task unknown.")

	@commands.command(aliases=['bstatus'])
	async def betastatus(self, ctx):
		ctx = Context(ctx)
		_loops = self.task.taskList()

		embed = Embed(title="Taches en cours", color=0xe80005, timestamp=datetime.datetime.today(), thumbnail=self.LOGO)
		if(len(_loops) > 0):
			for e in _loops:
				_value = ""
				_data = e.data
				for k,v in _data.items():
					_value += "> `{}`: {}\n".format(k,v)
				embed.add_field(name=e.getName(), value="Task is running : {}\n{}".format(e.isRunning(), _value), inline=False)
		else:
			embed.add_field(name="Aucune taches", value="Sadge", inline=False)
		embed.set_footer(text="".format("The Reverse"))

		await ctx.send(embed=embed)
	
	@commands.command(aliases=['brestart'])
	async def betarestart(self, ctx, *args):
		ctx = Context(ctx)
		_loops = self.task.taskList()
		_kwargs, _args = utils.parse_args(args)
		_found = _kwargs.get('task', "release_today")
		_kwargs.pop('task', None)

		for e in _loops:
			if(e.getName() == _found):
				if("stop" in args):
					if("force" in args):
						e.cancel()
						self.task.remove(e)
						await ctx.send("{} cold shutdown successfully.".format(_found))
						return
					e.stop()
					await ctx.send("{} warm shutdown. This will allows the task to finish its current iteration.".format(_found))
					return
				e.restart(**_kwargs)
				await ctx.send("{} restart successfully.".format(_found))

	@commands.command()
	async def pt(self, ctx):
		"""Alias for Planning Calendar today

		Parameters
    	-----------
			ctx: :class:`reverse.core._models.Context`
		"""
		Context(ctx)
		await self.planning_today()

	async def release_today(self, **kwargs) -> None:
		"""Send embed listing today release from specified BetaSeries account

		Parameters
    	-----------
			ctx: :class:`reverse.core._models.Context`
		"""
		ctx = kwargs['ctx']

		data = await self.planning_today()
		episodes = data.get('days', [])

		embed=Embed(title="Sortie du jour", color=0xe80005, timestamp=datetime.datetime.today(), thumbnail=self.LOGO)
		if(len(episodes) > 0):
			for e in episodes['events']:
				e = e['payload']
				name = "{} {} — {}".format(e['show_title'], e['code'], e['title'])
				value = "[Source]({})".format(e['resource_url'])
				embed.add_field(name=name, value=value, inline=False)
		else:
			embed.add_field(name="Aucune sortie", value="N'oubliez pas d'ajouter de nouvelle séries sur Betaseries.", inline=False)
		embed.set_footer(text="".format("The Reverse"))

		await ctx.send(embed=embed)

	async def planning_member(self) -> dict:
		"""Return dictionnary of released planning of user
		"""
		r = Route('GET', '/planning/member')
		return await self.b.request(r)

	async def planning_today(self) -> dict:
		"""Return dictionnary of planning of today release from specified user
		"""
		today = datetime.date.today()
		r = Route('GET', '/planning/calendar', '&start={start}&end={end}&type={type}', start=today, end=today, type='all')
		return await self.b.request(r)

	
def setup(bot):
	bot.add_cog(Series(bot))