########################################################################
# Autres classes de la console interactive
########################################################################
from triumphum.__init__ import *

def printSplash():
    # Affiche un message d’information sur la sortie standard
    print(SPLASH_MESSAGE)

########################################################################
# Fonction de listage
########################################################################
from prettytable import PrettyTable

from triumphum.global_variables import *
from triumphum.debug import * # TODO

GAME_HEADERS=["Plateforme", "Titre", "Licence", "Genre", "Date", "Dernière ouverture", "Temps cumulé", "Auteur", "Studio"]
LICENCE_HEADERS=["Titre", "URL", "Coeficient"]
PLATFORM_HEADERS=["Titre", "Acronyme"]
GENRES_HEADERS=["Titre", "Acronyme"]

def printObjectsFromTypeTable(object_headers, listOfObjectsFromType):
    # Constructeur d’affichage sur la sortie standard de liste d’objets
    table = PrettyTable()
    table.field_names = object_headers

    for anObject in listOfObjectsFromType:
        # Ajout des données à la table
        row=listOfObjectsFromType[anObject].asciiRow()
        table.add_row(row)

    for anElement in table.field_names:
        table.align[anElement] = "l"

    # Affichage de la table
    print(table)

#
# Déploiement des élemnts construits
#

def printGamesTable():
    printObjectsFromTypeTable(GAME_HEADERS, listOfGames)

def printLicencesTable():
    printObjectsFromTypeTable(LICENCE_HEADERS, listOfLicences)

def printPlatformsTable():
    printObjectsFromTypeTable(PLATFORM_HEADERS, listOfPlatforms)

def printGenresTable():
    printObjectsFromTypeTable(GENRES_HEADERS, listOfGenres)

