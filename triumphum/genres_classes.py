########################################################################
# Classe des genres de jeux
########################################################################
import json
from triumphum.global_variables import *
import triumphum.config_file as config_file
from triumphum.symbols import *


# Défffinition de classe
class Genre:
    def __init__(self, name=None, code=None, abbr=None, includeInSorting=True):
        self.name = name
        self.code = code
        self.abbr = abbr
        self.includeInSorting = includeInSorting

        listOfGenres[self.code]=self # Adjonction à la liste des genres de jeux

    def shortName(self):
        # Recherche d’un nom abbrégé si il existe. Sinon renvoit le nom complet
        if self.abbr != None:
            return self.abbr
        return self.name

    # Méthodes de comparaison entre deux variables de type Genre
    # Particulièrement utile dans le tri de colones.
    # Permet de comparer deux genre d’après l’ordre alphabétique du nom abrégé des genres.
    def __eq__(self, other):
        if isinstance(other, Genre):
            return self.abbr == other.abbr
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Genre):
            return self.abbr <  other.abbr
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Genre):
            return self.abbr > other.abbr
        return NotImplemented

    def makeFlatData(self):
        # Retourne un dictionnaire descriptif du jeu
        flatData={
            "name":self.name,
            "code":self.code,
            "abbr":self.abbr
        }
        return flatData

    def asciiRow(self):
        # Préparation de la ligne de tableau

        # Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
        asciiRow = [
            self.name or GENERAL_VOID_SYMBOL,
            self.abbr or GENERAL_VOID_SYMBOL,
        ]
        return asciiRow

def create_game_genre_objects():
    # Extraction des genres de jeux

    # Réinitialisation de la liste des jeux
    listOfGenres={}

    # Extraction des genres de jeux du fichier
    with open(config_file.GENRE_FILE.fullPath()) as f:
        listOfGenresData = json.load(f)["genres"]

    # Déploiment des objet de genre de jeux
    for aGenre in listOfGenresData:
        Genre(
            name=aGenre.get("name"),
            code=aGenre.get("code"),
            abbr=aGenre.get("abbr")
        )

# Déclaration de la variable de genre inconnu
unknowngenre=Genre(name="Genre inconu", abbr=GENRE_VOID_SYMBOL.value, code="unknowngenre", includeInSorting=False)

def get_genre_object_after_code(code):
    # Obtenir la variable d’un Genre en fonction de son code
    if code in listOfGenres:
        return listOfGenres[code]
    return unknowngenre
