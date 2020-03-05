from discord.ext import commands
import asyncio
from urllib import parse


class DefaultCog(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
		await ctx.send('Pong!')

	
	@commands.command(pass_context = True)
	async def clear(self, ctx, amount: int = 1, wait: int = 0):
		""" Clear chat command """
		channel = ctx.message.channel
		author  = ctx.author
		guild   = ctx.guild

		if(await self.specifiedRole("Cleaner", guild, author, ctx=ctx)):
			if(wait > 0):
				await ctx.send("Removed in {}".format(wait))
				await asyncio.sleep(wait)
			async for message in channel.history(limit=amount+1):
				await message.delete()

	@commands.command(pass_context = True)
	async def delete(self, ctx, *args):
		if(not args):
			await ctx.send("Specify url")
			raise Exception("Cancelled")

		channel = ctx.message.channel
		author  = ctx.author
		guild   = ctx.guild

		if(await self.specifiedRole("Cleaner", guild, author, ctx=ctx)):
			checker = ["channels", str(guild.id)]
			for channel in guild.text_channels:
				checker.append(str(channel.id))

			for url in args:
				parsed_url = parse.urlparse(url)
				path_message = parsed_url.path.split("/")[1:]
				if(self.isListContains(checker, path_message[:3])):
					channel = guild.get_channel(int(path_message[2]))
					try:
						msg = await channel.fetch_message(int(path_message[3]))
						await msg.delete()
					except :
						print("could find message")
		
	async def specifiedRole(self, name: str, guild: list, author: list, attr: str = "name", ctx = None):
		g_role = False
		a_role = False
		if(g_role := self.isNameInList(name, guild.roles)) == False:
			if(ctx is not None):
				await ctx.send("You need to create the role `{}` to use this on you server.".format(name))
		if(a_role := self.isNameInList(name, author.roles)) == False:
			if(ctx is not None):
				await ctx.send("You need the role `{}`.".format(name))
		return all([g_role, a_role])

	def isListContains(self, lesser: list, bigger: list):
		"""Check if bigger contains all elements in lesser"""
		return all(elem in lesser for elem in bigger)

	def isNameInList(self, name: str, array: list, attr: str = "name"):
		"""Look for string in list of object on specific attribute

		Keyword arguments:
		name 	-- String to find
		array 	-- List of Object
		attr 	-- Attribute to check in the Object
		"""
		for role in array:
			if(name == getattr(role, attr)):
				return True
		return False

def setup(bot):
	bot.add_cog(DefaultCog(bot))