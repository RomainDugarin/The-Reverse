# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import time, os, calendar
import platform
import requests
import threading
import logging
from logging.handlers import RotatingFileHandler

#File [GLOBAL][INFO]
filePath = "dist/alreadyPick.txt"

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

client.run('NDA1MzIyMzQ4MTI0ODMxNzQ0.DUivbw.oVnS3eNcH-hm7GAtQdJ87yqC8qM')