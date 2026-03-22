
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
