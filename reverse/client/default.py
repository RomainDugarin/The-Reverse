from discord.ext import commands
import asyncio
from urllib import parse
from reverse.core import utils


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

		if(await utils.specifiedRole("Cleaner", guild, author, ctx=ctx)):
			if(wait > 0):
				await ctx.send("Removed in {}".format(wait))
				await asyncio.sleep(wait)
			async for message in channel.history(limit=amount+1):
				await message.delete()

	@commands.command()
	async def gamer(self, ctx):
		await ctx.send("Answer me and I will come to you, and I will tell you great and powerful things. Gamers, answer my call and I will give you glory.")
	
	@commands.command(pass_context=True, aliases=['mc', 'dcf'])
	async def countfrom(self, ctx, *args):
		"""Count the number of messages from link. Aliases: !mc !dcf"""
		if(not args):
			await ctx.send("Specify url")
			raise Exception("Cancelled")

		channel = ctx.message.channel
		author  = ctx.author
		guild   = ctx.guild
		msg = None

		checker = ["channels", str(guild.id)]
		for channel in guild.text_channels:
			checker.append(str(channel.id))

		for url in args:
			parsed_url = parse.urlparse(url)
			path_message = parsed_url.path.split("/")[1:]
			if(utils.isListContains(checker, path_message[:3])):
				channel = guild.get_channel(int(path_message[2]))
				try:
					msg = await channel.fetch_message(int(path_message[3]))
				except:
					print("could find message")
					return

		channel = channel or ctx.channel
		count = 0

		#TODO : Verifier que le bot a acces au channel avant de compter
		async for message in channel.history(limit=None):
			count += 1
			if(message == msg):
				break
		
		#TODO : Choisir un meilleur message
		await ctx.send("Message is {}+1 layers deep.".format(count))

	@commands.command(pass_context=True)
	async def md(self, ctx, *args):

		channel = ctx.message.channel
		author  = ctx.author
		guild   = ctx.guild
		msg = None

		_kwargs, _args = utils.parse_args(args)
		obligatory_keys = ["start"]
		print(_kwargs)
		print(_args)

		n = _kwargs.get("start", None)
		for arg in obligatory_keys:
			n = _kwargs.get(arg, None)
			if((n := _kwargs.get(arg, None)) == None):
				print("Argument \"{}\" missing.".format(arg))
				return

		try:
			msg = await self.get_message(guild, _kwargs['start'])
		except:
			print("Link error.")
			return

		try:
			if((n := _kwargs.get('end', None)) != None):
				end = await self.get_message(guild, _kwargs['end'])
		except:
			print("End link error.")
			return

		
		channel = channel or ctx.channel
		count = 0

		#TODO : Verifier que le bot a acces au channel avant de compter
		async for message in channel.history(limit=None):
			count += 1
			if(message == msg):
				break
		
		#TODO : Choisir un meilleur message
		await ctx.send("Message is {}+1 layers deep.".format(count))

	async def get_message(self, guild, url):
		checker = ["channels", str(guild.id)]
		for channel in guild.text_channels:
			checker.append(str(channel.id))

		parsed_url = parse.urlparse(url)
		path_message = parsed_url.path.split("/")[1:]
		if(utils.isListContains(checker, path_message[:3])):
			channel = guild.get_channel(int(path_message[2]))
			try:
				msg = await channel.fetch_message(int(path_message[3]))
				return msg
			except:
				print("could find message")
				return None

	@commands.command(pass_context = True)
	async def delete(self, ctx, *args):
		"""Delete specific message from link."""
		if(not args):
			await ctx.send("Specify url")
			raise Exception("Cancelled")

		channel = ctx.message.channel
		author  = ctx.author
		guild   = ctx.guild

		if(await utils.specifiedRole("Cleaner", guild, author, ctx=ctx)):
			checker = ["channels", str(guild.id)]
			for channel in guild.text_channels:
				checker.append(str(channel.id))

			for url in args:
				parsed_url = parse.urlparse(url)
				path_message = parsed_url.path.split("/")[1:]
				if(utils.isListContains(checker, path_message[:3])):
					channel = guild.get_channel(int(path_message[2]))
					try:
						msg = await channel.fetch_message(int(path_message[3]))
						print(msg)
					except:
						print("could find message")

def setup(bot):
	bot.add_cog(DefaultCog(bot))