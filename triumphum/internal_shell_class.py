########################################################################
# Classe du shell interne
########################################################################

import re

from triumphum.global_variables import *
import triumphum.global_variables as global_variables
from triumphum.descriptors import addNewGameAfterInterativeDescriptor, addNewGenreAfterInterativeDescriptor, addNewLicenceAfterInterativeDescriptor, addNewPlatformAfterInterativeDescriptor
from triumphum.tui_screens import drawAboutScreen
from triumphum.tui import  setBottomBarContent
from triumphum.debug import  * # TODO

### Constructeurs des expressions regex les plus courantes
#

def getPaternToMatchAllCodesInDictionnary(dictionnary):
	# Primitive de construction des regex
	# Prend en entrée une liste de srt et en fait une regex d’alternatives.
	# 
	# Exemple :
	# Input = ["foo", "bar", "baz"]
	# Output = "(foo|bar|baz)"
	patern=""
	for aCode in dictionnary:
		patern=patern+aCode+"|"
	patern="("+patern[:-1]+")"
	return patern

def getPaternToMatchAllLayoutCodes():
	# Returne une chaine de regex d’alternative des codes de dispositions possibles
	# Exemple : "(bepo|azerty|qwerty)"
	patern=getPaternToMatchAllCodesInDictionnary(global_variables.listOfLayouts)
	return patern

def getPaternToMatchAllLicencesCodes():
	# Returne une chaine de regex d’alternative des codes de licences possibles
	# Exemple : "(unknownlicence|gpl|dp|c|mit|apache|bsd"
	patern=getPaternToMatchAllCodesInDictionnary(listOfLicences)
	return patern

#
## Classe des commandes du shell interne
#

class InternalShellCommand:
	# Classe des commandes du shell intrne
	# code : Commande à executer par l’utilisateur (et aussi clé de l’objet au sein de la liste)
	# patern : patern permettant de matcher la commande
	# description : Descrption telle que lisible par l’utilisateur dans les interfaces d’aide
	# options : Alors là, aucune idée, mais probablement prévu en cas d’évolution de commandes prenant des paramettres mais n’éxistant pas dans la version actuelle 2024-10-21
	# synopsis : Description, telle que visible par l’utilisateur dans les documentations et interface d’aide, des différentes varientes d’appel de la commande
	# fulldesc : Description complette et exaustive
	# wrongMatch : Probablement lié à `options` et décrit comment utiliser… non en vrais je sais pas.
	# instructions : Fonction associée à l’execution de la commande
	# activated : Si mis sur False alors la fonction est encore expérimentale et sa mise en œuvre est incomplette
	def __init__(self, code=None, patern=None, description=None, options=None, synopsis=None, fulldesc=None, wrongMatch=None, instructions=None, activated=True):
		self.code=code
		self.patern="^"+patern+"\s*$"
		self.description=description
		self.options=options
		self.synopsis=synopsis
		self.fulldesc=fulldesc
		self.wrongMatch=wrongMatch
		self.activated=activated

		if instructions:
		# Si pas d’instruction car la commande est expérimentale, lui attribuer le comportement idoine avec `unactivatedInternallShellInstruction()`
		# Autrement lui attribuer la fonction donnée en entrée
			if not self.activated:
				setattr(self, 'executeInstructions', unactivatedInternallShellInstruction)
			else:
				setattr(self, 'executeInstructions', instructions)

		ListOfInternalShellCommand[code]=self

	def executeInstructions(self, shellInput):
		# Éxecuter la fonction associée lors de l’appel à la commande
		# /!\ Même si dans la version actuelle aucune commande n’a de fonction utilisant le paramettre `shellInput`, il faut le conserver. Car il servira ultérieurement à parser les paramettres des commandes qui en auront.
		setBottomBarContent(self.description)

#
## Fonctinos générales liées au shell interne
#

def unactivatedInternallShellInstruction():
	# Que faire lorsque la fonction éxiste mais n’est pas encore implémentée
	setBottomBarContent("Fonction non implémentée dans la version actuelle")

def whatTodoWhenShellInputIsWrong(shellInput):
	# Que faire lorsque la fonction  n’éxiste pas du tout
	setBottomBarContent(f"La commande « {shellInput} » est invalide.")


def whatToDoWithShellInput(shellInput):
	# Traitement de la saisie du shell
	writeInTmp(shellInput)
	isShellInputValid=False
	for anInternalCommand in ListOfInternalShellCommand:
	# Recherche une correpsondance eventuelle de la saisie du shell avec un patern valide
		match = re.match(ListOfInternalShellCommand[anInternalCommand].patern, shellInput)
		writeInTmp(ListOfInternalShellCommand[anInternalCommand].patern)
		writeInTmp(getPaternToMatchAllLayoutCodes())
		if match:
			# Si le paterne est trouvé, alors execute la commande associée
			isShellInputValid=True
			ListOfInternalShellCommand[anInternalCommand].executeInstructions(shellInput)

	if isShellInputValid == False:
		# Si le paterne n’est pas trouvé, alors renvoit le message d’erreur
		whatTodoWhenShellInputIsWrong(shellInput)

########################################################################
# Fonctions du shell interne
########################################################################

addNewGamepatern='(a|add|addgame)\s+.*'

def internalShelldrawAboutScreen(shellInput):
	drawAboutScreen()

def internalShellbindMakeDonationFunction(shellInput):
	from triumphum.keybindings import bindMakeDonationFunction
	bindMakeDonationFunction()

def internalShellLayoutFunction(shellInput):
	# TODO utiliser la fonction factorisée
	matchedInput=re.match("(l|layout)\s+(?P<relevant>[a-z]+)", shellInput)
	askedLayout=matchedInput.group("relevant")
	if askedLayout in global_variables.listOfLayouts:
		global_variables.listOfLayouts[askedLayout].apply()
		setBottomBarContent(f"{global_variables.listOfLayouts[askedLayout].fancyName}")
	else:
		setBottomBarContent(f"Disposition « {askedLayout} » inconue")

def setInternalShellCommands():
	InternalShellCommand(code="addNewGame", patern=addNewGamepatern, description="Ajouter un nouveau jeu à la base de donnée", synopsis=":a :add :addgame name=<Game name> code=<code> [genre=<genre>] [licence=getPaternToMatchAllLicencesCodes()]", instructions=addNewGameAfterInterativeDescriptor)
	InternalShellCommand(code="about", patern='about', description="À propos", synopsis=":about", instructions=internalShelldrawAboutScreen)

	InternalShellCommand(code="donate", patern='(d|don|donate)', description="Faire un don", synopsis=":d :don :donate", instructions=internalShellbindMakeDonationFunction)
	writeInTmp("internalshelcalss")
	writeInTmp(getPaternToMatchAllLayoutCodes())
	InternalShellCommand(code="layout", patern=f'(l|layout)\s+(?P<layout>{getPaternToMatchAllLayoutCodes()})', description="Changer de disposition de clavier", synopsis=":l :layout <layout>", instructions=internalShellLayoutFunction)
	InternalShellCommand(code="comment", patern='(c|comment)', description="Ajouter un commentaire", synopsis=":c :comment", activated=False)
	InternalShellCommand(code="viewComment", patern='(v|view)', description="Voir les commentaires", synopsis=":v :vew", activated=False)
