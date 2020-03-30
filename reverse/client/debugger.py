from discord.ext import commands
import asyncio
from urllib import parse
from discord import Embed

from reverse.core._service import SqliteService


class Debugger(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot

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
		embed.set_footer(text="Asked by {}".format(ctx.author.name))
		await ctx.send(embed=embed)
		
def setup(bot):
	bot.add_cog(Debugger(bot))