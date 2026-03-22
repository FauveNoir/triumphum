########################################################################
# classe des plateformes
########################################################################
import json
from triumphum.global_variables import *
import triumphum.config_file as config_file
import triumphum.symbols as symbols

# défffinition de classe
class Platform:
    def __init__(self, name=None, code=None, abbr=None, includeInSorting=True):
        self.name = name
        self.code = code
        self.abbr = abbr
        self.includeInSorting = includeInSorting

        listOfPlatforms[self.code]=self # Adjonction à la liste des plateformes

    def asciiRow(self):
        # Retourne la cellule particulière pour la construction de la table des jeux
        # Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
        asciiRow = [
            self.name or symbols.GENERAL_VOID_SYMBOL,
            self.abbr or symbols.GENERAL_VOID_SYMBOL,
        ]
        return asciiRow

    # Blocs de comparaisons permétant de trier les plateformes entre elles d’après le paramettre .abbr
    def __eq__(self, other):
        if isinstance(other, Platform):
            return self.abbr == other.abbr
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Platform):
            return self.abbr <  other.abbr
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Platform):
            return self.abbr > other.abbr
        return NotImplemented

def create_platform_objects():
    # Création de la liste des plateformes disponibles

    # Extraction des plateformes
    with open(config_file.PLATFORM_FILE.fullPath()) as f:
        listOfPlatformsData = json.load(f)["platforms"]

    # Déploiment des objet de licence
    for aPlatform in listOfPlatformsData:
        Platform(
            name=aPlatform.get("name"),
            code=aPlatform.get("code"),
            abbr=aPlatform.get("abbr")
        )

# Objet spécifique de plateforme inconue
unknownplatform=Platform(name="Plateforme inconue", code="unknownplatform", abbr="", includeInSorting=False)

def get_platform_object_after_code(code=None):
    # fonction retournant l’objet de plateforme d’après le code fourni en entrée
    # Si rien n’y correspond, retourne l’objet spécial `unknownplatform`
    if code in listOfPlatforms:
        return listOfPlatforms[code]
    return unknownplatform

