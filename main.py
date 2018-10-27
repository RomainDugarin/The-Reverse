# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord, asyncio
from lib.discord.ext.commands import Bot
from lib.discord.ext import commands
import time, os, calendar, platform, requests, threading, sys
import logging, json
from logging.handlers import RotatingFileHandler


#Reverse
from Reverse import reverseClient, environment

#========================================================
#===============		LOGGER			=================
# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à INFO
logger.setLevel(logging.INFO)
 
# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1, encoding='utf-8')
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
 
# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
#======================================================
#======================================================

client = Bot(description="The Reverse", command_prefix="-", pm_help = False)
reverseClient = reverseClient()

@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('You are running {} {}'.format(reverseClient.creator['name'], reverseClient.creator['version']))
	print(reverseClient.creator['description'])
	await reverseClient.registerServers(client.servers)
	return await client.change_presence(game=discord.Game(name=reverseClient.creator['game']['name']))

@client.event
async def on_reaction_add(reaction, user):
	if user.permissions_in(reaction.message.channel).administrator:
		if reaction.emoji == '👊':
			try:
				await client.kick(reaction.message.author)
				await client.send_message(reaction.message.channel, 'Ouf, tu vas te prendre un punch {}'.format(reaction.message.author.mention))
			except:
				await client.send_message(reaction.message.channel, 'Ouf, tu as esquivé de justesse le punch {}'.format(reaction.message.author.mention))

# Register the new user
async def registerMember(ctx):
	r = reverseClient.registerMember(ctx)
	# Logger
	logger.info('Post : {} <- {}'.format(r.url, r.json))	
	

@client.command(pass_context = True)
async def newChannel(ctx, channelName, type=None):
	#Search for the channelType value
	await registerMember(ctx.message.author)
	if type is not None:
		for channelType in discord.ChannelType:
			if type == channelType.name: type = channelType
	#Define permission for creator
	permissionCreator = discord.PermissionOverwrite(read_messages=True, manage_channels=True, manage_roles=True)
	#Define permission for everyone
	permissionEveryone = discord.PermissionOverwrite(read_messages=False)
	if not Environment.server.get(ctx.message.server.id):
		await client.say('Private category for conversation doesn\'t exist, ask admin to create one.')
	else:
		#Define permission for creator
		await client.create_channel(ctx.message.server, channelName, Environment.server[ctx.message.server.id]['privateConversation_id'], (ctx.message.server.default_role, permissionEveryone), (ctx.message.author, permissionCreator), type=type)

@client.command(pass_context = True)
async def setPrivateCategory(ctx, categoryName):
	category = reverseClient.findChannel(ctx, categoryName)
	if category is not None:
		if Environment.server.get(ctx.message.server.id):
			await client.send_message(ctx.message.channel, 'Key exist')
		Environment.server[ctx.message.server.id] = { 'privateConversation_id': category.id }
		await client.send_message(ctx.message.channel, 'The private conversation category set to {}.'.format(category.name))
	else:
		await client.send_message(ctx.message.channel, 'No category found.')

@client.command()
async def r():
	sys.exit(0)


client.run(environment.token)