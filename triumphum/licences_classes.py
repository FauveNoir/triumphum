########################################################################
# Classe des licences de jeux
########################################################################
import json
from triumphum.global_variables import *
import triumphum.config_file as config_file
from triumphum.symbols import *

# Défffinition de classe
class Licence:
    def __init__(self, name=None, abbr=None, code=None, url=None, shortText=None, fullText=None, freedomCoefficient=0, includeInSorting=True):
        self.name = name
        self.abbr = abbr
        self.code = code
        self.url = url
        self.shortText = shortText
        self.fullText = fullText
        self.freedomCoefficient = freedomCoefficient
        self.includeInSorting = includeInSorting

        listOfLicences[self.code]=self # Adjonction à la liste des licences

    # Blocs de comparaisons permétant de trier les licences entre elles de la plus libre à la moins libre
    def __eq__(self, other):
        if isinstance(other, Licence):
            return self.freedomCoefficient == other.freedomCoefficient
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Licence):
            return self.freedomCoefficient <  other.freedomCoefficient
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Licence):
            return self.freedomCoefficient <= other.freedomCoefficient
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Licence):
            return self.freedomCoefficient >  other.freedomCoefficient
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Licence):
            return self.freedomCoefficient >= other.freedomCoefficient
        return NotImplemented
    def asciiRow(self):
        # Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
        asciiRow = [
            self.name or GENERAL_VOID_SYMBOL,
            self.url or GENERAL_VOID_SYMBOL,
            self.freedomCoefficient or GENERAL_VOID_SYMBOL,
        ]
        return asciiRow

def create_licence_objects():
    # Fonction d’extraction depuis les fichiers des licences définies et déploiement

    # Extraction des licences
    with open(config_file.LICENCE_FILE.fullPath()) as f:
        listOfLicencesData = json.load(f)["licences"]

    # Déploiment des objet de licence
    for aLicence in listOfLicencesData:
        Licence(
            name=aLicence.get("name"),
            code=aLicence.get("code"),
            abbr=aLicence.get("abbr"),
            url=aLicence.get("url"),
            shortText=aLicence.get("shortText"),
            freedomCoefficient=aLicence.get("freedomCoefficient") or 0
        )

# Objet spécifique de licence inconue
unknownlicence=Licence(name="Licence inconue", abbr=LICENCE_VOID_SYMBOL.value, code="unknownlicence", includeInSorting=False)

def get_licence_object_after_code(code=None):
    # fonction retournant l’objet de licence d’après le code fourni en entrée
    # Si rien n’y correspond, retourne l’objet spécial `unknownlicence`
    if code in listOfLicences:
        return listOfLicences[code]
    return unknownlicence
