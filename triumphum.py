#!/usr/bin/python3

import curses
import subprocess
import threading
import json
import webbrowser
import pyperclip
import appdirs
import re
from datetime import datetime
from tabulate import tabulate

########################################################################
# Variables globales
########################################################################

APP_CODE_NAME="triumphum"
APP_FANCY_NAME="Triumphum"
APP_DESCRIPTION="Gestionnaire de ludothèque en Python et NCurses"
APP_VERSION="0.1"
APP_AUTHOR="Fauve"
APP_AUTHOR_MAIL="fauve.ordinator@taniere.info"
APP_URL=""

########################################################################
# Répertoire de configuration
########################################################################

# Obtenez le répertoire de configuration de l'application
CONFIG_DIR = appdirs.user_config_dir(APP_CODE_NAME)

BASE_NAME_GAME_FILE="games.json"
BASE_NAME_TYPE_FILE="listOfGameTypes.json"

print("Répertoire de configuration:", CONFIG_DIR)

########################################################################
# Classe des types de jeux
########################################################################

# Défffinition de classe
listOfGameTypes=[]
class GameType:
	def __init__(self, name=None, code=None, abbr=None):
		self.name = name
		self.code = code
		self.abbr = abbr

		listOfGameTypes.append(self) # Adjonction à la liste des types de jeux
		globals()[code] = self # Déclaration de la variable globale pérmétant d’atteindre directement le type voulu

		def shortName(self):
			# Recherche d’un nom abbrégé
			if self.abbr != None:
				return self.abbr
			return self.name

# Extraction des types de jeux
with open(CONFIG_DIR + '/listOfGameTypes.json') as f:
	listOfGameTypesData = json.load(f)["gameTypes"]

# Déploiment des objet de type de jeux
for aGameType in listOfGameTypesData:
	GameType(name=aGameType.get("name"), code=aGameType.get("code"), abbr=aGameType.get("abbr"))

########################################################################
# Classe des licences de jeux
########################################################################

# Défffinition de classe
listOfLicences=[]
class Licence:
	def __init__(self, name=None, abbr=None, code=None, url=None, shortText=None, fullText=None, freedomCoefficient=0):
		self.name = name
		self.abbr = abbr
		self.code = code
		self.url = url
		self.shortText = shortText
		self.fullText = fullText
		self.freedomCoefficient = freedomCoefficient

		listOfLicences.append(self) # Adjonction à la liste des licences
		globals()[code] = self # Déclaration de la variable globale pérmétant d’atteindre directement le type voulu

	# Blocs de comparaisons permétant de trier les licences entre elles de la plus libre à la moins libre
	def __eq__(self, other):
		if isinstance(other, Licence):
			return self.freedomCoefficient == other.freedomCoefficient
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, Licence):
			return self.freedomCoefficient < other.freedomCoefficient
		return NotImplemented

	def __le__(self, other):
		if isinstance(other, Licence):
			return self.freedomCoefficient < other.freedomCoefficient
		return NotImplemented

	def __gt__(self, other):
		if isinstance(other, Licence):
			return self.freedomCoefficient > other.freedomCoefficient
		return NotImplemented

	def __ge__(self, other):
		if isinstance(other, Licence):
			return self.freedomCoefficient > other.freedomCoefficient
		return NotImplemented

# Extraction des licences
with open(CONFIG_DIR + '/listOfLicences.json') as f:
	listOfGameTypesData = json.load(f)["licences"]

# Déploiment des objet de licence
for aLicence in listOfGameTypesData:
	Licence(name=aLicence.get("name"), code=aLicence.get("code"), abbr=aLicence.get("abbr"), url=aLicence.get("url"), shortText=aLicence.get("shortText"), freedomCoefficient=aLicence.get("freedomCoefficient"))

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
			"start_time": self.start_time,
			"end_time": self.end_time,
			"duration": self.duration,
		}

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
		if self.newer() != None:
			return self.newer().end_time
		return None

########################################################################
# Fonctions d’éxtraction de l’historique pour un jeu donné

def is_history_date_relevant(date):
	# Filtre des dates pertinantes

	# Définir le motif de l'expression régulière pour le format AAAA-MM-JJThh:mm
	pattern = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$')
	if pattern.match(date):
		return True
	return False

def is_history_entry_relevant(history_entry):
	
	if "start_time" in history_entry and "end_time" in history_entry and "duration" in history_entry :
		if is_history_date_relevant(history_entry["start_time"]) and is_history_date_relevant(history_entry["end_time"]) and is_history_date_relevant(history_entry["duration"]):
			return True
	return False

def retrive_history_of_a_game(game):
	prepared_history = History()
	with open(CONFIG_DIR + '/history.json') as f:
		data = json.load(f)
	if 'history' in data and game.codeName in data['history']:
		# Récupération de l’historique du jeu en cours
		get_history = data['history'][game.codeName]
		for history_entry in get_history:
			if is_history_entry_relevant(history_entry):
				prepared_history.append(HistoryEntry(dictionnary=history_entry))

	return prepared_history

########################################################################
# Classe des jeux
########################################################################

# Défffinition de classe
listOfGames=[]
class Game:
	def __init__(self, name=None, codeName=None, licence=None, url=None, year=None, type_=None, author=None, command=None, comments=None):
		self.name = name
		self.codeName = codeName
		self.licence = licence
		self.url = url
		self.year = year
		self.type_ = type_
		self.author = author
		self.command = command
		self.comments = comments
		self.history = self.get_history()

		listOfGames.append(self) # Adjonction à la liste des jeux

	def ncurseLine(self):
		# Préparation de la ligne de tableau

		# Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
		ncurseLine = [self.name or "-", self.licence or "-", self.type_ or "-", self.year or "-", self.latest_opening() or "-", self]
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
			["Dernière ouverture", self.latest_opening()],
		]

		print(tabulate(sheet_data))

	def get_history(self):
		# Retourne l’historique des dates et heures de parties jouées
		return retrive_history_of_a_game(self)

	def latest_opening(self):
		# Retourne la dernière date où le jeu a ét éouvert
		return self.history.last_date()

# Extraction des jeux
with open(CONFIG_DIR + '/games.json') as f:
	listOfGamesData = json.load(f)["games"]

## Déploiment des objet de jeux
for aGame in listOfGamesData:
	Game(name=aGame.get("name"), codeName=aGame.get("codeName"), licence=aGame.get("licence"), url=aGame.get("url"), year=aGame.get("year"), type_=aGame.get("type"), command=aGame.get("command"), author=aGame.get("author"))

########################################################################
# Fonctions de l’interface interactive
########################################################################

# Fonction pour trier les jeux par titre
def sort_by_title(items):
	return sorted(items, key=lambda x: x[0].lower())

# Fonction pour trier les jeux par licence
def sort_by_license(items):
	return sorted(items, key=lambda x: x[1].lower())

# Fonction pour trier les jeux par type
def sort_by_type(items):
	return sorted(items, key=lambda x: x[2].lower())

# Fonction pour trier les jeux par date
def sort_by_date(items):
	return sorted(items, key=lambda x: str(x[3]))

def run_command(command):
	# Exécuter le sous-processus tout en redirigeant les entrées/sorties standard
	runed_command = subprocess.Popen(command.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	output, error = runed_command.communicate()
	end_time = datetime.now()
	with open('/tmp/triumphumlogs', 'w') as f:
		f.write(end_time.strftime("%Y-%m-%dT%H:%M"))

def write_opening_date_on_history(game):
	# Charger le JSON existant depuis un fichier
	with open(CONFIG_DIR + '/history.json') as f:
		data = json.load(f)

	if 'history' not in data:
		data['history'] = {}

	if game.codeName not in data['history']:
		data['history'][game.codeName] = []
	data['history'][game.codeName].append(datetime.now().strftime("%Y-%m-%dT%H:%M"))

	# Enregistrer la structure de données modifiée en tant que JSON
	with open(CONFIG_DIR + '/history.json', 'w') as f:
		json.dump(data, f, indent=4)


def run_command_and_write_on_history(game):
	# Enregistrement de l’heure de début
	running_start_time = datetime.now()

	# Lancement du procéssus
	command_process = subprocess.Popen(game.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	# Mise en atente pour la fin du processus
	output, error = command_process.communicate()

	# Récupération de l’heure de fin
	running_end_time = datetime.now()

	# Date
	running_duration = running_end_time - running_start_time

########################################################################
# Interface
########################################################################

def makeItemsList():
	items=[]
	global listOfGames
	for aGame in listOfGames:
		items.append(aGame.ncurseLine())
	return items

items = makeItemsList() # TODO : déglobaliser

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

	# Titres des colonnes
	titles = ["Titre", "Licence", "Type", "Date", "Dernière ouverture"]

	# Données de la liste
	global items

	# Index de la ligne sélectionnée
	selected_row = 0

	# Boucle principale
	while True:
		curses.noecho()  # Désactiver l'écho des touches
		stdscr.clear()

		# Dessiner la barre supérieure avec le nom de l'application
		stdscr.attron(curses.color_pair(1))
		stdscr.addstr(0, 0, app_name.ljust(curses.COLS), curses.color_pair(2))
		stdscr.attroff(curses.color_pair(1))

		col_widths = [max(len(str(column)) for column in col) for col in zip(*items)]
		# Affichage des titres de colonnes
		for i, title in enumerate(titles):
			#stdscr.addstr(1, i * 20, title)
#			stdscr.addstr(1, (i * 20 + i), title)
			stdscr.addstr(1, sum(col_widths[:i]) + i * 2, str(title), curses.color_pair(2) | curses.A_BOLD)

		# Affichage des données de la liste
		for i, item in enumerate(items):
			for j, column in enumerate(item):
				# Mettre en surbrillance la ligne sélectionnée
				if i == selected_row:
					pass
#				elif j != 4:  # Masquer la colonne "commande"
				elif j < 5:  # Masquer la colonne "commande"
					stdscr.addstr(i + 2, sum(col_widths[:j]) + j * 2, str(column))

		stdscr.addstr(selected_row + 2, 0, " " * curses.COLS, curses.color_pair(2))  # Effacer toute la ligne avec la couleur de fond
		# Affichage des données de la liste avec surbrillance pour la ligne sélectionnée
		for j, column in enumerate(items[selected_row][:5]):  # Afficher seulement les 4 premières colonnes
			stdscr.addstr(selected_row + 2, sum(col_widths[:j]) + j * 2, str(column), curses.color_pair(2) | curses.A_BOLD)

		# Rafraîchir l'écran
		stdscr.refresh()

		# Lecture de la touche pressée
		key = stdscr.getch()

		# Gestion de la navigation entre les lignes
		if key == ord('t'):
			selected_row = min(len(items) - 1, selected_row + 1)
		elif key == ord('s'):
			selected_row = max(0, selected_row - 1)
		elif key == curses.KEY_ENTER or key in [10, 13]:  # Touche "Entrée"
			# Exécuter la commande de lancement du jeu associée à la ligne sélectionnée
			write_opening_date_on_history(items[selected_row][5])
			self = items[selected_row][5]
			threading.Thread(target=run_command, args=(self,)).start()
		elif key == ord('a'):  # Ouvrir le lien associé au jeu si la touche 'a' est pressée
			url = items[selected_row][5].url  # Supposons que l'URL est stockée à l'indice 5
			webbrowser.open(url)
		elif key == ord('b'):  # Trier par titre si la touche 'b' est pressée
			items = sort_by_title(items)
		elif key == ord('é'):  # Trier par licence si la touche 'é' est pressée
			items = sort_by_license(items)
		elif key == ord('p'):  # Trier par type si la touche 'p' est pressée
			items = sort_by_license(items)
		elif key == ord('o'):  # Trier par date si la touche 'o' est pressée
			items = sort_by_date(items)
		elif key == ord('y'):  # Trier par date si la touche 'o' est pressée
			url = items[selected_row][5].url  
			pyperclip.copy(url)
		elif key == ord('q'):  # Quitter si la touche 'q' est pressée
			break

curses.wrapper(main)

