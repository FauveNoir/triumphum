import argparse
import sys
from triumphum.__init__ import *

########################################################################
# Options de la ligne de commande
########################################################################

# Déploiment du parsseur pour les optinos de la ligne de commande
parser = argparse.ArgumentParser(prog=APP_CODE_NAME, description=APP_FANCY_NAME + " " + APP_VERSION + " " + APP_DESCRIPTION)

# 1. Groupe du comportement de l’interface
interfaceBehaviour = parser.add_argument_group('Interface behaviour')
interfaceBehaviourGroup = interfaceBehaviour.add_mutually_exclusive_group() # Rend les arguments du groupe mutuellement exlusifs

interfaceBehaviourGroup.add_argument("--tui", action="store_true", default = True, help = "Run the game selection interface (default).")
run_command=interfaceBehaviourGroup.add_argument("-r", "--run", metavar="GAME", help = "Run a given game and track playing time.")

# 1. Groupe des arguments généraux
generalArgument = parser.add_argument_group('General arguments')
generalArgument.add_argument("-a", "--about", action="store_true", help = "Show about message.")
generalArgument.add_argument("-v", "--verbose", action="store_true", help = "Show debug inromations.")
generalArgument.add_argument("-d", "--donate", action="store_true", help = "Open link to give a tip.")
generalArgument.add_argument("--no-splash", action="store_true", help = "Do not show splash at opening.")
generalArgument.add_argument("--list-games", action="store_true", help = "Afficher la liste des jeux.")
generalArgument.add_argument("--list-licences", action="store_true", help = "Afficher la liste des licences.")
generalArgument.add_argument("--list-genres", action="store_true", help = "Afficher la liste des genres de jeu.")
generalArgument.add_argument("--list-platforms", action="store_true", help = "Afficher la liste des genres des plateformes.")

# 2. Groupe des fichiers de configuration
configurationFile = parser.add_argument_group('Configuration file')
configurationFile.add_argument("-c", "--config-file", help = "Select different config file from default one.")
configurationFile.add_argument("-g", "--games", dest="games_file", metavar="FILE", help = "Select different game file from default one.")
configurationFile.add_argument("-p", "--platforms", dest="platforms_file", metavar="FILE", help = "Select different platform file from default one.")
configurationFile.add_argument("-l", "--licences", dest="licences_file", metavar="FILE", help = "Select different licence file from default one.")
configurationFile.add_argument("-t", "--genres", dest="genres_file", metavar="FILE", help = "Select different game genre file from default one.")
configurationFile.add_argument("--layout", dest="layout", action="store", help = f"Utiliser des raccourcis dactyliques adaptés à la disposition de clavier.")

# 2. Groupe de l’insertion de donnée
addingData = parser.add_argument_group('Adding data')
addingDataGroup = addingData.add_mutually_exclusive_group()
addingDataGroup.add_argument("--add-game", dest="newGameDescriptor", metavar="GAME_DESCRIPTOR", nargs='*', help = "Ajouter un nouveau jeu.")

addingDataGroup.add_argument("--add-licence", dest="newLicenceDescriptor", metavar="LICENCE", nargs='*', help = "Ajouter une nouvelle licence.")
addingDataGroup.add_argument("--add-genre", dest="newGenreDescriptor", nargs='*', metavar="GENRE", help = "Ajouter un nouveau genre de jeu.")
addingDataGroup.add_argument("--add-platform", dest="newPlatformDescriptor", nargs='*', metavar="PLATFORM", help = "Ajouter une nouvelle plateforme.")

# 3. Gestion du lanceur de jeux avec traqeur
trakerLauncher = parser.add_argument_group('Game launcher with traking')
trakerLauncherGroup = trakerLauncher.add_mutually_exclusive_group()
trakerLauncherGroup.add_argument("--create-launcher", action="store_true", default=None, dest="shouldCreateTheLauncher", help = "Créer le lanceur de jeu avec le traqueur de pérformances. (Défaut)")
trakerLauncherGroup.add_argument("--no-create-launcher",  action="store_false", default=None, dest="shouldCreateTheLauncher", help = "Créer le lanceur de jeu sans le traqueur de pérformances.")
trakerLauncherGroup.add_argument("--regenerate-launcher", metavar="GAME", action="store", help = "Regénérer le lanceur avec traqeur de performances de GAME.")
trakerLauncherGroup.add_argument("--regenerate-all-launcher", action="store_true", help = "Regénérer le lanceur avec traqeur de performances pour tous les jeux.")

# 2. Groupe de la délétion de donnée
deletingData = parser.add_argument_group('Deleting data')
deletingDataGroup = deletingData.add_mutually_exclusive_group()
deletingDataGroup.add_argument("--del-game", dest="delGame", metavar="GAME", help = "Suprimer un jeu.")
deletingDataGroup.add_argument("--del-licence", dest="delLicence", metavar="LICENCE", help = "Suprimer une licence.")
deletingDataGroup.add_argument("--del-genre", dest="delGenre", metavar="GENRE", help = "Suprimer un genre de jeu.")
deletingDataGroup.add_argument("--del-platform", dest="delPlatform", metavar="PLATFORM", help = "Suprimer une plateforme.")

# 2. Groupe de la génération d’autocomplexion
autocompletionFunctions = parser.add_argument_group('For autocomplexion only')
autocompletionFunctionsGroup = autocompletionFunctions.add_mutually_exclusive_group()
autocompletionFunctionsGroup.add_argument("--ag", action="store_true",  dest="autocompletionGame", help = "Lister les codes des jeux")
autocompletionFunctionsGroup.add_argument("--al", action="store_true",  dest="autocompletionLicence", help = "Lister les codes des licences.")
autocompletionFunctionsGroup.add_argument("--at", action="store_true",  dest="autocompletionGenre", help = "Lister les codes des genres de jeu.")
autocompletionFunctionsGroup.add_argument("--ap", action="store_true",  dest="autocompletionPlatform", help = "Lister les codes des plateformes.")

########################################################################
# Éléments à exporter
########################################################################
# Execution du pareur
args = parser.parse_args()

if args.newGameDescriptor == None:
    if args.shouldCreateTheLauncher == True:
        print("L’argument --create-launcher ne peut être appellé sans --new-game")
        sys.exit()
    elif args.shouldCreateTheLauncher == False:
        print("L’argument --no-create-launcher ne peut être appellé sans --new-game")
        sys.exit()
else:
    if args.shouldCreateTheLauncher == None:
        args.shouldCreateTheLauncher = True


