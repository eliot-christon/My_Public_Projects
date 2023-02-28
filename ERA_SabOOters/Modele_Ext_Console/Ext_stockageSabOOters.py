"""
Created on Tue Oct 25 20:44:05 2022
@author: CHRISTON Eliot, LEVEQUE Robin, PETARD Adrien
"""

from couleurs import *

def dicoCartesChemin():
    dico = { # nom : (visuel, nombre, logique)
    ""      : (['     ','     ','     '], 0, [ 0, 0, 0, 0]),
    "START" : (['( | )','(-S-)','( | )'], 0, [ 1, 1, 1, 1]),
    "ST-UR" : (['( | )','( o-)','(   )'], 0, [ 1, 1, 0, 0]),
    "ST-UL" : (['( | )','(-o )','(   )'], 0, [ 1, 0, 0, 1]),
    "END"   : (['( | )','(-P-)','( | )'], 0, [ 1, 1, 1, 1]),
    "URDL+"	: (['( | )','(-+-)','( | )'], 5, [ 1, 1, 1, 1]),
    "URD+"	: (['( | )','( +-)','( | )'], 5, [ 1, 1, 1, 0]),
    "URL+"	: (['( | )','(-+-)','(   )'], 5, [ 1, 1, 0, 1]),
    "UR+"	: (['( | )','( +-)','(   )'], 5, [ 1, 1, 0, 0]),
    "UL+"	: (['( | )','(-+ )','(   )'], 4, [ 1, 0, 0, 1]),
    "UD+"	: (['( | )','( | )','( | )'], 4, [ 1, 0, 1, 0]),
    "RL+"	: (['(   )','(---)','(   )'], 3, [ 0, 1, 0, 1]),
    "URDLx"	: (['( | )','(-X-)','( | )'], 1, [-1,-1,-1,-1]),
    "URDx"	: (['( | )','( X-)','( | )'], 1, [-1,-1,-1, 0]),
    "URLx"	: (['( | )','(-X-)','(   )'], 1, [-1,-1, 0,-1]),
    "URx"	: (['( | )','( X-)','(   )'], 1, [-1,-1, 0, 0]),
    "ULx"	: (['( | )','(-X )','(   )'], 1, [-1, 0, 0,-1]),
    "UDx"	: (['( | )','( X )','( | )'], 1, [-1, 0,-1, 0]),
    "RLx"	: (['(   )','(-X-)','(   )'], 1, [ 0,-1, 0,-1]),
    "Ux"	: (['( | )','( X )','(   )'], 1, [-1, 0, 0, 0]),
    "Rx"	: (['(   )','( X-)','(   )'], 1, [ 0,-1, 0, 0]),
    # Cartes de l'extension :
    #    E   : Echelle
    #    B,V : Porte Bleue et Porte Verte
    #    C   : Cristal
    "UR+DL+" : (['( | )','(-\-)','( | )'], 1, [ 1, 1, 2, 2]),
    "UL+RD+" : (['( | )','(-/-)','( | )'], 1, [ 1, 2, 2, 1]),
    "UD+RL+" : (['( | )','(---)','( | )'], 2, [ 1, 2, 1, 2]),
    "UD+RLx" : (['( | )','(X|X)','( | )'], 1, [ 1,-1, 1,-1]),
    "RL+UDx" : (['( X )','(---)','( X )'], 1, [-1, 1,-1, 1]),
    "UD+Rx"  : (['( | )','( |X)','( | )'], 1, [ 1,-1, 1, 0]),
    "UL+Dx"  : (['( | )','(-+ )','( X )'], 1, [ 1, 0,-1, 1]),
    "RD+Ux"  : (['( X )','( +-)','( | )'], 1, [-1, 1, 1, 0]),
    "UR+Dx"  : (['( | )','( +-)','( X )'], 1, [ 1, 1,-1, 0]),
    "UR+E"   : (['( | )','( E-)','(   )'], 1, [ 1, 1, 0, 0]),
    "UL+E"   : (['( | )','(-E )','(   )'], 1, [ 1, 0, 0, 1]),
    "UxE"    : (['( | )','( E )','(   )'], 1, [ 1, 0, 0, 0]),
    "RxE"    : (['(   )','( E-)','(   )'], 1, [ 0, 1, 0, 0]),
    "UD+B"   : (['( | )','( B )','( | )'], 1, [ 1, 0, 1, 0]),
    "UR+B"   : (['( | )','( B-)','(   )'], 1, [ 1, 1, 0, 0]),
    "RL+B"   : (['(   )','(-B-)','(   )'], 1, [ 0, 1, 0, 1]),
    "UL+V"   : (['( | )','(-V )','(   )'], 1, [ 1, 0, 0, 1]),
    "RL+V"   : (['(   )','(-V-)','(   )'], 1, [ 0, 1, 0, 1]),
    "UD+RxV" : (['( | )','( VX)','( | )'], 1, [ 1,-1, 1, 0]),
    "URDL+C" : (['( | )','(-C-)','( | )'], 1, [ 1, 1, 1, 1]),
    "URD+LxC": (['( | )','(XC-)','( | )'], 1, [ 1, 1, 1,-1]),
    "URL+DxC": (['( | )','(-C-)','( X )'], 1, [ 1, 1,-1, 1]),
    "RL+UxC" : (['( X )','(-C-)','(   )'], 1, [-1, 1, 0, 1]),
    "URD+C"  : (['( | )','( C-)','( | )'], 1, [ 1, 1, 1, 0]),
    "URL+C"  : (['( | )','(-C-)','(   )'], 3, [ 1, 1, 0, 1]),
    "UxC"    : (['( | )','( C )','(   )'], 1, [-1, 0, 0, 0]),
    "RxC"    : (['(   )','( C-)','(   )'], 1, [ 0,-1, 0, 0]),
    }
    return dico

def dicoCartesAction():
    dico = { # nom : (visuel, nombre)
    "Li+" : (['(DEF)','(Li )','(   )'],2),
    "P+"  : (['(DEF)','(P  )','(   )'],2),
    "W+"  : (['(DEF)','(W  )','(   )'],2),
    "LiP+": (['(DEF)','(Li )','(P  )'],1),
    "LiW+": (['(DEF)','(Li )','(W  )'],1),
    "PW+" : (['(DEF)','(P  )','(W  )'],1),
    "Lix" : (['(ATT)','(Li )','(   )'],3),
    "Px"  : (['(ATT)','(P  )','(   )'],3),
    "Wx"  : (['(ATT)','(W  )','(   )'],3),
    "RoF" : (['(   )','(RoF)','(   )'],4),  # +1 avec l'extension
    "MAP" : (['(   )','(MAP)','(   )'],6),
    # Cartes de l'extension :
    "Pri+" : (['(DEF)','(Pri)','(   )'],4),
    "Vol-" : (['(ATT)','(Vol)','(   )'],3),
    "Prix" : (['(ATT)','(Pri)','(   )'],3),
    "Vol#" : (['(BE )','(Vol)','(   )'],4),
    "VuR"  : (['(   )','(VuR)','(   )'],2), # Voir un Role
    "CdR"  : (['(   )','(CdR)','(   )'],2), # Changer de Role
    "CdM"  : (['(   )','(CdM)','(   )'],2)  # Changer de Main
    }
    return dico


def dicoRoles():
    dico = { # nb_joueurs : [nb_saboteurs, nb_nains]
    fg.green+"NainVert"+fg.res : 4,
    fg.blue+"NainBleu"+fg.res : 4,
    fg.red+"Saboteur"+fg.res : 3,
    fg.cyan+"Géologue"+fg.res : 2,
    fg.darkgrey+"Profiteur"+fg.res : 1,
    fg.blue+"Bo"+fg.green+"ss"+fg.res : 1
    }
    return dico
