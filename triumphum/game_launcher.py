########################################################################
# Fonctions créant le script de lancement
########################################################################
from triumphum.__init__ import *
from triumphum.cli_options import run_command
from datetime import datetime
from pathlib import Path

import os

def commentText(theGame):
    return f"""#!/bin/sh
# Ce script a été généré automatiquement par {APP_FANCY_NAME} {APP_VERSION} le {datetime.now()}.
# Le présent lanceur d’application permet d’executer le jeu {theGame.name} avec le traqueur de pérformance de {APP_FANCY_NAME}.

"""

def prepare_script_command(theGame):
    script_path= os.path.abspath(__file__)
    run_option=run_command.option_strings[0]
    launcher_command= " ".join([script_path, run_option, theGame.code])
    return launcher_command


def full_script_content(theGame):
    script_content=commentText(theGame)
    script_content+=prepare_script_command(theGame)
    return script_content


def create_game_launcher(theGame):
    directory = Path("~/.local/bin/triumphum_launchers").expanduser()
    file_name=theGame.code
    Path(directory) \
        .mkdir(parents=True, exist_ok=True)
    content=full_script_content(theGame)
    file_path = os.path.join(directory, file_name)
    try:
        with open(file_path, 'x') as f:
            f.write(content)
        print(f"✔️ Lanceur généré pour « {theGame.name} »")
    except:
        print(f"❌ Une érreur est survenue dans la génération du lanceur pour « {theGame.name} »")
