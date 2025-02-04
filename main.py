#!/usr/bin/python3

from triumphum.config_file import prepareConfigFiles, verifyConfigFileExistence
import triumphum.config_file as config_file
import triumphum.global_variables as global_variables
from triumphum.keybindings import declareBindings
import triumphum.layouts
from triumphum.cli_options import args
from triumphum.tui_list import VisualListOfGames
from triumphum.run import processArgs


def main():

	declareBindings()
	#makeLayoutsList()

	# /!\ Il est imporatnt que prepareConfigFiles() soit éxecutée après les déclarations de bindings car elle en a besoin pour générer les bindings par défaut.
	prepareConfigFiles()
	verifyConfigFileExistence()

	# /!\ Il est imporatnt que VisualListOfGames() vienne après prepareConfigFiles() car ce dernier décalre des variables globales dont VisualListOfGames() a besoin
	VisualListOfGames()

	processArgs(args)


main()
