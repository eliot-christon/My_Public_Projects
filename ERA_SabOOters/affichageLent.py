"""
Created on Tue Oct 25 20:44:05 2022
@author: CHRISTON Eliot, LEVEQUE Robin, PETARD Adrien
"""
import sys
from time import sleep

def ecriture(text, t = 0.01):
    """defilement du texte"""
    for c in text:
        print(c, end='')
        sys.stdout.flush()
        sleep(t)
    print()