# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import assignation
from assignation import *
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
from igdb_api_python.igdb import igdb
import time, os, calendar
import platform
import requests
import threading
import logging
from logging.handlers import RotatingFileHandler

#File [GLOBAL][INFO]
filePath = "temp/alreadyPick.txt"

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

#Channel for BonjourMadame/NSFW
cuisine = "414004404170129409"

#Dictionary
peopleMagazine = {
	"sacrezar":
		{
			"youtubeDay": "Dimanche",
			"youtubeChannel": "UCulTxICf-VY2MQ1Ghgh3FhA",
			"age": 18,
			"taille": 180,
			"Java": True,
		},
	"lstf":
		{
			"youtubeDay": "Aucune Idée",
			"youtubeChannel": "UCXGdFAJCL6vweQbXH9f0Pkg",
			"age": 18,
			"taille": 170,
			"Java": False,
		},
}

def game_url(a):
    try:
        return a["websites"][0].get('url')
    except (IndexError, KeyError):
        return "NoWebsite"

def game_check(a, arrayIndex):
    try:
        return a[arrayIndex]
    except IndexError:
        return "NoInformation"

def game_dev(a, b):
    try:
        s = str(a["developers"])[1:].split(']', 1 )[0]
        companie = b.companies({
            'fields': ['name', 'url'],
            'ids': int(s),
            'limit': 1
        })
        return companie.body[0]
    except KeyError:
        return {"name": "NoDevelopers", "url": "http://NoDevelopers.com/"}

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Basic Bot by Habchy#1665", command_prefix="-", pm_help = False)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Support Discord Server: https://discord.gg/FNNNgqb')
	print('Github Link: https://github.com/Habchy/BasicBot')
	print('--------')
	print('You are running BasicBot v2.1') #Do not change this. This will really help us support you, if you need support.
	print('Created by Habchy#1665')
	return await client.change_presence(game=discord.Game(name='Street Fighter VI')) #This is buggy, let us know if it doesn't work.

# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(*args):

	await client.say(":ping_pong: Pong!")
# After you have modified the code, feel free to delete the line above so it does not keep popping up everytime you initiate the ping commmand.

@client.command()
async def pong(*args):

	await client.say(":ping_pong: Ping!")

@client.command()
async def releaseSoon(*args):
	entryNumber = 6
	igdbKey = igdb("7e828d5d6221bd313a973b7cc579517c")
	print(42)

	#Get platform info
	platform = igdbKey.platforms({
		'ids':6,
		'fields' : ['games','name']
	})

	#Release soon for "platforms"
	result = igdbKey.release_dates({
		'filters' :{
			"[platform][eq]": 6,
			"[date][gt]"    : int(round(time.time() * 1000))
		},
		'order':"date:asc",
		'fields':"game"
	})
	await client.say("Game release soon for " + platform.body[0]["name"])
	for i in range(0, entryNumber):
		#print(result.body[i]["game"])
		entry = igdbKey.games(result.body[i]["game"])
		for game in entry.body:
			#Get developers
			dev = game_dev(game, igdbKey)
			#Send Embeb
			embed=discord.Embed(title=game["name"], url=game["url"], description=game["summary"])
			embed.set_author(name=dev["name"], url=dev["url"], icon_url="https://images.igdb.com/igdb/image/upload/t_logo_med/gmvivzajx011hypgi2tu.png")
			embed.set_thumbnail(url="https://images.igdb.com/igdb/image/upload/t_cover_big/wazuvwow24jyyrrdhlbc.jpg")
			embed.add_field(name="Genre", value=game["genres"], inline=False)
			embed.add_field(name="GameMode", value=game["player_perspectives"], inline=True)
			embed.add_field(name="Website", value=game_url(game), inline=True)
			embed.add_field(name="Release Date", value=time.strftime("%d/%m/%Y", time.localtime(game_check(game, "first_release_date")/1000)), inline=True)
			embed.add_field(name="Note", value="Not released Yet", inline=True)
			await client.say(embed=embed)

@client.command()
async def sacrezar(*args):
	embed=discord.Embed(title="Un petit producteur...", url="https://www.youtube.com/user/sacrezar", description="Youtube")
	embed.set_author(name="Lainkulte", url="https://twitter.com/sacrezar")
	embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/851600203828350976/JuNIgQ3K_400x400.jpg")
	embed.add_field(name="--", value="-------------------------------------------------------------", inline=True)
	embed.set_footer(text="Je vous présente aujourd'hui, un petit youtuber dévoué. En effet, ce jeune homme plein de bonne volonté ne souhaite que nous faire découvrir sa passion. Il ne fait pas de vidéo minecraft à la con mais présente  ses trouvailles, ses pépites et ses attentes. Il soutient les jeux indépendants comme il soutient la volonté, l'acharnement et la détermination des petites entreprises.")
	await client.say(embed=embed)

@client.command(pass_context = True)
async def SetCuisine(ctx, args):
	#if ctx.message.author.server_permissions.administrator:
	global cuisine
	cuisine = str(args)
	await client.say("Cuisine is set in {}".format(client.get_channel(args).name))
	return cuisine

@client.command()
async def GetCuisine(ctx):
	#if ctx.message.author.server_permissions.administrator:
	await client.say("Cuisine is actually in {}".format(client.get_channel(cuisine).name))
	return cuisine

@client.command(pass_context = True)
async def BonjourMadame(ctx, *args):
	if ctx.message.author.server_permissions.administrator:
		response = requests.get("https://bonjourmadame.xorhak.io/api/latest")
		response = response.json()
		embed=discord.Embed(title=response["title"], url="http://dites.bonjourmadame.fr/")
		embed.set_author(name="Joakim [Lord of Uganda]")
		embed.set_image(url=response["url"])
		channel = client.get_channel(cuisine)
		logger.info("Message send in %s with commands BonjourMadame." % channel.name)
		await client.send_message(channel, embed=embed)

@client.command(pass_context = True)
async def periodic(ctx):
    #Periodic
	if ctx.message.author.server_permissions.administrator:
		sleep = 3600
		isSummer = True
		if isSummer:
			next_hour = 28800
		else:
			next_hour = 32400
		#Next show next day 10h
		tuple_time = time.gmtime( int(time.time()) + (86400 - (int(time.time()) % 86400)) + next_hour)

		lastShow = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(calendar.timegm(time.gmtime())))
		nextShow = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(calendar.timegm(tuple_time)))
		while True:
			logger.info("Last show : {}".format(lastShow))
			logger.info("Next show : {}".format(nextShow))
			#if heure actuelle >= prochaine event
			if time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(calendar.timegm(time.gmtime()))) >= nextShow:
				tuple_time = time.gmtime( int(time.time()) + (86400 - (int(time.time()) % 86400)) + next_hour)
				lastShow = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(calendar.timegm(time.gmtime())))
				nextShow = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime( calendar.timegm(tuple_time) ))
				response = requests.get("https://bonjourmadame.xorhak.io/api/latest")
				response = response.json()
				embed=discord.Embed(title=response["title"], url="http://dites.bonjourmadame.fr/")
				embed.set_author(name="Joakim [Lord of Uganda]")
				embed.set_image(url=response["url"])
				channel = client.get_channel(cuisine)
				logger.info("Message send in %s with commands BonjourMadame." % channel.name)
				await client.send_message(channel, embed=embed)
			else:
				print("Pas maintenant. heure actuelle : " + time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(calendar.timegm(time.gmtime()))))
			await asyncio.sleep(sleep)

async def sacrezarSpecial(ctx, *args):
@client.command(pass_context = True)
	argument = list(args)
	for i in range(0, len(argument)):
		try:
			argument[i] = peopleMagazine[argument[i].lower()]['youtubeChannel']
		except:
			logger.warning("User = {}, Channel = {}, Command  = YoutubeLastVideoPreview, INFO = Don't found the user {}".format(ctx.message.author, ctx.message.channel, argument[i]))
			argument.pop[i]
	#Info
	logger.info("User = {}, Channel = {}, Command  = YoutubeLastVideoPreview, Youtuber = {}".format(ctx.message.author, ctx.message.channel, argument))
	for i in range(0, len(argument)):
		#Get info request
		response = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&maxResults=1&order=date&type=video&key=AIzaSyCNbAUjTx07i7cWw1fyKDxhM9PFpUtwQ-o".format(argument[i]))
		response = response.json()
		#Debug
		logger.debug(response)
		#Embed
		thumbnails = response['items'][0]['snippet']
		embed=discord.Embed(title=thumbnails['title'], url="https://www.youtube.com/watch?v={}".format(response['items'][0]['id']['videoId']))
		embed.set_author(name=thumbnails['channelTitle'], url="https://www.youtube.com/channel/{}".format(thumbnails['channelId']))
		embed.set_thumbnail(url=thumbnails['thumbnails']['high']['url'])
		embed.set_footer(text=response['items'][0]['snippet']['description'])
		#Send
		logger.info("Send youtuber embed {}".format(thumbnails['title']))
		await client.say(embed=embed)

@client.command()
async def getPeople():
	await client.say(peopleMagazine)

@client.command(pass_context = True)
async def getVideos(ctx, *args):
	argument = list(args)
	for i in range(0, len(argument)):
		#Get info request
		response = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&maxResults=1&order=date&type=video&key=AIzaSyCNbAUjTx07i7cWw1fyKDxhM9PFpUtwQ-o".format(argument[i]))
		response = response.json()
		#Debug
		logger.debug(response)
		#Embed
		thumbnails = response['items'][0]['snippet']
		#Info Youtuber Name
		logger.info("User = {}, Channel = {}, Command = YoutubeLastVideoPreview INFO = YoutuberName : {}".format(ctx.message.author, ctx.message.channel, thumbnails['channelTitle']))
		try:
			
			try:
				peopleMagazine[thumbnails['channelTitle'].lower()]
			except:
				peopleMagazine[thumbnails['channelTitle'].lower()] = {}

			peopleMagazine[thumbnails['channelTitle'].lower()]['youtubeChannel'] = argument[i]
		except:
			logger.warning("User = {}, Channel = {}, Command = YoutubeLastVideoPreview INFO = YoutuberName : {} Error adding in dictionnary PeopleMagazine".format(ctx.message.author, ctx.message.channel, thumbnails['channelTitle']))
		#Embeb
		embed=discord.Embed(title=thumbnails['title'], url="https://www.youtube.com/watch?v={}".format(response['items'][0]['id']['videoId']))
		embed.set_author(name=thumbnails['channelTitle'], url="https://www.youtube.com/channel/{}".format(thumbnails['channelId']))
		embed.set_thumbnail(url=thumbnails['thumbnails']['high']['url'])
		embed.set_footer(text=response['items'][0]['snippet']['description'])
		#Send
		logger.info("Send youtuber embed {}".format(thumbnails['title']))
		await client.say(embed=embed)

@client.command(pass_context = True)
async def clearGod(ctx, number):
	if ctx.message.author.server_permissions.administrator:
		logger.info("User = {}, Clear Number = {}, Channel = {},".format(ctx.message.author, number, ctx.message.channel) )
		mgs = [] #Empty list to put all the messages in the log
		number = int(number) #Converting the amount of messages to delete to an integer
		async for x in client.logs_from(ctx.message.channel, limit = number):
			mgs.append(x)
		await client.delete_messages(mgs)
	else:
		logger.warning("{} don't have the right to use command clear".format(ctx.message.author))

@client.command()
async def addMusic(*args):
	#Private variable
	argument = list(args)
	filemode = "a"
	startForValue = 0

	#Check if the user want to clean the file
	if argument[0] == "clear":
			filemode = "w"
			startForValue = 1
			print("File mode Writing, delete the old file")

	#Append in the file
	with open("D:\FiftyTwo\BasicBot\Music\musicList.txt", filemode) as myfile:
		print("File musicList append. number of block : %s" % len(argument))
		for i in range(startForValue, len(argument)):
			try:
				myfile.write("%s \n" % argument[i].split('`')[1])
			except:
				myfile.write("%s \n" % argument[i])
			print("    %s" % argument[i])

@client.command(pass_context=True)
async def roll(ctx):  
	if(str(ctx.message.author.id) == '205327380334510081' or str(ctx.message.author.id) == '124598335230312448'):
		listG1 = ["Dorian BUQUET", "Valentin CASEN", "Christophe CHICHMANIAN", "Paul DESBUISSONS", "Pierre FLEURY", "Gregory HUE", "Thomas ISAAC", "Alexandre JALLAN", "Francois MOUTON", "Jonathan SEGUIN", "Charles SEMARD" ]
		listG2 = ["Charlotte BENARD", "Clement BLIN", "Achille BROSSIER", "Michael DRACY", "Romain DUGARIN", "Vincent JOULAIN", "Gwendal LUPART", "Theophile RENOUF", "Thomas SOULAS", "Youssef ZAAGOUGUI"]
		listG3 = ["Alexi AL KHOURY", "Meline AMBROSINI", "Pierre BOUTIN", "Louis CHOCHOY", "Corentin HANGARD", "Adrien LALISSE", "Guillaume LEGUIDE", "Pierre-Loup MARTIGNE", "Pierre OUDIN", "Gauthier PARVILLERS", "Antoine SOULAIRE", "Alexandre VIVIER BAUDRY"]

		assigner = Assignation_roles_random(0, 1, len(listG1)-1)
		logger.info("G1 : {}".format(assigner))
		tirLeader1 = listG1[assigner['leader']]
		tirSecret1 = listG1[assigner['secretaire']]
		tirScrib1 = listG1[assigner['scribe']]
		tirTkeeper1 = listG1[assigner['gestionnaire']]

		assigner = Assignation_roles_random(0, 2,  len(listG2)-1)
		logger.info("G2 : {}".format(assigner))
		tirLeader2 = listG2[assigner['leader']]
		tirSecret2 = listG2[assigner['secretaire']]
		tirScrib2 = listG2[assigner['scribe']]
		tirTkeeper2 = listG2[assigner['gestionnaire']]

		assigner = Assignation_roles_random(0, 3, len(listG3)-1)
		logger.info("G3 : {}".format(assigner))
		tirLeader3 = listG3[assigner['leader']]
		tirSecret3 = listG3[assigner['secretaire']]
		tirScrib3 = listG3[assigner['scribe']]
		tirTkeeper3 = listG3[assigner['gestionnaire']]
		await client.say("@everyone\n ```md\n /* Attribution des rôles pour le prochain prosit :* \n \n Groupe 1 : \n--------\n\n* Animateur : < " + tirLeader1 + " > \n* Secrétaire : < " + tirSecret1 + " > \n* Scribe : < " + tirScrib1 + " > \n* Gestionnaire : < " + tirTkeeper1 +" > \n \n\n Groupe 2 : \n--------\n\n* Animateur : < " + tirLeader2 + " > \n* Secrétaire : < " + tirSecret2 + " > \n* Scribe : < " + tirScrib2 + " > \n* Gestionnaire : < " + tirTkeeper2 + " > \n\n \n Groupe 3 : \n--------\n\n* Animateur : < " + tirLeader3 + " > \n* Secrétaire : < " + tirSecret3 + " > \n* Scribe : < " + tirScrib3 + " > \n* Gestionnaire : < " + tirTkeeper3 + " >\n \n> Amusez vous bien ! \n ```" )
	else:
		await client.say("`\nTu n'es pas autorisé\n`")
		time.sleep(1)
		mgs = []
		async for x in client.logs_from(ctx.message.channel,2):
			mgs.append(x)
		await client.delete_messages(mgs)  
        
#Modifier la ligne Genre
#Modifier la ligne Gamemode par ["per"]

client.run('NDA1MzIyMzQ4MTI0ODMxNzQ0.DUivbw.oVnS3eNcH-hm7GAtQdJ87yqC8qM')