########################################################################
# Éidition des bases de données | Inséretion
########################################################################
import json

from triumphum.global_variables import *
import triumphum.config_file as config_file
from triumphum.debug import * # TODO

#
# Fonctions primitives
#

def isObjectExistInsideListOfObjects(theObject, listOfObjects):
    # Test de l’exitence de l’objet dans sa base de donnée
    # Utilisé pour éviter l’écrasement d’objets déjà éxistants par de nouveaux
    for anObject in listOfObjects:
        if theObject["code"] == listOfObjects[anObject].code:
            return True
    return False

def isNewObjectCodeAllowed(theObject, listOfObjects):
    # Test si le code du nouvel objet à ajouter est autorisé
    # Notament dans les cas où un objet ayant le même code éxiste déjà
    if not isObjectExistInsideListOfObjects(theObject, listOfObjects) and theObject["code"] != None:
        return True
    return False

def realyAddObjectToDataBase(theObject=None, object_file=None, objectGroupName=None):
    # Insertion de l’objet dans sa base de données

    # Charger le contenu JSON depuis le fichier
    with open(object_file, 'r') as jsonFile:
        jsonContent = json.load(jsonFile)

    jsonContent[objectGroupName].append(theObject)

    # Réécrire le fichier JSON avec le contenu mis à jour
    with open(object_file, 'w') as jsonFile:
        json.dump(jsonContent, jsonFile, indent="\t")

#
# Fonction de factorisation
#

def addObjectToDataBase(theObject=None, listOfObjects=None, object_file=None, objectGroupName=None, object_name=None):
    # Cette fonction décrit le cas général d’insertion d’objet de tout type dans son fichier spécifique
    # Comme le fonctionnement de l’insértion est, à quelques détails prêt, le même pour les jeux, genres, plateformes, et licences, cette fonction permet de facotoriser la mécanique d’insérsion en ne modifieant que les aspects qui changent vraiment entre les différents typesd’objet. Comme le fichier contenant les déffinitions, la variable contenant le type d’objet en question, ou le nom du type d’objet pour les afficher en message.
    if isNewObjectCodeAllowed(theObject, listOfObjects) :
        realyAddObjectToDataBase(theObject=theObject, object_file=object_file, objectGroupName=objectGroupName)
        return True
    elif isObjectExistInsideListOfObjects(theObject, listOfObjects): # TODO voir pourquoi isObjectExistInsideListOfObjects() est utilisé deux fois qui font doublon
        print(f"Le code « {theObject['code']} » éxiste déjà.")
        return False
    elif code == None:
        print(f"Veuillez déffinir un code d’entification pour le {object_name}.")
        return False

#
# Fonctions dérrivées
#

def addGameToDataBase(theObject):
    # ajouter l’objet jeu `theObject` à la base de données
    return addObjectToDataBase(theObject=theObject, listOfObjects=listOfGames, object_file=config_file.GAME_FILE.fullPath(), objectGroupName="games", object_name="jeu")

def addGenreToDataBase(theObject):
    # ajouter l’objet genre `theObject` à la base de données
    addObjectToDataBase(theObject=theObject, listOfObjects=listOfGenres, object_file=config_file.GENRE_FILE.fullPath(), objectGroupName="genres", object_name="genre")

def addLicenceToDataBase(theObject):
    # ajouter l’objet licence `theObject` à la base de données
    addObjectToDataBase(theObject=theObject, listOfObjects=listOfLicences, object_file=config_file.LICENCE_FILE.fullPath(), objectGroupName="licences", object_name="licence")

def addPlatformToDataBase(theObject):
    # ajouter l’objet plateforme `theObject` à la base de données
    addObjectToDataBase(theObject=theObject, listOfObjects=listOfPlatforms, object_file=config_file.PLATFORM_FILE.fullPath(), objectGroupName="platforms", object_name="plateforme")

########################################################################
# Éidition des bases de données | Délétion
########################################################################

#
# Fonction de factorisation
#

def deleteObjectFromDatabase(givenObject=None, listOfObjectsFile=None, objectGroupName=None):
    # Cette fonction décrit le cas général de délétion d’objet de tout type dans son fichier spécifique
    # Comme le fonctionnement de la délétion est, à quelques détails prêt, le même pour les jeux, genres, plateformes, et licences, cette fonction permet de facotoriser la mécanique d’insérsion en ne modifieant que les aspects qui changent vraiment entre les différents typesd’objet. Comme le fichier contenant les déffinitions, la variable contenant le type d’objet en question, ou le nom du type d’objet pour les afficher en message.
    with open(listOfObjectsFile, 'r') as f:
        jsonContent = json.load(f)  # Charger le JSON dans une structure de données Python

    founded=False
    # Vérifier si la clé contenue dans `objectGroupName` existe et qu'elle est une liste
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
# Fonctons dérrivée
#

def deleteGameFromDatabase(givenObject):
    deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=config_file.GAME_FILE.fullPath(), objectGroupName="games")

def deleteLicenceFromDatabase(givenObject):
    deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=config_file.LICENCE_FILE.fullPath(), objectGroupName="licences")

def deleteGenreFromDatabase(givenObject):
    deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=config_file.GENRE_FILE.fullPath(), objectGroupName="genres")

def deletePlatformFromDatabase(givenObject):
    deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=config_file.PLATFORM_FILE.fullPath(), objectGroupName="platforms")

