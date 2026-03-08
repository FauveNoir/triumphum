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

class VisuaColumn:
    # EXPERIMENTAL
    def __init__(self, label=None, property_=None):
        self.label=label
        self.property=property_

        listOfPossibleColumns.append(self)

def getColWidths():
    itemsMergedWithTitle = global_variables.items[:]
    itemsMergedWithTitle.append(titles)
    col_widths = [max(len(str(column[0])) for column in col) for col in zip(*itemsMergedWithTitle)]

    return col_widths

########################################################################
# Classe de la liste visuelle
########################################################################
class ListMove:
    def __init__(self, label=None, code=None):
        self.label=label
        self.code=code
        globals()[self.code] = self # Le seul objet de cette classe est TheVisualListOfGames


ListMove(label="Go up", code="goUp")
ListMove(label="Go down", code="goDown")
########################################################################
# Classe de la liste visuelle
########################################################################

class Sort:
    # EXPERIMENTAL
    def __init__(self, label=None, code=None, command=None):
        self.label = label
        self.code = code
        self.command = command

        listOflistSorting.append(self) # Adjonction à la liste des jeux


SORTING_ORDER=[True, False]


def getNextSortingOrder(currentSortingOrder):
    global SORTING_ORDER
    currentIndex=SORTING_ORDER.index(currentSortingOrder)
    tmpNextIndex=currentIndex+1
    realNextIndex=tmpNextIndex % len(SORTING_ORDER)
    nextSortingOrder=SORTING_ORDER[realNextIndex]
    
    return nextSortingOrder

class VisualListOfGames:
    def __init__(self):
        self.columns=None
        self.titles = [" ", "Titre", "Licence", "Genre", "Date", "Dernière ouverture", "Temps cumulé", "Auteur", "Studio"]
        self.list=None
        #self.relevantList=None
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
        if self.relevantList() in [None, []]:
            return True
        return False

    def getNthNLines(self, lineRank, numberOfLines):
        # Retourne une portion de la liste commençan par lineRank et contenant numberOfLines lignes
        subList = self.relevantList()[lineRank:lineRank+numberOfLines]
        return subList

    # TODO intégéré screenHeight-3 dans la déffiniton de classe
    def visualHighlightedLineNumber(self, screenHeight):
        visualHighlightedLineNumber=self.selected_row-self.firstRowOnVisibleList
        return visualHighlightedLineNumber

    def getCurrentVisibleList(self, screenHeight):
        if self.lastMove == goDown:
            if self.selected_row > self.firstRowOnVisibleList + screenHeight-4-3 :
                self.firstRowOnVisibleList+=1

        if self.lastMove == goUp:
            if self.selected_row == self.firstRowOnVisibleList +1 and self.selected_row > 1 :
                self.firstRowOnVisibleList-=1


        visibleList=self.getNthNLines(self.firstRowOnVisibleList, screenHeight-4) # TODO remplacer le 2 par une variable


        return visibleList

    def goDown(self):
        self.selected_row = min(len(self.relevantList()) - 1, self.selected_row + 1)
        self.lastMove=goDown

    def goUp(self):
        self.selected_row = max(0, self.selected_row - 1)
        self.lastMove=goUp

    def openCurrent(self):
        # Exécuter la commande de lancement du jeu associée à la ligne sélectionnée
        global HIDED_DATA_COLUMN
        setBottomBarContent(f"Ouverture de « {self.relevantList()[self.selected_row][HIDED_DATA_COLUMN].name} ».")
        game = self.relevantList()[self.selected_row][HIDED_DATA_COLUMN]
        threading.Thread(target=run_command_and_write_on_history, args=(game,)).start()

    def currentGame(self):
        # TODO factorisé un peu partout.
        game = self.relevantList()[self.selected_row][HIDED_DATA_COLUMN]
        return game

    def deleteCurrent(self):
        # Exécuter la commande de lancement du jeu associée à la ligne sélectionnée
        global HIDED_DATA_COLUMN
        setBottomBarContent(f"Supression du jeu « {self.relevantList()[self.selected_row][HIDED_DATA_COLUMN].name} ».")
        game = self.relevantList()[self.selected_row][HIDED_DATA_COLUMN]
        if self.selected_row == len(self.relevantList())-1:
            self.goUp()
            game = self.relevantList()[self.selected_row+1][HIDED_DATA_COLUMN]
        game.delete()
        self.relevantList()[self.selected_row]
        self.refresh()

    def copyLinkToClipBoard(self):
        url = self.relevantList()[self.selected_row][self.hiden_data_column_number()].url
        if url != None:
            setBottomBarContent(f"Copie de « {self.relevantList()[self.selected_row][HIDED_DATA_COLUMN].url} » dans le presse-papier.")
            pyperclip.copy(url)
        else:
            setBottomBarContent(f"Aucun lien associé à « {self.relevantList()[self.selected_row][HIDED_DATA_COLUMN].name} », rien à copier.")

    def openLink(self):
        global HIDED_DATA_COLUMN
        url = self.relevantList()[self.selected_row][HIDED_DATA_COLUMN].url  # Supposons que l'URL est stockée à l'indice 5
        if url != None:
            setBottomBarContent(f"Ouverture de « {self.relevantList()[self.selected_row][HIDED_DATA_COLUMN].url} »")
            self.refresh()
            threading.Thread(target=webbrowser.open, args=(url,)).start()
        else:
            setBottomBarContent(f"Pas de lien associé à « {self.relevantList()[self.selected_row][HIDED_DATA_COLUMN].name} »")

    def hiden_data_column_number(self):
        return len(self.list[0])-1

    def refresh(self):
        retrive_datas()
        global_variables.listOfGames

        self.list=[]
        for aGame in global_variables.listOfGames:
            self.list.append(global_variables.listOfGames[aGame].ncurseLine())

    def shiftSortingState(self, property_):
        if ( property_ == self.sortByProperty) :
            self.sortingState=getNextSortingOrder(self.sortingState)

    def isAtributeShouldBeSorted(self, attribute):
        if attribute in ["-", None]:
            return False
        if hasattr(attribute, "includeInSorting"):
            if attribute.includeInSorting == False:
                return False

        return True

    def putVoidAtEnd(self, oldList, property_):
        beginingOfNewList=[]
        endOfNewList=[]
        for item in oldList:
            if self.isAtributeShouldBeSorted(getattr(item[self.hiden_data_column_number()], property_)) :
                beginingOfNewList.append(item)
            else:
                endOfNewList.append(item)
        newList= beginingOfNewList + endOfNewList
        return newList

    def softSortBy(self, relevantList):
        property_=self.sortByProperty
        if property_:
            tmpList0=relevantList
            tmpList1 = sorted(tmpList0, 
                             reverse=self.sortingState, 
                             key=lambda x: (getattr(x[self.hiden_data_column_number()], property_) is None, 
                                            getattr(x[self.hiden_data_column_number()], property_)))

            tmpList2=self.putVoidAtEnd(tmpList1, property_)
            return tmpList2
        return relevantList

    def sortBy(self, property_):
        self.shiftSortingState(property_)
        self.sortByProperty=property_

    def columnsWidth(self):
        itemsMergedWithTitle = self.items[:]
        itemsMergedWithTitle.append(self.titles)
        col_widths = [max(len(str(column)) for column in col) for col in zip(*itemsMergedWithTitle)]

        return col_widths

    def allHistoryEntries(self):
        global HIDED_DATA_COLUMN

        allHistoryEntriesList=History()
        for aGameRow in self.list:
            allHistoryEntriesList.history.extend(aGameRow[HIDED_DATA_COLUMN].history.history)

        return allHistoryEntriesList

    def set_filter(self, filter_text):
        old_relevant_list=self.relevantList()
        self.filter_input=filter_text
        self.selected_row=self.get_new_selected_row(old_relevant_list)

    def unactivate_filter(self):
        self.filter_input=""
        self.filter_mode=False


    def get_new_selected_row(self, old_relevant_list):
        global HIDED_DATA_COLUMN
        new_relevant_list=self.relevantList()
        old_postion=self.selected_row
        old_code=old_relevant_list[self.selected_row][HIDED_DATA_COLUMN].code

        if any(row[-1].code == old_code for row in new_relevant_list):
        # Si l’élement existe encore dans la liste filtrée, retourner sa position
            for index, aRow in enumerate(new_relevant_list):
                if aRow[-1].code == old_code:
                    return index
        elif len(new_relevant_list) > old_postion:
        # si l’élement n’existe plus, retourner sa position (à condition que la liste soit suffisement longue)
            return old_postion
        else:
            # Sinon, retourner la dernière ligne
            return len(new_relevant_list)-1

    def relevantList(self):
        relevantList=[]
        if self.filter_input in [None, ""]:
            relevantList=self.list
        else:
            for aGame in self.list:
                aGameObject=aGame[self.hiden_data_column_number()]
                if re.search(self.filter_input, aGameObject.name, re.IGNORECASE):
                    relevantList.append(aGame)
        relevantList=self.softSortBy(relevantList)
        return relevantList
