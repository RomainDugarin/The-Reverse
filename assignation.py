import discord
import os
import random, time
import linecache, re #Inutiliser
import logging
from logging.handlers import RotatingFileHandler

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
file_handler = RotatingFileHandler('assignation.log', 'a', 1000000, 1, encoding='utf-8')
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


#Role disponible [GLOBAL][INFO]
role = ['leader', 'scribe', 'secretaire', 'gestionnaire']
#File [GLOBAL][INFO]
filePath = "temp/alreadyPick.txt"

#Assignation_roles_random(choix, i, nbPersonnes)
    #Choix  -> Prasit(1) ou 0
    #i      -> Numéro de groupe
    #nbPersonnes -> Nombre de personne(Len())
    #Role disponible : variable role [global] par default
def Assignation_roles_random(choix, groupNumberGlobal, nbPersonnes, tempRole=role):

    #Role disponible
    if tempRole:
        tempRole = role
    else:
        tempRole = ['leader', 'scribe', 'secretaire', 'gestionnaire']
    logger.debug(tempRole)

    #Recuperation des données -> Liste
    myDict = {}
    with open(filePath, "r+") as f:
      for line in f:
            #Variable de check
            temp = re.split(',|\n|:', line)

            #Iniatialise le format des données
            for i in range(0, len(temp)):
                if(temp[i] == ''):
                    del temp[i]
                elif(temp[i] in tempRole):
                    logger.debug(temp[i])
                else:
                    temp[i] = int(temp[i])
            
            #Verifie si la variable myDict a besoin d'une inialisation
            try:
                myDict[temp[0]]
            except:
                myDict[temp[0]] = {}

            #Ajoutes les valeurs au dictionnaire
            myDict[temp[0]][temp[1]] = temp[2:]

            #Check les valeurs [DEBUG]
            logger.debug("Numero deja passer dans les roles suivant : {}".format(myDict))
    #Ferme le fichier
    f.closed

    #Initialise myDict si alreadyPick.txt est vide
    if(myDict == {}):
        for iGroup in range(1,3):
            myDict[iGroup] = {}
            for iRole in role:
                myDict[iGroup][iRole] = []

    logger.info(myDict[3])
    #Valeur recupèrer
    logger.debug("Valeur recuperer : {}".format(myDict))

    #Random value
    randValue = getTirage(myDict[groupNumberGlobal], time.time(), nbPersonnes, tempRole,)
    logger.info("valeur random : {}".format(randValue))

    finalization(myDict, randValue, 8, groupNumberGlobal)

    return randValue

#Retourne un élément de la liste
def getTirage(mylist, seedValue, maxUser, role):
    #Variable local
    random.seed(seedValue)
    randValue = random.randint(0, maxUser)
    randReturn = {}
    logger.debug("RandValue : {}".format(randValue))

    #Fais un tirage sur tout les roles
    for i in role:
        #Verifie si il y a une valeur a recuperer
        try:
            #Si une valeur a etait deja prise, en rand une autre
            while(randValue in mylist[i] or randValue in randReturn.values()):
                #Creer une boucle infini si randValue == 0, on ajoute donc 1 dans ce genre de cas
                if(randValue == 0):
                    seedValue += randValue+1
                else:
                    seedValue += randValue
                #Lance un nouveau random
                random.seed(seedValue)
                randValue = random.randint(0, maxUser)
                logger.debug("{} IDTemporaire : {}".format(i, randValue))
            
        #Sinon prend une valeur au hasard différente des autres
        except:
            #logger.info("Mylist[{}] doesn't exist, random value : ".format(i))
            while(randValue in randReturn.values()):
                #Creer une boucle infini si randValue == 0, on ajoute donc 1 dans ce genre de cas
                if(randValue == 0):
                    seedValue += randValue+1
                else:
                    seedValue += randValue
                #Lance un nouveau random
                random.seed(seedValue)
                randValue = random.randint(0, maxUser)
                logger.debug("{} IDTemporaire : {}".format(i, randValue))
    
        #Ajoute la valeur dans un dictionnaire
        randReturn[i] = randValue
        #Donne l'information sur l'ID à itération de la boucle
        logger.debug("{} ID : {}".format(i, randReturn))

    #Renvoie les valeurs recuperer
    logger.debug("Numero recuperer avant le return getTirage() : {}".format(randReturn))
    return randReturn

#Retourne le nom des personnes selectionné
    #Mettre à jour les paramètres de la fonction
    #getName(randValue, myDict, i)
def getName(randValue, mylist):
    try:
        return mylist[i][randValue]
    except:
        return -1

#Recréer le fichier alreadyPick
def finalization(alreadyPick, randomList, arrayRange, groupNumber):
    stemp = ""
    stempIn = ""
    #Add picked value in dictionnary 
    logger.info(alreadyPick)
    for lineRole in role:
        try:
            #Add value in the dictionnary
            alreadyPick[groupNumber][lineRole].append(randomList[lineRole])
        except:
            #Try failed, check if role in dictionnary exist
            alreadyPick[groupNumber][lineRole] = [randomList[lineRole]]

    #[1, 2, 3]      
    for keyOut in alreadyPick:
        #['leader', 'scribe', 'secretaire', 'gestionnaire']
        for keyIn in alreadyPick[keyOut]:
            #Initialise la detection de chaine
            stempIn = str(keyOut) + ":" + keyIn + ":" 

            #Delete element out of range, arrayRange var int
            if(len(alreadyPick[keyOut][keyIn]) > arrayRange):
                del alreadyPick[keyOut][keyIn][:len(alreadyPick[keyOut][keyIn])-arrayRange]
                logger.debug("The array reached max element value, NEWARRAY = {}".format(alreadyPick[keyOut][keyIn]))

            #for i in alreadyPick[keyOut][keyIn]:
            for i in range(len(alreadyPick[keyOut][keyIn])):
                stempIn += str(alreadyPick[keyOut][keyIn][i]) + ","
            
            #Initialise LOCAL var to inject in file alreadyPick.txt
            stemp += stempIn[:-1] + "\n"
            logger.debug("String send in record file = {}".format(stempIn[:-1]))
    logger.info("FILE = {}".format(stemp))

    #Modify alreadyPick.txt for next assignement
    the_file = open(filePath, 'w')
    the_file.write(stemp)
    the_file.close()

def createFile():
    the_file = open(filePath, 'w')
    the_file.close()

