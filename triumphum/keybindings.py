########################################################################
# Classe des racoucris dactyliques
########################################################################

from triumphum.global_variables import listOfBindings
import triumphum.global_variables as global_variables
from triumphum.debug import * # TODO

#
## Diverses fonctions utiles à la gestion des racourcis dactyliques
#

def getElementHavingParameterWithValue(givenList=None, parameter=None, value=None):
	# Parcourt la liste `givenList` pour y trouver un élément ayant un paramettre nomé `parameter` et ayant pour valeur `value`.
	if parameter is None or value is None:
		return None

	for anElement in givenList:
		if hasattr(anElement, parameter) and getattr(anElement, parameter) == value:
				return anElement
	return None

def getListOfAParametterFromAListOfObjects(givenList=None, parameter=None):
	if parameter is None or parameter is None:
		return None

	outputList=[]
	for anElement in givenList:
		outputList.append(getattr(anElement, parameter))
	return outputList

# Cas particuliers des mapings où le keycode ne correspond pas au symbole produit.
KEY_MAPPING = {
	# label, caractère
	"Enter": "\n",
	"Return": "\r",
	"Space": " ",
}

def reverseDictionnary(dictionnary):
	# Inverse les clés et valeurs du dictionnaire
	return {v: k for k, v in dictionnary.items()}

def transformKeyToCharacter(key_name):
	# Transformee les codes lisibles en caractères
	return KEY_MAPPING.get(key_name, key_name)

def transform_character_to_key(character_name):
	# Transformes les caractères reçus au claviers en labels lisibles
	reverseKeyMapping=reverseDictionnary(KEY_MAPPING)
	return reverseKeyMapping.get(character_name, character_name)

########################################################################

class Binding:
	# Classe des racourcis dactyliques.
	# key : touche associée
	# code : nom de la variable de l’objet créé
	# description : Description de l’usage tel qu’elle apparaitra à l’utilisateur dans les interfaces d’aide
	# configFileName : Nom de la fonction à utiliser par le fichier de configuration. Par défaut c’est code qui est utilisé afin de maintenir la plus grande homogénéité entre le code python et le fichier de configuration.
	#                 /!\ Ne déclarer éxplicitement une valeur pour `configFileName` que s’il éxiste une raison valable.
	# instructions : Nom de la fonction à déclencher lors de la pression sur le binding.
	def __init__(self, key=None, code=None, description=None, configFileName=None, instructions=None):
		self.key = None
		self.setKey(key)
		self.description = description
		self.code = code

		if configFileName == None:
			self.configFileName = self.code
		else:
			self.configFileName = configFileName
		globals()[code] = self # Déclaration de la variable globale pérmétant d’atteindre directement le genre voulu

		if instructions:
			setattr(self, 'executeInstructions', instructions)

		listOfBindings.append(self) # Adjonction à la liste des genres de jeux

	def setKey(self, key):
		# Transforme les codes lisibles en caractères
		self.key = transformKeyToCharacter(key)

	def executeInstructions(self):
		# Éxectue la fontion associée au binding
		setBottomBarContent(f"{self.key} : Aucune action associée.")

	def makeDefaultConfigEntry(self):
		# Renvoit la ligne de fichier de configuration apropriée
		configEntry=self.configFileName + "=" + transform_character_to_key(self.key)
		return configEntry

########################################################################

#
## Fonctions dédiées aux actions des caractères dactyliques
#

def bindGoDownFunction():
	# Focale sur l’élément suivant de la liste visuelle
	global_variables.THE_VISUAL_LIST_OF_GAMES.goDown()

def bindGoUpFunction():
	# Focale sur l’élément précédent de la liste visuelle
	global_variables.THE_VISUAL_LIST_OF_GAMES.goUp()

def bindSortByNameFunction():
	# Trie la liste par ordre alphabétique
	global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("name")
	setBottomBarContent(f"Tri par ordre alphabétique.")

def bindSortByLicenceFunction():
	# Trie la liste par coeficient de liberté des licences
	global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("licence")
	setBottomBarContent(f"Tri par permissivité des licences.")

def bindSortByGenreFunction():
	# Trie la liste par genre
	global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("genre")
	setBottomBarContent(f"Tri par genre de jeu.")

def bindSortByDateFunction():
	# Trie la liste par genre
	global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("year")
	setBottomBarContent(f"Tri par année de sortie.")

def bindSortByLastOpeningFunction():
	# Trie la liste par date de dernière ouverture
	global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("latest_opening_date_value")
	setBottomBarContent(f"Tri par date de dernière ouverture.")

def bindSortByPlayingDurationFunction():
	# Trie la liste par dérée de jeu cumulée
	global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("playing_duration")
	setBottomBarContent(f"Tri par durée de jeu cumulée.")

def bindSortByPlatformFunction():
	# Trie la liste par plateforme
	global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("platform")
	setBottomBarContent(f"Tri par plateforme.")

def bindRunGameFunction():
	# Execute la commande associée à l’item ayant le focus
	global_variables.THE_VISUAL_LIST_OF_GAMES.openCurrent()

def bindDeleteGameFunction():
	# Suprime le jeu ayant le focus
	currentGame=global_variables.THE_VISUAL_LIST_OF_GAMES.currentGame().name
	if questionMode(f"Supprimer « {currentGame} » ?"):
		global_variables.THE_VISUAL_LIST_OF_GAMES.deleteCurrent()
	else:
		setBottomBarContent(f"« {currentGame} est conservé. Rien n’est altéré.")

def bindOpenLinkFunction():
	# Ouvrir le lien associé à l’item ayant le focus
	global_variables.THE_VISUAL_LIST_OF_GAMES.openLink()

def bindCopyLinkFunction():
	# Copier le lien associé à l’item ayant le focus dans le presse papier
	global_variables.THE_VISUAL_LIST_OF_GAMES.copyLinkToClipBoard()

def bindMakeDonationFunction():
	# Ouvrir le lien pour faire un don
	setBottomBarContent(f"Merci de me faire un don sur « {APP_AUTHOR_DONATION_LINK} » (^.^)")
	threading.Thread(target=webbrowser.open, args=(APP_AUTHOR_DONATION_LINK,)).start()

def bindRefreshScreenFunction():
	# Rafraichir la vue
	global_variables.THE_VISUAL_LIST_OF_GAMES.refresh()
