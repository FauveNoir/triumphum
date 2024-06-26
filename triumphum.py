#!/usr/bin/python3

import curses
import subprocess
import threading
import json
import webbrowser
import pyperclip
import appdirs
import re
from datetime import date, datetime, timedelta
from tabulate import tabulate
import humanize
import pendulum
import locale
import time
import argparse
import configparser
from Xlib import XK
from Xlib.display import Display


########################################################################
# fonctions de test
########################################################################

def tprint(content):
	print(content)

def writeInTmp(text):
	with open('/tmp/output', 'a') as f:
		f.write(f"[{datetime.now()}] {text} \n")

########################################################################
# Variables globales
########################################################################

APP_CODE_NAME="triumphum"
APP_FANCY_NAME="Triumphum"
APP_DESCRIPTION="Gestionnaire de ludothèque en Python et NCurses pour GNU/Linux"
APP_VERSION="0.1"
APP_AUTHOR="Fauve"
APP_AUTHOR_MAIL="fauve.ordinator@taniere.info"
APP_AUTHOR_DONATION_LINK="https://paypal.me/ihidev"
APP_URL=""

# Définir la locale dans Pendulum
pendulum.set_locale('fr')
_t = humanize.i18n.activate("fr_FR")


########################################################################
# Répertoire de configuration
########################################################################

# Obtenez le répertoire de configuration de l'application
CONFIG_DIR = appdirs.user_config_dir(APP_CODE_NAME)

CONFIG_FILE= appdirs.user_config_dir("triumphumrc")

BASE_NAME_GAME_FILE="games.json"
BASE_NAME_TYPE_FILE="listOfGameTypes.json"
BASE_NAME_LICENCE_FILE="listOfLicences.json"
BASE_NAME_PLATFORM_FILE="listOfPlatforms.json"

GAME_FILE=CONFIG_DIR + "/" + BASE_NAME_GAME_FILE
TYPE_FILE=CONFIG_DIR + "/" + BASE_NAME_TYPE_FILE
LICENCE_FILE=CONFIG_DIR + "/" + BASE_NAME_LICENCE_FILE
PLATFORM_FILE=CONFIG_DIR + "/" + BASE_NAME_PLATFORM_FILE


########################################################################
# Options de la ligne de commande
########################################################################

parser = argparse.ArgumentParser(description=APP_FANCY_NAME + " " + APP_VERSION + " " + APP_DESCRIPTION)

interfaceBehaviour = parser.add_argument_group('Interface behaviour')

interfaceBehaviour.add_argument("--tui", action="store_true", default = True, help = "Run the game selection interface (default).")
interfaceBehaviour.add_argument("-r", "--run", metavar="game", help = "Run a given game and track playing time.")

generalArgument = parser.add_argument_group('General arguments')
generalArgument.add_argument("-a", "--about", action="store_true", help = "Show about message.")
generalArgument.add_argument("-d", "--donate", action="store_true", help = "Open link to give a tip.")
generalArgument.add_argument("--list-games", action="store_true", help = "Afficher la liste des jeux.")

configurationFile = parser.add_argument_group('Configuration file')
configurationFile.add_argument("-c", "--config-file", help = "Select different config file from default one.")
configurationFile.add_argument("-g", "--games", metavar="file", help = "Select different game file from default one.")
configurationFile.add_argument("-p", "--platforms", metavar="file", help = "Select different platform file from default one.")
configurationFile.add_argument("-l", "--licences", metavar="file", help = "Select different licence file from default one.")
configurationFile.add_argument("-t", "--game-types", metavar="file", help = "Select different game type file from default one.")

addingData = parser.add_argument_group('Adding data')
addingData.add_argument("--add-game", metavar="game", help = "Ajouter un nouveau jeu.")
addingData.add_argument("--add-licence", metavar="licence", help = "Ajouter une nouvelle licence.")
addingData.add_argument("--add-type", metavar="type", help = "Ajouter un nouveau type de jeu.")
addingData.add_argument("--add-platform", metavar="platform", help = "Ajouter une nouvelle plateforme.")

layoutArguments = parser.add_argument_group('Layout and keybinding')

########################################################################
# Classe des symbols graphiques
########################################################################

listOfGraphicalSymbols=[]
class GraphicalSymbol:
	def __init__(self, localName=None, fileConfigName=None, description=None, value=None):
		self.localName=localName
		if fileConfigName == None:
			self.fileConfigName=self.localName.lower()
		else:
			self.fileConfigName=fileConfigName
		self.description=description
		self.value=value

		listOfGraphicalSymbols.append(self)
		globals()[localName] = self # Déclaration de la variable globale pérmétant d’atteindre directement le type voulu

	def __str__(self):
		return self.value

	def __add__(self, other):
		if isinstance(other, str):
			return str(self) + other
		else:
			return NotImplemented


GraphicalSymbol(localName="GENERAL_VOID_SYMBOL", value="-")

GraphicalSymbol(localName="NAME_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL)
GraphicalSymbol(localName="TITLE_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL)
GraphicalSymbol(localName="LICENCE_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL)
GraphicalSymbol(localName="TYPE_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL)
GraphicalSymbol(localName="DATE_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL)
GraphicalSymbol(localName="LASTOPENING_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL)
GraphicalSymbol(localName="CUMULATEDTIME_VOID_SYMBOL", value="0")
GraphicalSymbol(localName="AUTHOR_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL)
GraphicalSymbol(localName="STUDIO_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL)
GraphicalSymbol(localName="PLATFORM_VOID_SYMBOL", value=" ")

GraphicalSymbol(localName="CUMULATED_TIME_PLAYED_PER_DAY", value="D")
GraphicalSymbol(localName="CUMULATED_TIME_PLAYED_PER_WEEK", value="W")
GraphicalSymbol(localName="CUMULATED_TIME_PLAYED_PER_MONTH", value="M")
GraphicalSymbol(localName="CUMULATED_TIME_PLAYED_PER_YEAR", value="Y")
GraphicalSymbol(localName="CUMULATED_TIME_PLAYED_SEPARATOR", value="│")

########################################################################
# Classe des racoucris dactyliques
########################################################################

def getKeycode(key_name):
	display = Display()
	keysym = XK.string_to_keysym(key_name)
	keycode = display.keysym_to_keycode(keysym)
	display.close()
	return keycode

########################################################################

def getListOfKeyBindingsCodes():
	global listOfBindings
	listOfKeyBindingsStrokes=[]
	for aBinding in listOfBindings:
		listOfKeyBindingsStrokes.append((aBinding.key))
	return listOfKeyBindingsStrokes

def returnBindingAfterKeyStroke(key):
	for aBinding in listOfBindings:
		if key == aBinding.key:
			return aBinding
	return None

########################################################################

def getListOfConfigKeyCodes():
	global listOfBindings
	listOfConfigKeyCodes=[]
	for aBinding in listOfBindings:
		listOfConfigKeyCodes.append(aBinding.configFileName)
	return listOfConfigKeyCodes

def returnBindingAfterConfigKeyCode(configKeyCode):
	for aBinding in listOfBindings:
		if configKeyCode == aBinding.configFileName:
			return aBinding
	return None

########################################################################

def transform_key_to_character(key_name):
	key_mapping = {
		"Enter": "\n",
		"Return": "\r",
		"Space": " ",
	}

	# Return the mapped character if it exists in the dictionary,
	# otherwise return the original key_name (which might be a letter or unknown key)
	return key_mapping.get(key_name, key_name)


########################################################################

listOfBindings=[]
class Binding:
	def __init__(self, key=None, code=None, description=None, configFileName=None, instructions=None):
		self.key = None
		self.setKey(key)
		self.description = description
		self.code = code
		if configFileName == None:
			self.configFileName = self.code
		else:
			self.configFileName = configFileName
		globals()[code] = self # Déclaration de la variable globale pérmétant d’atteindre directement le type voulu
		if instructions:
			setattr(self, 'executeInstructions', instructions)

		listOfBindings.append(self) # Adjonction à la liste des types de jeux
	def setKey(self, key):
		self.key = transform_key_to_character(key)

def bindGoDownFunction():
	THE_VISUAL_LIST_OF_GAMES.goDown()
def bindGoUpFunction():
	THE_VISUAL_LIST_OF_GAMES.goUp()

def bindSortByNameFunction():
	global THE_VISUAL_LIST_OF_GAMES
	THE_VISUAL_LIST_OF_GAMES.sortBy("name")
	setBottomBarContent(f"Tri par ordre alphabétique.")

def bindSortByLicenceFunction():
	global THE_VISUAL_LIST_OF_GAMES
	THE_VISUAL_LIST_OF_GAMES.sortBy("licence")
	setBottomBarContent(f"Tri par permissivité des licences.")

def bindSortByTypeFunction():
	global THE_VISUAL_LIST_OF_GAMES
	THE_VISUAL_LIST_OF_GAMES.sortBy("type_")
	setBottomBarContent(f"Tri par type de jeu.")

def bindSortByDateFunction():
	global THE_VISUAL_LIST_OF_GAMES
	THE_VISUAL_LIST_OF_GAMES.sortBy("year")
	setBottomBarContent(f"Tri par année de sortie.")

def bindSortByLastOpeningFunction():
	global THE_VISUAL_LIST_OF_GAMES
	THE_VISUAL_LIST_OF_GAMES.sortBy("latest_opening_date_value")
	setBottomBarContent(f"Tri par date de dernière ouverture.")

def bindRunGameFunction():
	THE_VISUAL_LIST_OF_GAMES.openCurrent()

def bindOpenLinkFunction():
	THE_VISUAL_LIST_OF_GAMES.openLink()

def bindCopyLinkFunction():
	THE_VISUAL_LIST_OF_GAMES.copyLinkToClipBoard()

def bindMakeDonationFunction():
	setBottomBarContent(f"Merci de me faire un don sur « {APP_AUTHOR_DONATION_LINK} » (^.^)")
	threading.Thread(target=webbrowser.open, args=(APP_AUTHOR_DONATION_LINK,)).start()

def bindRefreshScreenFunction():
	THE_VISUAL_LIST_OF_GAMES.refresh()

Binding(key="t", code="bindGoDown", description="Aller en haut", instructions=bindGoDownFunction, configFileName="bind_down")
Binding(key="s", code="bindGoUp", description="Aller en bas", instructions=bindGoUpFunction, configFileName="bind_up")
Binding(key="\n", code="bindRunGame", description="Lancer le jeu", instructions=bindRunGameFunction, configFileName="bind_play")

Binding(key="b", code="bindSortByName", description="Trier par nom", instructions=bindSortByNameFunction, configFileName="bind_sort_title")
Binding(key="é", code="bindSortByLicence", description="Trire par licence", instructions=bindSortByLicenceFunction, configFileName="bind_sort_licence")
Binding(key="p", code="bindSortByType", description="Trier par type", instructions=bindSortByTypeFunction, configFileName="bind_sort_game_type")
Binding(key="o", code="bindSortByDate", description="Trier par date", instructions=bindSortByDateFunction, configFileName="bind_sort_year")
Binding(key="è", code="bindSortByLastOpening", description="Trier par date de dernière ouverture", instructions=bindSortByLastOpeningFunction, configFileName="bind_sort_last_opening")


Binding(key="^", code="bindSortByPlayingDuration", description="Trier par heure cumulé", configFileName="bind_sort_playing_duration")
Binding(key="!", code="bindSortByPlatform", description="Trier par plateforme", configFileName="bind_sort_playing_platform")

Binding(key="A", code="bindOpenLink", description="Ouvrir le site web associé", instructions=bindOpenLinkFunction, configFileName="bind_open_link")
Binding(key="e", code="bindEditData", description="Éditer les données", configFileName="bind_edit")
#Binding(key="d", code="bindDelete", description="Suprimer le jeu de la liste", configFileName="bind_delete")
Binding(key="i", code="bindComment", description="Commenter", configFileName="bind_comment")
Binding(key="u", code="bindMakeDonation", description="Faire un don", instructions=bindMakeDonationFunction, configFileName="bind_donate")
Binding(key="w", code="bindShowFullLicence", description="Afficher le texte de la licence", configFileName="bind_show_licence")
Binding(key="/", code="bindFilter", description="Filtrer", configFileName="bind_filter")
Binding(key="h", code="bindSeeBindingHelp", description="Montrer l’aide", configFileName="bind_help")
Binding(key="y", code="bindCopyLink", description="Copier le lien dans le presse-papier", instructions=bindCopyLinkFunction, configFileName="bind_copy_link")
Binding(key="l", code="bindRefreshScreen", description="Rafraichir l’écran", instructions=bindRefreshScreenFunction, configFileName="bind_refresh")
Binding(key="q", code="bindQuit", description=f"Quitter {APP_FANCY_NAME}", configFileName="bind_quit")

########################################################################
# Dispositions de clavier
########################################################################

def getListOfBindingsCode():
	listOfBindingsCode=[]
	for aBinding in listOfBindings:
		listOfBindingsCode.append(aBinding.code)
	return listOfBindingsCode


def returnBindingAfterCode(code):
	for aBinding in listOfBindings:
		if code == aBinding.code:
			return aBinding
	return None

########################################################################

listOfBindingsCode=getListOfBindingsCode()
attributs = {attr: None for attr in listOfBindingsCode}
class Layout:
	def __init__(self, fancyName=None, codeName=None, **attributs):
		self.fancyName=fancyName
		self.codeName=codeName

		layoutArguments.add_argument(f"--{codeName}", action="store_true", help = f"Lancer l’interface avec une carte de touches adaptée à la disposition {fancyName}.")

		globals()[codeName] = self # Déclaration de la variable globale pérmétant d’atteindre directement le type voulu

	def apply(self):
		for aKey in getListOfBindingsCode():
			if hasattr(self, aKey):
				value = getattr(self, aKey)
				returnBindingAfterCode(aKey).setKey(value)

Layout(fancyName="BÉPO", codeName="bepo",
	bindGoDown="t",
	bindGoUp="s",
	bindRunGame="\n",
	bindSortByName="b",
	bindSortByLicence="é",
	bindSortByType="p",
	bindSortByDate="o",
	bindSortByLastOpening="è",
	bindSortByPlayingDuration="^",
	bindSortByPlatform="!",
	bindOpenLink="A",
	bindEditData="e",
#	bindDelete="d",
	bindComment="i",
	bindMakeDonation="x",
	bindShowFullLicence="w",
	bindFilter="/",
	bindSeeBindingHelp="h",
	bindCopyLink="y",
	bindRefreshScreen="l",
	bindQuit="q"
	)

Layout(fancyName="AZERTY", codeName="azerty",
	bindGoDown="j",
	bindGoUp="k",
	bindRunGame="\n",
	bindSortByName="a",
	bindSortByLicence="z",
	bindSortByType="e",
	bindSortByDate="r",
	bindSortByLastOpening="t",
	bindSortByPlayingDuration="y",
	bindSortByPlatform="o",
	bindOpenLink="A",
	bindEditData="f",
#	bindDelete="d",
	bindComment="s",
	bindMakeDonation="c",
	bindShowFullLicence="p",
	bindFilter="/",
	bindSeeBindingHelp="h",
	bindCopyLink="y",
	bindRefreshScreen="l",
	bindQuit="q"
	)

Layout(fancyName="QWERTY", codeName="qwerty",
	bindGoDown="j",
	bindGoUp="k",
	bindRunGame="\n",
	bindSortByName="q",
	bindSortByLicence="w",
	bindSortByType="e",
	bindSortByDate="r",
	bindSortByLastOpening="t",
	bindSortByPlayingDuration="y",
	bindSortByPlatform="u",
	bindOpenLink="A",
	bindEditData="f",
#	bindDelete="d",
	bindComment="s",
	bindMakeDonation="c",
	bindShowFullLicence="p",
	bindFilter="/",
	bindSeeBindingHelp="h",
	bindCopyLink="y",
	bindRefreshScreen="l",
	bindQuit="x"
	)

#for aBinding in listOfBindings:
#	print(f"{aBinding.key}	{aBinding.code}")

args = parser.parse_args()

########################################################################
# Traitement du fichier de configuration
########################################################################

def applyFileConfigurationsBindings():
	config = configparser.ConfigParser()

	config.read('triumphumrc')
#	config.read(CONFIG_FILE)
	configValues={}

	for aConfigKey in getListOfConfigKeyCodes():
		# TODO chercher la clé si elle existe
		if config.has_option("General", aConfigKey):
			configValues[aConfigKey]=config.get("General", aConfigKey)
			returnBindingAfterConfigKeyCode(aConfigKey).setKey(configValues[aConfigKey])


def applyFileConfigurationsGraphicalSymbols():
	config = configparser.ConfigParser()

	config.read('triumphumrc')
	#config.read(CONFIG_FILE)

	for aConfigiGrahpicalSymbol in listOfGraphicalSymbols:
		if config.has_option("General", aConfigiGrahpicalSymbol.fileConfigName):
			aConfigiGrahpicalSymbol.value=config.get("General", aConfigiGrahpicalSymbol.fileConfigName)

applyFileConfigurationsGraphicalSymbols()
for element in listOfGraphicalSymbols:
	print(element.value)

########################################################################
# classe des plateformes
########################################################################

# défffinition de classe
listofPlatforms=[]
class Platform:
	def __init__(self, name=None, code=None, abbr=None, includeInSorting=True):
		self.name = name
		self.code = code
		self.abbr = abbr
		self.includeInSorting = includeInSorting
		globals()[code] = self # Déclaration de la variable globale pérmétant d’atteindre directement le type voulu

def create_platform_objects():
	# Création de la liste des plateformes disponibles

	# Extraction des plateformes
	with open(CONFIG_DIR + '/listOfPlatforms.json') as f:
		listOfPlatformsData = json.load(f)["platforms"]

	# Déploiment des objet de licence
	for aPlatform in listOfPlatformsData:
		Platform(
			name=aPlatform.get("name"),
			code=aPlatform.get("code"),
			abbr=aPlatform.get("abbr")
		)

Platform(name="Plateforme inconue", code="unknownplatform", abbr="", includeInSorting=False)

def get_platform_object_after_code(code):
	if code in globals():
		return globals()[code]
	return unknownplatform

########################################################################
# Classe des types de jeux
########################################################################

def formatDataListToLitteralList(list_):
	try:
		n = len(list_)
	except:
		n = 0
	if n == 0:
		return "-" # TODO
	elif n == 1:
		return list_[0]
	elif n == 2:
		return f"{list_[0]} et {list_[1]}"
	else:
		elements = ", ".join(list_[:-1])
		return f"{elements}, et {list_[-1]}"

# Défffinition de classe
listOfGameTypes=[]
class GameType:
	def __init__(self, name=None, code=None, abbr=None, includeInSorting=True):
		self.name = name
		self.code = code
		self.abbr = abbr
		self.includeInSorting = includeInSorting

		listOfGameTypes.append(self) # Adjonction à la liste des types de jeux
		globals()[code] = self # Déclaration de la variable globale pérmétant d’atteindre directement le type voulu

		def shortName(self):
			# Recherche d’un nom abbrégé
			if self.abbr != None:
				return self.abbr
			return self.name

	def __eq__(self, other):
		if isinstance(other, GameType):
			return self.abbr == other.abbr
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, GameType):
			return self.abbr <  other.abbr
		return NotImplemented

	def __gt__(self, other):
		if isinstance(other, GameType):
			return self.abbr > other.abbr
		return NotImplemented

def create_game_type_objects():
	# Extraction des types de jeux

	# Réinitialisation de la liste des jeux
	global listOfGameTypes
	listOfGameTypes=[]

	# Extraction des types de jeux du fichier
	with open(CONFIG_DIR + '/listOfGameTypes.json') as f:
		listOfGameTypesData = json.load(f)["gameTypes"]

	# Déploiment des objet de type de jeux
	for aGameType in listOfGameTypesData:
		GameType(
			name=aGameType.get("name"),
			code=aGameType.get("code"),
			abbr=aGameType.get("abbr")
		)

GameType(name="Type inconu", abbr=TYPE_VOID_SYMBOL.value, code="unknowntype", includeInSorting=False)

def get_type_object_after_code(code):
	if code in globals():
		return globals()[code]
	return unknowntype

########################################################################
# Classe des licences de jeux
########################################################################

# Défffinition de classe
listOfLicences=[]
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

		listOfLicences.append(self) # Adjonction à la liste des licences
		globals()[code] = self # Déclaration de la variable globale pérmétant d’atteindre directement le type voulu

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

def create_licence_objects():
	# Extraction des licences
	with open(CONFIG_DIR + '/listOfLicences.json') as f:
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

Licence(name="Licence inconue", abbr=LICENCE_VOID_SYMBOL.value, code="unknownlicence", includeInSorting=False)

def get_licence_object_after_code(code):
	if code in globals():
		return globals()[code]
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
	with open(CONFIG_DIR + '/history.json') as f:
		data = json.load(f)

	if 'history' in data and game.codeName in data['history']:
		# Récupération de l’historique du jeu en cours
		game_history = data['history'][game.codeName]
		for history_entry in game_history:
			if is_history_entry_relevant(history_entry):
				prepared_history.append(HistoryEntry(dictionnary=history_entry))

	return prepared_history

########################################################################
# Classe année permetant la comparaison avec les années non renseignées, donc none
########################################################################

class Year:
	def __init__(self, year=None):
		if year is None:
			self._year = None
			self.includeInSorting=False
		else:
			self._year = int(year)
			self.includeInSorting=True

	def __str__(self):
		if self._year is None:
			return DATE_VOID_SYMBOL.value
		return str(self._year)

	def __eq__(self, other):
		if isinstance(other, Year):
			if self._year is None:
				return other._year is None
			else:
				return self._year == other._year
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, Year):
			if self._year is None:
				return True
			elif other._year is None:
				return False
			else:
				return self._year < other._year
		return NotImplemented

	def __gt__(self, other):
		if isinstance(other, Year):
			if self._year is None:
				return False
			elif other._year is None:
				return True
			else:
				return self._year > other._year
		return NotImplemented

########################################################################
# Classe des jeux
########################################################################

# Défffinition de classe
listOfGames=[]
class Game:
	def __init__(self, name=None, codeName=None, licence=None, url=None, year=None, type_=None, authors=None, studios=[], command=None, comments=None, platform=None):
		self.name = name
		self.codeName = codeName
		self.licence = licence
		self.url = url
		self.year = Year(year)
		self.type_ = type_
		self.authors = authors
		self.studios = studios
		self.command = command
		self.comments = comments
		self.platform = platform
		self.history = self.get_history()
		self.latest_opening_date_value = self.latest_opening_date()

		listOfGames.append(self) # Adjonction à la liste des jeux

	def ncurseLine(self):
		# Préparation de la ligne de tableau

		# Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
		ncurseLine = [
			self.platform.abbr or PLATFORM_VOID_SYMBOL.value,
			self.name or NAME_VOID_SYMBOL.value,
			self.licence.abbr or LICENCE_VOID_SYMBOL.value,
			self.type_.abbr or TYPE_VOID_SYMBOL.value,
			self.year or DATE_VOID_SYMBOL.value,
			self.human_latest_opening_duration() or LASTOPENING_VOID_SYMBOL.value,
			self.human_cumulate_time() or CUMULATEDTIME_VOID_SYMBOL.value,
			self.listOfAuthors() or AUTHOR_VOID_SYMBOL.value,
			self.listOfStudios() or STUDIO_VOID_SYMBOL.value,
			self
		]
		return ncurseLine

	def sheet(self):
		# Fiche rapide de description de jeu
		sheet_data=[
			["Nom", self.name],
			["code", self.codeName],
			["Licence", self.licence],
			["URL", self.url],
			["Type", self.type_],
			["Auteur", self.author],
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
		return formatDataListToLitteralList(self.authors)

	def listOfStudios(self):
		return formatDataListToLitteralList(self.studios)

def create_game_objects():
	# Création de la liste des jeux

	# Intialisation
	global listOfGames
	listOfGames=[]

	# Extraction des jeux
	with open(CONFIG_DIR + '/games.json') as f:
		listOfGamesData = json.load(f)["games"]

	## Déploiment des objet de jeux
	for aGame in listOfGamesData:
		Game(
			name=aGame.get("name"),
			codeName=aGame.get("codeName"),
			licence=get_licence_object_after_code(aGame.get("licence")),
			url=aGame.get("url"),
			year=aGame.get("year"),
			type_=get_type_object_after_code(aGame.get("type")),
			command=aGame.get("command"),
			authors=aGame.get("authors"),
			studios=aGame.get("studios"),
			platform=get_platform_object_after_code(aGame.get("platform")),
		)

########################################################################
# Classe des colones de la liste visuelle
########################################################################

listOfPossibleColumns=[]
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
	# Déploiement des objets de types de jeux
	create_game_type_objects()
	# Déploiement des objets de licence
	create_licence_objects()
	# Déploiement des objets de jeux
	create_game_objects()

########################################################################
# Classe de la liste visuelle
########################################################################

listOflistSorting=[]
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
		self.titles = [" ", "Titre", "Licence", "Type", "Date", "Dernière ouverture", "Temps cumulé", "Auteur", "Studio"]
		self.list=None
		self.sortByProperty=None
		self.sortingState=SORTING_ORDER[1]
		self.selected_row = 0

		self.refresh()
		globals()["THE_VISUAL_LIST_OF_GAMES"] = self # Le seul objet de cette classe est TheVisualListOfGames

	def goDown(self):
		self.selected_row = min(len(self.list) - 1, self.selected_row + 1)

	def goUp(self):
		self.selected_row = max(0, self.selected_row - 1)

	def openCurrent(self):
		# Exécuter la commande de lancement du jeu associée à la ligne sélectionnée
		global HIDED_DATA_COLUMN
		setBottomBarContent(f"Ouverture de « {self.list[self.selected_row][HIDED_DATA_COLUMN].name} ».")
		game = self.list[self.selected_row][HIDED_DATA_COLUMN]
		threading.Thread(target=run_command_and_write_on_history, args=(game,)).start()

	def copyLinkToClipBoard(self):
		url = self.list[self.selected_row][self.hiden_data_column_number()].url
		if url != None:
			setBottomBarContent(f"Copie de « {self.list[self.selected_row][HIDED_DATA_COLUMN].url} » dans le presse-papier.")
			pyperclip.copy(url)
		else:
			setBottomBarContent(f"Aucun lien associé à « {self.list[self.selected_row][HIDED_DATA_COLUMN].name} », rien à copier.")

	def refresh(self):
		retrive_datas()
		makeItemsList()

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
			self.list.append(aGame.ncurseLine())
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
			tmpList1=sorted(tmpList0, reverse=self.sortingState, key=lambda x: getattr(x[self.hiden_data_column_number()], property_))
			tmpList2=self.putVoidAtEnd(tmpList1, property_)
			# Déplacer les entrées avec property_ == "-" à la fin
			self.list=tmpList2

	def sortBy(self, property_):
		self.shiftSortingState(property_)
		self.softSortBy(property_)

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

VisualListOfGames()

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

# Fonction pour trier les jeux par type
def sort_by_type(items):
	return sorted(items, key=lambda x: x[2].lower())

# Fonction pour trier les jeux par date
def sort_by_date(items):
	return sorted(items, key=lambda x: str(x[3]))

def history_data_with_current_game(game):
	with open(CONFIG_DIR + '/history.json') as f:
		data = json.load(f)

	if 'history' not in data:
		data['history'] = {}

	if game.codeName not in data['history']:
		data['history'][game.codeName] = []

	return data

def write_opening_date_on_history(game=None, start_time=None, end_time=None, duration=None):
	try:
		# Charger le JSON existant depuis un fichier
		with open(CONFIG_DIR + '/history.json') as f:
			data = json.load(f)

		data = history_data_with_current_game(game)
		history_entry=HistoryEntry(start_time=start_time, end_time=end_time, duration=duration)
		data['history'][game.codeName].append(history_entry.make_data())

		# Enregistrer la structure de données modifiée en tant que JSON
		with open(CONFIG_DIR + '/history.json', 'w') as f:
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
# Interface
########################################################################

# Titres des colonnes
titles = [" ", "Titre", "Licence", "Type", "Date", "Dernière ouverture", "Temps cumulé", "Auteur", "Studio"]

SORTING_COLUMN=0

items=[]
def makeItemsList():
	global items
	items=[]
	global listOfGames
	for aGame in listOfGames:
		items.append(aGame.ncurseLine())
	return items

#makeItemsList()

SPACE_COLUMN_SEPARATION_NUMBER=2

BOTTOM_BAR_TEXT=""
def setBottomBarContent(newBottomBarText):
	global BOTTOM_BAR_TEXT
	BOTTOM_BAR_TEXT = newBottomBarText

# Barre inférieure
def draw_bottom_bar(stdscr):
	# Récupère les dimensions de l'écran
	global BOTTOM_BAR_TEXT
	h, w = stdscr.getmaxyx()

	# Dessine la barre au bas de l'écran
	bar_text = f" {BOTTOM_BAR_TEXT} "
#	stdscr.addstr(h-1, 0, bar_text.ljust(w), curses.A_REVERSE)
	stdscr.addstr(h-1, 0, bar_text, curses.A_REVERSE)
	stdscr.chgat(h-1, 0, w, curses.A_REVERSE)


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

# Barre inférieure
def draw_bottom_right(stdscr, visualListOfGames):
	# Récupère les dimensions de l'écran

	rightIndicatorText=prepareTextForRightIndicator(visualListOfGames)
	h, w = stdscr.getmaxyx()

	# Définir le texte de la barre inférieure

	# Calculer la position de départ pour l'alignement à droite
	x_start = w - len(rightIndicatorText) - 1  # -1 pour éviter le débordement

	# Effacer l'arrière-plan de la ligne
	stdscr.move(h-1, 0)

	# Dessiner le texte avec la couleur d'origine, sans arrière-plan
	stdscr.addstr(h-1, x_start, rightIndicatorText, curses.A_REVERSE)

	# Rafraîchir l'écran
	stdscr.refresh()


def main(stdscr):
	# Initialisation de ncurses
	curses.curs_set(0)  # Masquer le curseur

	# Initialiser les couleurs
	curses.start_color()
	curses.use_default_colors()

	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Noir sur fond blanc
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Blanc sur fond noir

	# Définir la couleur du texte comme étant la même que la couleur du fond
	curses.init_pair(1, -1, -1)  # Utilise la couleur par défaut du terminal

	# Nom de l'application
	app_name = APP_FANCY_NAME + " | " + APP_DESCRIPTION


	global THE_VISUAL_LIST_OF_GAMES
	global BOTTOM_BAR_TEXT
	global bindSortByName
	# Boucle principale
	while True:

		# Mise à jour de l’historique
		#retrive_datas()
		# Mise à jour de la liste des jeux
		makeItemsList() # TODO : déglobaliser
		THE_VISUAL_LIST_OF_GAMES.refresh()

		curses.noecho()  # Désactiver l'écho des touches # TODO à édcommenter avant prod
		stdscr.clear()

		# Dessiner la barre supérieure avec le nom de l'application
		stdscr.attron(curses.color_pair(1))
		stdscr.addstr(0, 0, app_name.ljust(curses.COLS), curses.color_pair(2))
		stdscr.attroff(curses.color_pair(1))


		draw_bottom_bar(stdscr)
		draw_bottom_right(stdscr, THE_VISUAL_LIST_OF_GAMES)

		# Calcul de la largeur des colones
		col_widths = getColWidths()

		for row_number, title in enumerate(titles):
			stdscr.addstr(1, sum(col_widths[:row_number]) + row_number * 2, str(title), curses.color_pair(2) | curses.A_BOLD)

		# Affichage des données de la liste
		for row_number, item in enumerate(THE_VISUAL_LIST_OF_GAMES.list):
			for column_number, column in enumerate(item):
				if column_number < HIDED_DATA_COLUMN:  # Masquer la colonne "commande"
					stdscr.addstr(row_number + 2, sum(col_widths[:column_number]) + column_number * 2, str(column))

		stdscr.addstr(THE_VISUAL_LIST_OF_GAMES.selected_row + 2, 0, " " * curses.COLS, curses.color_pair(2))  # Effacer toute la ligne avec la couleur de fond

		# Affichage des données de la liste avec surbrillance pour la ligne sélectionnée
		# Cas particulier de la ligne ayant le focus
		for column_number, column in enumerate(THE_VISUAL_LIST_OF_GAMES.list[THE_VISUAL_LIST_OF_GAMES.selected_row][:HIDED_DATA_COLUMN]):  # Afficher seulement les 4 premières colonnes
			stdscr.addstr(THE_VISUAL_LIST_OF_GAMES.selected_row + 2, sum(col_widths[:column_number]) + column_number * 2, str(column), curses.color_pair(2) | curses.A_BOLD)

		# Rafraîchir l'écran
		stdscr.refresh()

		# Lecture de la touche pressée
		key = transform_key_to_character(stdscr.get_wch())
#		setBottomBarContent(f"Touche préssée {key}")

		writeInTmp(key)

		if (key) == transform_key_to_character('q'):  # Quitter si la touche 'q' est pressée
			break
		elif (key) in getListOfKeyBindingsCodes():
			returnBindingAfterKeyStroke(key).executeInstructions()

########################################################################
# Fonctions de la ligne de commande
########################################################################

def getGameObjectByItCodeName(codeName):
	global listOfGames
	for aGame in listOfGames:
		if aGame.codeName == codeName:
			return aGame
	return None

########################################################################
# Que faire
########################################################################

if args.config_file != None:
	CONFIG_FILE=args.config_file
	applyFileConfigurationsBindings()
if args.games != None:
	GAME_FILE=args.games
if args.game_types != None:
	TYPE_FILE=args.game_types
if args.licences != None:
	LICENCE_FILE=args.licences
if args.platforms != None:
	PLATFORM_FILE=args.platforms

elif  args.about != True:
	print(f"Fichier de configuration principal : {CONFIG_FILE}")
	print(f"Fichier des jeux : {GAME_FILE}")
	print(f"Fichier des types de jeux : {TYPE_FILE}")
	print(f"Fichier des licences : {LICENCE_FILE}")
	print(f"Fichier des plateformes : {PLATFORM_FILE}")

if args.run not in [None, False]:
	theGame=getGameObjectByItCodeName(args.run)
	if theGame != None:
		print(f"Ouverture de « {theGame.name} »")
		threading.Thread(target=run_command_and_write_on_history, args=(theGame,)).start()
	else:
		print(f"Aucun jeu ne correspond à l’identifiant « {args.run} »")

elif  args.about == True:
	print(APP_FANCY_NAME + " " + APP_VERSION + " " + APP_DESCRIPTION)

elif args.donate == True:
	print(f"Pour soutenir {APP_FANCY_NAME} et faire en sorte qu’il continue et s’améliore, merci de faire un don à <{APP_AUTHOR_DONATION_LINK}>. (^.^)")
	webbrowser.open(APP_AUTHOR_DONATION_LINK)

elif args.tui == True:
	curses.wrapper(main)


