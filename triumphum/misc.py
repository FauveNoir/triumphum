import curses

from triumphum.tui import bottomBarCoordinate
from triumphum.debug import * # TODO
import triumphum.global_variables as global_variables

def getElementHavingParameterWithValue(givenList=None, parameter=None, value=None):
	# Parcourt la liste `givenList` pour y trouver un élément ayant un paramettre nomé `parameter` et ayant pour valeur `value`.
	if parameter is None or value is None:
		return None

	for anElement in givenList:
		if hasattr(anElement, parameter) and getattr(anElement, parameter) == value:
				return anElement
	return None

def enteringExMode(stdscr):
	# Activer la saisie de texte

	h, w = bottomBarCoordinate(stdscr)
	curses.curs_set(1)  # Afficher le curseur

#	curses.init_pair(h-2, curses.COLOR_BLUE, curses.COLOR_BLACK)
	# Position de départ pour la saisie de texte
	stdscr.move(h-1, 0)

	# Initialiser une liste pour stocker les caractères saisis
	input_text = ""

	stdscr.addch(":")  # Afficher le caractère saisi à l'écran
	while True:
		# Capturer un caractère
		ch = stdscr.getch()

		if ch == 27:  # Si ESC est pressé
			break

		elif ch == 263: # Si BSP est préssé
			y, x = stdscr.getyx()

			if x > 1:
				input_text=input_text[:-1]
				stdscr.move(y, x - 1)  # Déplace le curseur à la position juste avant
				stdscr.delch()         # Supprime le caractère à cette position

				stdscr.refresh()
			else:
				break

		elif ch in [curses.KEY_ENTER, 10]:  # Si Entrée est pressé (curses.KEY_ENTER vaut 10)

			whatToDoWithShellInput(input_text)
			break  # Sortir de la boucle de saisie

		else:
			# Ajouter le caractère à la chaîne de texte
			input_text += chr(ch)
			stdscr.addch(ch)  # Afficher le caractère saisi à l'écran
			stdscr.refresh()

	curses.curs_set(0)  # Masquer le curseur

def enteringExModeByBinding():
	writeInTmp(global_variables.STDSCR)
	enteringExMode(global_variables.STDSCR)
