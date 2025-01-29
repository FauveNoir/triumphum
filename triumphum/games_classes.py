########################################################################
# Classe des jeux
########################################################################
import humanize
from datetime import date, datetime, timedelta
from tabulate import tabulate
import json

from triumphum.global_variables import *
import triumphum.config_file as config_file
from triumphum.history_classes import retrive_history_of_a_game
from triumphum.licences_classes import  get_licence_object_after_code
from triumphum.genres_classes import get_genre_object_after_code
from triumphum.platforms_classes import get_platform_object_after_code
import triumphum.symbols as symbols

from triumphum.debug import * # TODO

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
			self.platform.abbr or symbols.PLATFORM_VOID_SYMBOL.value,
			self.name or symbols.NAME_VOID_SYMBOL.value,
			self.licence.abbr or symbols.LICENCE_VOID_SYMBOL.value,
			self.genre.abbr or symbols.GENRE_VOID_SYMBOL.value,
			self.year or symbols.DATE_VOID_SYMBOL.value,
			self.human_latest_opening_duration() or symbols.LASTOPENING_VOID_SYMBOL.value,
			self.human_cumulate_time() or symbols.CUMULATEDTIME_VOID_SYMBOL.value,
			self.listOfAuthors() or symbols.AUTHOR_VOID_SYMBOL.value,
			self.listOfStudios() or symbols.STUDIO_VOID_SYMBOL.value,
			self
		]
		return ncurseLine

	def asciiRow(self):
		# Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
		asciiRow = [
			self.platform.abbr or symbols.PLATFORM_VOID_SYMBOL.value,
			self.name or symbols.NAME_VOID_SYMBOL.value,
			self.licence.abbr or symbols.LICENCE_VOID_SYMBOL.value,
			self.genre.abbr or symbols.GENRE_VOID_SYMBOL.value,
			self.year or symbols.DATE_VOID_SYMBOL.value,
			self.human_latest_opening_duration() or symbols.LASTOPENING_VOID_SYMBOL.value,
			self.human_cumulate_time() or symbols.CUMULATEDTIME_VOID_SYMBOL.value,
			self.listOfAuthors() or symbols.AUTHOR_VOID_SYMBOL.value,
			self.listOfStudios() or symbols.STUDIO_VOID_SYMBOL.value
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
		return formatDataListToLitteralList(self.authors, symbols.AUTHOR_VOID_SYMBOL.value)

	def listOfStudios(self):
		return formatDataListToLitteralList(self.studios, symbols.STUDIO_VOID_SYMBOL.value)

	def delete(self):
		deleteGameFromDatabase(self.code)

	def showPlot(self):
		pass


def create_game_objects():
	# Création de la liste des jeux

	# Extraction des jeux
	with open(config_file.GAME_FILE.fullPath()) as f:
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
