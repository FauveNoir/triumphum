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
        self.relevantList=None
        self.sortByProperty=None
        self.sortingState=SORTING_ORDER[1]
        self.selected_row = 0
        self.firstRowOnVisibleList = 0
        self.lastMove=None

        self.refresh()
        global_variables.THE_VISUAL_LIST_OF_GAMES = self # Le seul objet de cette classe est TheVisualListOfGames

    def isTheListEmpty(self):
        if self.list in [None, []]:
            return True
        return False

    def getNthNLines(self, lineRank, numberOfLines):
        # Retourne une portion de la liste commençan par lineRank et contenant numberOfLines lignes
        subList = self.list[lineRank:lineRank+numberOfLines]
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
        self.selected_row = min(len(self.list) - 1, self.selected_row + 1)
        self.lastMove=goDown

    def goUp(self):
        self.selected_row = max(0, self.selected_row - 1)
        self.lastMove=goUp

    def openCurrent(self):
        # Exécuter la commande de lancement du jeu associée à la ligne sélectionnée
        global HIDED_DATA_COLUMN
        setBottomBarContent(f"Ouverture de « {self.list[self.selected_row][HIDED_DATA_COLUMN].name} ».")
        game = self.list[self.selected_row][HIDED_DATA_COLUMN]
        threading.Thread(target=run_command_and_write_on_history, args=(game,)).start()

    def currentGame(self):
        # TODO factorisé un peu partout.
        game = self.list[self.selected_row][HIDED_DATA_COLUMN]
        return game

    def deleteCurrent(self):
        # Exécuter la commande de lancement du jeu associée à la ligne sélectionnée
        global HIDED_DATA_COLUMN
        setBottomBarContent(f"Supression du jeu « {self.list[self.selected_row][HIDED_DATA_COLUMN].name} ».")
        game = self.list[self.selected_row][HIDED_DATA_COLUMN]
        if self.selected_row == len(self.list)-1:
            self.goUp()
            game = self.list[self.selected_row+1][HIDED_DATA_COLUMN]
        game.delete()
        writeInTmp("deletion done")
        self.list[self.selected_row]
        self.refresh()

    def copyLinkToClipBoard(self):
        url = self.list[self.selected_row][self.hiden_data_column_number()].url
        if url != None:
            setBottomBarContent(f"Copie de « {self.list[self.selected_row][HIDED_DATA_COLUMN].url} » dans le presse-papier.")
            pyperclip.copy(url)
        else:
            setBottomBarContent(f"Aucun lien associé à « {self.list[self.selected_row][HIDED_DATA_COLUMN].name} », rien à copier.")

    def openLink(self):
        global HIDED_DATA_COLUMN
        url = self.list[self.selected_row][HIDED_DATA_COLUMN].url  # Supposons que l'URL est stockée à l'indice 5
        if url != None:
            setBottomBarContent(f"Ouverture de « {self.list[self.selected_row][HIDED_DATA_COLUMN].url} »")
            self.refresh()
            threading.Thread(target=webbrowser.open, args=(url,)).start()
        else:
            setBottomBarContent(f"Pas de lien associé à « {self.list[self.selected_row][HIDED_DATA_COLUMN].name} »")

    def hiden_data_column_number(self):
        return len(self.list[0])-1

    def refresh(self):
        retrive_datas()
        global_variables.listOfGames

        self.list=[]
        for aGame in global_variables.listOfGames:
            self.list.append(global_variables.listOfGames[aGame].ncurseLine())
        self.softSortBy(self.sortByProperty)

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

    def softSortBy(self, property_):
        if property_:
            self.sortByProperty=property_
            tmpList0=self.list
            tmpList1 = sorted(tmpList0, 
                             reverse=self.sortingState, 
                             key=lambda x: (getattr(x[self.hiden_data_column_number()], property_) is None, 
                                            getattr(x[self.hiden_data_column_number()], property_)))

            tmpList2=self.putVoidAtEnd(tmpList1, property_)
            # Déplacer les entrées avec property_ == "-" à la fin
            self.list=tmpList2

    def sortBy(self, property_):
        self.shiftSortingState(property_)
        self.softSortBy(property_)

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

    def filterByPattern(self, pattern):
        self.relevantList=[]
        for aGame in self.list:
            aGameObject=aGame[self.hiden_data_column_number()]
            if re.search(pattern, aGameObject.name, re.IGNORECASE):
                self.relevantList.append(aGame)
        writeInTmp(self.relevantList)
