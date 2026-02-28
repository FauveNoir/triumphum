########################################################################
# Éidition des bases de données (nouveau)
########################################################################
import json

from triumphum.global_variables import *
import triumphum.config_file as config_file
from triumphum.debug import * # TODO

# Fonctions primitives #################################################

def isObjectExistInsideListOfObjects(theObject, listOfObjects):
    for anObject in listOfObjects:
        if theObject["code"] == listOfObjects[anObject].code:
            return True
    return False

def isNewObjectCodeAllowed(theObject, listOfObjects):
    if not isObjectExistInsideListOfObjects(theObject, listOfObjects) and theObject["code"] != None:
        return True
    return False

def realyAddObjectToDataBase(theObject=None, object_file=None, objectGroupName=None):

    # Charger le contenu JSON depuis le fichier
    with open(object_file, 'r') as jsonFile:
        jsonContent = json.load(jsonFile)

    jsonContent[objectGroupName].append(theObject)

    # Réécrire le fichier JSON avec le contenu mis à jour
    with open(object_file, 'w') as jsonFile:
        json.dump(jsonContent, jsonFile, indent="\t")

# Fonctions primitive #################################################################

def addObjectToDataBase(theObject=None, listOfObjects=None, object_file=None, objectGroupName=None, object_name=None):
    if isNewObjectCodeAllowed(theObject, listOfObjects) :
        realyAddObjectToDataBase(theObject=theObject, object_file=object_file, objectGroupName=objectGroupName)
        return True
    elif isObjectExistInsideListOfObjects(theObject, listOfObjects):
        print(f"Le code « {theObject['code']} » éxiste déjà.")
        return False
    elif code == None:
        print(f"Veuillez déffinir un code d’entification pour le {object_name}.")
        return False

# Fonctions dérrivées #################################################################

def addGameToDataBase(theObject):
    return addObjectToDataBase(theObject=theObject, listOfObjects=listOfGames, object_file=config_file.GAME_FILE.fullPath(), objectGroupName="games", object_name="jeu")

def addGenreToDataBase(theObject):
    addObjectToDataBase(theObject=theObject, listOfObjects=listOfGenres, object_file=config_file.GENRE_FILE.fullPath(), objectGroupName="genres", object_name="genre")

def addLicenceToDataBase(theObject):
    addObjectToDataBase(theObject=theObject, listOfObjects=listOfLicences, object_file=config_file.LICENCE_FILE.fullPath(), objectGroupName="licences", object_name="licence")

def addPlatformToDataBase(theObject):
    addObjectToDataBase(theObject=theObject, listOfObjects=listOfPlatforms, object_file=config_file.PLATFORM_FILE.fullPath(), objectGroupName="platforms", object_name="plateforme")

########################################################################
# Éidition des bases de données | Délétion (nouveau)
########################################################################

#
# Primitive
#

def deleteObjectFromDatabase(givenObject=None, listOfObjectsFile=None, objectGroupName=None):
    with open(listOfObjectsFile, 'r') as f:
        jsonContent = json.load(f)  # Charger le JSON dans une structure de données Python

    founded=False
    # Vérifier si la clé "games" existe et qu'elle est une liste
    if objectGroupName in jsonContent and isinstance(jsonContent[objectGroupName], list):
        list_ = jsonContent[objectGroupName]
        # Parcourir la liste des jeux
        for anObject in list_:
            # Vérifier si l'objet a pour valeur "code": "abc"
            if isinstance(anObject, dict) and anObject.get('code') == givenObject:
                founded=True
                list_.remove(anObject)  # Supprimer l'élément de la liste
    
    if founded:
        # Réécrire le fichier JSON avec les modifications
        with open(listOfObjectsFile, 'w') as f:
            json.dump(jsonContent, f, indent='\t')  # Réécrire le JSON avec indentation pour la lisibilité

#
# Dérrivée
#

def deleteGameFromDatabase(givenObject):
    deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=config_file.GAME_FILE.fullPath(), objectGroupName="games")

def deleteLicenceFromDatabase(givenObject):
    deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=config_file.LICENCE_FILE.fullPath(), objectGroupName="licences")

def deleteGenreFromDatabase(givenObject):
    deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=config_file.GENRE_FILE.fullPath(), objectGroupName="genres")

def deletePlatformFromDatabase(givenObject):
    deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=config_file.PLATFORM_FILE.fullPath(), objectGroupName="platforms")

