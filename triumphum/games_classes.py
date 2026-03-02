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


file_path = Path("mon_fichier.txt")
content = "Contenu du fichier"

def yesNoCreateFile(file_path=None, content=None):
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
    return f"""#!/bin/sh
# Ce script a été généré automatiquement par {APP_FANCY_NAME} {APP_VERSION} le {datetime.now()}.
# Le présent lanceur d’application permet d’executer le jeu {theGame.name} avec le traqueur de pérformance de {APP_FANCY_NAME}.

"""

def prepare_script_command(theGame):
    entry_point = " ".join(
        [shlex.quote(sys.executable)] +
        [shlex.quote(sys.argv[0])]
    )
    #entry_point = Path(sys.argv[0]).resolve()
    entry_point=APP_CODE_NAME
    run_option=run_command.option_strings[0]
    launcher_command= " ".join([str(entry_point), run_option, theGame.code])
    return launcher_command


def full_script_content(theGame):
    script_content=commentText(theGame)
    script_content+=prepare_script_command(theGame)
    return script_content

########################################################################
# Autre (à commenter)
########################################################################

def formatDataListToLitteralList(list_, voidSymbol):
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
    return (n // base) * base

def colorForTheYear(year):
    if not isinstance(year, int):
        return 1
    decade=str(year)[-2:]
    decade=int(decade)
    decade=floor_to_base(decade)
    decadeColor=YEAR_COLOR[decade]
#    ncursesColorSlot=decadeColor.ncursesSlot
    return decadeColor

def prepareNcurseRow(value=None, altValue=None, color=1):
    if value != None:
        return (str(value), color)
    return (str(altValue), 1)

def set_color_according_to_cumulate_time(delta):
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
        self.history = self.get_history()
        self.latest_opening_date_value = self.latest_opening_date()
        self.playing_duration = self.cumulate_time()

        listOfGames[self.code]=self # Adjonction à la liste des jeux

    def ncurseLine(self):
        # Préparation de la ligne de tableau

        # Vérifier chaque clé pour une éventuelle valeur vide et remplacer par "-"
        ncurseLine = [
            prepareNcurseRow(value=self.platform.abbr, altValue=symbols.PLATFORM_VOID_SYMBOL.value),
            prepareNcurseRow(value=self.name, altValue=symbols.NAME_VOID_SYMBOL.value),
            prepareNcurseRow(value=self.licence.abbr, altValue=symbols.LICENCE_VOID_SYMBOL.value),
            prepareNcurseRow(value=self.genre.abbr, altValue=symbols.GENRE_VOID_SYMBOL.value),
            prepareNcurseRow(value=self.year, altValue=symbols.DATE_VOID_SYMBOL.value, color=colorForTheYear(self.year)),
            prepareNcurseRow(value=self.human_latest_opening_duration(), altValue=symbols.LASTOPENING_VOID_SYMBOL.value, color=set_color_according_to_cumulate_time(self.latest_opening_duration())),
            prepareNcurseRow(value=self.human_cumulate_time(), altValue=symbols.CUMULATEDTIME_VOID_SYMBOL.value),
            prepareNcurseRow(value=self.listOfAuthors(), altValue=symbols.AUTHOR_VOID_SYMBOL.value),
            prepareNcurseRow(value=self.listOfStudios(), altValue=symbols.STUDIO_VOID_SYMBOL.value),
            self
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
        # Fiche rapide de description de jeu
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
        return formatDataListToLitteralList(self.authors, symbols.AUTHOR_VOID_SYMBOL.value)

    def listOfStudios(self):
        return formatDataListToLitteralList(self.studios, symbols.STUDIO_VOID_SYMBOL.value)

    def delete(self):
        deleteGameFromDatabase(self.code)

    def showPlot(self):
        pass

    def create_launcher(self):
        directory = Path("~/.local/bin").expanduser()
        file_name=self.code
        Path(directory) \
            .mkdir(parents=True, exist_ok=True)
        content=full_script_content(self)
        file_path = os.path.join(directory, file_name)
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
