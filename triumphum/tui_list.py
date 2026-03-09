########################################################################
# Classe des colones de la liste visuelle
########################################################################
import pyperclip
import threading
import webbrowser
import re

from triumphum.global_variables import *
import triumphum.global_variables as global_variables
from triumphum.config_file import retrive_datas
from triumphum.history_classes import  History
from triumphum.tui import setBottomBarContent
from triumphum.tui_functions import run_command_and_write_on_history

from triumphum.debug import * # TODO

def getColWidths():
    itemsMergedWithTitle = global_variables.items[:]
    itemsMergedWithTitle.append(titles)
    col_widths = [max(len(str(column[0])) for column in col) for col in zip(*itemsMergedWithTitle)]

    return col_widths

########################################################################
# Classe de la liste visuelle
########################################################################

class ListMove:
    # Classe des mouvements au sein d’une liste. C’est à dire HAUT et BAS
    def __init__(self, label=None, code=None):
        self.label=label
        self.code=code
        globals()[self.code] = self # les objets déffinits deviennent des variables globales identifiées par self.code

# Les deux mouvements de classe ListMove
ListMove(label="Go up", code="goUp")
ListMove(label="Go down", code="goDown")

########################################################################
# Classe de la liste ligne de liste visuelle
########################################################################

class VisualRow:
    # Classe de liste visuelle Ncurses
    def __init__(self, game):
        self.data=game
        self.formated_data=game.ncurseLine()


########################################################################
# Classe de la liste visuelle
########################################################################

SORTING_ORDER=[True, False]

def getNextSortingOrder(currentSortingOrder):
    # Les types de tri sont circulaires, entre Croissant, décroissant, et pas-de-tri.
    # Aussi cette fonction permet d’obtenir le type de tri suivant dans l’ordre de succèssion, selon le type actuellement en vigeur
    global SORTING_ORDER
    currentIndex=SORTING_ORDER.index(currentSortingOrder)
    tmpNextIndex=currentIndex+1
    realNextIndex=tmpNextIndex % len(SORTING_ORDER)
    nextSortingOrder=SORTING_ORDER[realNextIndex]

    return nextSortingOrder

class VisualListOfGames:
    # Classe de liste visuelle Ncurses
    def __init__(self):
        self.columns=None
        self.titles = [" ", "Titre", "Licence", "Genre", "Date", "Dernière ouverture", "Temps cumulé", "Auteur", "Studio"]
        self.list=None
        self.filter_input=""
        self.filter_mode=False
        self.patern=None
        self.sortByProperty=None
        self.sortingState=SORTING_ORDER[1]
        self.selected_row = 0
        self.firstRowOnVisibleList = 0
        self.lastMove=None

        self.refresh()
        global_variables.THE_VISUAL_LIST_OF_GAMES = self # Le seul objet de cette classe est TheVisualListOfGames

    def isTheListEmpty(self):
        # Renvoies True ou False, selon que la liste soit pleine ou vide
        if self.relevantList() in [None, []]:
            return True
        return False

    def getNthNLines(self, lineRank, numberOfLines):
        # Retourne une portion de la liste commençan par lineRank et contenant numberOfLines lignes
        # Cette fonction est utile pour la pagination
        subList = self.relevantList()[lineRank:lineRank+numberOfLines]
        return subList

    # TODO intégéré screenHeight-3 dans la déffiniton de classe
    def visualHighlightedLineNumber(self, screenHeight):
        visualHighlightedLineNumber=self.selected_row-self.firstRowOnVisibleList
        return visualHighlightedLineNumber

    def getCurrentVisibleList(self, screenHeight):
        # Retourne la partie visible de la liste d’après la hauteur disponible de l’écran
        if self.lastMove == goDown:
            if self.selected_row > self.firstRowOnVisibleList + screenHeight-4-3 :
                self.firstRowOnVisibleList+=1

        if self.lastMove == goUp:
            if self.selected_row == self.firstRowOnVisibleList +1 and self.selected_row > 1 :
                self.firstRowOnVisibleList-=1

        visibleList=self.getNthNLines(self.firstRowOnVisibleList, screenHeight-4) # TODO remplacer le 2 par une variable

        return visibleList

    def goDown(self):
        # Déplace le focus d’une ligne vers le bas
        self.selected_row = min(len(self.relevantList()) - 1, self.selected_row + 1)
        self.lastMove=goDown

    def goUp(self):
        # Déplace le focus d’une ligne vers le haut
        self.selected_row = max(0, self.selected_row - 1)
        self.lastMove=goUp

    def openCurrent(self):
        # Exécuter la commande de lancement du jeu associée à la ligne sélectionnée
        setBottomBarContent(f"Ouverture de « {self.currentGame().name} ».")
        threading.Thread(target=run_command_and_write_on_history, args=(self.currentGame(),)).start()

    def currentGame(self):
        # objet Game ayant le focus
        game = self.relevantList()[self.selected_row].data
        return game

    def deleteCurrent(self):
        # Supprimer le jeu ayant le focus de la base de donnée
        setBottomBarContent(f"Supression du jeu « {self.openCurrent().name} ».")
        game = self.currentGame()
        if self.selected_row == len(self.relevantList())-1:
            # Après avoir supprimé le jeu, postioner le focus sur le jeu ayant prit sa place dans l’ordre 
            self.goUp()
            game = self.relevantList()[self.selected_row+1].data
        game.delete()
        self.relevantList()[self.selected_row]
        self.refresh()

    def copyLinkToClipBoard(self):
        # Copier le lien du jeu dans le presse papier
        url = self.relevantList()[self.selected_row].data.url
        if url != None:
            setBottomBarContent(f"Copie de « {self.currentGame().url} » dans le presse-papier.")
            pyperclip.copy(url)
        else:
            setBottomBarContent(f"Aucun lien associé à « {self.currentGame().name} », rien à copier.")

    def openLink(self):
        # Ouvrir l’URL du jeu dans le navigateur par défaut
        url = self.currentGame().url  # Supposons que l'URL est stockée à l'indice 5
        if url != None:
            setBottomBarContent(f"Ouverture de « {url} »")
            self.refresh()
            threading.Thread(target=webbrowser.open, args=(url,)).start()
        else:
            setBottomBarContent(f"Pas de lien associé à « {self.currentGame().name} »")

    def refresh(self):
        # Rafraichir la liste, notament en ré-interogant la base de donnée
        retrive_datas()
        global_variables.listOfGames

        self.list=[]
        for aGame in global_variables.listOfGames.values():
            self.list.append(VisualRow(aGame))

    def shiftSortingState(self, property_):
        # Basculer le type d’ordre de tri vers le suivant dans la liste
        if ( property_ == self.sortByProperty) :
            self.sortingState=getNextSortingOrder(self.sortingState)

    def isAtributeShouldBeSorted(self, attribute):
        # Tester si l’attribut doit être inclus dans l’ordre de tri, ou relégé vers le bas
        if attribute in ["-", None]:
            return False
        if hasattr(attribute, "includeInSorting"):
            if attribute.includeInSorting == False:
                return False

        return True

    def putVoidAtEnd(self, oldList, property_):
        # Relegué vers le bas les jeux dont l’attribut selon lequel il faut trier est vide
        beginingOfNewList=[] # Éléments qui seront en haut
        endOfNewList=[] # Éléments qui seront en bas
        for item in oldList:
            if self.isAtributeShouldBeSorted(getattr(item.data, property_)) :
                beginingOfNewList.append(item)
            else:
                endOfNewList.append(item)
        newList= beginingOfNewList + endOfNewList # fusion des deux listes
        return newList

    def softSortBy(self, relevantList):
        property_=self.sortByProperty
        if property_:
            # Procéder au tri si une option de tri est déffinie
            relevantList = sorted(relevantList, 
                             reverse=self.sortingState, # Inverser l’ordre de tri si besoin
                             key=lambda x: (getattr(x.data, property_) is None, 
                                            getattr(x.data, property_)))

            # Relégué les jeux dont la propriété a triée est vide vers le bas
            relevantList=self.putVoidAtEnd(relevantList, property_) 
        return relevantList # retourner directement la liste donnée en entrée s’il n’y a rien à trier

    def sortBy(self, property_):
        # Déffinir la propriété selon laquelle trier et le sens de tri (croissant ou décroissant)
        # MAIS ne trie pas à proprement parler
        self.shiftSortingState(property_)
        self.sortByProperty=property_

    def columnsWidth(self):
        # Définir la largeur des colones d’après leur contenu le plus large
        itemsMergedWithTitle = self.items[:] # Inclure les titres de colones
        itemsMergedWithTitle.append(self.titles) # Inclure le corps du tableau
        col_widths = [max(len(str(column)) for column in col) for col in zip(*itemsMergedWithTitle)]

        return col_widths

    def allHistoryEntries(self):
        # Ensemble de l’historique de tous les jeux confondus
        # En vue d’établir des statistiques globales de jeu

        allHistoryEntriesList=History()
        for aGameRow in self.list:
            allHistoryEntriesList.history.extend(aGameRow.data.history.history)

        return allHistoryEntriesList

    def set_filter(self, filter_text):
        # Activer le filtre de recherche
        old_relevant_list=self.relevantList()
        self.filter_input=filter_text
        self.selected_row=self.get_new_selected_row(old_relevant_list)

    def unactivate_filter(self):
        # Désactiver le filtre de recherche
        self.filter_input=""
        self.filter_mode=False


    def get_new_selected_row(self, old_relevant_list):
        # Définir la nouvelle ligne ayant le focus après un filtre
        new_relevant_list=self.relevantList()
        old_postion=self.selected_row
        old_code=old_relevant_list[self.selected_row].data.code

        if any(row.data.code == old_code for row in new_relevant_list):
        # Si l’élement existe encore dans la liste filtrée, retourner sa position
            for index, aRow in enumerate(new_relevant_list):
                if aRow.data.code == old_code:
                    return index
        elif len(new_relevant_list) > old_postion:
        # si l’élement n’existe plus, retourner sa position (à condition que la liste soit suffisement longue)
            return old_postion
        else:
            # Sinon, retourner la dernière ligne
            return len(new_relevant_list)-1

    def relevantList(self):
        # Retourne la liste pertinante des jeux, en prenant en compte un filtre de recherche éventuel
        relevantList=[]
        if self.filter_input in [None, ""]:
            # Si aucun filtre n’est actif, retourner toute la liste
            relevantList=self.list
        else:
            # Si un filtre existe, alors retourner les jeux qui y correspondent
            for aGame in self.list:
                aGameObject=aGame.data
                if re.search(self.filter_input, aGameObject.name, re.IGNORECASE):
                    relevantList.append(aGame)
        relevantList=self.softSortBy(relevantList)
        return relevantList
