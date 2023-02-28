"""
Created on Tue Oct 25 20:44:05 2022
@author: CHRISTON Eliot, LEVEQUE Robin, PETARD Adrien
"""
# Main

from time import sleep

import Modele_Console.ClassesCarte as C
import Modele_Console.ClassesJoueur as C 
import Modele_Console.ClassesPartie as C
import Modele_Ext_Console.Ext_ClassesCarte as Ext
import Modele_Ext_Console.Ext_ClassesJoueur as Ext
import Modele_Ext_Console.Ext_ClassesPartie as Ext
from Modele_Ext_Console import Ext_Regles
from Modele_Console import Regles

from couleurs import fg,colors
from affichageLent import ecriture
from clearConsole import clear


def debutJeu() :
    clear() ; print("\n\n\n"+fg.green+fg.bold+'3'+fg.res) ; sleep(1)
    clear() ; print("\n\n\n"+fg.green+fg.bold+'2'+fg.res) ; sleep(1)
    clear() ; print("\n\n\n"+fg.green+fg.bold+'1'+fg.res) ; sleep(1)
    clear() ; print("\n\n\n"+fg.green+fg.bold+'DEBUT DU JEU !\n\n'+fg.res) ; sleep(1)


affMenu1 = '\n' + colors.underline + "MENU PRINCIPAL\n" + colors.res +"\
   1    :   Jeu de base\n\
   2    :   Extension\n\
   Autre:   Exit\n"

while True :

    clear()
    print(fg.pink+fg.bold+fg.underline+"Bienvenue sur SabOOters !\n"+fg.res)
    ecriture("Vous pouvez choisir de jouer "+fg.bold+"AVEC"+fg.res+" ou "+fg.bold+"SANS"+fg.res+" extension !", t=0.02)
    print(affMenu1)
       
    try : # on demande des valeurs entieres a l'utilisateur
        UserIn = int(input("Veuillez choisir votre jeu : "))
    except : 
        UserIn = 0 # Exit


    # partie sans extension
    if UserIn == 1 :
        UserInRegles = input("Souhaitez-vous afficher les règles ? o/n : ")
        if UserInRegles in ['o', 'oui', 'y', 'yes', 'O', 'Oui', 'Y', 'Yes', '0'] :
            Regles.regles()
        debutJeu()
        mapartie = C.Partie()
    
    # partie avec extension
    elif UserIn == 2 :
        UserInRegles = input("Souhaitez-vous afficher les règles ? o/n : ")
        if UserInRegles in ['o', 'oui', 'y', 'yes', 'O', 'Oui', 'Y', 'Yes', '0'] :
            Ext_Regles.regles()
        debutJeu()
        mapartie = Ext.Partie()
    
    # Exit
    else : 
        break
    
    mapartie.jouerPartie()
    print(fg.green + fg.bold +"\n\nFin de la partie" + fg.res)
    sleep(3)
    clear()
    

print(fg.pink + fg.bold +"\nA bientôt !" + fg.res)