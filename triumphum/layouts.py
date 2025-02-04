########################################################################
# Dispositions de clavier
########################################################################

import triumphum.global_variables as global_variables
from triumphum.misc import getElementHavingParameterWithValue
from triumphum.debug import * # TODO

def getListOfAParametterFromAListOfObjects(givenList=None, parameter=None):
	if parameter is None or parameter is None:
		return None

	outputList=[]
	for anElement in givenList:
		outputList.append(getattr(anElement, parameter))
	return outputList


class Layout:
	# Classe des disposition de clavier ayant chacune son propre jeu de binding
	# fancyName : Nom littéral tel qu’il apparaitra à l’utilisateur lorsqu’une représentation linguistique est permise
	# code : code de la disposition qui sert 1. dans la variable locale de l’objet 2. Que l’utilisateur utilesra lors de ses configurations et appels à la ligne de commande
	# **attributs : Autres paramettres sensés être générés d’après la liste des racourcis actyliques disponibles
	def __init__(self, fancyName=None, code=None, **attributs):
		self.fancyName=fancyName
		self.code=code

		# Enregistrer tous les attributs supplémentaires de **attributs comme autant de paramettres
		# TODO limiter les attributs à la liste des racourcis dactyliques disponibles
		for attributName, value in attributs.items():
			setattr(self, attributName, value)

		global_variables.listOfLayouts[self.code]=self

	def apply(self):
	# Appliquer les associations de la disposition et utiliser ses racourcis dactyliques
		for aKey in getListOfAParametterFromAListOfObjects(givenList=global_variables.listOfBindings, parameter="code"):
		# Parcour `listOfBindings` pour ittérer sur chacun des paramettres `.code` des éléments qu’elle contient.
			if hasattr(self, aKey):
				value = getattr(self, aKey)
				# ↓ Récupére le Binding ayant pour `.code` la valeur de `aKey`
				theBinding=getElementHavingParameterWithValue(givenList=global_variables.listOfBindings, parameter="code", value=aKey)
				theBinding.setKey(value)

#
## Déffinition des dispositions disponibles
#

def makeLayoutsList():
	Layout(fancyName="BÉPO", code="bepo",
		bindGoDown="t",
		bindGoUp="s",
		bindRunGame="\n",
		bindSortByName="b",
		bindSortByLicence="é",
		bindSortByGenre="p",
		bindSortByDate="o",
		bindSortByLastOpening="è",
		bindSortByPlayingDuration="v",
		bindSortByPlatform="!",
		bindOpenLink="A",
		bindEditData="e",
	#	bindDelete="d",
		bindComment="i",
		bindMakeDonation="x",
		bindShowFullLicence="w",
		bindFilter="/",
		bindSeeBindingHelp="h",
		bindCopyLink="y",
		bindRefreshScreen="l",
		bindQuit="q"
		)

	Layout(fancyName="AZERTY", code="azerty",
		bindGoDown="j",
		bindGoUp="k",
		bindRunGame="\n",
		bindSortByName="a",
		bindSortByLicence="z",
		bindSortByGenre="e",
		bindSortByDate="r",
		bindSortByLastOpening="t",
		bindSortByPlayingDuration="y",
		bindSortByPlatform="o",
		bindOpenLink="A",
		bindEditData="f",
	#	bindDelete="d",
		bindComment="s",
		bindMakeDonation="c",
		bindShowFullLicence="p",
		bindFilter="/",
		bindSeeBindingHelp="h",
		bindCopyLink="y",
		bindRefreshScreen="l",
		bindQuit="q"
		)

	Layout(fancyName="QWERTY", code="qwerty",
		bindGoDown="j",
		bindGoUp="k",
		bindRunGame="\n",
		bindSortByName="q",
		bindSortByLicence="w",
		bindSortByGenre="e",
		bindSortByDate="r",
		bindSortByLastOpening="t",
		bindSortByPlayingDuration="y",
		bindSortByPlatform="u",
		bindOpenLink="A",
		bindEditData="f",
	#	bindDelete="d",
		bindComment="s",
		bindMakeDonation="c",
		bindShowFullLicence="p",
		bindFilter="/",
		bindSeeBindingHelp="h",
		bindCopyLink="y",
		bindRefreshScreen="l",
		bindQuit="x"
		)
