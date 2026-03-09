#!/usr/bin/python3

########################################################################
# Fonction de l’autocompletion
########################################################################
from triumphum.global_variables import *
from triumphum.debug import * # TODO

def deleteBlancLines(chaine):
    #Supression d’éventuelles lignes blanches

    # Divise la chaîne en lignes individuelles
    lignes = chaine.splitlines()
    
    # Filtre les lignes qui ne sont pas vides
    lignes_non_vides = [ligne for ligne in lignes if ligne.strip() != '']
    
    # Rejoint les lignes non vides en une seule chaîne
    chaine_sans_lignes_vides = '\n'.join(lignes_non_vides)
    
    return chaine_sans_lignes_vides

def listAllObjectsCodeOfClassCodePerLine(listOfObjectsOfClass):
    # Constructeur des chaines d’autocompletion par objet à autocmpletéer
    # Cette fonction est le cas générique des constructeur des formules d’autocompletion.
    listOfCodes=""
    for anObject in listOfObjectsOfClass:
        listOfCodes+=f"'{anObject}[{listOfObjectsOfClass[anObject].name}]' "
    return deleteBlancLines(listOfCodes)

def listOfAllGamesCodePerLine():
    return listAllObjectsCodeOfClassCodePerLine(listOfGames)

def listOfAllLicencesCodePerLine():
    return listAllObjectsCodeOfClassCodePerLine(listOfLicences)

def listOfAllGenresCodePerLine():
    return listAllObjectsCodeOfClassCodePerLine(listOfGenres)

def listOfAllPlatformsCodePerLine():
    return listAllObjectsCodeOfClassCodePerLine(listOfPlatforms)
