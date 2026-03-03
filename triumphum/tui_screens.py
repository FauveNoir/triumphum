########################################################################
# Autres écrans
########################################################################
import locale
import curses

from triumphum.__init__ import *
from triumphum.tui import  setBottomBarContent, drawBothBars
import triumphum.global_variables as global_variables

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
    global_variables.STDSCR.timeout(-1)
    while True:
        setBottomBarContent(f"Retour:q  Faire un don:x")
        centeredMessage(global_variables.STDSCR,APP_SPLASH)
        drawBothBars(global_variables.STDSCR)
        # Lecture de la touche pressée
        from triumphum.keybindings import transformKeyToCharacter
        key = transformKeyToCharacter(global_variables.STDSCR.get_wch())
        if key == "x":
            from triumphum.keybindings import bindMakeDonationFunction
            bindMakeDonationFunction()
        else:
            setBottomBarContent("")
            break

def drawGamePlot():
    global_variables.STDSCR.timeout(-1)
    game=global_variables.THE_VISUAL_LIST_OF_GAMES.currentGame()
    plot=game.history.generate_plot()
    if plot == None:
        setBottomBarContent(f"Il n’existe pas d’historique de jeu pour « {game.name} ».")

    else:
        while True:
            setBottomBarContent(f"Fréquence de jeu pour « {game.name} »")
            centeredMessage(global_variables.STDSCR,plot)
            drawBothBars(global_variables.STDSCR)
            # Lecture de la touche pressée
            from triumphum.keybindings import transformKeyToCharacter
            key = transformKeyToCharacter(global_variables.STDSCR.get_wch())
            if key == "x":
                from triumphum.keybindings import bindMakeDonationFunction
                bindMakeDonationFunction()
            else:
                setBottomBarContent("")
                break

########################################################################
# Écran d’aide

def showHelpScreen():
    pass
