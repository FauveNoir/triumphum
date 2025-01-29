########################################################################
# Fonctions ésthétiques de l’interface interactive
########################################################################
from triumphum.global_variables import *
import triumphum.global_variables as global_variables

def getColWidths():
	global titles
	global items

	itemsMergedWithTitle = items[:]
	itemsMergedWithTitle.append(titles)
	col_widths = [max(len(str(column)) for column in col) for col in zip(*itemsMergedWithTitle)]

	return col_widths
