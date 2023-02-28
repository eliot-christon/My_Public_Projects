"""
Created on Tue Oct 25 20:44:05 2022
@author: CHRISTON Eliot, LEVEQUE Robin, PETARD Adrien
"""
from os import name, system

#%% CLEAR CONSOLE

def clear():
    """Fonction qui print 100 retour à la ligne dans la console avant d'effacer son contenu
    Grace aux retours a la ligne, on peut acceder a l'historique de la partie en scrollant vers le haut"""
    print("\n" * 100)
    if name == 'nt': system('cls')   # pour windows
    else :           system("clear") # pour autre os