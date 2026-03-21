########################################################################
# Interface
########################################################################
import curses
import humanize

import sys
import traceback

from triumphum.__init__ import *
from triumphum.global_variables import *
from triumphum.colors import *
#from triumphum.global_variables import STDSCR as STDSCR
import triumphum.global_variables as global_variables
import triumphum.symbols as symbols
from triumphum.misc import bottomBarCoordinate
from triumphum.misc import getElementHavingParameterWithValue
from triumphum.debug import *
from triumphum.debug import * # TODO

# Titres des colonnes

SORTING_COLUMN=0

def makeItemsList():
    global_variables.THE_VISUAL_LIST_OF_GAMES.items=[]
    for aGame in listOfGames:
        global_variables.THE_VISUAL_LIST_OF_GAMES.items.append(listOfGames[aGame].ncurseLine())
    return global_variables.THE_VISUAL_LIST_OF_GAMES.items

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

def truncate(text=None, max_len=8):
    text=str(text)
    if len(text) <= max_len:
        return text
    return text[:max_len - 1] + "…"

def display_too_small_terminal_message(stdscr):
    height, width = global_variables.STDSCR.getmaxyx()
    display_centered_text(stdscr, f"Le terminal est trop petit pour lancer {APP_FANCY_NAME}\nVeuillez utiliser un terminal d’au moins {height}×{width}.")


def display_filter_if_needed(stdscr):
    if global_variables.THE_VISUAL_LIST_OF_GAMES.filter_mode:
       display_filter(stdscr)

def display_filter(stdscr):
    stdscr.timeout(1000)
    curses.curs_set(1)  # Afficher le curseur
    h, w = bottomBarCoordinate(stdscr)

    # Position de départ pour la saisie de texte
    stdscr.move(h-1, 0)

    # Initialiser une liste pour stocker les caractères saisis
    input_text = global_variables.THE_VISUAL_LIST_OF_GAMES.filter_input

    stdscr.addch("/")  # Afficher le caractère saisi à l'écran

    stdscr.addstr(input_text)  # Afficher le caractère saisi à l'écran
    stdscr.move(h-1, len(input_text)+1)

    # Capturer un caractère
    ch = stdscr.getch()

    if ch == 27:  # Si ESC est pressé
        global_variables.THE_VISUAL_LIST_OF_GAMES.unactivate_filter()

    elif ch == 263: # Si BSP est préssé
        y, x = stdscr.getyx()

        if x > 1:
            input_text=input_text[:-1]
            stdscr.move(y, x - 1)  # Déplace le curseur à la position juste avant
            stdscr.delch()         # Supprime le caractère à cette position

        else:
            global_variables.THE_VISUAL_LIST_OF_GAMES.unactivate_filter()

    elif ch in [curses.KEY_ENTER, 10]:  # Si Entrée est pressé (curses.KEY_ENTER vaut 10)
            global_variables.THE_VISUAL_LIST_OF_GAMES.unactivate_filter()

    else:
        # Ajouter le caractère à la chaîne de texte
        try:
            input_text += chr(ch)
        except:
            pass
    global_variables.THE_VISUAL_LIST_OF_GAMES.set_filter(input_text)

    curses.curs_set(0)  # Masquer le curseur

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

        # Affichage de l’entête de liste
        for row_number, title in enumerate(titles):
            stdscr.addstr(1, sum(col_widths[:row_number]) + row_number * 2, str(title), curses.color_pair(2) | curses.A_BOLD)

        # Affichage des données de la liste
        for row_number, item in enumerate(global_variables.THE_VISUAL_LIST_OF_GAMES.getCurrentVisibleList(screenHeight)):
            for column_number, column in enumerate(item.formated_data):
                stdscr.addstr(row_number + 2,
                              sum(col_widths[:column_number]) + column_number * 2,
                              column[0],
                              curses.color_pair(column[1]))

        stdscr.addstr(global_variables.THE_VISUAL_LIST_OF_GAMES.visualHighlightedLineNumber(screenHeight) + 2, 0, " " * curses.COLS, curses.color_pair(2))  # Effacer toute la ligne avec la couleur de fond

        # Affichage des données de la liste avec surbrillance pour la ligne sélectionnée
        # Cas particulier de la ligne ayant le focus
        for column_number, column in enumerate(global_variables.THE_VISUAL_LIST_OF_GAMES.relevantList()[global_variables.THE_VISUAL_LIST_OF_GAMES.selected_row].formated_data):  # Afficher seulement les 4 premières colonnes
            stdscr.addstr(global_variables.THE_VISUAL_LIST_OF_GAMES.visualHighlightedLineNumber(screenHeight) + 2,
                          sum(col_widths[:column_number]) + column_number * 2,
                          str(column[0]),
                          curses.color_pair(3) | curses.A_BOLD)


def questionMode(question):
    setBottomBarContent(question + " (Y/n)")
    draw_bottom_bar(global_variables.STDSCR)
    global_variables.STDSCR.refresh()
    from triumphum.keybindings import transformKeyToCharacter
    while True:
        try:
            key = transformKeyToCharacter(global_variables.STDSCR.get_wch())
            if key in ['y', 'yes']:
                return True
            elif key in ['n', 'no']:
                return False
            else:
                setBottomBarContent("Veuillez répondre par 'Y' ou 'n'.")
                draw_bottom_bar(global_variables.STDSCR)
                global_variables.STDSCR.refresh()
        except:
            pass

########################################################################
# Main
########################################################################


def mainTui(stdscr):

    global_variables.STDSCR=stdscr
    # Initialisation de ncurses
    curses.curs_set(0)  # Masquer le curseur
    screenHeight, screenWidth = stdscr.getmaxyx()

    # Initialiser les couleurs
    curses.start_color()
    curses.use_default_colors()
    use_curses_colors()

    # Définir la couleur du texte comme étant la même que la couleur du fond
    curses.init_pair(1, -1, -1)  # Utilise la couleur par défaut du terminal


    global BOTTOM_BAR_TEXT
    global bindSortByName

    # Boucle principale
    while True:
        stdscr.timeout(1000)
        # Mise à jour de l’historique
        #retrive_datas()
        # Mise à jour de la liste des jeux

        curses.noecho()  # Désactiver l'écho des touches
        stdscr.clear()

        try:
            drawListOfGames(stdscr)
            drawBothBars(stdscr)
            display_filter_if_needed(stdscr)
            stdscr.refresh()

        except curses.error as e:
            display_too_small_terminal_message(stdscr)
            height, width = global_variables.STDSCR.getmaxyx()
            print(f"Le terminal est trop petit pour lancer {APP_FANCY_NAME}\nVeuillez utiliser un terminal d’au moins {height}×{width}.")

        # Rafraîchir l'écran
        stdscr.refresh()

        # Lecture de la touche pressée
        if not global_variables.THE_VISUAL_LIST_OF_GAMES.filter_mode:
            from triumphum.keybindings import transformKeyToCharacter
            try:
                key = stdscr.get_wch()
                key = transformKeyToCharacter(key)
            except curses.error:
                key = None  # aucune touche pressée pendant 1 seconde

            if (key) == transformKeyToCharacter('q'):  # Quitter si la touche 'q' est pressée # TODO factoriser
                break
            elif any(key == aBinding.key for aBinding in global_variables.listOfBindings):
                # Teste si la touche préssé correspond à l’attribut key d’un des élements de listOfBindings
                setBottomBarContent("")

                # ↓ Trouver au sein de `listOfBindings` l’élément ayant dans son paramettre « key » la valeure contenue dans `value`, et en éxecute aussitôt les instructions.
                getElementHavingParameterWithValue(givenList=global_variables.listOfBindings, parameter="key", value=key).executeInstructions()


def runTui():
    curses.wrapper(mainTui)
