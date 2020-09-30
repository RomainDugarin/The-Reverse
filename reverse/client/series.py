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

	@commands.command()
	async def start(self, ctx):
		"""Start coroutine that trigger every day at 7am to display Planning of specified day released

		Parameters
		----------
		ctx : :class:`reverse.core._models.Context`
			Context
		"""
		ctx = Context(ctx)

		next_call = utils.now() + datetime.timedelta(days=1)
		next_call = next_call.replace(hour=7, minute=0, second=0)

		delta = utils.time_until(next_call)
		data = {}
		print(delta)
		
		_loop = self.task.createLoop(self.release_today, seconds=delta, ctx=ctx, data=data)
		_loop.start(ctx=_loop.ctx, data=_loop.data)

	@commands.command()
	async def pt(self, ctx):
		"""Alias for Planning Calendar today

		Parameters
    	-----------
			ctx: :class:`reverse.core._models.Context`
		"""
		Context(ctx)
		await self.planning_today()

	async def release_today(self, **kwargs):
		"""Send embed listing today release from specified BetaSeries account

		Parameters
    	-----------
			ctx: :class:`reverse.core._models.Context`
		"""
		ctx = kwargs['ctx']

		data = await self.planning_today()
		episodes = data['days'][0]

		embed=Embed(title="Sortie du jour", color=0xe80005, timestamp=datetime.datetime.today(), thumbnail="https://www.betaseries.com/images/site/betaseries.svg")
		for e in episodes['events']:
			e = e['payload']
			name = "{} {} — {}".format(e['show_title'], e['code'], e['title'])
			value = "[Source]({})".format(e['resource_url'])
			embed.add_field(name=name, value=value, inline=False)
		embed.set_footer(text="".format("The Reverse"))

		await ctx.send(embed=embed)

	async def planning_member(self):
		"""Return dictionnary of released planning of user
		"""
		r = Route('GET', '/planning/member')
		return await self.b.request(r)

	async def planning_today(self):
		"""Return dictionnary of planning of today release from specified user
		"""
		today = datetime.date.today()
		r = Route('GET', '/planning/calendar', '&start={start}&end={end}&type={type}', start=today, end=today, type='all')
		return await self.b.request(r)

	
def setup(bot):
	bot.add_cog(Series(bot))