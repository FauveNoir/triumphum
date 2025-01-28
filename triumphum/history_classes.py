########################################################################
# Classe des historiques
########################################################################
import json
from datetime import date, datetime, timedelta
import re
from triumphum.global_variables import *
import triumphum.config_file as config_file
from triumphum.symbols import *

# Classe d’une entrée particulière d’un historique
class HistoryEntry:
	def __init__(self, start_time=None, end_time=None, duration=None, dictionnary=None):
		self.start_time=start_time or dictionnary["start_time"]
		self.end_time=end_time or dictionnary["end_time"]
		self.duration=duration or dictionnary["duration"]

	def make_data(self):
		data = {
			"start_time": self.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
			"end_time": self.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
			"duration": self.duration.__str__(),
		}

		return data

	def make_json(self):
		# Bloc de transforamtion en json pour l’inscription dans l’historique persistant
		data=self.make_data()
		json_data = json.dumps(data)
		return json_data

	# Blocs de comparaison pour le tri
	def __eq__(self, other):
		if isinstance(other, HistoryEntry):
			return self.end_time == other.end_time
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, HistoryEntry):
			return self.end_time <  other.end_time
		return NotImplemented

	def __le__(self, other):
		if isinstance(other, HistoryEntry):
			return self.end_time <= other.end_time
		return NotImplemented

	def __gt__(self, other):
		if isinstance(other, HistoryEntry):
			return self.end_time >  other.end_time
		return NotImplemented

	def __ge__(self, other):
		if isinstance(other, HistoryEntry):
			return self.end_time >= other.end_time
		return NotImplemented

########################################################################

# Classe d’historique d’un jeu donné
class History:
	def __init__(self):
		self.history = []

	def append(self, historyEntry):
		self.history.append(historyEntry)
		self.sort()

	def sort(self):
		self.history.sort(reverse=True)

	def newer(self):
		if len(self.history) > 0:
			return self.history[0]
		return None

	def last_date(self):
		# Retourne la dateHeure de fermeture de la dernière partie jouée
		if self.newer() != None:
			return self.newer().end_time
		return None

	def cumulate_time(self):
		total_time = timedelta()
		for history_entry in self.history:
			t = datetime.strptime(history_entry.duration,"%H:%M:%S.%f")
			duration = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
			total_time+=duration
		return total_time

	def historyEntriesFromNDays(self, numberOfDays):
		today = date.today()
		durationAgo = today - timedelta(days=numberOfDays)
		durationEntries = History()
		for entry in self.history:
			if durationAgo <= datetime.strptime(entry.start_time, '%Y-%m-%dT%H:%M:%S').date() <= today:
				durationEntries.append(entry)

		return durationEntries

	def cumulatedPlayingTimeFromNDays(self, numberOfDays):
		cumulatedTime=self.historyEntriesFromNDays(numberOfDays)
		return cumulatedTime.cumulate_time()

########################################################################
# Fonctions d’éxtraction de l’historique pour un jeu donné

def is_history_date_relevant(date):
	# Filtre des dates pertinantes

	# Définir le motif de l'expression régulière pour le format AAAA-MM-JJThh:mm
	pattern = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$')
	if pattern.match(date):
		return True
	return False

def is_history_duration_relevant(date):
	# Filtre des dates pertinantes

	# Définir le motif de l'expression régulière pour le format AAAA-MM-JJThh:mm
	pattern = re.compile(r'^\d+:\d{2}:\d{2}.\d{6}$')
	if pattern.match(date):
		return True
	return False

def is_history_entry_relevant(history_entry):
	
	if "start_time" in history_entry and "end_time" in history_entry and "duration" in history_entry :
		if is_history_date_relevant(history_entry["start_time"]) and is_history_date_relevant(history_entry["end_time"]) and is_history_duration_relevant(history_entry["duration"]):
			return True
	return False

def retrive_history_of_a_game(game):
	prepared_history = History()
	with open(config_file.HISTORY_FILE.fullPath()) as f:
		data = json.load(f)

	if 'history' in data and game.code in data['history']:
		# Récupération de l’historique du jeu en cours
		game_history = data['history'][game.code]
		for history_entry in game_history:
			if is_history_entry_relevant(history_entry):
				prepared_history.append(HistoryEntry(dictionnary=history_entry))

	return prepared_history

