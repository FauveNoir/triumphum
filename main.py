#!/usr/bin/python3

import curses
import subprocess
import threading
import json
import webbrowser
import re
from datetime import date, datetime, timedelta
#import pendulum
import locale
import time
import shlex
from Xlib import XK
from Xlib.display import Display
import curses.textpad
import os
import plotext as plt
import numpy as np

from triumphum.debug import * # TODO

from triumphum.__init__ import *
from triumphum.global_variables import *
from triumphum.config_file import prepareConfigFiles, verifyConfigFileExistence, applyFileConfigurationsBindings, applyFileConfigurationsGraphicalSymbols, retrive_datas
import triumphum.config_file as config_file
from triumphum.cli_options import args
from triumphum.symbols import *
from triumphum.keybindings import *
from triumphum.layouts import *
from triumphum.internal_shell_class import *
from triumphum.descriptors import addNewGameAfterInterativeDescriptor, addNewGenreAfterInterativeDescriptor, addNewLicenceAfterInterativeDescriptor, addNewPlatformAfterInterativeDescriptor
from triumphum.cli_functions import *
from triumphum.autocomplection import listOfAllGamesCodePerLine, listOfAllLicencesCodePerLine, listOfAllGenresCodePerLine, listOfAllPlatformsCodePerLine
from triumphum.cli_list import printGamesTable, printLicencesTable, printPlatformsTable, printGenresTable
from triumphum.db_edition import addGameToDataBase, addGenreToDataBase, addLicenceToDataBase, addPlatformToDataBase
from triumphum.db_edition import deleteGameFromDatabase, deleteLicenceFromDatabase, deleteGenreFromDatabase, deletePlatformFromDatabase
from triumphum.tui_list import VisualListOfGames
from triumphum.tui_functions import run_command_and_write_on_history
from triumphum.tui_screens import drawAboutScreen
from triumphum.tui import drawListOfGames, drawBothBars, setBottomBarContent

verifyConfigFileExistence()

















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
