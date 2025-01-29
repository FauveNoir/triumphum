########################################################################
# Fonctions foncitonnelles de l’interface interactive
########################################################################
import json
from datetime import date, datetime, timedelta
import subprocess

from triumphum.global_variables import *
import triumphum.config_file as config_file
from triumphum.history_classes import HistoryEntry


def history_data_with_current_game(game):
	with open(config_file.HISTORY_FILE.fullPath()) as f:
		data = json.load(f)

	if 'history' not in data:
		data['history'] = {}

	if game.code not in data['history']:
		data['history'][game.code] = []

	return data

def write_opening_date_on_history(game=None, start_time=None, end_time=None, duration=None):
	try:
		# Charger le JSON existant depuis un fichier
		with open(config_file.HISTORY_FILE.fullPath()) as f:
			data = json.load(f)

		data = history_data_with_current_game(game)
		history_entry=HistoryEntry(start_time=start_time, end_time=end_time, duration=duration)
		data['history'][game.code].append(history_entry.make_data())

		# Enregistrer la structure de données modifiée en tant que JSON
		with open(config_file.HISTORY_FILE.fullPath(), 'w') as f:
			json.dump(data, f, indent=4)
	except:
		pass

def run_command_and_write_on_history(game):
	# Enregistrement de l’heure de début
	start_time = datetime.now()

	# Lancement du procéssus
	command_process = subprocess.Popen(game.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	# Mise en atente pour la fin du processus
	output, error = command_process.communicate()

	# Récupération de l’heure de fin
	end_time = datetime.now()

	# Date
	duration = end_time - start_time

	# Inscription de l’évenement dans l’historique
	write_opening_date_on_history(game, start_time=start_time, end_time=end_time, duration=duration)
