"""
Created on Tue Oct 25 20:44:05 2022
@author: CHRISTON Eliot, LEVEQUE Robin, PETARD Adrien
"""

import sys
import random
from abc import ABC, abstractmethod

from couleurs import fg
from .stockageSabOOters import dicoCartesChemin


#%% LISTE DE CARTES
class ListeCartes( list ):
    """Sous-classe de list"""
    
    def __new__(cls, data=None):
        obj = super(ListeCartes, cls).__new__(cls, data)
        return obj
    
    def __getslice__( self, start, stop) :
        return self.__class__(super(ListeCartes, self).__getslice__(start, stop))
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(super(self.__class__, self).__getitem__(key))
        else:
            return super(self.__class__, self).__getitem__(key) 
        
    def __str__(self) :
        """
        Cette fonction affiche plusieurs cartes dans la console
        """
        if len(self) == 0 : return ""
        choix =['',1]
        affichage = ''
        for j in range(3):
            for i,carte in enumerate(self):
                affichage += ' ' + str(choix[j%2]*(i+1)) + ' ' + (' '*(1-j%2))
                affichage += carte.visuColor(j)
            affichage += '\n'
        return affichage[:-1]

    def choisirCarte( self ) :
        """ self -> Carte """
        # renvoie la carte choisie par le joueur parmi celles de sa main
        # si la main est vide alors on renvoie une erreur
        if len(self) == 0 : return Carte("Erreur",[['     ',' ERR ','     ']])
        #initialisation
        choix, First = 0, True
        while not (1 <= choix <= len(self)) :
            if not First : # sauf a la premiere iteration
                print(f"1 <= choix <= {len(self)}")
            else : First = False
            while True : # tant qu'il n'y a pas d'exceptions
                try :  
                    choix = input()
                    choix = int(choix)
                except : 
                    if choix in ["quit","exit"]:
                        sys.exit() # on autorise l'utilisateur a ecrire quit ou exit pour arreter le code
                    print("ATTENTION : Veuillez renseigner un entier !") # sinon le format n'est pas le bon
                else :   break     # pas d'exceptions => c'est bien un entier
        return self[choix-1]  # la carte choisie
    
    def defausserCarte( self, carte ) :
        if carte in self : self.remove(carte)
        else : print("Cette carte ne peut pas être défaussée..")


#%% CARTES
class Carte :
    
    def __init__( self, nom, visuel ) :
        self._nom    = nom
        self._visuel = visuel

    def visuColor(self,i, parentheses = True):
        """coloration de la rangee i de l'affichage d'une carte (self._visuel[i])"""
        # on recupere la rangee a colorer
        visu = str(self._visuel[i])
        # on regarde si l'on souhaite afficher les parentheses ou non
        if not(parentheses) :
            # dans le cas ou ne veut pas de parentheses, on peut les remplacer 
            visu = visu.replace('(-', '--').replace('-)', '--').replace('(X', 'X ').replace('X)', ' X').replace('(', ' ').replace(')', ' ')
            
        if isinstance(self, CarteChemin) :
            """La coloration des cartes chemins ne s'effectue que sur certains caracteres"""
            aff = ''
            if 'END' in visu or '?' in visu : return fg.darkgrey + visu + fg.res
            for c in visu :
                if c == 'X' : aff += fg.red  + c + fg.res
                elif c == '+' : aff += fg.green+ c + fg.res
                elif c == 'S' or c == 'P' : aff += fg.yellow + c + fg.res
                else : aff += c
            return aff
        
        elif isinstance(self, CarteAction) :
            """La coloration des cartes action concerne toute la carte sauf les parentheses"""
            if   '+' in self._nom: return visu[0] + fg.green + visu[1:-1] + fg.res + visu[-1]
            elif 'x' in self._nom: return visu[0] + fg.red +   visu[1:-1] + fg.res + visu[-1]
        
        return visu

    def __str__( self ) :
        affichage = ""
        for i in range(3):
            affichage += self.visuColor(i) + "\n"
        return affichage
    
    def __eq__( self, other ) :
        if not isinstance( other, Carte ) :     return False
        if self is other :                      return True
        if self._nom != other._nom :            return False
        if self._visuel != other._visuel :      return False
        return True
        
    
class CarteChemin( Carte ) :
    """Carte qui represente le chemin des mineurs qui explorent la mine
       Ces Cartes peuvent etre posees sur le plateau de jeu"""
       
    def __init__( self, nom, visuel, logic ) :
        self._logic  = logic
        super().__init__(nom, visuel)
    
    def flip( self ) : # URDL <= DLUR
        self._logic = [self._logic[2], self._logic[3], self._logic[0], self._logic[1]]
        self._visuel = [self._visuel[2], \
                       self._visuel[1][0] + self._visuel[1][3:0:-1] + self._visuel[1][-1], \
                       self._visuel[0]]
    

class CarteVide( CarteChemin ) :
    
    def __init__( self ) :
        super().__init__("", dicoCartesChemin()[""][0], dicoCartesChemin()[""][2])


class CarteDebut( CarteChemin ) :
    
    def __init__( self ) :
        super().__init__("START", dicoCartesChemin()["START"][0], dicoCartesChemin()["START"][2])


class CarteFin( CarteChemin ) :
    
    def __init__( self, nom ) :
        self.__visible = False
        super().__init__( nom, ['( ? )','(END)','( ? )'], [1,1,1,1] )
        # on initialise le meme visuel pour les cartes fin pour que l'on ne puisse pas savoir ou se cache la pepite d'or
    
    @property
    def visible( self ) : # lecture de self.__visible (mais on ne peut toujours pas modifier l'attribut sans passer par decouvrir)
        return self.__visible
    
    def decouvrir ( self, plateau ) : # action irreversible
        self.__visible = True
        self._visuel = dicoCartesChemin()[self._nom][0] # nouveau visuel stocke dans le dictionnaire, en fonction du nom de la carteFin
        self._logic  = dicoCartesChemin()[self._nom][2] # nouvelle logique
        # on recupere la ligne et la colonne a partir des trois emplacements possibles sur le plateau
        for i in range(3) :
            if   plateau.table[2*i + plateau.posStart[0] -2][plateau.posStart[1]+8]._nom == self._nom : 
                l, c = 2*i + plateau.posStart[0] -2, plateau.posStart[1]+8 ; break
        # on supprime la carte du plateau
        plateau.table[l][c] = CarteVide()
        # on pose la nouvelle carte
        mess, posee = plateau.poserCarte( self, l, c, 'joueur') ; print(mess)
        if not posee : # si on ne peut pas poser la carte normalement
            sera_flip = random.randint(0,1)
            if sera_flip : self.flip()
            plateau.table[l][c] = self  # alors on force la pose de la carte dans une direction au hasard


class CarteAction( ABC, Carte ) :
    """ Chaque CarteAction a une sous-classe qui contient son action specifique (methode .action( self, manche ))
        La methode .action( self, manche) renvoie systematiquement un message et un booleen pour savoir si l'action
        a bien ete effectuee"""
    
    @abstractmethod
    def action( self, manche ) : pass


class CarteDefausser( CarteAction ) :
    """Cette carte est la seule CarteAction a ne pas etre dans le deck
       Elle est uniquement dans la main du joueur au moment ou il joue"""
       
    def __init__( self ) :
        super().__init__("Def", ['','Defausser',''])
        
    def action( self, manche ) :
        if len(manche.celuiQuiJoue.main) > 0 :
            if manche.celuiQuiJoue.who()=='RobOOt': # Si le joueur n'est pas humain on met une valeur par défaut et on ne demande pas d'input 
                carteChoisie = manche.celuiQuiJoue.main[0]
            if manche.celuiQuiJoue.who()=='joueur':
                print("Quelle carte voulez-vous defausser : ", end='')
                carteChoisie = manche.celuiQuiJoue.main.choisirCarte()
            manche.celuiQuiJoue.defausser( carteChoisie )
            manche.celuiQuiJoue.piocher( manche.deck )
            return "La carte est défausée !", True
        return "Vous n'avez plus de carte", True


class CarteRoF( CarteAction ) : #RoF
    
    def action( self, manche ) : # ebouler
        # ebouler = remplacer une carte par une carte vide
        print("Quelle Carte voulez-vous ébouler ?")
        if manche.celuiQuiJoue.who()=='joueur': # Permet de séparer les joueurs humains des ordinateurs
            ligne, colonne = manche.plateau.askForLC()
        if manche.celuiQuiJoue.who()=='RobOOt': # Si le joueur n'est pas humain on met une valeur par défaut et on ne demande pas d'input
            ligne, colonne = random.randint(1,manche.plateau.L-1),random.randint(1,manche.plateau.C-1)
        if manche.plateau.table[ligne][colonne] == CarteVide() :
            return "Il n'y a rien a ebouler !", False
        if manche.plateau.table[ligne][colonne] == CarteDebut() \
          or isinstance(manche.plateau.table[ligne][colonne], CarteFin):
            return "Impossible d'ebouler cette carte", False
        #else
        manche.plateau.table[ligne][colonne] = CarteVide()
        # manche.plateau.table2 = manche.plateau.checkChemin(copy.deepcopy(manche.plateau.table), CarteDebut(), manche.plateau.posStart)
        manche.plateau.updateAccess()
        return "L'eboulement enleve une carte..", True


class CarteMap( CarteAction ) : #MAP
    
    def action( self, manche ) : # devoiler / regarder CarteFin
        # pos prend les valeurs 1, 2 ou 3, 1 pour haut, 2 pour centre, 3 pour bas
        pos = 0
        if manche.celuiQuiJoue.who()=='RobOOt': pos = random.randint(1,3) # Si le joueur n'est pas humain on met une valeur par défaut et on ne demande pas d'input
        while not(1 <= pos <=3) :
            while True :
                try :     pos = int(input("Quelle CarteFin voulez-vous connaitre ?\n1 pour haut  , 2 pour centre, 3 pour bas : "))
                except :  print("ATTENTION : Veuillez renseigner un entier !")
                else :    break # pas d'exceptions => c'est bien un entier
        p = manche.plateau
        choix = [p.table[p.posStart[0]-2][p.posStart[1]+8], p.table[p.posStart[0]][p.posStart[1]+8], p.table[p.posStart[0]+2][p.posStart[1]+8]]
        choix = choix[pos-1]
        if choix._nom == "END" :
            return "OUI : Cette carte est la Pepite d'or convoitee !", True
        return "NON : Cette carte n'est pas la Pepite..", True


class CarteATT( CarteAction ) :
    
    def action( self, manche ) : # attaquer
        # construction de la liste des joueurs pour lesquels l'attaque est applicable
        ListeJoueursOkAtt = []
        for cejoueur in manche.joueurs :
            if cejoueur != manche.celuiQuiJoue and not(self in cejoueur.banc):
                ListeJoueursOkAtt.append(cejoueur)
        if len(ListeJoueursOkAtt) == 0 : return "L'attaque ne peut être effectuée sur aucun joueur ...", False
        if manche.celuiQuiJoue.who()=='RobOOt': # Si le joueur n'est pas humain on met une valeur par défaut et on ne demande pas d'input
            joueurCible = ListeJoueursOkAtt[0]
        elif manche.celuiQuiJoue.who()=='joueur': # choix d'un joueur parmi la liste
            joueurCible = manche.choisirJoueur(ListeJoueursOkAtt)
        #poser un malus sur le banc du joueur cible
        joueurCible.banc.append(self)
        return "Le malus a été posé sur le banc de " + joueurCible._nom + " !", True


class CarteDEF( CarteAction ) :
    
    def action( self, manche ) : # defendre
        # construction de la liste des joueurs pour lesquels la defense est applicable
        ListeJoueursOkDef = []
        for cejoueur in manche.joueurs :
            for carte in cejoueur.banc :
                if (carte._nom[-1] == "x") and (carte._nom[:-1] in self._nom) :
                    ListeJoueursOkDef.append(cejoueur) ; break
        if len(ListeJoueursOkDef) == 0 : return "La défense ne peut être effectuée sur aucun joueur ...", False
        if manche.celuiQuiJoue.who()=='RobOOt': # Si le joueur n'est pas humain on met une valeur par défaut et on ne demande pas d'input
            joueurCible = ListeJoueursOkDef[0]
        elif manche.celuiQuiJoue.who()=='joueur':# choix d'un joueur parmi la liste
            joueurCible = manche.choisirJoueur(ListeJoueursOkDef)
        # if malus sur banc => enlever malus
        for carte in joueurCible.banc :
            if (carte._nom[-1] == "x") and (carte._nom[:-1] in self._nom) :
                joueurCible.banc.defausserCarte(carte)
                return "Le malus a été enlevé du banc de " + joueurCible._nom + " !", True
        # else imposible de jouer, (securite, ne devrait jamais renvoyer ce message)
        return joueurCible._nom + " n'a pas de carte correspondante sur son banc.", False
