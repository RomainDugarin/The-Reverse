from discord.ext import commands
from discord.utils import get
from discord import Guild, Embed
import asyncio, datetime
from reverse.core._service import SqliteService
from reverse.core._models import Context, Role, Message
from reverse.core import utils


class pierre(commands.Cog):

	REACTION = [
		"😩",
		"🙁",
		"😶",
		"😐",
		"🙂",
		"😁"
	]

	def __init__(self, bot):
		self.bot = bot
		self.db = SqliteService()
		
	@commands.command()
	async def askme(self, ctx):
		embed = Embed(title="How are you ?", color=0xe80005, timestamp=datetime.datetime.today())
		embed.add_field(name="Terrible", value=":weary:", inline=True)
		embed.add_field(name="Sad", value=":slight_frown:", inline=True)
		embed.add_field(name="Don't know", value=":no_mouth:", inline=True)
		embed.add_field(name="Ok-ish", value=":neutral_face:", inline=True)
		embed.add_field(name="Good", value=":slight_smile:", inline=True)
		embed.add_field(name="Fine", value=":grin:", inline=True)
		message = await ctx.send(embed=embed)
		
		for item in pierre.REACTION:
			await message.add_reaction(item)

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if(user.id != 501719851740561408):
			message = reaction.message
			await message.channel.send("Merci {} de ta réponse. ({})".format(user, reaction))
			await message.delete()
		
		


def setup(bot):
	bot.add_cog(pierre(bot))