from discord.ext import commands
import asyncio
from urllib import parse
from reverse.core._service import SqliteService

class Missy(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = SqliteService()

	@commands.command()
	async def whoismissy(self, ctx):
		await ctx.send("Une horreur lovecraftienne... Tempus edax rerum.")
	
	@commands.command()
	async def debugSQL(self, ctx, table="missy", column="id integer PRIMARY KEY, name text"):
		self.db.createTable(table, column)

	@commands.command()
	async def showTable(self, ctx):
		record = self.db._fetchAll(self.db.listTable())
		for v in record:
			await ctx.send("Table {}.".format(*v))

	async def tableToList(self):
		record = self.db._fetchAll(self.db.listTable())
		return [item for t in record for item in t]

	@commands.command()
	async def debugInsertAllMembers(self, ctx):
		guild = ctx.guild
		await ctx.send("Fetch all members from {} called by {}".format(ctx.guild.name, ctx.author.name))
		self.db.createTable(guild.name, "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, discordID TEXT, UNIQUE(id, discordID)")
		for v in guild.members:
			self.db.insertion(guild.name, ["name", "discordID"], [v.name, str(v.id)], ignore=True)
		await ctx.send("Successfully inserted {} entries to Table {} ".format(len(guild.members), guild.name))

def setup(bot):
	bot.add_cog(Missy(bot))