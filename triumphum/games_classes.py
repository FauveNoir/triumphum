########################################################################
# Classe des jeux
########################################################################

import sys
import humanize
from datetime import date, datetime, timedelta
from tabulate import tabulate
import json
import os
import stat
import shlex
import curses

from triumphum.global_variables import *
import triumphum.config_file as config_file
from triumphum.history_classes import retrive_history_of_a_game
from triumphum.licences_classes import  get_licence_object_after_code
from triumphum.genres_classes import get_genre_object_after_code
from triumphum.platforms_classes import get_platform_object_after_code
from triumphum.db_edition import  deleteGameFromDatabase
import triumphum.symbols as symbols
from triumphum.__init__ import *
from triumphum.cli_options import run_command
from datetime import datetime
from pathlib import Path
from triumphum.colors import *

from triumphum.debug import * # TODO

########################################################################
# Fonctions de création du lanceur
########################################################################


file_path = Path("mon_fichier.txt") # \__ TODO à quoi servent ces deux variables ?
content = "Contenu du fichier"      # /

def yesNoCreateFile(file_path=None, content=None):
    # Dialogue de la ligne de commande posant une question fermée sur la création de fichier
    # file_path : chemin vers le fichier à créer
    # content : contenu à mettre dans le fichier
    file_path=Path(file_path)
    if file_path.exists():
        answer = input(f"Le fichier « {file_path} » existe déjà. Écraser ? [o/N] ").strip().lower()
        if answer not in ("o", "oui", "y", "yes"):
            print("Opération annulée.")
            return False
        else:
            file_path.write_text(content)
            print("Fichier écrasé.")
            return True
    else:
        file_path.write_text(content)
        print("Fichier créé.")
        return True

def commentText(theGame):
    # Retourne le texte d’entête contenu dans le script de lanceur de jeu
    # theGame : variable de type Game du jeu dont il s’agira d’écrire le lanceur
    return f"""#!/bin/sh
# Ce script a été généré automatiquement par {APP_FANCY_NAME} {APP_VERSION} le {datetime.now()}.
# Le présent lanceur d’application permet d’executer le jeu {theGame.name} avec le traqueur de pérformance de {APP_FANCY_NAME}.

"""

def prepare_script_command(theGame):
    # Retourne la partie du script correspondant à la commande à proprement parler (et non au script d’entête)
    # theGame : variable de type Game du jeu dont il s’agira d’écrire le lanceur
    entry_point = " ".join(
        [shlex.quote(sys.executable)] +
        [shlex.quote(sys.argv[0])]
    )
    entry_point=APP_CODE_NAME
    run_option=run_command.option_strings[0]
    launcher_command= " ".join([str(entry_point), run_option, theGame.code])
    return launcher_command


def full_script_content(theGame):
    # Retourne l’ensemble du contenu du script
    # theGame : variable de type Game du jeu dont il s’agira d’écrire le lanceur
    script_content=commentText(theGame)
    script_content+=prepare_script_command(theGame)
    return script_content

########################################################################
# Effets visuels d’NCurses
########################################################################

def formatDataListToLitteralList(list_, voidSymbol):
    # Formate les listes (notament d’auteurs et de studios) selon la bonne typographie.
    # C’est à dire en plaçant des virgules et un « et » préposal aux bons endroits.

    # prétraitement du nombre d’éléments de la liste, avec la prise en compte du cas où la liste est vide, ou où elle correspond juste à None, ou autre chose qu’une liste
    try:
        n = len(list_)
    except:
        n = 0
    if n == 0:
        return voidSymbol # TODO
    elif n == 1:
        return list_[0]
    elif n == 2:
        return f"{list_[0]} et {list_[1]}"
    else:
        elements = ", ".join(list_[:-1])
        return f"{elements}, et {list_[-1]}"



def floor_to_base(n, base=10):
    # Arondi à l’année d’entrée de décénie
    # Par exemple 1984→1980, 1992→1990, 2020→2020
    return (n // base) * base

def colorForTheYear(year):
    # Établissement de la couleur de décénie selon l’année donnée en entrée
    if not isinstance(year, int):
        return 1
    decade=str(year)[-2:]
    decade=int(decade)
    decade=floor_to_base(decade)
    decadeColor=YEAR_COLOR[decade]
    return decadeColor

def prepare_NCurses_cell(value=None, altValue=None, color=1):
    # Préparation de la cellule NCURSES
    if value != None:
        return (str(value), color)
    return (str(altValue), 1)

def set_color_according_to_last_opening_duration(delta):
    # Établissement de la couleur selon la dernière date d’ouverture
    if delta == None:
        return 1
    if delta < timedelta(minutes=1):
        return PASSED_TIME_COLOR["s"]
    elif delta < timedelta(hours=1):
        return PASSED_TIME_COLOR["min"]
    elif delta < timedelta(days=1):
        return PASSED_TIME_COLOR["h"]
    elif delta < timedelta(days=7):
        return PASSED_TIME_COLOR["d"]
    elif delta < timedelta(days=30):
        return PASSED_TIME_COLOR["w"]
    elif delta < timedelta(days=365):
        return PASSED_TIME_COLOR["m"]
    else:
        return PASSED_TIME_COLOR["y"]

def set_color_according_to_cumulate_time(delta):
    # Établissement de la couleur selon le temps cumulé de jeu
    if delta == None:
        return 1
    if delta < timedelta(minutes=1):
        return CUMULATED_TIME_COLOR["s"]
    elif delta < timedelta(hours=1):
        return CUMULATED_TIME_COLOR["min"]
    elif delta < timedelta(days=1):
        return CUMULATED_TIME_COLOR["h"]
    elif delta < timedelta(days=7):
        return CUMULATED_TIME_COLOR["d"]
    elif delta < timedelta(days=30):
        return CUMULATED_TIME_COLOR["w"]
    elif delta < timedelta(days=365):
        return CUMULATED_TIME_COLOR["m"]
    else:
        return CUMULATED_TIME_COLOR["y"]

# Défffinition de classe
class Game:
    def __init__(self, name=None, code=None, licence=None, url=None, year=None, genre=None, authors=None, studios=[], command=None, comments=None, platform=None):
        self.name = name
        self.code = code
        self.licence = licence
        self.url = url
        self.year = year
        self.genre = genre
        self.authors = authors
        self.studios = studios
        self.command = command
        self.comments = comments
        self.platform = platform
        self.history = self.get_history()                            #
        self.latest_opening_date_value = self.latest_opening_date()  # TODO à voir s’il ne faudra pas supprimer ses attributs,
        self.playing_duration = self.cumulate_time()                 # et utiliser à la place les méthodes diréctement, partout où y est fait appel

        listOfGames[self.code]=self # Adjonction à la liste des jeux

    def ncurseLine(self):
        # Préparation de la ligne de tableau

        # Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
        ncurseLine = [
            prepare_NCurses_cell(value=self.platform.abbr, altValue=symbols.PLATFORM_VOID_SYMBOL.value),
            prepare_NCurses_cell(value=self.name, altValue=symbols.NAME_VOID_SYMBOL.value),
            prepare_NCurses_cell(value=self.licence.abbr, altValue=symbols.LICENCE_VOID_SYMBOL.value),
            prepare_NCurses_cell(value=self.genre.abbr, altValue=symbols.GENRE_VOID_SYMBOL.value),
            prepare_NCurses_cell(value=self.year, altValue=symbols.DATE_VOID_SYMBOL.value, color=colorForTheYear(self.year)),
            prepare_NCurses_cell(value=self.human_latest_opening_duration(), altValue=symbols.LASTOPENING_VOID_SYMBOL.value, color=set_color_according_to_last_opening_duration(self.latest_opening_duration())),
            prepare_NCurses_cell(value=self.human_cumulate_time(), altValue=symbols.CUMULATEDTIME_VOID_SYMBOL.value, color=set_color_according_to_cumulate_time(self.cumulate_time())),
            prepare_NCurses_cell(value=self.listOfAuthors(), altValue=symbols.AUTHOR_VOID_SYMBOL.value),
            prepare_NCurses_cell(value=self.listOfStudios(), altValue=symbols.STUDIO_VOID_SYMBOL.value),
        ]
        return ncurseLine

    def asciiRow(self):
        # Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
        asciiRow = [
            self.platform.abbr or symbols.PLATFORM_VOID_SYMBOL.value,
            self.name or symbols.NAME_VOID_SYMBOL.value,
            self.licence.abbr or symbols.LICENCE_VOID_SYMBOL.value,
            self.genre.abbr or symbols.GENRE_VOID_SYMBOL.value,
            self.year or symbols.DATE_VOID_SYMBOL.value,
            self.human_latest_opening_duration() or symbols.LASTOPENING_VOID_SYMBOL.value,
            self.human_cumulate_time() or symbols.CUMULATEDTIME_VOID_SYMBOL.value,
            self.listOfAuthors() or symbols.AUTHOR_VOID_SYMBOL.value,
            self.listOfStudios() or symbols.STUDIO_VOID_SYMBOL.value
        ]
        return asciiRow

    def sheet(self):
        # Fiche rapide de description de jeu à afficher sur la sortie standard
        sheet_data=[
            ["Nom", self.name],
            ["code", self.code],
            ["Licence", self.licence.name],
            ["URL", self.url],
            ["Genre", self.genre.name],
            ["Auteur", self.listOfAuthors()],
            ["Commande", self.command],
            ["Dernière ouverture", self.latest_opening_date()],
        ]

        print(tabulate(sheet_data))

    def get_history(self):
        # Retourne l’historique des dates et heures de parties jouées
        return retrive_history_of_a_game(self)

    def cumulate_time(self):
        # Temps de jeu cumulé
        return self.history.cumulate_time()

    def human_cumulate_time(self):
        # Retourne le temps total joué humainement lisible
        if self.history.cumulate_time() == timedelta(): # test si le temps cumulate_time() retourne bien un delta et non le caractère "-"
            return " "
        delta = humanize.naturaldelta(self.history.cumulate_time())
        return delta

    def latest_opening_date(self):
        # Retourne la dernière date où le jeu a ét éouvert
        return self.history.last_date()

    def latest_opening_duration(self):
        # Retourne la durée depuis laquelle le jeu a été ouvert
        if self.latest_opening_date():

            # Réception de la chaine string et transformation en datetime
            last_date= datetime.strptime(self.history.last_date(), "%Y-%m-%dT%H:%M:%S") 
            delta=datetime.now() - last_date
            return delta
        return None

    def human_latest_opening_duration(self):
        # Temps depuis la dernière ouverture humainement lisible
        if self.latest_opening_date():
            return humanize.naturaldelta(self.latest_opening_duration())
        return "-"

    def listOfAuthors(self):
        # Retourne la liste des auteurs formatées avec les bons séparateurs
        return formatDataListToLitteralList(self.authors, symbols.AUTHOR_VOID_SYMBOL.value)

    def listOfStudios(self):
        # Retourne la liste des studios formatées avec les bons séparateurs
        return formatDataListToLitteralList(self.studios, symbols.STUDIO_VOID_SYMBOL.value)

    def delete(self):
        # Supprimer le jeu de la base de donnée
        deleteGameFromDatabase(self.code)

    def create_launcher(self):
        # Création du lanceur du jeu avec traqeur de startistiques de Triumphum
        directory=Path("~/.local/bin").expanduser() # Déffinition du répertoire où sera créé le lanceur
        file_name=self.code # Déffinition du nom du fichier d’après le code du jeu
        Path(directory) \
            .mkdir(parents=True, exist_ok=True) # Création du répertoire au cas où il n’existerait pas déjà
        content=full_script_content(self) # Récupération du contenu du  scirpt
        file_path=os.path.join(directory, file_name) # Déclaration du lien complet du scirpt
        try:
            # Création
            isFileCreated=yesNoCreateFile(file_path=file_path, content=content)
            # Attribution des droits d’execution
            if isFileCreated:
                st = os.stat(file_path)
                os.chmod(file_path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
                print(f"✔️ Lanceur généré pour « {self.name} »")
        except:
            print(f"❌ Une érreur est survenue dans la génération du lanceur pour « {self.name} »")


def create_game_objects():
    # Création de la liste des jeux

    # Extraction des jeux
    with open(config_file.GAME_FILE.fullPath()) as f:
        listOfGamesData = json.load(f)["games"]

    listOfGames.clear()
    ## Déploiment des objet de jeux
    for aGame in listOfGamesData:
        Game(
            name=aGame.get("name"),
            code=aGame.get("code"),
            licence=get_licence_object_after_code(aGame.get("licence")),
            url=aGame.get("url"),
            year=aGame.get("year"),
            genre=get_genre_object_after_code(aGame.get("genre")),
            command=aGame.get("command"),
            authors=aGame.get("authors"),
            studios=aGame.get("studios"),
            platform=get_platform_object_after_code(aGame.get("platform")),
        )
