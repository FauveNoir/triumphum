########################################################################
# Classe des symbols graphiques
########################################################################

from triumphum.global_variables import listOfGraphicalSymbols

## Explication
# Les symboles graphiques sont l’ensemble des éléments d’interface qui se présente sous la forme d’ùn caractère typographique, comme les lignes permettant de dessiner les boites, ou encore les symboles ayant un rôle presque pictographique.

class GraphicalSymbol:
	# Classe des symboles graphiques, qui crée les variables globales désignants les dits symbols
	def __init__(self, localName=None, fileConfigName=None, description=None, value=None):
		self.localName=localName # Nom sous lequel sera désignée la variable du fichier dans le code python

		# Bloc attribuant un nom identitique ou différent à localName
		# TODO semblant innutile, penser à le suprimer
		if fileConfigName == None:  
			self.fileConfigName=self.localName.lower()
		else:
			self.fileConfigName=fileConfigName
		self.description=description # Description, notement utile pour lesinterfaces d’aide
		self.value=value # Le symbole à proprement parler

		# Versement de l’objet à la liste de tous les objets du même type
		listOfGraphicalSymbols.append(self)
		globals()[localName] = self # Déclaration de la variable globale pérmétant d’atteindre directement le genre voulu

	def __str__(self):
		# Lorsque transformé en chaine, l’objet renvoit sa valeur à prement parler
		return self.value

	def __add__(self, other):
		# S’il doit être sommé à un autre objet de type char, alors l’objet renvoit sa .value à preprement parler.
		if isinstance(other, str):
			return str(self) + other
		else:
			return NotImplemented

#
## Déclaration des symboles graphiques
#

### Symboles de déclaration d’asbcence de donnée
GraphicalSymbol(localName="GENERAL_VOID_SYMBOL", value="-", description="Symbole d’absecnce de donnée par défaut")

GraphicalSymbol(localName="NAME_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL.value, description="Symbole d’abscence de nom connu")
GraphicalSymbol(localName="LICENCE_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL.value, description="Symbole d’abscence de licence connue")
GraphicalSymbol(localName="GENRE_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL.value, description="Symbole d’abscence de genre connu")
GraphicalSymbol(localName="DATE_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL.value, description="Symbole d’abscence de date connue")
GraphicalSymbol(localName="LASTOPENING_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL.value, description="Symbole d’abscence de date de dernière ouverture connue")
GraphicalSymbol(localName="CUMULATEDTIME_VOID_SYMBOL", value="0", description="Symbole d’abscence de temps de jeu connu")
GraphicalSymbol(localName="AUTHOR_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL.value, description="Symbole d’abscence d’auteur connu")
GraphicalSymbol(localName="STUDIO_VOID_SYMBOL", value=GENERAL_VOID_SYMBOL.value, description="Symbole d’abscence de studio connu")
GraphicalSymbol(localName="PLATFORM_VOID_SYMBOL", value=" ", description="Symbole d’abscence de plateforme connue")

### Symbole de désignation des durées cumulées
GraphicalSymbol(localName="CUMULATED_TIME_PLAYED_PER_DAY", value="D", description="Symbole de temps de jeu cumulé durant la journée")
GraphicalSymbol(localName="CUMULATED_TIME_PLAYED_PER_WEEK", value="W", description="Symbole de temps de jeu cumulé durant la semaine")
GraphicalSymbol(localName="CUMULATED_TIME_PLAYED_PER_MONTH", value="M", description="Symbole de temps de jeu cumulé durant le mois")
GraphicalSymbol(localName="CUMULATED_TIME_PLAYED_PER_YEAR", value="Y", description="Symbole de temps de jeu cumulé durant l’année ")
GraphicalSymbol(localName="CUMULATED_TIME_PLAYED_SEPARATOR", value="│", description="Séparateur des indicateurs de temps de jeu cumulé")
