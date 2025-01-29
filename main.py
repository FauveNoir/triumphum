#!/usr/bin/python3

#from triumphum.__init__ import *
#from triumphum.global_variables import *
#import triumphum.global_variables as global_variables
#from triumphum.symbols import *
#from triumphum.layouts import *
#from triumphum.internal_shell_class import *
#from triumphum.cli_functions import *
#from triumphum.db_edition import addGameToDataBase, addGenreToDataBase, addLicenceToDataBase, addPlatformToDataBase
#from triumphum.tui_functions import run_command_and_write_on_history
#from triumphum.tui_screens import drawAboutScreen
#from triumphum.tui import drawListOfGames, drawBothBars, setBottomBarContent

from triumphum.config_file import prepareConfigFiles, verifyConfigFileExistence
import triumphum.config_file as config_file
from triumphum.cli_options import args
from triumphum.tui_list import VisualListOfGames
from triumphum.run import processArgs

verifyConfigFileExistence()
# /!\ Il est imporatnt que prepareConfigFiles() soit éxecutée après les déclarations de bindings car elle en a besoin pour générer les bindings par défaut.
prepareConfigFiles()

# /!\ Il est imporatnt que VisualListOfGames() vienne après prepareConfigFiles() car ce dernier décalre des variables globales dont VisualListOfGames() a besoin
VisualListOfGames()

processArgs(args)
