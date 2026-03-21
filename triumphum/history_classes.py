########################################################################
# Classe des historiques
########################################################################
import json
import subprocess
from datetime import date, datetime, timedelta
from collections import defaultdict
import re
import triumphum.global_variables as global_variables
import triumphum.config_file as config_file
from triumphum.symbols import *
from triumphum.debug import * # TODO

def parse_str_duration_to_time_delta(str_duration: str) -> timedelta:
    # Transformer les expressions littérales de temps en timedelta
    h, m, s = str_duration.split(":")
    return timedelta(
        hours=int(h),
        minutes=int(m),
        seconds=float(s)
    )

class HistoryEntry:
    # Classe d’une entrée particulière d’un historique
    def __init__(self, start_time=None, end_time=None, duration=None, dictionnary=None):
        self.start_time=start_time or dictionnary["start_time"]
        self.end_time=end_time or dictionnary["end_time"]
        self.duration=duration or dictionnary["duration"]

    def date(self):
        # Retourne la date seule, sans le temps
        return self.start_time.split("T")[0]

    def make_data(self):
        # retourne les valeures sous forme de structure de données.
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

class History:
    # Classe d’historique d’ensemble d’un jeu donné
    def __init__(self):
        self.history = [] # Attends d’être allimentée d’une suite de valeures de type HistoryEntry

    def append(self, historyEntry):
        # Ajoute une entrée HistoryEntry à l’historique
        self.history.append(historyEntry)
        self.sort()

    def sort(self):
        # Trie l’historique de sorte à ce que les entrées se retrouvent dans l’ordre chronologique
        self.history.sort(reverse=True)

    def last_date(self):
        # Retourne la date de dernière ouverture
        if len(self.history) > 0:
            return self.history[0].end_time
        return None

    def reducedToDay(self):
    # Retourne un historique avec le temps cumulé par jour
        if self.history == []:
            return self.history

        durations_by_date = defaultdict(timedelta)

        for anEntry in self.history:
            durations_by_date[anEntry.date()] += parse_str_duration_to_time_delta(anEntry.duration)

        result = []
        for date in sorted(durations_by_date.keys()):
            total = durations_by_date[date]
            result.append(HistoryEntry(start_time=date, end_time=date, duration=total))

        return result

    def fill_missing_dates(self, data: dict[str, float]) -> dict[str, float]:
        # convertir les clés en datetime
        #print(data)
        dates = [datetime.strptime(d, "%Y-%m-%d") for d in data.keys()]
        
        start = min(dates)
        end = max(dates)

        filled = {}
        current = start

        while current <= end:
            key = current.strftime("%Y-%m-%d")
            filled[key] = data.get(key, 0.0)
            current += timedelta(days=1)

        return filled

    def flat(self):
        # Méthode de préparation de liste plate pour asciichart.py
        if self.history == []:
            return {}
        flatHistory={}
        for aHistoryEntry in self.reducedToDay():
            h, m, s = str(aHistoryEntry.duration).split(":")
            total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
            total_minuts=total_seconds/60
            flatHistory[aHistoryEntry.start_time]=total_minuts
        flatHistory=self.fill_missing_dates(flatHistory)
        return flatHistory

    def flat_for_gnuplot(self):
        gnuplot_ready_str=""
        flaten=self.flat()
        for anEntry in flaten:
            gnuplot_ready_str+=anEntry + " " + str(flaten[anEntry]) + "\n"
        return gnuplot_ready_str

    def generate_plot(self):
        if self.history == []:
            return None
        max_y, max_x = global_variables.STDSCR.getmaxyx()
        width=max_x
        height=max_y-4
        cmd = f"""
        set terminal dumb size {width}, {height};
        set xdata time;
        set timefmt '%Y-%m-%d';
        unset xtics;
        plot '-' using 1:2 with lines notitle
        """

        proc = subprocess.Popen(
            ["gnuplot", "-e", cmd],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        out, _ = proc.communicate(self.flat_for_gnuplot())
        return out

    def cumulate_time(self):
        # Retourne le temps joué cumulé depuis la première partie
        total_time = timedelta()
        for history_entry in self.history:
            t = datetime.strptime(history_entry.duration,"%H:%M:%S.%f")
            duration = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            total_time+=duration
        return total_time

    def historyEntriesFromNDays(self, numberOfDays):
        # Retourne un sous-ensemble de l’historique commençant depuis n jours
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

