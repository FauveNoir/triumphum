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
    # Traitement des paramettre d’appel en ligne de commande

    if args.config_file != None:
        # Cas d’appel avec un fichier de configuration explicite
        config_file.CONFIG_FILE.setNew(args.config_file)


    # Bloc de génération des racourcis clavier et des symboles graphiques
    applyFileConfigurationsBindings()
    applyFileConfigurationsGraphicalSymbols()

    # Fichiers de configuration
    if args.games_file:
        # Base de données des jeux
        config_file.GAME_FILE.setNew(args.games_file)
    if args.genres_file:
        # Base de données des genres
        config_file.GENRE_FILE.setNew(args.genres_file)
    if args.licences_file:
        # Base de données des licences
        config_file.LICENCE_FILE.setNew(args.licences_file)
    if args.platforms_file:
        # Base de données des plateformes
        config_file.PLATFORM_FILE.setNew(args.platforms_file)

    if  args.verbose == True:
        # Cas dappel avec le paramettre verbose
        print(f"Fichier de configuration principal : {config_file.CONFIG_FILE}")
        print(f"Fichier des jeux : {config_file.GAME_FILE}")
        print(f"Fichier des genres de jeux : {config_file.GENRE_FILE}")
        print(f"Fichier des licences : {config_file.LICENCE_FILE}")
        print(f"Fichier des plateformes : {config_file.PLATFORM_FILE}")

    # Section des adjonctions
    if args.newGameDescriptor :
        # Adjonction de jeux
        addNewGameAfterInterativeDescriptor(descriptor=args.newGameDescriptor, isSplited=True, shouldCreateTheLauncher=args.shouldCreateTheLauncher)
    elif args.newGenreDescriptor :
        # Adjonction de genres
        addNewGenreAfterInterativeDescriptor(args.newGenreDescriptor, True)
    elif args.newLicenceDescriptor :
        # Adjonction de licences
        addNewLicenceAfterInterativeDescriptor(args.newLicenceDescriptor, True)
    elif args.newPlatformDescriptor :
        # Adjonction de plateformes
        addNewPlatformAfterInterativeDescriptor(args.newPlatformDescriptor, True)

    # Parametres de l’autocompletion
    elif args.autocompletionGame:
        # Génération de l’autocmpletion pour les jeux disponibles
        print(listOfAllGamesCodePerLine())
    elif args.autocompletionGenre :
        # Génération de l’autocmpletion pour les genres disponibles
        print(listOfAllGenresCodePerLine())
    elif args.autocompletionLicence :
        # Génération de l’autocmpletion pour les licences disponibles
        print(listOfAllLicencesCodePerLine())
    elif args.autocompletionPlatform :
        # Génération de l’autocmpletion pour les plateformes disponibles
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

    # Autres fonctions autonomes. C’est à dire n’étant pas sensées être combinables avec d’autres paramettres.
    elif  args.about == True:
        print(APP_FANCY_NAME + " " + APP_VERSION + " " + APP_DESCRIPTION)

    elif args.donate == True:
        print(f"Pour soutenir {APP_FANCY_NAME} et faire en sorte qu’il continue et s’améliore, merci de faire un don à <{APP_AUTHOR_DONATION_LINK}>. (^.^)")
        webbrowser.open(APP_AUTHOR_DONATION_LINK)

    elif args.regenerate_launcher:
        # Cas de la regénération des lanceurs d’un jeu spécifique
        try:
            theGame=listOfGames[args.regenerate_launcher]
            theGame.create_launcher()
        except:
            print(f"Aucun jeu ne correspond à l’identifiant « {args.regenerate_launcher} »")

    elif args.regenerate_all_launcher:
        # Cas de la regénération des lanceurs de tous les jeux
        for aGameCode in listOfGames:
            listOfGames[aGameCode].create_launcher()

    elif args.tui == True:
        # cas (défaut) de lancement de la TUI pour la liste visuelle des jeux.
        if args.layout:
            layout=global_variables.listOfLayouts[args.layout]
            layout.apply()
        printSplash()
        runTui()
