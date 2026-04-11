########################################################################
# Géstion des couleurs
########################################################################

import curses
# Initilasitaion
curses.setupterm()

########################################################################
# Classe des couleurs
########################################################################
ncursesColorRegister={} # dictionnaire permettant de retenir les positions au sein du registre d’NCurses
listOfColors={}
class Color:
    # Classe des couleurs
    def __init__(self, name=None, code256=None, code10=None):
        self.name = name # Nom de la variable d’après laquelle seront désignées les couleurs
        self.code256=code256 # Code couleur à utiliser dans le cas de 256 couleurs
        self.code10=code10 # Code couleur a utiliser dans le cas de 10 couleurs
        self.ncursesSlot=None # Position au sein du registre ncruses

        globals()[self.name] = self # Déclaration de la variable globale de la couleur

        listOfColors[self.name]=self # Adjonction à la liste des jeux

    def set_ncurses(self):
        # Déploiement au sein d’NCurses
        if curses.tigetnum("colors") == 256:
            curses.init_pair(len(ncursesColorRegister)+1, listOfColors[self.name].code256, -1)  # Noir sur fond blanc
        else:
            curses.init_pair(len(ncursesColorRegister)+1, listOfColors[self.name].code10, -1)  # Noir sur fond blanc
        self.ncursesSlot=len(ncursesColorRegister)+1 # Déclaraition au sein d’NCurses
        ncursesColorRegister[self.name]=self # Inscription au sein du registre

    def __int__(self):
        return self.__index__()

    def __index__(self):
        return int(self.ncursesSlot)

    def __repr__(self):
        return f"Color(name='{self.name}')"

########################################################################
# Déploiement des couleurs
########################################################################

def use_curses_colors():
    # Fonction de déploiment éffective des couleurs
    curses.init_pair(1, curses.COLOR_BLACK, -1)  # Noir sur fond blanc
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Blanc sur fond noir
    curses.init_pair(3, -1, curses.COLOR_BLACK)  # Blanc sur fond noir
    ncursesColorRegister["mainWhite"]=None
    ncursesColorRegister["mainGray"]=None
    ncursesColorRegister["secondGray"]=None
    for aColor in listOfColors:
        listOfColors[aColor].set_ncurses()

#
# Pré-déclaration des couleurs en attente de leur déclaration dans le bon contexte
#
Color(name="white",  code256=15,  code10=curses.COLOR_WHITE) # white
Color(name="gray",   code256=245, code10=curses.COLOR_BLACK) # gray → pas dispo, approx noir
Color(name="yellow", code256=226, code10=curses.COLOR_YELLOW) # yellow
Color(name="silver", code256=250, code10=curses.COLOR_WHITE) # silver → blanc
Color(name="brown",  code256=94,  code10=curses.COLOR_YELLOW) # brown → jaune foncé approx
Color(name="orange", code256=208, code10=curses.COLOR_YELLOW) # orange → pas dispo, approx jaune
Color(name="purple", code256=129, code10=curses.COLOR_MAGENTA) # purple
Color(name="green",  code256=46,  code10=curses.COLOR_GREEN) # green
Color(name="white",  code256=15,  code10=curses.COLOR_WHITE) # white
Color(name="blue",   code256=27,  code10=curses.COLOR_BLUE) # blue
Color(name="red",    code256=196, code10=curses.COLOR_RED) # red

#
# Code colore selon les contextes
#

YEAR_COLOR = {
    # Code color pour les décénies
    30: gray, # Ambiance délétaire
    40: yellow, # Photographies jaunies de la seconde guerre
    50: silver, # Metal chromé des 
    60: brown, #
    70: orange, # Motifs psychédéliques
    80: purple, # Synthwave
    90: green, # Vert de l’écran électroluminescent de Matrix
    00: white, # Clips de rap et de pop tournés à l’intérieur d’une rapière à fromage en métal chromé
    10: blue, # Lien hypertextes et entête de Facebook
    20: red, # COVID-19, guerres, génocides, pump it up
}

# /!\ Note que si, je ne sais par quel miracle, est trouvé un jeu ayant été édité avant les années 1930 (et déjà 1930 c’est une prouesse incomensurable), comme par exemple une découverte d’un jeu vidéo dévelopé par dame Ada Lovelace en 1840, eh bien le code couleur utilisé pour sa date sera bien le même jaune que celui utilisé pour 1940. 
# Le mécanisme d’attribution des couleurs affecte une même couleur selon la décénie, sans égard pour le siècle.

PASSED_TIME_COLOR = {
    # Code colore pour le temps écoulé depuis la dernière ouverture
    # Le principe est que plus la dernière ouverture remonte à longtemps, plus la couleur doit alerter sur le fait qu’un jeu a été délaissé
    "s": gray,
    "min": white,
    "h": green,
    "d": blue,
    "w": yellow,
    "m": orange,
    "y": red,
}

CUMULATED_TIME_COLOR = {
    # Code colore pour le temps cumulé à un jeu
    # Le principe est que moins l’on a joué à un jeu, plus la couleur doit alerter sur le fait qu’un jeu a été délaissé
    "s": red,
    "min": orange,
    "h": yellow,
    "d": blue,
    "w": green,
    "m": white,
    "y": gray,
}
