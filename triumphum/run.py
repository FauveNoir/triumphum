########################################################################
# Que faire
########################################################################
import threading
import webbrowser

from triumphum.__init__ import *
from triumphum.global_variables import *
import triumphum.global_variables as global_variables
import triumphum.config_file as config_file
from triumphum.cli_functions import *

from triumphum.config_file import  applyFileConfigurationsBindings, applyFileConfigurationsGraphicalSymbols
from triumphum.descriptors import addNewGameAfterInterativeDescriptor, addNewGenreAfterInterativeDescriptor, addNewLicenceAfterInterativeDescriptor, addNewPlatformAfterInterativeDescriptor
from triumphum.autocomplection import listOfAllGamesCodePerLine, listOfAllLicencesCodePerLine, listOfAllGenresCodePerLine, listOfAllPlatformsCodePerLine
from triumphum.db_edition import deleteGameFromDatabase, deleteLicenceFromDatabase, deleteGenreFromDatabase, deletePlatformFromDatabase
from triumphum.tui import runTui
from triumphum.tui_functions import run_command_and_write_on_history

from triumphum.debug import * # TODO

def processArgs(args):
    if args.config_file != None:
        config_file.CONFIG_FILE.setNew(args.config_file)


    applyFileConfigurationsBindings()
    applyFileConfigurationsGraphicalSymbols()

    # Fichiers de configuration
    if args.games_file:
        config_file.GAME_FILE.setNew(args.games_file)
    if args.genres_file:
        config_file.GENRE_FILE.setNew(args.genres_file)
    if args.licences_file:
        config_file.LICENCE_FILE.setNew(args.licences_file)
    if args.platforms_file:
        config_file.PLATFORM_FILE.setNew(args.platforms_file)

    if  args.verbose == True:
        print(f"Fichier de configuration principal : {config_file.CONFIG_FILE}")
        print(f"Fichier des jeux : {config_file.GAME_FILE}")
        print(f"Fichier des genres de jeux : {config_file.GENRE_FILE}")
        print(f"Fichier des licences : {config_file.LICENCE_FILE}")
        print(f"Fichier des plateformes : {config_file.PLATFORM_FILE}")

    # Configuration


    # Section des adjonctions
    if args.newGameDescriptor :
        addNewGameAfterInterativeDescriptor(descriptor=args.newGameDescriptor, isSplited=True, shouldCreateTheLauncher=args.shouldCreateTheLauncher)
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
        deleteGameFromDatabase(args.delGame)
    elif args.delLicence:
        deleteLicenceFromDatabase(args.delLicence)
    elif args.delGenre:
        deleteGenreFromDatabase(args.delGenre)
    elif args.delPlatform:
        deletePlatformFromDatabase(args.delPlatform)

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

    elif args.regenerate_launcher:
        try:
            theGame=listOfGames[args.regenerate_launcher]
            theGame.create_launcher()
        except:
            print(f"Aucun jeu ne correspond à l’identifiant « {args.regenerate_launcher} »")

    elif args.regenerate_all_launcher:
        for aGameCode in listOfGames:
            listOfGames[aGameCode].create_launcher()

    elif args.tui == True:
        if args.layout:
            layout=global_variables.listOfLayouts[args.layout]
            layout.apply()
        printSplash()
        runTui()
