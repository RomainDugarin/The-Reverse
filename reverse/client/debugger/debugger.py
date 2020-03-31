from discord.ext import commands
import asyncio
from urllib import parse
from discord import Embed

from reverse.core._service import SqliteService
from reverse.core import utils


class Debugger(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		try:
			self.config = utils.load_custom_config('config.json', __file__, path='')
		except:
			self.config = None
		
		

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



def setup(bot):
	bot.add_cog(Debugger(bot))