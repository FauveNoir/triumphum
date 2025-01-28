#!/usr/bin/python3

import curses
import subprocess
import threading
import json
import webbrowser
import pyperclip
import re
from datetime import date, datetime, timedelta
from tabulate import tabulate
import humanize
#import pendulum
import locale
import time
import shlex
from Xlib import XK
from Xlib.display import Display
import curses.textpad
import os
from prettytable import PrettyTable
import plotext as plt
import numpy as np


from triumphum.__init__ import *
from triumphum.global_variables import *
from triumphum.config_file import prepareConfigFiles, verifyConfigFileExistence, applyFileConfigurationsBindings, applyFileConfigurationsGraphicalSymbols
import triumphum.config_file as config_file
from triumphum.cli_options import args
from triumphum.symbols import *
from triumphum.keybindings import *
from triumphum.layouts import *
from triumphum.internal_shell_class import *
from triumphum.descriptors import addNewGameAfterInterativeDescriptor, addNewGenreAfterInterativeDescriptor, addNewLicenceAfterInterativeDescriptor, addNewPlatformAfterInterativeDescriptor
from triumphum.platforms_classes import create_platform_objects, get_platform_object_after_code
from triumphum.genres_classes import create_game_genre_objects, get_genre_object_after_code
from triumphum.cli_functions import *
from triumphum.debug import *



verifyConfigFileExistence()











########################################################################
# Classe des licences de jeux
########################################################################

# Défffinition de classe
class Licence:
	def __init__(self, name=None, abbr=None, code=None, url=None, shortText=None, fullText=None, freedomCoefficient=0, includeInSorting=True):
		self.name = name
		self.abbr = abbr
		self.code = code
		self.url = url
		self.shortText = shortText
		self.fullText = fullText
		self.freedomCoefficient = freedomCoefficient
		self.includeInSorting = includeInSorting

		listOfLicences[self.code]=self # Adjonction à la liste des licences

	# Blocs de comparaisons permétant de trier les licences entre elles de la plus libre à la moins libre
	def __eq__(self, other):
		if isinstance(other, Licence):
			return self.freedomCoefficient == other.freedomCoefficient
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, Licence):
			return self.freedomCoefficient <  other.freedomCoefficient
		return NotImplemented

	def __le__(self, other):
		if isinstance(other, Licence):
			return self.freedomCoefficient <= other.freedomCoefficient
		return NotImplemented

	def __gt__(self, other):
		if isinstance(other, Licence):
			return self.freedomCoefficient >  other.freedomCoefficient
		return NotImplemented

	def __ge__(self, other):
		if isinstance(other, Licence):
			return self.freedomCoefficient >= other.freedomCoefficient
		return NotImplemented
	def asciiRow(self):
		# Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
		asciiRow = [
			self.name or GENERAL_VOID_SYMBOL,
			self.url or GENERAL_VOID_SYMBOL,
			self.freedomCoefficient or GENERAL_VOID_SYMBOL,
		]
		return asciiRow

def create_licence_objects():
	# Extraction des licences
	with open(LICENCE_FILE.fullPath()) as f:
		listOfLicencesData = json.load(f)["licences"]

	# Déploiment des objet de licence
	for aLicence in listOfLicencesData:
		Licence(
			name=aLicence.get("name"),
			code=aLicence.get("code"),
			abbr=aLicence.get("abbr"),
			url=aLicence.get("url"),
			shortText=aLicence.get("shortText"),
			freedomCoefficient=aLicence.get("freedomCoefficient") or 0
		)

unknownlicence=Licence(name="Licence inconue", abbr=LICENCE_VOID_SYMBOL.value, code="unknownlicence", includeInSorting=False)

def get_licence_object_after_code(code):
	if code in listOfLicences:
		return listOfLicences[code]
	return unknownlicence

########################################################################
# Classe des commentaires
########################################################################

class Comment:
	def __init__(self, date=None, content=None):
		self.date = date
		self.content = content

########################################################################
# Classe des historiques
########################################################################

# Classe d’une entrée particulière d’un historique
class HistoryEntry:
	def __init__(self, start_time=None, end_time=None, duration=None, dictionnary=None):
		self.start_time=start_time or dictionnary["start_time"]
		self.end_time=end_time or dictionnary["end_time"]
		self.duration=duration or dictionnary["duration"]

	def make_data(self):
		data = {
			"start_time": self.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
			"end_time": self.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
			"duration": self.duration.__str__(),
		}

		return data

	def make_json(self):
		# Bloc de transforamtion en json pour l’inscription dans l’historique persistant
		data=self.make_data()
		json_data = json.dumps(data)
		return json_data

	# Blocs de comparaison pour le tri
	def __eq__(self, other):
		if isinstance(other, HistoryEntry):
			return self.end_time == other.end_time
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, HistoryEntry):
			return self.end_time <  other.end_time
		return NotImplemented

	def __le__(self, other):
		if isinstance(other, HistoryEntry):
			return self.end_time <= other.end_time
		return NotImplemented

	def __gt__(self, other):
		if isinstance(other, HistoryEntry):
			return self.end_time >  other.end_time
		return NotImplemented

	def __ge__(self, other):
		if isinstance(other, HistoryEntry):
			return self.end_time >= other.end_time
		return NotImplemented

########################################################################

# Classe d’historique d’un jeu donné
class History:
	def __init__(self):
		self.history = []

	def append(self, historyEntry):
		self.history.append(historyEntry)
		self.sort()

	def sort(self):
		self.history.sort(reverse=True)

	def newer(self):
		if len(self.history) > 0:
			return self.history[0]
		return None

	def last_date(self):
		# Retourne la dateHeure de fermeture de la dernière partie jouée
		if self.newer() != None:
			return self.newer().end_time
		return None

	def cumulate_time(self):
		total_time = timedelta()
		for history_entry in self.history:
			t = datetime.strptime(history_entry.duration,"%H:%M:%S.%f")
			duration = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
			total_time+=duration
		return total_time

	def historyEntriesFromNDays(self, numberOfDays):
		today = date.today()
		durationAgo = today - timedelta(days=numberOfDays)
		durationEntries = History()
		for entry in self.history:
			if durationAgo <= datetime.strptime(entry.start_time, '%Y-%m-%dT%H:%M:%S').date() <= today:
				durationEntries.append(entry)

		return durationEntries

	def cumulatedPlayingTimeFromNDays(self, numberOfDays):
		cumulatedTime=self.historyEntriesFromNDays(numberOfDays)
		return cumulatedTime.cumulate_time()

########################################################################
# Fonctions d’éxtraction de l’historique pour un jeu donné

def is_history_date_relevant(date):
	# Filtre des dates pertinantes

	# Définir le motif de l'expression régulière pour le format AAAA-MM-JJThh:mm
	pattern = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$')
	if pattern.match(date):
		return True
	return False

def is_history_duration_relevant(date):
	# Filtre des dates pertinantes

	# Définir le motif de l'expression régulière pour le format AAAA-MM-JJThh:mm
	pattern = re.compile(r'^\d+:\d{2}:\d{2}.\d{6}$')
	if pattern.match(date):
		return True
	return False

def is_history_entry_relevant(history_entry):
	
	if "start_time" in history_entry and "end_time" in history_entry and "duration" in history_entry :
		if is_history_date_relevant(history_entry["start_time"]) and is_history_date_relevant(history_entry["end_time"]) and is_history_duration_relevant(history_entry["duration"]):
			return True
	return False

def retrive_history_of_a_game(game):
	prepared_history = History()
	with open(HISTORY_FILE.fullPath()) as f:
		data = json.load(f)

	if 'history' in data and game.code in data['history']:
		# Récupération de l’historique du jeu en cours
		game_history = data['history'][game.code]
		for history_entry in game_history:
			if is_history_entry_relevant(history_entry):
				prepared_history.append(HistoryEntry(dictionnary=history_entry))

	return prepared_history

########################################################################
# Classe des jeux
########################################################################

def formatDataListToLitteralList(list_, voidSymbol):
	try:
		n = len(list_)
	except:
		n = 0
	if n == 0:
		return voidSymbol # TODO
	elif n == 1:
		return list_[0]
	elif n == 2:
		return f"{list_[0]} et {list_[1]}"
	else:
		elements = ", ".join(list_[:-1])
		return f"{elements}, et {list_[-1]}"

# Défffinition de classe
class Game:
	def __init__(self, name=None, code=None, licence=None, url=None, year=None, genre=None, authors=None, studios=[], command=None, comments=None, platform=None):
		self.name = name
		self.code = code
		self.licence = licence
		self.url = url
		self.year = year
		self.genre = genre
		self.authors = authors
		self.studios = studios
		self.command = command
		self.comments = comments
		self.platform = platform
		self.history = self.get_history()
		self.latest_opening_date_value = self.latest_opening_date()
		self.playing_duration = self.cumulate_time()

		listOfGames[self.code]=self # Adjonction à la liste des jeux

	def ncurseLine(self):
		# Préparation de la ligne de tableau

		# Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
		ncurseLine = [
			self.platform.abbr or PLATFORM_VOID_SYMBOL.value,
			self.name or NAME_VOID_SYMBOL.value,
			self.licence.abbr or LICENCE_VOID_SYMBOL.value,
			self.genre.abbr or GENRE_VOID_SYMBOL.value,
			self.year or DATE_VOID_SYMBOL.value,
			self.human_latest_opening_duration() or LASTOPENING_VOID_SYMBOL.value,
			self.human_cumulate_time() or CUMULATEDTIME_VOID_SYMBOL.value,
			self.listOfAuthors() or AUTHOR_VOID_SYMBOL.value,
			self.listOfStudios() or STUDIO_VOID_SYMBOL.value,
			self
		]
		return ncurseLine

	def asciiRow(self):
		# Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
		asciiRow = [
			self.platform.abbr or PLATFORM_VOID_SYMBOL.value,
			self.name or NAME_VOID_SYMBOL.value,
			self.licence.abbr or LICENCE_VOID_SYMBOL.value,
			self.genre.abbr or GENRE_VOID_SYMBOL.value,
			self.year or DATE_VOID_SYMBOL.value,
			self.human_latest_opening_duration() or LASTOPENING_VOID_SYMBOL.value,
			self.human_cumulate_time() or CUMULATEDTIME_VOID_SYMBOL.value,
			self.listOfAuthors() or AUTHOR_VOID_SYMBOL.value,
			self.listOfStudios() or STUDIO_VOID_SYMBOL.value
		]
		return asciiRow

	def sheet(self):
		# Fiche rapide de description de jeu
		sheet_data=[
			["Nom", self.name],
			["code", self.code],
			["Licence", self.licence.name],
			["URL", self.url],
			["Genre", self.genre.name],
			["Auteur", self.listOfAuthors()],
			["Commande", self.command],
			["Dernière ouverture", self.latest_opening_date()],
		]

		print(tabulate(sheet_data))

	def get_history(self):
		# Retourne l’historique des dates et heures de parties jouées
		return retrive_history_of_a_game(self)

	def cumulate_time(self):
		# Temps de jeu cumulé
		return self.history.cumulate_time()

	def human_cumulate_time(self):
		# Retourne le temps total joué humainement lisible
		if self.history.cumulate_time() == timedelta(): # test si le temps cumulate_time() retourne bien un delta et non le caractère "-"
			return " "
		delta = humanize.naturaldelta(self.history.cumulate_time())
		return delta

	def latest_opening_date(self):
		# Retourne la dernière date où le jeu a ét éouvert
		return self.history.last_date()

	def latest_opening_duration(self):
		# Retourne la durée depuis laquelle le jeu a été ouvert
		if self.latest_opening_date():

			# Réception de la chaine string et transformation en datetime
			last_date= datetime.strptime(self.history.last_date(), "%Y-%m-%dT%H:%M:%S") 
			delta=datetime.now() - last_date
			return delta
		return None

	def human_latest_opening_duration(self):
		# Temps depuis la dernière ouverture humainement lisible
		if self.latest_opening_date():
			return humanize.naturaldelta(self.latest_opening_duration())
		return "-"

	def listOfAuthors(self):
		return formatDataListToLitteralList(self.authors, AUTHOR_VOID_SYMBOL.value)

	def listOfStudios(self):
		return formatDataListToLitteralList(self.studios, STUDIO_VOID_SYMBOL.value)

	def delete(self):
		deleteGameFromDatabase(self.code)

	def showPlot(self):
		pass


def create_game_objects():
	# Création de la liste des jeux

	# Intialisation
	global listOfGames
	listOfGames={}

	# Extraction des jeux
	with open(GAME_FILE.fullPath()) as f:
		listOfGamesData = json.load(f)["games"]

	## Déploiment des objet de jeux
	for aGame in listOfGamesData:
		Game(
			name=aGame.get("name"),
			code=aGame.get("code"),
			licence=get_licence_object_after_code(aGame.get("licence")),
			url=aGame.get("url"),
			year=aGame.get("year"),
			genre=get_genre_object_after_code(aGame.get("genre")),
			command=aGame.get("command"),
			authors=aGame.get("authors"),
			studios=aGame.get("studios"),
			platform=get_platform_object_after_code(aGame.get("platform")),
		)

########################################################################
# Fonction de l’autocompletion
########################################################################

def deleteBlancLines(chaine):
	# Divise la chaîne en lignes individuelles
	lignes = chaine.splitlines()
	
	# Filtre les lignes qui ne sont pas vides
	lignes_non_vides = [ligne for ligne in lignes if ligne.strip() != '']
	
	# Rejoint les lignes non vides en une seule chaîne
	chaine_sans_lignes_vides = '\n'.join(lignes_non_vides)
	
	return chaine_sans_lignes_vides

def listAllObjectsCodeOfClassCodePerLine(listOfObjectsOfClass):
	listOfCodes=""
	for anObject in listOfObjectsOfClass:
#		listOfCodes+="\n" + anObject
		listOfCodes+="\n" + f"{anObject}[{listOfObjectsOfClass[anObject].name}]"
	return deleteBlancLines(listOfCodes)

def listOfAllGamesCodePerLine():
	return listAllObjectsCodeOfClassCodePerLine(listOfGames)

def listOfAllLicencesCodePerLine():
	return listAllObjectsCodeOfClassCodePerLine(listOfLicences)

def listOfAllGenresCodePerLine():
	return listAllObjectsCodeOfClassCodePerLine(listOfGenres)

def listOfAllPlatformsCodePerLine():
	return listAllObjectsCodeOfClassCodePerLine(listOfPlatforms)

########################################################################
# Fonction de listage
########################################################################

GAME_HEADERS=["Plateforme", "Titre", "Licence", "Genre", "Date", "Dernière ouverture", "Temps cumulé", "Auteur", "Studio"]
LICENCE_HEADERS=["Titre", "URL", "Coeficient"]
PLATFORM_HEADERS=["Titre", "Acronyme"]
GENRES_HEADERS=["Titre", "Acronyme"]

def printObjectsFromTypeTable(object_headers, listOfObjectsFromType):
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

def printGamesTable():
	printObjectsFromTypeTable(GAME_HEADERS, listOfGames)

def printLicencesTable():
	printObjectsFromTypeTable(LICENCE_HEADERS, listOfLicences)

def printPlatformsTable():
	printObjectsFromTypeTable(PLATFORM_HEADERS, listOfPlatforms)

def printGenresTable():
	printObjectsFromTypeTable(GENRES_HEADERS, listOfGenres)

########################################################################
# Éidition des bases de données (nouveau)
########################################################################

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
	elif isObjectExistInsideListOfObjects(theObject, listOfObjects):
		print(f"Le code « {theObject['code']} » éxiste déjà.")
	elif code == None:
		print(f"Veuillez déffinir un code d’entification pour le {object_name}.")

# Fonctions dérrivées #################################################################

def addGameToDataBase(theObject):
	addObjectToDataBase(theObject=theObject, listOfObjects=listOfGames, object_file=GAME_FILE.fullPath(), objectGroupName="games", object_name="jeu")

def addGenreToDataBase(theObject):
	addObjectToDataBase(theObject=theObject, listOfObjects=listOfGenres, object_file=GENRE_FILE.fullPath(), objectGroupName="genres", object_name="genre")

def addLicenceToDataBase(theObject):
	addObjectToDataBase(theObject=theObject, listOfObjects=listOfLicences, object_file=LICENCE_FILE.fullPath(), objectGroupName="licences", object_name="licence")

def addPlatformToDataBase(theObject):
	addObjectToDataBase(theObject=theObject, listOfObjects=listOfPlatforms, object_file=PLATFORM_FILE.fullPath(), objectGroupName="platforms", object_name="plateforme")

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
	deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=GAME_FILE.fullPath(), objectGroupName="games")

def deleteLicenceFromDatabase(givenObject):
	deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=LICENCE_FILE.fullPath(), objectGroupName="licences")

def deleteGenreFromDatabase(givenObject):
	deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=GENRE_FILE.fullPath(), objectGroupName="genres")

def deletePlatformFromDatabase(givenObject):
	deleteObjectFromDatabase(givenObject=givenObject, listOfObjectsFile=PLATFORM_FILE.fullPath(), objectGroupName="platforms")


########################################################################
# Classe des colones de la liste visuelle
########################################################################

class VisuaColumn:
	def __init__(self, label=None, property_=None):
		self.label=label
		self.property=property_

		listOfPossibleColumns.append(self)

########################################################################
# Fonctions d’extraction des données
########################################################################

def retrive_datas():
	# Déploiement des objets de plateforme
	create_platform_objects()
	# Déploiement des objets de genres de jeux
	create_game_genre_objects()
	# Déploiement des objets de licence
	create_licence_objects()
	# Déploiement des objets de jeux
	create_game_objects()

########################################################################
# Classe de la liste visuelle
########################################################################
class ListMove:
	def __init__(self, label=None, code=None):
		self.label=label
		self.code=code
		globals()[self.code] = self # Le seul objet de cette classe est TheVisualListOfGames


ListMove(label="Go up", code="goUp")
ListMove(label="Go down", code="goDown")
########################################################################
# Classe de la liste visuelle
########################################################################

class Sort:
	def __init__(self, label=None, code=None, command=None):
		self.label = label
		self.code = code
		self.command = command

		listOflistSorting.append(self) # Adjonction à la liste des jeux


SORTING_ORDER=[True, False]


def getNextSortingOrder(currentSortingOrder):
	global SORTING_ORDER
	currentIndex=SORTING_ORDER.index(currentSortingOrder)
	tmpNextIndex=currentIndex+1
	realNextIndex=tmpNextIndex % len(SORTING_ORDER)
	nextSortingOrder=SORTING_ORDER[realNextIndex]
	
	return nextSortingOrder

HIDED_DATA_COLUMN=9
class VisualListOfGames:
	def __init__(self):
		self.columns=None
		self.titles = [" ", "Titre", "Licence", "Genre", "Date", "Dernière ouverture", "Temps cumulé", "Auteur", "Studio"]
		self.list=None
		self.sortByProperty=None
		self.sortingState=SORTING_ORDER[1]
		self.selected_row = 0
		self.firstRowOnVisibleList = 0
		self.lastMove=None

		self.refresh()
		global_variables.THE_VISUAL_LIST_OF_GAMES = self # Le seul objet de cette classe est TheVisualListOfGames

	def isTheListEmpty(self):
		if self.list in [None, []]:
			return True
		return False

	def getNthNLines(self, lineRank, numberOfLines):
		# Retourne une portion de la liste commençan par lineRank et contenant numberOfLines lignes
		subList = self.list[lineRank:lineRank+numberOfLines]
		return subList

	# TODO intégéré screenHeight-3 dans la déffiniton de classe
	def visualHighlightedLineNumber(self, screenHeight):
		visualHighlightedLineNumber=self.selected_row-self.firstRowOnVisibleList
		return visualHighlightedLineNumber

	def getCurrentVisibleList(self, screenHeight):
		if self.lastMove == goDown:
			if self.selected_row > self.firstRowOnVisibleList + screenHeight-4-3 :
				self.firstRowOnVisibleList+=1

		if self.lastMove == goUp:
			if self.selected_row == self.firstRowOnVisibleList +1 and self.selected_row > 1 :
				self.firstRowOnVisibleList-=1


		visibleList=self.getNthNLines(self.firstRowOnVisibleList, screenHeight-4) # TODO remplacer le 2 par une variable


		return visibleList

	def goDown(self):
		self.selected_row = min(len(self.list) - 1, self.selected_row + 1)
		self.lastMove=goDown

	def goUp(self):
		self.selected_row = max(0, self.selected_row - 1)
		self.lastMove=goUp

	def openCurrent(self):
		# Exécuter la commande de lancement du jeu associée à la ligne sélectionnée
		global HIDED_DATA_COLUMN
		setBottomBarContent(f"Ouverture de « {self.list[self.selected_row][HIDED_DATA_COLUMN].name} ».")
		game = self.list[self.selected_row][HIDED_DATA_COLUMN]
		threading.Thread(target=run_command_and_write_on_history, args=(game,)).start()

	def currentGame(self):
		# TODO factorisé un peu partout.
		game = self.list[self.selected_row][HIDED_DATA_COLUMN]
		return game

	def deleteCurrent(self):
		# Exécuter la commande de lancement du jeu associée à la ligne sélectionnée
		global HIDED_DATA_COLUMN
		setBottomBarContent(f"Supression du jeu « {self.list[self.selected_row][HIDED_DATA_COLUMN].name} ».")
		game = self.list[self.selected_row][HIDED_DATA_COLUMN]
		if self.selected_row == len(self.list)-1:
			
			self.goUp()
			game = self.list[self.selected_row+1][HIDED_DATA_COLUMN]
		game.delete()
		self.refresh()

	def copyLinkToClipBoard(self):
		url = self.list[self.selected_row][self.hiden_data_column_number()].url
		if url != None:
			setBottomBarContent(f"Copie de « {self.list[self.selected_row][HIDED_DATA_COLUMN].url} » dans le presse-papier.")
			pyperclip.copy(url)
		else:
			setBottomBarContent(f"Aucun lien associé à « {self.list[self.selected_row][HIDED_DATA_COLUMN].name} », rien à copier.")

	def openLink(self):
		global HIDED_DATA_COLUMN
		url = self.list[self.selected_row][HIDED_DATA_COLUMN].url  # Supposons que l'URL est stockée à l'indice 5
		if url != None:
			setBottomBarContent(f"Ouverture de « {self.list[self.selected_row][HIDED_DATA_COLUMN].url} »")
			self.refresh()
			threading.Thread(target=webbrowser.open, args=(url,)).start()
		else:
			setBottomBarContent(f"Pas de lien associé à « {self.list[self.selected_row][HIDED_DATA_COLUMN].name} »")

	def hiden_data_column_number(self):
		return len(self.list[0])-1

	def refresh(self):
		retrive_datas()
		global listOfGames

		self.list=[]
		for aGame in listOfGames:
			self.list.append(listOfGames[aGame].ncurseLine())
		self.softSortBy(self.sortByProperty)

	def shiftSortingState(self, property_):
		if ( property_ == self.sortByProperty) :
			self.sortingState=getNextSortingOrder(self.sortingState)

	def isAtributeShouldBeSorted(self, attribute):
		if attribute in ["-", None]:
			return False
		if hasattr(attribute, "includeInSorting"):
			if attribute.includeInSorting == False:
				return False

		return True

	def putVoidAtEnd(self, oldList, property_):
		beginingOfNewList=[]
		endOfNewList=[]
		for item in oldList:
			if self.isAtributeShouldBeSorted(getattr(item[self.hiden_data_column_number()], property_)) :
				beginingOfNewList.append(item)
			else:
				endOfNewList.append(item)
		newList= beginingOfNewList + endOfNewList
		return newList

	def softSortBy(self, property_):
		if property_:
			self.sortByProperty=property_
			tmpList0=self.list
			tmpList1 = sorted(tmpList0, 
							 reverse=self.sortingState, 
							 key=lambda x: (getattr(x[self.hiden_data_column_number()], property_) is None, 
											getattr(x[self.hiden_data_column_number()], property_)))

			tmpList2=self.putVoidAtEnd(tmpList1, property_)
			# Déplacer les entrées avec property_ == "-" à la fin
			self.list=tmpList2

	def sortBy(self, property_):
		self.shiftSortingState(property_)
		self.softSortBy(property_)
		# Cas particuliers 
		#  "latest_opening_date_value"

	def columnsWidth(self):
		itemsMergedWithTitle = self.items[:]
		itemsMergedWithTitle.append(self.titles)
		col_widths = [max(len(str(column)) for column in col) for col in zip(*itemsMergedWithTitle)]

		return col_widths

	def allHistoryEntries(self):
		global HIDED_DATA_COLUMN

		allHistoryEntriesList=History()
		for aGameRow in self.list:
			allHistoryEntriesList.history.extend(aGameRow[HIDED_DATA_COLUMN].history.history)

		return allHistoryEntriesList

	def filterByPattern(self, pattern):
		pass


########################################################################
# Fonctions foncitonnelles de l’interface interactive
########################################################################

# Fonction pour trier les jeux par titre
def sort_by_title(items):
	return sorted(items, key=lambda x: x[0].lower())

# Fonction pour trier les jeux par licence
def sort_by_license(items):
	items_sorted_by_licence_name=sorted(items, key=lambda x: x[7].licence.name)
	return sorted(items_sorted_by_licence_name, key=lambda x: x[7].licence)

# Fonction pour trier les jeux par genre
def sort_by_genre(items):
	return sorted(items, key=lambda x: x[2].lower())

# Fonction pour trier les jeux par date
def sort_by_date(items):
	return sorted(items, key=lambda x: str(x[3]))

def history_data_with_current_game(game):
	with open(HISTORY_FILE.fullPath()) as f:
		data = json.load(f)

	if 'history' not in data:
		data['history'] = {}

	if game.code not in data['history']:
		data['history'][game.code] = []

	return data

def write_opening_date_on_history(game=None, start_time=None, end_time=None, duration=None):
	try:
		# Charger le JSON existant depuis un fichier
		with open(HISTORY_FILE.fullPath()) as f:
			data = json.load(f)

		data = history_data_with_current_game(game)
		history_entry=HistoryEntry(start_time=start_time, end_time=end_time, duration=duration)
		data['history'][game.code].append(history_entry.make_data())

		# Enregistrer la structure de données modifiée en tant que JSON
		with open(HISTORY_FILE.fullPath(), 'w') as f:
			json.dump(data, f, indent=4)
	except:
		pass

def run_command_and_write_on_history(game):
	# Enregistrement de l’heure de début
	start_time = datetime.now()

	# Lancement du procéssus
	command_process = subprocess.Popen(game.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	# Mise en atente pour la fin du processus
	output, error = command_process.communicate()

	# Récupération de l’heure de fin
	end_time = datetime.now()

	# Date
	duration = end_time - start_time

	# Inscription de l’évenement dans l’historique
	write_opening_date_on_history(game, start_time=start_time, end_time=end_time, duration=duration)

########################################################################
# Fonctions ésthétiques de l’interface interactive
########################################################################

def getColWidths():
	global titles
	global items

	itemsMergedWithTitle = items[:]
	itemsMergedWithTitle.append(titles)
	col_widths = [max(len(str(column)) for column in col) for col in zip(*itemsMergedWithTitle)]

	return col_widths

########################################################################
# Autres écrans
########################################################################

def centeredMessage(stdscr, text):
	# Permettre à ncurses d'utiliser les caractères Unicode correctement
	locale.setlocale(locale.LC_ALL, '')
	# Initialiser ncurses
	stdscr.clear()
	curses.curs_set(0)  # Masquer le curseur

	# Récupérer la taille de l'écran
	max_y, max_x = stdscr.getmaxyx()

	# Diviser le texte en lignes
	lines = text.splitlines()
	num_lines = len(lines)
	max_len = max(len(line) for line in lines)

	# Calculer les positions pour centrer le texte
	start_y = max_y // 2 - num_lines // 2
	start_x = max_x // 2 - max_len // 2

	# Afficher chaque ligne centrée
	for i, line in enumerate(lines):
		stdscr.addstr(start_y + i, start_x, line)

	stdscr.refresh()

def drawAboutScreen():
	while True:
		setBottomBarContent(f"Retour:q  Faire un don:x")
		centeredMessage(STDSCR,APP_SPLASH)
		drawBothBars(STDSCR)
		# Lecture de la touche pressée
		key = transformKeyToCharacter(STDSCR.get_wch())
		if key == "x":
			bindMakeDonationFunction()
		else:
			setBottomBarContent("")
			break

########################################################################
# Écran d’aide

def showHelpScreen():
	pass

########################################################################
# Interface
########################################################################

# Titres des colonnes
titles = [" ", "Titre", "Licence", "Genre", "Date", "Dernière ouverture", "Temps cumulé", "Auteur", "Studio"]

SORTING_COLUMN=0

def makeItemsList():
	global items
	items=[]
	for aGame in listOfGames:
		items.append(listOfGames[aGame].ncurseLine())
	return items

SPACE_COLUMN_SEPARATION_NUMBER=2

BOTTOM_BAR_TEXT=APP_MOTO
def setBottomBarContent(newBottomBarText):
	global BOTTOM_BAR_TEXT
	BOTTOM_BAR_TEXT = newBottomBarText
	STDSCR.refresh()

def setBottomBarColor(color):
	pass

def bottomBarCoordinate(stdscr):
	return stdscr.getmaxyx()

# Barre inférieure
def draw_bottom_bar(stdscr):
	# Récupère les dimensions de l'écran
	global BOTTOM_BAR_TEXT
	h, w = bottomBarCoordinate(stdscr)

	# Dessine la barre au bas de l'écran
	bar_text = f" {BOTTOM_BAR_TEXT} "
	stdscr.chgat(h-MAIN_SCREEN_MARGIN_BOTTOM, 0, w, curses.A_REVERSE)
	stdscr.addstr(h-MAIN_SCREEN_MARGIN_BOTTOM, 0, bar_text, curses.A_REVERSE)


def prepareTextForRightIndicator(visualListOfGames):
	global CUMULATED_TIME_PLAYED_PER_DAY
	global CUMULATED_TIME_PLAYED_PER_WEEK
	global CUMULATED_TIME_PLAYED_PER_MONTH
	global CUMULATED_TIME_PLAYED_PER_YEAR
	global CUMULATED_TIME_PLAYED_SEPARATOR

	rightIndicatorText=  CUMULATED_TIME_PLAYED_PER_DAY + ": "
	rightIndicatorText+= humanize.naturaldelta(visualListOfGames.allHistoryEntries().cumulatedPlayingTimeFromNDays(1))

	rightIndicatorText+= "" + str(CUMULATED_TIME_PLAYED_SEPARATOR) + ""

	rightIndicatorText+= CUMULATED_TIME_PLAYED_PER_WEEK + ": "
	rightIndicatorText+= humanize.naturaldelta(visualListOfGames.allHistoryEntries().cumulatedPlayingTimeFromNDays(7))

	rightIndicatorText+= "" + str(CUMULATED_TIME_PLAYED_SEPARATOR) + ""

	rightIndicatorText+= CUMULATED_TIME_PLAYED_PER_MONTH + ": "
	rightIndicatorText+= humanize.naturaldelta(visualListOfGames.allHistoryEntries().cumulatedPlayingTimeFromNDays(30))

	rightIndicatorText+= "" + str(CUMULATED_TIME_PLAYED_SEPARATOR) + ""

	rightIndicatorText+= CUMULATED_TIME_PLAYED_PER_YEAR + ": "
	rightIndicatorText+= humanize.naturaldelta(visualListOfGames.allHistoryEntries().cumulatedPlayingTimeFromNDays(365))

	return rightIndicatorText

MAIN_SCREEN_MARGIN_BOTTOM=2
STDSCR=""
# Barre inférieure
def draw_bottom_right(stdscr, visualListOfGames):
	global STDSCR
	# Récupère les dimensions de l'écran

	rightIndicatorText=prepareTextForRightIndicator(visualListOfGames)
	h, w = stdscr.getmaxyx()
	STDSCR=stdscr

	# Définir le texte de la barre inférieure

	# Calculer la position de départ pour l'alignement à droite
	x_start = w - len(rightIndicatorText)

	# Effacer l'arrière-plan de la ligne
	stdscr.move(h-MAIN_SCREEN_MARGIN_BOTTOM, 0)

	# Dessiner le texte avec la couleur d'origine, sans arrière-plan
	stdscr.addstr(h-MAIN_SCREEN_MARGIN_BOTTOM, x_start, rightIndicatorText, curses.A_REVERSE)

	# Rafraîchir l'écran
	stdscr.refresh()

def drawBothBars(stdscr):
	# Dessiner la barre supérieure avec le nom de l'application
	stdscr.attron(curses.color_pair(1))
	stdscr.addstr(0, 0, APP_NAME.ljust(curses.COLS), curses.color_pair(2))
	stdscr.attroff(curses.color_pair(1))

	# Dessiner la barre Inférieure
	draw_bottom_bar(stdscr)
	draw_bottom_right(stdscr, global_variables.THE_VISUAL_LIST_OF_GAMES)

def display_centered_text(stdscr, text):
	# Obtenir les dimensions de l'écran
	h, w = stdscr.getmaxyx()

	# Diviser le texte en lignes si ce n'est pas déjà fait
	lines = text.splitlines()

	# Calculer la hauteur totale requise pour afficher toutes les lignes
	total_lines = len(lines)
	text_height = total_lines

	# Calculer la position verticale (y) pour commencer à afficher les lignes
	start_y = (h - text_height) // 2

	# Afficher chaque ligne au milieu de l'écran
	for i, line in enumerate(lines):
		# Calculer la position horizontale (x) pour centrer la ligne
		x = (w - len(line)) // 2
		stdscr.addstr(start_y + i, x, line)

def drawListOfGames(stdscr):
	#setBottomBarContent("Don:x  Quitter:q  Tri par nom:b  Par date:o  Par licence:é  Par genre:p Par date:o  Par durée de jeu:!") # TODO rendre automatique
	makeItemsList()
	global_variables.THE_VISUAL_LIST_OF_GAMES.refresh()
	screenHeight, screenWidth = stdscr.getmaxyx()
	if global_variables.THE_VISUAL_LIST_OF_GAMES.isTheListEmpty():
		noGameFoundText="""Aucun jeu trouvé.
 Saissez :h ou consultez man triphum
		"""
		display_centered_text(stdscr,noGameFoundText)
	else:
		# Calcul de la largeur des colones
		col_widths = getColWidths()

		for row_number, title in enumerate(titles):
			stdscr.addstr(1, sum(col_widths[:row_number]) + row_number * 2, str(title), curses.color_pair(2) | curses.A_BOLD)

		# Affichage des données de la liste
		for row_number, item in enumerate(global_variables.THE_VISUAL_LIST_OF_GAMES.getCurrentVisibleList(screenHeight)):
			for column_number, column in enumerate(item):
				if column_number < HIDED_DATA_COLUMN:  # Masquer la colonne "commande"
					stdscr.addstr(row_number + 2, sum(col_widths[:column_number]) + column_number * 2, str(column))

		stdscr.addstr(global_variables.THE_VISUAL_LIST_OF_GAMES.visualHighlightedLineNumber(screenHeight) + 2, 0, " " * curses.COLS, curses.color_pair(2))  # Effacer toute la ligne avec la couleur de fond

		# Affichage des données de la liste avec surbrillance pour la ligne sélectionnée
		# Cas particulier de la ligne ayant le focus
		for column_number, column in enumerate(global_variables.THE_VISUAL_LIST_OF_GAMES.list[global_variables.THE_VISUAL_LIST_OF_GAMES.selected_row][:HIDED_DATA_COLUMN]):  # Afficher seulement les 4 premières colonnes
			stdscr.addstr(global_variables.THE_VISUAL_LIST_OF_GAMES.visualHighlightedLineNumber(screenHeight) + 2, sum(col_widths[:column_number]) + column_number * 2, str(column), curses.color_pair(2) | curses.A_BOLD)

def questionMode(question):
	setBottomBarContent(question + " (Y/n)")
	draw_bottom_bar(STDSCR)
	STDSCR.refresh()
	while True:
		key = transformKeyToCharacter(STDSCR.get_wch())
		if key in ['y', 'yes']:
			return True
		elif key in ['n', 'no']:
			return False
		else:
			setBottomBarContent("Veuillez répondre par 'Y' ou 'n'.")
			draw_bottom_bar(STDSCR)
			STDSCR.refresh()

########################################################################
# Internal shell
########################################################################

addNewGamepatern='(n|new|newgame)\s+.*'

def internalShelldrawAboutScreen(shellInput):
	drawAboutScreen()

def internalShellbindMakeDonationFunction(shellInput):
	bindMakeDonationFunction()

def internalShellLayoutFunction(shellInput):
	# TODO utiliser la fonction factorisée
	matchedInput=re.match("(l|layout)\s+(?P<relevant>[a-z]+)", shellInput)
	askedLayout=matchedInput.group("relevant")
	if askedLayout in listOfLayouts:
		listOfLayouts[askedLayout].apply()
		setBottomBarContent(f"{listOfLayouts[askedLayout].fancyName}")
	else:
		setBottomBarContent(f"Disposition « {askedLayout} » inconue")

InternalShellCommand(code="addNewGame", patern=addNewGamepatern, description="Ajouter un nouveau jeu à la base de donnée", synopsis=":n :new :newgame name=<Game name> code=<code> [genre=<genre>] [licence=getPaternToMatchAllLicencesCodes()]", instructions=addNewGameAfterInterativeDescriptor)
InternalShellCommand(code="about", patern='(a|about)', description="À propos", synopsis=":a :about", instructions=internalShelldrawAboutScreen)

InternalShellCommand(code="donate", patern='(d|don|donate)', description="Faire un don", synopsis=":d :don :donate", instructions=internalShellbindMakeDonationFunction)
InternalShellCommand(code="layout", patern=f'(l|layout)\s+(?P<layout>{getPaternToMatchAllLayoutCodes()})', description="Changer de disposition de clavier", synopsis=":l :layout <layout>", instructions=internalShellLayoutFunction)
InternalShellCommand(code="comment", patern='(c|comment)', description="Ajouter un commentaire", synopsis=":c :comment", activated=False)
InternalShellCommand(code="viewComment", patern='(v|view)', description="Voir les commentaires", synopsis=":v :vew", activated=False)

########################################################################
# Éexecution des fichiers de configuration
########################################################################

# /!\ Il est imporatnt que prepareConfigFiles() soit éxecutée après les déclarations de bindings car elle en a besoin pour générer les bindings par défaut.

prepareConfigFiles()

# /!\ Il est imporatnt que VisualListOfGames() vienne après prepareConfigFiles() car ce dernier décalre des variables globales dont VisualListOfGames() a besoin


GAME_FILE=config_file.GAME_FILE
GENRE_FILE=config_file.GENRE_FILE
LICENCE_FILE=config_file.LICENCE_FILE
PLATFORM_FILE=config_file.PLATFORM_FILE
HISTORY_FILE=config_file.HISTORY_FILE
CONFIG_FILE=config_file.CONFIG_FILE
writeInTmp(global_variables.THE_VISUAL_LIST_OF_GAMES)
VisualListOfGames()

########################################################################
# Fonctions main
########################################################################

STDSCR=None
def main(stdscr):
	global STDSCR

	STDSCR=stdscr
	# Initialisation de ncurses
	curses.curs_set(0)  # Masquer le curseur
	screenHeight, screenWidth = stdscr.getmaxyx()

	# Initialiser les couleurs
	curses.start_color()
	curses.use_default_colors()

	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Noir sur fond blanc
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Blanc sur fond noir

	# Définir la couleur du texte comme étant la même que la couleur du fond
	curses.init_pair(1, -1, -1)  # Utilise la couleur par défaut du terminal

	# Nom de l'application


#	global global_variables.THE_VISUAL_LIST_OF_GAMES
	global BOTTOM_BAR_TEXT
	global bindSortByName
	# Boucle principale
	while True:

		# Mise à jour de l’historique
		#retrive_datas()
		# Mise à jour de la liste des jeux

		curses.noecho()  # Désactiver l'écho des touches
		stdscr.clear()

		drawListOfGames(stdscr)

		drawBothBars(stdscr)

		# Rafraîchir l'écran
		stdscr.refresh()

		# Lecture de la touche pressée
		key = transformKeyToCharacter(stdscr.get_wch())
#		setBottomBarContent(f"Touche préssée {key}")

		if (key) == transformKeyToCharacter('q'):  # Quitter si la touche 'q' est pressée # TODO factoriser
			break
		elif any(key == aBinding.key for aBinding in listOfBindings):
			# Teste si la touche préssé correspond à l’attribut key d’un des élements de listOfBindings
			setBottomBarContent("")

			# ↓ Trouver au sein de `listOfBindings` l’élément ayant dans son paramettre « key » la valeure contenue dans `value`, et en éxecute aussitôt les instructions.
			getElementHavingParameterWithValue(givenList=listOfBindings, parameter="key", value=key).executeInstructions()

########################################################################
# Que faire
########################################################################

if args.config_file != None:
	CONFIG_FILE.setNew(args.config_file)

applyFileConfigurationsBindings()
applyFileConfigurationsGraphicalSymbols()

# Fichiers de configuration
if args.games_file:
	GAME_FILE.setNew(args.games_file)
if args.genres_file:
	GENRE_FILE.setNew(args.genres_file)
if args.licences_file:
	LICENCE_FILE.setNew(args.licences_file)
if args.platforms_file:
	PLATFORM_FILE.setNew(args.platforms_file)

if  args.verbose == True:
	print(f"Fichier de configuration principal : {CONFIG_FILE}")
	print(f"Fichier des jeux : {GAME_FILE}")
	print(f"Fichier des genres de jeux : {GENRE_FILE}")
	print(f"Fichier des licences : {LICENCE_FILE}")
	print(f"Fichier des plateformes : {PLATFORM_FILE}")

# Configuration


# Section des adjonctions
if args.newGameDescriptor :
	addNewGameAfterInterativeDescriptor(args.newGameDescriptor, True)
elif args.newGenreDescriptor :
	addNewGenreAfterInterativeDescriptor(args.newGenreDescriptor, True)
elif args.newLicenceDescriptor :
	addNewLicenceAfterInterativeDescriptor(args.newLicenceDescriptor, True)
elif args.newPlatformDescriptor :
	addNewPlatformAfterInterativeDescriptor(args.newPlatformDescriptor, True)

# Parametres de l’autocompletion
elif args.autocompletionGame:
	print(listOfAllGamesCodePerLine())
elif args.autocompletionGenre :
	print(listOfAllGenresCodePerLine())
elif args.autocompletionLicence :
	print(listOfAllLicencesCodePerLine())
elif args.autocompletionPlatform :
	print(listOfAllPlatformsCodePerLine())

# Affichages des listes cli
elif args.list_games:
	printGamesTable()
elif args.list_genres :
	printGenresTable()
elif args.list_licences :
	printLicencesTable()
elif args.list_platforms :
	printPlatformsTable()

# Section des suppresions
elif args.delGame:
	deleteGameFromDatabase(iargs.delGame)
elif args.delLicence:
	deleteLicenceFromDatabase(iargs.delLicence)
elif args.delGenre:
	deleteGenreFromDatabase(iargs.delGenre)
elif args.delPlatform:
	deletePlatfromFromDatabase(iargs.delPlatform)

# Execution d’un jeu
elif args.run not in [None, False]:
	theGame=listOfGames[args.run]
	if theGame != None:
		print(f"Ouverture de « {theGame.name} »")
		theGame.sheet()
		threading.Thread(target=run_command_and_write_on_history, args=(theGame,)).start()
	else:
		print(f"Aucun jeu ne correspond à l’identifiant « {args.run} »")

# Autres fonctions autonomes
elif  args.about == True:
	print(APP_FANCY_NAME + " " + APP_VERSION + " " + APP_DESCRIPTION)

elif args.donate == True:
	print(f"Pour soutenir {APP_FANCY_NAME} et faire en sorte qu’il continue et s’améliore, merci de faire un don à <{APP_AUTHOR_DONATION_LINK}>. (^.^)")
	webbrowser.open(APP_AUTHOR_DONATION_LINK)

elif args.tui == True:
	if args.layout:
		layout=listOfLayouts[args.layout]
		print(layout.code)
		print(layout.bindGoDown)
		layout.apply()
	printSplash()
	curses.wrapper(main)
