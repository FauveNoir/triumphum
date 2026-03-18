import appdirs
import configparser
import os

from triumphum.__init__ import *
from triumphum.global_variables import *
import triumphum.global_variables as global_variables
from triumphum.misc import *

from triumphum.platforms_classes import create_platform_objects
from triumphum.genres_classes import create_game_genre_objects
from triumphum.licences_classes import create_licence_objects
from triumphum.games_classes import  create_game_objects

########################################################################
# Répertoire de configuration
########################################################################

# Obtenir le répertoire de configuration de l’application
CONFIG_DIR = appdirs.user_config_dir(APP_CODE_NAME)

########################################################################
# Initialisation
########################################################################

listOfConfigurationFile={}
class ConfigurationFile:
    # Classe des fichiers de configuration, qui crée les variables globales désignant les fichiers
    # code : Nom de la variable sous laquelle sera désigné le dit fichier
    # baseName : Nom atomique du fichier (sans le lien complet)
    # path : Lien vers le fichier dans l’arborescence sans le nom atomique
    # minimalContent : Contenu de base du fichier, lorsque rien n’y a encore été inscrit
    def __init__(self, code=None, baseName=None, path=CONFIG_DIR, minimalContent=None):
        self.code=code
        self.baseName=baseName
        self.path=path
        self.minimalContent=minimalContent

        # Versement de l’objet à la liste de tous les objets du même type
        listOfConfigurationFile[self.code]=self
        # Versement de l’objet aux variables globales
        globals()[self.code]=self

    def fullPath(self):
        # retourne le lien entier, path+baseName
        return self.path + "/" + self.baseName

    def isExisting(self):
        # Test si le fichier est présent sur le disque
        return os.path.exists(self.fullPath())

    def createMinimalFile(self):
        # Crée un fichier minimal avec du contenu
        # Particulièrement utile en cas de premier lancement de Triumphum
        try:
            with open(self.fullPath(), 'w') as f:
                f.write(self.minimalContent)
            print(f"Le fichier « {self.fullPath()} » a été créé avec succès.")
        except IOError:
            print(f"Erreur : Impossible de créer le fichier « {file_path} ».")

    def testAndAskToCreateIfNone(self):
        # Crée le fichier à l’emplacement associé si ce dernier n’y est pas déjà
        if not self.isExisting():
            if ask_yes_no_question(f"Créer le fichier « {self.fullPath()} » ?"):
                self.createMinimalFile()

    def setNew(self, newPath):
        # Changer le lien vers le fichier
        self.baseName=os.path.basename(newPath)
        self.path=os.path.dirname(newPath)

    def __str__(self):
        # Traitement de l’objet en tant que chaine de caractère.
        # Le comportement en tant que conversion vers les chaines de caractères est d’afficher le lien complet vers le fichier.
        return self.fullPath()

def ask_yes_no_question(question):
    # Queestion Oui-Non à la aptitude
    # question : la question littérale qui apparaitra à l’utilisateur
    while True:
        user_input = input(f"{question} (Y/n): ").strip().lower()
        if user_input in ['y', 'yes']:
            return True
        elif user_input in ['n', 'no']:
            return False
        else:
            print("Veuillez répondre par 'Y' ou 'n'.")

def makeFileConfigMinimalContent():
    # Préparation du contenu minimal du fichier de configuration

    # Déffinition de la langue
    fileConfigMinimalContent="language=fre"

    # Collecte des symboles graphiques
    for aGraphicalSymbol in listOfGraphicalSymbols:
        fileConfigMinimalContent+="\n" + aGraphicalSymbol.fileConfigName + "=" + aGraphicalSymbol.value
    # Collecte des formations de touches
    for aBinding in global_variables.listOfBindings:
        fileConfigMinimalContent+="\n" + aBinding.makeDefaultConfigEntry()

    return fileConfigMinimalContent

def prepareConfigFiles():
    # Préparation de tous les fichiers de configuration et de donnée
    from triumphum.default_files_content import defaultGenresContent, defaultLicencesContent, defaultPlatformsContent
    ConfigurationFile(code="GAME_FILE",     minimalContent="""{"games":[]}""",      baseName="games.json")
    ConfigurationFile(code="GENRE_FILE",    minimalContent=defaultGenresContent,    baseName="listOfGenres.json")
    ConfigurationFile(code="LICENCE_FILE",  minimalContent=defaultLicencesContent,  baseName="listOfLicences.json")
    ConfigurationFile(code="PLATFORM_FILE", minimalContent=defaultPlatformsContent, baseName="listOfPlatforms.json")
    ConfigurationFile(code="HISTORY_FILE",  minimalContent="""{"history":[]}""",    baseName="history.json")
    ConfigurationFile(code="CONFIG_FILE",   minimalContent=makeFileConfigMinimalContent(),    baseName="triumphumrc", path=appdirs.user_config_dir())

def verifyConfigFileExistence():
    # Vérifie l’éxistence des fichiers de configuration et les crée sinon.
    for aFile in listOfConfigurationFile:
        listOfConfigurationFile[aFile].testAndAskToCreateIfNone()

########################################################################
# Traitement du fichier de configuration
########################################################################

def applyFileConfigurationsBindings():
    # Récupérer des fichiers de configuration les bindings de l’utilisateur et les déployer
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE.fullPath())

    configValues={}
    for aBinding in global_variables.listOfBindings:
        aConfigKey=aBinding.configFileName
        # TODO chercher la clé si elle existe
        if config.has_option("General", aConfigKey):
            configValues[aConfigKey]=config.get("General", aConfigKey)

            # ↓ Trouver au sein de `listOfBindings` l’élément ayant dans son paramettre « configFileName` la valeure contenue dans `value`, et en lui attribue aussitôt la valeur de `aConfigKey`.
            getElementHavingParameterWithValue(givenList=global_variables.listOfBindings, parameter="configFileName", value=aConfigKey).setKey(configValues[aConfigKey])

def applyFileConfigurationsGraphicalSymbols():
    # Récupérer des fichiers de configuration les symbols graphiques définis par l’utilisateur et les déployer
    config = configparser.ConfigParser()

    config.read(CONFIG_FILE.fullPath())

    for aConfigiGrahpicalSymbol in listOfGraphicalSymbols:
        if config.has_option("General", aConfigiGrahpicalSymbol.fileConfigName):
            aConfigiGrahpicalSymbol.value=config.get("General", aConfigiGrahpicalSymbol.fileConfigName)

########################################################################
# Fonctions d’extraction des données
########################################################################

def retrive_datas():
    # Dépoloiement de l’ensemble des caractéristiques paramettrables par l’utilisateur

    # Déploiement des objets de plateforme
    create_platform_objects()
    # Déploiement des objets de genres de jeux
    create_game_genre_objects()
    # Déploiement des objets de licence
    create_licence_objects()
    # Déploiement des objets de jeux
    create_game_objects()
