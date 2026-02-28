########################################################################
# Fonctions des descripteurs
########################################################################
import re
import shlex

from triumphum.db_edition import addGameToDataBase, addGenreToDataBase, addLicenceToDataBase, addPlatformToDataBase
from triumphum.debug import *
from triumphum.global_variables import *
from triumphum.games_classes import  create_game_objects

#
# Classe
#

class promptStatement:
    def __init__(self, name=None, patern=None, isNecessary=False, isLabelNecessary=True, multipleValues=False):
        self.name=name
        self.patern=f"{name}=(?P<relevant>{patern})"
        if isNecessary:
            self.patern=f"(?P<relevant>{patern})"
        self.isNecessary=isNecessary
        self.isLabelNecessary=isLabelNecessary
        self.multipleValues=multipleValues

    def add_to_dict(self, dictionary):
        dictionary[self.name] = self

    def getRelevant(self, inputStatement):
        match = re.match(self.patern, anInputStatement)
        if self.multipleValues:
            return match.group("relevant").split(',')
        return match.group("relevant")

#
# Shémats
#

ADD_GAME_STATEMENTS={
    "name": promptStatement(name="name", patern=".*", isNecessary=True, isLabelNecessary=False),
    "code": promptStatement(name="code", patern="[a-z0-9]*", isNecessary=True),
    "genre": promptStatement(name="genre", patern="[a-z0-9]*"),
    "licence": promptStatement(name="licence", patern="[a-z0-9]*"),
    "command": promptStatement(name="command", patern='.*'),
    "url": promptStatement(name="url", patern="\S+"),
    "studios": promptStatement(name="studios", patern=".*", multipleValues=True),
    "authors": promptStatement(name="authors", patern=".*", multipleValues=True),
    "shortDesc":promptStatement(name="shortDesc", patern=".*"),
    "year":promptStatement(name="year", patern="[0-9]*"),
}
# TODO YEAR


ADD_GENRE_STATEMENTS={
    "name": promptStatement(name="name", patern=".*", isNecessary=True, isLabelNecessary=False),
    "code": promptStatement(name="code", patern="[a-z0-9]*", isNecessary=True),
    "abbr": promptStatement(name="abbr", patern="[a-z0-9]*"),
}

ADD_PLATFORM_STATEMENTS={
    "name": promptStatement(name="name", patern=".*", isNecessary=True, isLabelNecessary=False),
    "code": promptStatement(name="code", patern="[a-z0-9]*", isNecessary=True),
    "abbr": promptStatement(name="abbr", patern="[a-z0-9]*"),
}

ADD_LICENCE_STATEMENTS={
    "name": promptStatement(name="name", patern=".*", isNecessary=True, isLabelNecessary=False),
    "code": promptStatement(name="code", patern="[a-z0-9]*", isNecessary=True),
    "abbr": promptStatement(name="abbr", patern="[a-z0-9]*"),
    "url": promptStatement(name="url", patern="\S+"),
    "freedomCoefficient": promptStatement(name="freedomCoefficient", patern="(0(\.\d*)?|1(\.0*)?|\.\d+)"),
    "shortDesc":promptStatement(name="shortDesc", patern=".*"),
}

#
# Fonctions
#

def splitDescriptorIntoList(inputChain):
    objectDescriptorList=shlex.split(inputChain)
    return objectDescriptorList

def sanitizeDescriptorListFromKeysWithoutValues(inputChain):
    # Expurger le descripteur des clés n’étant associées à aucune valeur
    sanitizedObjectDescriptorList=[]
    wrongStatements=[]
    for aStatement in inputChain:
        if "=" in aStatement:
            sanitizedObjectDescriptorList.append(aStatement)
        else:
            wrongStatements.append(aStatement)
    return sanitizedObjectDescriptorList, wrongStatements

def descriptorIntoDict(inputChain):
    dictConfig={}
    for aStatement in inputChain:
        statementName, statementValue = aStatement.split("=")
        dictConfig[statementName] = statementValue

    return dictConfig

def canonicalizeDescriptorChain(inputChain, objectSchema):
    outputChain={}
    for aStatementName, aStatementValue in inputChain.items():
        if aStatementName in objectSchema:
            if objectSchema[aStatementName].multipleValues:
                outputChain[aStatementName] = aStatementValue.split(",")
            else:
                outputChain[aStatementName] = aStatementValue
    return outputChain

def interactiveDescriptorIntoDictionnary(newObjectDescriptor, objectSchema, isSplited=False):
    if not isSplited:
        outputChain=splitDescriptorIntoList(newObjectDescriptor)
    else:
        outputChain=newObjectDescriptor
    outputChain, wrongStatements=sanitizeDescriptorListFromKeysWithoutValues(outputChain)
    outputChain=descriptorIntoDict(outputChain)
    outputChain=canonicalizeDescriptorChain(outputChain, objectSchema)
    return outputChain

#
# Fonctions par objet
#

def addNewGameAfterInterativeDescriptor(descriptor=None, isSplited=False, shouldCreateTheLauncher=None):
    dictionnaryDescriptor=interactiveDescriptorIntoDictionnary(descriptor, ADD_GAME_STATEMENTS, isSplited)
    if addGameToDataBase(dictionnaryDescriptor):
        create_game_objects()
        if shouldCreateTheLauncher:
            listOfGames[dictionnaryDescriptor['code']].create_launcher()

def addNewGenreAfterInterativeDescriptor(newGenreDescriptor, isSplited=False):
    dictionnaryDescriptor=interactiveDescriptorIntoDictionnary(newGenreDescriptor, ADD_GENRE_STATEMENTS, isSplited)
    addGenreToDataBase(dictionnaryDescriptor)

def addNewLicenceAfterInterativeDescriptor(newLicenceDescriptor, isSplited=False):
    dictionnaryDescriptor=interactiveDescriptorIntoDictionnary(newLicenceDescriptor, ADD_LICENCE_STATEMENTS, isSplited)
    addLicenceToDataBase(dictionnaryDescriptor)

def addNewPlatformAfterInterativeDescriptor(newPlatformDescriptor, isSplited=False):
    dictionnaryDescriptor=interactiveDescriptorIntoDictionnary(newPlatformDescriptor, ADD_PLATFORM_STATEMENTS, isSplited)
    addPlatformToDataBase(dictionnaryDescriptor)
