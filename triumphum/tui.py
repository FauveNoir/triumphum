########################################################################
# Interface
########################################################################
import curses
import humanize

from triumphum.__init__ import *
from triumphum.global_variables import *
#from triumphum.global_variables import STDSCR as STDSCR
import triumphum.global_variables as global_variables
import triumphum.symbols as symbols
from triumphum.misc import bottomBarCoordinate
from triumphum.misc import getElementHavingParameterWithValue
from triumphum.debug import *

# Titres des colonnes

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
	global_variables.STDSCR.refresh()

def setBottomBarColor(color):
	pass


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

	rightIndicatorText=  symbols.CUMULATED_TIME_PLAYED_PER_DAY + ": "
	rightIndicatorText+= humanize.naturaldelta(visualListOfGames.allHistoryEntries().cumulatedPlayingTimeFromNDays(1))

	rightIndicatorText+= "" + str(symbols.CUMULATED_TIME_PLAYED_SEPARATOR) + ""

	rightIndicatorText+= symbols.CUMULATED_TIME_PLAYED_PER_WEEK + ": "
	rightIndicatorText+= humanize.naturaldelta(visualListOfGames.allHistoryEntries().cumulatedPlayingTimeFromNDays(7))

	rightIndicatorText+= "" + str(symbols.CUMULATED_TIME_PLAYED_SEPARATOR) + ""

	rightIndicatorText+= symbols.CUMULATED_TIME_PLAYED_PER_MONTH + ": "
	rightIndicatorText+= humanize.naturaldelta(visualListOfGames.allHistoryEntries().cumulatedPlayingTimeFromNDays(30))

	rightIndicatorText+= "" + str(symbols.CUMULATED_TIME_PLAYED_SEPARATOR) + ""

	rightIndicatorText+= symbols.CUMULATED_TIME_PLAYED_PER_YEAR + ": "
	rightIndicatorText+= humanize.naturaldelta(visualListOfGames.allHistoryEntries().cumulatedPlayingTimeFromNDays(365))

	return rightIndicatorText

MAIN_SCREEN_MARGIN_BOTTOM=2
# Barre inférieure
def draw_bottom_right(stdscr, visualListOfGames):
	# Récupère les dimensions de l'écran

	rightIndicatorText=prepareTextForRightIndicator(visualListOfGames)
	h, w = stdscr.getmaxyx()
	global_variables.STDSCR=stdscr

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
	from triumphum.tui_list import getColWidths
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
		writeInTmp()

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
	draw_bottom_bar(global_variables.STDSCR)
	global_variables.STDSCR.refresh()
	from triumphum.keybindings import transformKeyToCharacter
	while True:
		key = transformKeyToCharacter(global_variables.STDSCR.get_wch())
		if key in ['y', 'yes']:
			return True
		elif key in ['n', 'no']:
			return False
		else:
			setBottomBarContent("Veuillez répondre par 'Y' ou 'n'.")
			draw_bottom_bar(global_variables.STDSCR)
			global_variables.STDSCR.refresh()

########################################################################
# Main
########################################################################

def main(stdscr):
	global_variables.STDSCR=stdscr
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
		from triumphum.keybindings import transformKeyToCharacter
		key = transformKeyToCharacter(stdscr.get_wch())
#		setBottomBarContent(f"Touche préssée {key}")

		if (key) == transformKeyToCharacter('q'):  # Quitter si la touche 'q' est pressée # TODO factoriser
			break
		elif any(key == aBinding.key for aBinding in listOfBindings):
			# Teste si la touche préssé correspond à l’attribut key d’un des élements de listOfBindings
			setBottomBarContent("")

			# ↓ Trouver au sein de `listOfBindings` l’élément ayant dans son paramettre « key » la valeure contenue dans `value`, et en éxecute aussitôt les instructions.
			getElementHavingParameterWithValue(givenList=listOfBindings, parameter="key", value=key).executeInstructions()


def runTui():
	curses.wrapper(main)
