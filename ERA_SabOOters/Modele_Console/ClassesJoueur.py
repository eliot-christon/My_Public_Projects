"""
Created on Tue Oct 25 20:44:05 2022
@author: CHRISTON Eliot, LEVEQUE Robin, PETARD Adrien
"""

from .ClassesCarte import ListeCartes,Carte,CarteATT
from couleurs import fg

#%% JOUEUR
class Joueur :
    
    def __init__( self, nom, role, main, banc ) :
        self._nom = nom
        self.__role = role
        self.main = main
        self.banc = banc
        self.score = []
    
    @property
    def role(self):
        return self.__role
    
    @role.setter
    def role(self,r):
        if r in [fg.red+"Saboteur"+fg.res , fg.green+"Nain"+fg.res]:
            self.__role = r 
    
    def __str__( self ) :
        mess = self._nom + " (" + self.role + "), Score : " + str(self.score) +'\n'
        mess += self.banc.__str__()
        return mess
    
    def __eq__( self, other ) :
        if not isinstance( other, Joueur ) :    return False
        if self is other :                      return True
        if self._nom != other._nom :            return False
        if self.role != other.role :            return False
        if self.main != other.main :            return False
        if self.banc != other.banc :            return False
        if self.score != other.score :          return False
        return True
    
    def piocher( self, deck ) :
        if isinstance(deck, Carte) : 
            self.main.append( deck )
        elif isinstance(deck, ListeCartes) and len(deck) > 0 : # si le deck est vide, on entre pas dans la condition
            cartePiochee = deck[0]
            deck.defausserCarte( cartePiochee )
            self.main.append( cartePiochee )

    def defausser( self, carte ) :
        return self.main.defausserCarte( carte )
    
    def estBloque( self ) :
        """None -> bool"""
        for carte in self.banc :
            # Si le joueur a une carte attaque sur son banc, alors il est bloque
            if isinstance(carte, CarteATT) : return True
        return False
    
    def who(self):
        return 'joueur'

class RobOOt(Joueur):
    """Cette classe h??rite directement de Joueur ce qui lui permet de faire exactement les m??me actions qu'un joueur humain.
    Cependant, dans ce code, les ordinateurs n'ont pas d'intelligence, ils jouent al??atoirement.
    Dans tout le code, ?? chaque fois qu'un input utilisateur est demand??, on le remplace par une valeur par d??faut souvent al??atoire.
    Pour aller plus loin : on cr??e des m??thodes pour chaque choix qui sont d??finies selon le 'niveau d'intelligence' de l'ordinateur.
    """
    def __init__( self, nom, role, main, banc):
       super().__init__(nom, role, main, banc)
    def who(self):
        return 'RobOOt'


