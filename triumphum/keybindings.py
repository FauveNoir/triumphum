########################################################################
# Classe des racoucris dactyliques
########################################################################
import curses
import threading
import webbrowser

from triumphum.__init__ import *
from triumphum.global_variables import listOfBindings
import triumphum.global_variables as global_variables
from triumphum.misc import getElementHavingParameterWithValue
from triumphum.debug import * # TODO
from triumphum.misc import bottomBarCoordinate
from triumphum.internal_shell_class import whatToDoWithShellInput
from triumphum.tui import  setBottomBarContent, questionMode

from triumphum.tui_screens import drawGamePlot, filterList

#
## Diverses fonctions utiles à la gestion des racourcis dactyliques
#


# Cas particuliers des mapings où le keycode ne correspond pas au symbole produit.
KEY_MAPPING = {
    # label, caractère
    "Enter": "\n",
    "Return": "\r",
    "Space": " ",
}

def reverseDictionnary(dictionnary):
    # Inverse les clés et valeurs du dictionnaire
    return {v: k for k, v in dictionnary.items()}

def transformKeyToCharacter(key_name):
    # Transformee les codes lisibles en caractères
    return KEY_MAPPING.get(key_name, key_name)

def transform_character_to_key(character_name):
    # Transformes les caractères reçus au claviers en labels lisibles
    reverseKeyMapping=reverseDictionnary(KEY_MAPPING)
    return reverseKeyMapping.get(character_name, character_name)

########################################################################

class Binding:
    # Classe des racourcis dactyliques.
    # key : touche associée
    # code : nom de la variable de l’objet créé
    # description : Description de l’usage tel qu’elle apparaitra à l’utilisateur dans les interfaces d’aide
    # configFileName : Nom de la fonction à utiliser par le fichier de configuration. Par défaut c’est code qui est utilisé afin de maintenir la plus grande homogénéité entre le code python et le fichier de configuration.
    #                 /!\ Ne déclarer éxplicitement une valeur pour `configFileName` que s’il éxiste une raison valable.
    # instructions : Nom de la fonction à déclencher lors de la pression sur le binding.
    def __init__(self, key=None, code=None, description=None, configFileName=None, instructions=None):
        self.key = None
        self.setKey(key)
        self.description = description
        self.code = code

        if configFileName == None:
            self.configFileName = self.code
        else:
            self.configFileName = configFileName
        globals()[code] = self # Déclaration de la variable globale pérmétant d’atteindre directement le genre voulu

        if instructions:
            setattr(self, 'executeInstructions', instructions)

        global_variables.listOfBindings.append(self) # Adjonction à la liste des genres de jeux

    def setKey(self, key):
        # Transforme les codes lisibles en caractères
        self.key = transformKeyToCharacter(key)

    def executeInstructions(self):
        # Éxectue la fontion associée au binding
        setBottomBarContent(f"{self.key} : Aucune action associée.")

    def makeDefaultConfigEntry(self):
        # Renvoit la ligne de fichier de configuration apropriée
        configEntry=self.configFileName + "=" + transform_character_to_key(self.key)
        return configEntry
    def __str__(self):
        return f"{self.code}: {self.key}"

########################################################################

#
## Fonctions dédiées aux actions des caractères dactyliques
#

def bindGoDownFunction():
    # Focale sur l’élément suivant de la liste visuelle
    global_variables.THE_VISUAL_LIST_OF_GAMES.goDown()

def bindGoUpFunction():
    # Focale sur l’élément précédent de la liste visuelle
    global_variables.THE_VISUAL_LIST_OF_GAMES.goUp()

def bindSortByNameFunction():
    # Trie la liste par ordre alphabétique
    global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("name")
    setBottomBarContent(f"Tri par ordre alphabétique.")

def bindSortByLicenceFunction():
    # Trie la liste par coeficient de liberté des licences
    global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("licence")
    setBottomBarContent(f"Tri par permissivité des licences.")

def bindSortByGenreFunction():
    # Trie la liste par genre
    global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("genre")
    setBottomBarContent(f"Tri par genre de jeu.")

def bindSortByDateFunction():
    # Trie la liste par genre
    global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("year")
    setBottomBarContent(f"Tri par année de sortie.")

def bindSortByLastOpeningFunction():
    # Trie la liste par date de dernière ouverture
    global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("latest_opening_date_value")
    setBottomBarContent(f"Tri par date de dernière ouverture.")

def bindSortByPlayingDurationFunction():
    # Trie la liste par dérée de jeu cumulée
    global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("playing_duration")
    setBottomBarContent(f"Tri par durée de jeu cumulée.")

def bindSortByPlatformFunction():
    # Trie la liste par plateforme
    global_variables.THE_VISUAL_LIST_OF_GAMES.sortBy("platform")
    setBottomBarContent(f"Tri par plateforme.")

def bindRunGameFunction():
    # Execute la commande associée à l’item ayant le focus
    global_variables.THE_VISUAL_LIST_OF_GAMES.openCurrent()

def bindDeleteGameFunction():
    # Suprime le jeu ayant le focus
    currentGame=global_variables.THE_VISUAL_LIST_OF_GAMES.currentGame().name
    if questionMode(f"Supprimer « {currentGame} » ?"):
        global_variables.THE_VISUAL_LIST_OF_GAMES.deleteCurrent()
    else:
        setBottomBarContent(f"« {currentGame} est conservé. Rien n’est altéré.")


def bindShowGameChart():
    currentGame=global_variables.THE_VISUAL_LIST_OF_GAMES.currentGame()
    drawGamePlot(game)



def bindOpenLinkFunction():
    # Ouvrir le lien associé à l’item ayant le focus
    global_variables.THE_VISUAL_LIST_OF_GAMES.openLink()

def bindCopyLinkFunction():
    # Copier le lien associé à l’item ayant le focus dans le presse papier
    global_variables.THE_VISUAL_LIST_OF_GAMES.copyLinkToClipBoard()

def bindMakeDonationFunction():
    # Ouvrir le lien pour faire un don
    setBottomBarContent(f"Merci de me faire un don sur « {APP_AUTHOR_DONATION_LINK} » (^.^)")
    threading.Thread(target=webbrowser.open, args=(APP_AUTHOR_DONATION_LINK,)).start()

def bindRefreshScreenFunction():
    # Rafraichir la vue
    global_variables.THE_VISUAL_LIST_OF_GAMES.refresh()

def enteringFilterMode(stdscr):
    stdscr.timeout(-1)
    curses.curs_set(1)  # Afficher le curseur
    h, w = bottomBarCoordinate(stdscr)

#    curses.init_pair(h-2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    # Position de départ pour la saisie de texte
    stdscr.move(h-1, 0)

    # Initialiser une liste pour stocker les caractères saisis
    input_text = ""

    stdscr.addch("/")  # Afficher le caractère saisi à l'écran

    while True:
        # Capturer un caractère
        ch = stdscr.getch()

        if ch == 27:  # Si ESC est pressé
            break

        elif ch == 263: # Si BSP est préssé
            y, x = stdscr.getyx()

            if x > 1:
                input_text=input_text[:-1]
                stdscr.move(y, x - 1)  # Déplace le curseur à la position juste avant
                stdscr.delch()         # Supprime le caractère à cette position

                stdscr.refresh()
            else:
                break

        elif ch in [curses.KEY_ENTER, 10]:  # Si Entrée est pressé (curses.KEY_ENTER vaut 10)

            whatToDoWithShellInput(input_text)
            global_variables.THE_VISUAL_LIST_OF_GAMES.filterByPattern(input_text)
            for aGame in global_variables.THE_VISUAL_LIST_OF_GAMES.relevantList:
                aGameObject=aGame[global_variables.THE_VISUAL_LIST_OF_GAMES.hiden_data_column_number()]
                writeInTmp(aGameObject.name)
            break  # Sortir de la boucle de saisie

        else:
            # Ajouter le caractère à la chaîne de texte
            input_text += chr(ch)
            stdscr.addch(ch)  # Afficher le caractère saisi à l'écran
            stdscr.refresh()

    curses.curs_set(0)  # Masquer le curseur

def enteringExMode(stdscr):
    stdscr.timeout(-1)
    # Activer la saisie de texte

    #stdscr.timeout(1000)  # attend max 1000 ms (1 seconde) pour une touche # TODO à déplacer dans le mode ex seulemet
    h, w = bottomBarCoordinate(stdscr)
    curses.curs_set(1)  # Afficher le curseur

#    curses.init_pair(h-2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    # Position de départ pour la saisie de texte
    stdscr.move(h-1, 0)

    # Initialiser une liste pour stocker les caractères saisis
    input_text = ""

    stdscr.addch(":")  # Afficher le caractère saisi à l'écran
    while True:
        # Capturer un caractère
        ch = stdscr.getch()

        if ch == 27:  # Si ESC est pressé
            break

        elif ch == 263: # Si BSP est préssé
            y, x = stdscr.getyx()

            if x > 1:
                input_text=input_text[:-1]
                stdscr.move(y, x - 1)  # Déplace le curseur à la position juste avant
                stdscr.delch()         # Supprime le caractère à cette position

                stdscr.refresh()
            else:
                break

        elif ch in [curses.KEY_ENTER, 10]:  # Si Entrée est pressé (curses.KEY_ENTER vaut 10)

            whatToDoWithShellInput(input_text)
            break  # Sortir de la boucle de saisie

        else:
            # Ajouter le caractère à la chaîne de texte
            input_text += chr(ch)
            stdscr.addch(ch)  # Afficher le caractère saisi à l'écran
            stdscr.refresh()

    curses.curs_set(0)  # Masquer le curseur

def enteringExModeByBinding():
    enteringExMode(global_variables.STDSCR)

def enteringFilterModeByBinding():
    enteringFilterMode(global_variables.STDSCR)

########################################################################
# Déclaration des racoucis dactiliques
########################################################################

def declareBindings():
    Binding(key="t", code="bindGoDown", description="Aller en haut", instructions=bindGoDownFunction, configFileName="bind_down")
    Binding(key="s", code="bindGoUp", description="Aller en bas", instructions=bindGoUpFunction, configFileName="bind_up")
    Binding(key="\n", code="bindRunGame", description="Lancer le jeu", instructions=bindRunGameFunction, configFileName="bind_play")

    Binding(key="b", code="bindSortByName", description="Trier par nom", instructions=bindSortByNameFunction, configFileName="bind_sort_title")
    Binding(key="é", code="bindSortByLicence", description="Trire par licence", instructions=bindSortByLicenceFunction, configFileName="bind_sort_licence")
    Binding(key="p", code="bindSortByGenre", description="Trier par genre", instructions=bindSortByGenreFunction, configFileName="bind_sort_game_genre")
    Binding(key="o", code="bindSortByDate", description="Trier par date", instructions=bindSortByDateFunction, configFileName="bind_sort_year")
    Binding(key="è", code="bindSortByLastOpening", description="Trier par date de dernière ouverture", instructions=bindSortByLastOpeningFunction, configFileName="bind_sort_last_opening")


    Binding(key="v", code="bindSortByPlayingDuration", description="Trier par heure cumulé", instructions=bindSortByPlayingDurationFunction, configFileName="bind_sort_playing_duration")
    Binding(key="!", code="bindSortByPlatform",instructions=bindSortByPlatformFunction, description="Trier par plateforme", configFileName="bind_sort_playing_platform")

    Binding(key="A", code="bindOpenLink", description="Ouvrir le site web associé", instructions=bindOpenLinkFunction, configFileName="bind_open_link")
    Binding(key="e", code="bindEditData", description="Éditer les données", configFileName="bind_edit")
    Binding(key="d", code="bindDelete", description="Suprimer le jeu de la liste", instructions=bindDeleteGameFunction, configFileName="bind_delete")
    Binding(key="i", code="bindComment", description="Commenter", configFileName="bind_comment")
    Binding(key="x", code="bindMakeDonation", description="Faire un don", instructions=bindMakeDonationFunction, configFileName="bind_donate")
    Binding(key="w", code="bindShowFullLicence", description="Afficher le texte de la licence", configFileName="bind_show_licence")
    Binding(key="/", code="bindFilter", description="Filtrer", configFileName="bind_filter", instructions=enteringFilterModeByBinding)
    Binding(key="h", code="bindSeeBindingHelp", description="Montrer l’aide", configFileName="bind_help")
    Binding(key="y", code="bindCopyLink", description="Copier le lien dans le presse-papier", instructions=bindCopyLinkFunction, configFileName="bind_copy_link")
    Binding(key="l", code="bindRefreshScreen", description="Rafraichir l’écran", instructions=bindRefreshScreenFunction, configFileName="bind_refresh")
    Binding(key="q", code="bindQuit", description=f"Quitter {APP_FANCY_NAME}", configFileName="bind_quit")
    Binding(key=":", code="bindExMode", description=f"Mode Ex", configFileName="bind_exMode", instructions=enteringExModeByBinding)
    Binding(key="g", code="bindShowPlot", description=f"Montrer le graphique du jeu", configFileName="bind_plot", instructions=drawGamePlot)
