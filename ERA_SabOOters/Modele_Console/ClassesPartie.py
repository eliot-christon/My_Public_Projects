"""
Created on Tue Oct 25 20:44:05 2022
@author: CHRISTON Eliot, LEVEQUE Robin, PETARD Adrien
"""

import sys
import random
from random import shuffle
from time import sleep

from couleurs import fg,colors
from clearConsole import clear
from affichageLent import ecriture
from .stockageSabOOters import dicoCartesAction,dicoCartesChemin,dicoRoles
from .ClassesCarte import *
from .ClassesJoueur import Joueur,RobOOt

#%% PLATEAU
class Plateau:
    
    def __init__(self, tableau_de_cartes = [[]], posStart = [0,0], parentheses = True):
        self.__C = len(tableau_de_cartes[0]) # nb de colonnes du tableau
        self.__L = len(tableau_de_cartes)    # nb de lignes du tableau
        self.table = tableau_de_cartes     # tableau de cartes
        self.posStart = posStart           # position de la carte de depart
        self.positionsPossibles = []       # liste d'emplacements libres relies a la carte START
        self.parentheses = parentheses     # le plateau peut etre affiche avec ou sans parentheses
            
    @property
    def C(self):
        return self.__C
    
    @property
    def L(self):
        return self.__L
    
    def __str__(self):
        affichage = ""
        if self.table == [[]] : # si le tableau est vide, on affiche rien
            return affichage
        #else
        lignes =['',1]
        affichage += "  |" +''.join(f"  {i} "+' '*(2-len(str(i))) for i in range(1,self.__C-1)) + '\n'
        affichage += "--+" + (self.__C-2)*5*"-" + '\n'
        for i in range(1,self.__L-1):
            for k in range(3):
                affichage += str(lignes[k%2]*i) + ' '*(2-len(str(lignes[k%2]*i))) + "|"
                for j in range(1,self.__C-1):
                    affichage += self.table[i][j].visuColor(k, self.parentheses)
                affichage += '\n'
        affichage += "--+" + (self.__C-2)*5*"-"
        return affichage
    
    def checkAgrandir( self, l, c ) : # On verifie si le plateau a besoin d'etre agrandi et dans quelle direction
        if   l == 0 :          self.agrandir('N')
        elif l == (self.__L-1) : self.agrandir('S')
        if   c == 0 :          self.agrandir('O')
        elif c == (self.__C-1) : self.agrandir('E')
    
    def agrandir( self, direction ) :
        # direction contient 'N' ou 'S' ou 'E' ou 'O'
        nord, sud, est, ouest = 0, 0, 0, 0
        
        for s in direction :
            if   s == 'N' : nord  += 1 ; self.posStart[0] += 1
            elif s == 'S' : sud   += 1
            elif s == 'E' : est   += 1
            elif s == 'O' : ouest += 1 ; self.posStart[1] += 1

        if nord == 0 and sud == 0 and est == 0 and ouest == 0 :
            return "Pas d'agrandissement"
        
        new_table = [[CarteVide() for _ in range(self.__C + ouest + est)] for _ in range(self.__L + nord + sud)]
                
        for l in range(len(new_table)):
            for c in range(len(new_table[0])):
                if (0 <= l - nord < self.__L) and (0 <= c - ouest < self.__C) :
                    new_table[l][c] = self.table[l - nord][c - ouest]
                else : pass
        
        self.__C = len(new_table[0]) # nb de colonnes du tableau
        self.__L = len(new_table)    # nb de lignes du tableau
        self.table = new_table
        return 'Agrandissement effectué'
    
    def config_initiale(self, lignes = 5, colonnes = 9) :
        ordre = ["ST-UR", "ST-UL", "END"]
        shuffle( ordre )
        table = [] # future grille du plateau contenant les cartes
        for i in range(lignes+2) :
            table.append([])
            for j in range(colonnes+2) :
                table[i].append(CarteVide())
        
        table[3][1] = CarteDebut()
        for i, c in enumerate( ordre ):
            table[2*i+1][colonnes] = CarteFin(c)
        
        self.__C = colonnes+2 # par soucis de lisibilite
        self.__L = lignes+2   # par soucis de lisibilite
        self.table = table
        self.posStart = [3,1]
        self.updateAccess()
    
    def askForLC( self ) :
        """ None -> int * int
        Demande a l'utilisateur de renseigner une ligne et une colonne valide selon le plateau
        """
        ligne, colonne, First = -1, -1, True
        while not(0 <= ligne < self.__L) or not(0 <= colonne < self.__C) :
            if not First : # sauf a la premiere iteration
                print("Placement non valide : \n"+ \
                        "\t0 <= ligne <= " + str(self.__L-1) + "\n" \
                        "\t0 <= colonne <= " + str(self.__C-1) + "\n")
            else : First = False
            while True : # Tant qu'il y a une exception
                try : # on demande des valeurs entieres a l'utilisateur
                    UserIn = input("Veuillez choisir une position : ligne,colonne : ").split(',')
                    ligne   = int(UserIn[0])
                    colonne = int(UserIn[1])
                except : 
                    if UserIn[0] in ["quit","exit"]:
                        sys.exit() # on autorise l'utilisateur a ecrire quit ou exit pour arreter le code
                    print("ATTENTION : Veuillez renseigner un entier !")
                else :   break # pas d'exceptions => c'est bien un entier
        return ligne, colonne
    
    def checkEmplacement( self, carte, ligne, colonne ) :
        """ CarteChemin * int * int -> String
        Teste les connections entre les cartes pour verifier qu'il est possible de
        poser la carte souhaitee dans la position souhaitee sur le plateau.
        connections : Up avec Down de la carte du dessus
                    Right avec Left de la carte de droite
                    Down avec Up de la carte du dessous
                    Left avec Right de la carte de gauche
        """
        if not(0 <= ligne < self.__L) or not(0 <= colonne < self.__C) : # normalement deja controle avant l'appel de la fonction, mais c'est une securite
            return "Placement non valide : \n\t0 <= ligne <= " + str(self.__L-1) + "\n\t0 <= colonne <= " + str(self.__C-1)
        if  not(isinstance(self.table[ligne][colonne], CarteVide)) :
            return "Une carte est deja posee a cet endroit"
        if not((ligne,colonne) in self.positionsPossibles) :
            return "Pas de connection avec la carte de début.."
        
        zero_co_cmpt = 0    # nombre d'absence de connections (mur contre mur) ou (chemin vers vide/fin_non_devoilee)
        
        for i in range(4) : # car 4 cartes voisines, U, R, D, L
            l, c = ligne + (i-1)*((i+1)%2), colonne + (2-i)*(i%2)
            connect = (0,0)
            if not(0 <= l < self.__L) or not(0 <= c < self.__C) : # si bord adjacent alors absence de connexion
                carte_voisine = CarteVide( )
            else :
                carte_voisine = self.table[l][c]
                connect = (carte._logic[i], carte_voisine._logic[(i+2)%4])
            
            if connect == (0,0) or isinstance(carte_voisine, CarteVide) \
                    or (isinstance(carte_voisine, CarteFin) and not(carte_voisine.visible)):
                zero_co_cmpt += 1
            elif connect[0] == 0 or connect[1] == 0 :
                return "Chemins incompatibles"
            
        if zero_co_cmpt == 4 :      return "Pas de chemin connecté"
        return "Placement valide"          
 
    def poserCarte( self, carte, ligne, colonne, typeJoueur) :
        """ CarteChemin -> String * bool
        Methode qui effectue la pose d'une carte sur un plateau et renvoie la statut de la pose
        Elle s'appuie sur checkEmplacement()
        On verifie toutes les possibilites de pose de cette carte et s'il en
        existe plusieurs on demande a l'utilisateur laquelle il prefere
        """
        C1 = CarteChemin( carte._nom, carte._visuel, carte._logic )
        C2 = CarteChemin( carte._nom, carte._visuel, carte._logic )
        C2.flip()
        
        mess1 = self.checkEmplacement( C1, ligne, colonne )
        mess2 = self.checkEmplacement( C2, ligne, colonne )
        
        if mess1 != "Placement valide" and mess2 != "Placement valide":
            return(mess1, False) # placement invalide
        elif mess1 == "Placement valide" and mess2 == "Placement valide" and C1._logic != C2._logic :
            if typeJoueur == 'joueur': # Permet de séparer les joueurs humains des ordinateurs
                print("Deux choix possibles")
                deuxChoix = ListeCartes([C1 , C2])
                print( deuxChoix ,end='')
                print("\n1 ou 2 : " ,end='')
                choice = deuxChoix.choisirCarte()
            if typeJoueur == 'RobOOt': choice = random.choice([C1 , C2]) # Si le joueur n'est pas humain on met une valeur par défaut et on ne demande pas d'input
            self.table[ligne][colonne] = choice ; del C1 ; del C2
            return("La carte a ete placee !", True)
        elif mess1 == "Placement valide":
            self.table[ligne][colonne] = C1 ; del C2
            return("La carte a ete placee !", True)
        elif mess2 == "Placement valide":
            carte.flip()
            self.table[ligne][colonne] = C2 ; del C1
            return("La carte a ete placee !", True)
        return("Impossible", False) # else    

    def distanceEnd( self, x, y ) :
        """distance au carre entre la carte END centrale et une carte de coordonnee x, y"""
        xEND, yEND = self.posStart[0] , self.posStart[1] + 8
        return ( (x-xEND)**2 + (y-yEND)**2 )
    
    def updateAccess( self ) :
        """update l'attribut self.positionsPossibles, qui est un tableau de booleens qui indiquent les cartes voisines qui sont reliees a la carte de debut"""
        ## initialisation
        res = False                       # le resultat, True si il y a une connection du debut a la fin
        self.positionsPossibles = []      # tableau de la meme taille que le plateau
        coord_non_visitees = []           # liste de coordonnees non visitees 
        coord_visitees = [self.posStart]  # liste de coordonnees visitees
        
        # on va parcourir en profondeur l'arbre des connections. En partant de la carte Start
        l, c = self.posStart[0], self.posStart[1]
        carte_courante = self.table[l][c]
        for k in range(4) :
            other_l, other_c = l + (k-1)*((k+1)%2), c + (2-k)*(k%2) # On regarde les cartes voisines, et on les ajoute a la liste des cartes a visiter
            coord_non_visitees.append( (other_l, other_c) )         # On souhaite forcement visiter toutes les cartes voisines a partir de la carte de debut
        
        ## recherche en profondeur
        while len(coord_non_visitees) > 0 :    # tant qu'il y a des coordonnees a visiter
            l, c = coord_non_visitees[-1][0], coord_non_visitees[-1][1] # on prend le dernier ajout dans la liste
            coord_visitees.append( (l,c) )     # on considere ces nouvelles coordonnees comme "visitees" pour la suite
            coord_non_visitees.pop(-1)         # elle ne sont donc plus "a visiter"
            carte_courante = self.table[l][c]  # changement de carte courante
            
            if not isinstance(carte_courante, CarteVide) and ('+' in carte_courante._nom) or  ( isinstance(carte_courante, CarteFin) and carte_courante.visible ) :
                # si ce n'est pas une carte vide et qu'elle contient au moins une connection ('+' dans le nom)
                for k in range(4) : # On regarde les cartes voisines
                    other_l, other_c = l + (k-1)*((k+1)%2), c + (2-k)*(k%2)
                    if self.table[l][c]._logic[k] > 0 and not((other_l,other_c) in coord_visitees) \
                            and ( not( isinstance(self.table[other_l][other_c], CarteFin) ) or self.table[other_l][other_c]._logic[(k+2)%4] > 0 ):
                        # s'il y a un chemin vers une carte, mais n'est pas ajoute a la liste des coordonnees a visiter
                        coord_non_visitees.append( (other_l, other_c) ) # on l'ajoute a cette liste
            elif isinstance(carte_courante, CarteVide) :
                self.positionsPossibles.append((l,c))
            elif isinstance(carte_courante, CarteFin) and not(carte_courante.visible) :
                self.positionsPossibles.append((l,c))
                carte_courante.decouvrir( self )
                if carte_courante._nom == "END" : res = True ; break
        
        # on trie les emplacements disponibles du plus proche de la carte END du milieu au plus lointain
        # choix arbitraire pour les RobOOts
        self.positionsPossibles = sorted(self.positionsPossibles, key=lambda pos: self.distanceEnd(pos[0], pos[1]))
        
        return res







#%% MANCHE

class Manche :
    """Chaque partie est constituee de 3 manches. Dans chaque manche il y a les joueurs de la partie, un nouveau plateau, un nouveau deck de cartes,
    et le reste des cartes or = pepites restantes. On decide egalement de garder en memoire le joueur qui joue"""
    
    def __init__( self, listeDeJoueurs, pepitesRestantes, affParentheses = False ) :
        self.joueurs = listeDeJoueurs
        self.celuiQuiJoue = listeDeJoueurs[0] # Contient le joueur courant
        self.plateau = Plateau(parentheses = affParentheses) ; self.plateau.config_initiale()
        self.restePepites = pepitesRestantes
        self.NewDeck() # self.deck # creation d'un deck
    
    def NewDeck( self ):
        """Methode qui cree un nouveau deck"""
        deck = []
        for k, v in dicoCartesChemin().items() :
            for _ in range(v[1]):
                deck.append(CarteChemin(k, v[0], v[2]))
            
        for k, v in dicoCartesAction().items() :
            for _ in range(v[1]):
                if k[-1] == "+" :    deck.append(CarteDEF(k, v[0]))
                elif k[-1] == "x" :  deck.append(CarteATT(k, v[0]))
                elif k == "MAP" :    deck.append(CarteMap(k, v[0]))
                elif k == "RoF" :    deck.append(CarteRoF(k, v[0]))
                else : print("Erreur : Carte Action sans sous-classe")
                
        shuffle(deck)
        self.deck = ListeCartes(deck)

    def distribuerMains( self ) :
        """On distribue le bon nombre de cartes a chaque joueur en debut de manche"""
        # Hyp: len(joueurs) > 2 sinon 7 cartes
        nb_cartes = 7
        for i in [3,6,8]:
            if len(self.joueurs)>=i:
                nb_cartes-=1
        
        # Piocher dans le deck et ajouter a la main d'un joueur
        for joueurCourant in self.joueurs:
            joueurCourant.main = ListeCartes([])
            joueurCourant.banc = ListeCartes([])
            for _ in range(nb_cartes):
                # hyp: len(deck) > 0 a chaque iteration
                joueurCourant.piocher( self.deck )
    
    def assignerRoles( self ) :
        """Chaque joueur se voit assigner un nouveau role"""
        nbRoles = dicoRoles()[len(self.joueurs)] # on recupere [nb_saboteurs, nb_nains] a partir du nombre de joueurs
        Roles = [fg.red+"Saboteur"+fg.res]*nbRoles[0] + [fg.green+"Nain"+fg.res]*nbRoles[1]
        shuffle(Roles) # on melange les roles
        for i, joueurCourant in enumerate(self.joueurs) : 
            joueurCourant.role = Roles[i] # on attribue les roles
    
    def choisirJoueur( self, listeJoueurs ) :
        """parfois il faut choisir un des joueurs de la liste fournie pour leur jouer un mauvais tour ! (ou les sauver)
        renvoie un joueur, hyp : listeJoueurs non vide"""
        
        # si un seul joueur est eligible, alors le choix est deja fait
        if len(listeJoueurs) == 1 :
            print("Un seul joueur est éligible :",listeJoueurs[0]._nom)
            return listeJoueurs[0]
        
        # else => plusieurs choix possibles
        print("Choisissez un joueur :")
        for i,jou in enumerate(listeJoueurs) :
            # on affiche la liste des joueurs eligibles
            print(f"  {i+1} : {jou._nom}")
        userInput = 0
        
        # Si le joueur n'est pas humain on met une valeur par défaut et on ne demande pas d'input
        if self.celuiQuiJoue.who()=='RobOOt': 
            userInput = random.randint(1,len(listeJoueurs))
            print(f"{listeJoueurs[userInput-1]._nom} est choisi.e !")
        # sinon si le joueur est humain on lui demande de choisir un joueur
        while not(1 <= userInput <= len(listeJoueurs)) :
            try :    userInput = int(input("Votre choix : "))
            except : print("ATTENTION : Veuillez renseigner un entier !")
        
        return listeJoueurs[userInput-1]
    
    def gainScore( self, nainGagne ) :
        print("Gain des Pépites en Fin de Jeu")
        listeNains, listeSaboteurs = [], []
        indexDernierJoueur = self.joueurs.index( self.celuiQuiJoue )
        pep = self.restePepites
        
        for i in range(len(self.joueurs)) :
            j = self.joueurs[indexDernierJoueur - i] # on parcours les joueurs a l'envers en partant du dernier a avoir joue
            j.score.append(0)                        # on ajoute une case a sa liste de score par manche
            if j.role == fg.green+"Nain"+fg.res :
                listeNains.append(j)
            else :
                listeSaboteurs.append(j)
        
        # si les nains gagnent
        if nainGagne :
            # on pioche des cartes gold
            gold = pep[:len(self.joueurs)] # on pioche le meme nombre de cartes que le nombre de joueurs
            gold.sort(reverse=True) # on trie la liste
            for j in listeNains :        # pour chaque Nain
                if len(pep) == 0 : print("Il n'y a plus assez de pepites a distribuer") ; break
                j.score[-1] += gold[0]   # on lui ajoute la plus grande pepite de la liste
                pep.remove(gold[0])      # on l'enleve de notre liste de pepites globale
                gold.pop(0)              # on l'enleve des cartes gold piochees de la liste de pepite
        
        # si les saboteurs gagnent
        else :
            for j in listeSaboteurs : # pour chaque saboteur
                # s'il est seul
                if len(listeSaboteurs) == 1 :
                    # il gagne 4 pepites (3+1, 2+2, 2+1+1, 1+1+1+1)
                    if 3 in pep and 1 in pep :           # 3+1
                        pep.remove(3) ; pep.remove(1)
                    elif pep.count(2) >= 2 :             # 2+2 
                        pep.remove(2) ; pep.remove(2)
                    elif 2 in pep and pep.count(1) >= 2 :# 2+1+1
                        pep.remove(2) ; pep.remove(1) ; pep.remove(1)
                    elif pep.count(1) >= 4 :             # 1+1+1+1
                        pep.remove(1) ; pep.remove(1) ; pep.remove(1) ; pep.remove(1)
                    else : print("Il n'y a plus assez de pepites a distribuer") ; break
                    j.score[-1] += 4
                # s'il sont deux ou trois
                elif 2 <= len(listeSaboteurs) <= 3 :
                    # ils gagnent 3 pepites (3, 2+1, 1+1+1)
                    if 3 in pep :                # 3
                        pep.remove(3)
                    elif 2 in pep and 1 in pep : # 2+1
                        pep.remove(2) ; pep.remove(1)
                    elif pep.count(1) >= 3 :     # 1+1+1
                        pep.remove(1) ; pep.remove(1) ; pep.remove(1)
                    else : print("Il n'y a plus assez de pepites a distribuer") ; break
                    j.score[-1] += 3
                # s'ils sont plus (ici, 4 maximum)
                else :
                    # ils gagnent 2 pepites (2, 1+1)
                    if 2 in pep :            # 2
                        pep.remove(2)
                    elif pep.count(1) >= 2 : # 1+1
                        pep.remove(1) ; pep.remove(1)
                    else : print("Il n'y a plus assez de pepites a distribuer") ; break
                    j.score[-1] += 2
                    
                    
    
    def jouerManche( self ) :
        self.assignerRoles()
        self.distribuerMains()
        print("Voici la grille de jeu\n")
        print(self.plateau)
        fin_manche, nainGagnent = False, False
        while not fin_manche:
            for joueurCourant in self.joueurs:
                
                if len(joueurCourant.main) == 0 : fin_manche = True ; break # self.celuiQuiJoue est donc le dernier a avoir pose une carte ! (joueur precedent)
                
                print(f"Au tour de : {joueurCourant._nom} ({joueurCourant.role})")
                self.celuiQuiJoue = joueurCourant # stockage du joueur courant en attribut de la Manche
                
                mess, tourOK = '', False
                while (not tourOK) : # tant que le tour n'a pas pu etre effectue
                    print("Quelle carte voulez-vous jouer ?")
                    if len(joueurCourant.banc) > 0 : print(joueurCourant.banc)
                    
                    joueurCourant.piocher( CarteDefausser() )        # on donne au joueurCourant une CarteDefausser
                    
                    # choisir une carte dans la main
                    print(joueurCourant.main)
                    if joueurCourant.who()=='joueur': # Permet de séparer les joueurs humains des ordinateurs
                        carteChoisie = joueurCourant.main.choisirCarte() # on lui demande de choisir une carte (dont les nouvelles cartes)
                    elif joueurCourant.who()=='RobOOt': # Si le joueur n'est pas humain on met une valeur par défaut et on ne demande pas d'input
                        carteChoisie = random.choice(joueurCourant.main)
                        
                    joueurCourant.defausser( CarteDefausser() )      # on lui retire la CarteDefausser pour qu'il ne la defausse pas
                                                                     # et pour qu'elle soit a nouveau a la fin de sa main au tour suivant
                    print(f"Carte choisie : {carteChoisie._nom}")
                                                                    
                    if isinstance( carteChoisie, CarteChemin ) and joueurCourant.estBloque() : # un joueur bloqué ne peut pas poser de chemin
                        mess = "Choisissez une autre carte, vous êtes bloqués."
                        tourOK = False
                    
                    elif isinstance( carteChoisie, CarteChemin ):                   # si c'est une CarteChemin
                        if joueurCourant.who()=='joueur': # Permet de séparer les joueurs humains des ordinateurs
                            l,c = self.plateau.askForLC()                               # on lui demande de choisir une ligne et une colonne
                        if joueurCourant.who()=='RobOOt': # Si le joueur n'est pas humain on met une valeur par défaut et on ne demande pas d'input
                            if len(self.plateau.positionsPossibles)>0:
                                l,c = self.plateau.positionsPossibles[0] # le bot choisit la meilleure position possible (voir self.updateAccess())
                            else: l,c = 0,0 # Aucune position possible, plateau.poserCarte renverra tourOk = False                             # on lui demande de choisir une ligne et une colonne
                        mess, tourOK = self.plateau.poserCarte( carteChoisie, l, c, self.celuiQuiJoue.who())# puis on tente de poser la carte
                        if tourOK : self.plateau.checkAgrandir(l,c) ; print( self.plateau )
                        nainGagnent = self.plateau.updateAccess()
                        
                    elif isinstance(carteChoisie,CarteAction):      # si c'est une CarteAction
                        mess, tourOK = carteChoisie.action( self )  # on tente de faire l'action
                    
                    print( colors.bold + mess + colors.res) # on print le message, qu'il reflette le bon ou le mauvais deroulement du tour
                
                if not isinstance(carteChoisie, CarteDefausser):    # La CarteDefausser est deja enlevee au debut du tour
                                                                    # la defausse se fait dans son action si elle est choisie
                    joueurCourant.defausser( carteChoisie )    # Sinon on defausse la carte jouee
                    joueurCourant.piocher( self.deck )         # pour en piocher une autre
                
                if joueurCourant.who() == 'joueur' : sleep(2)
                clear()
                        
                print("Cartes restantes dans le deck :",len(self.deck))
                print("###"+("#"*(self.plateau.C-2)*5))
                print(self.plateau)   # on affiche le plateau
                
                if nainGagnent : fin_manche = True ; break
        
        self.gainScore(nainGagnent)


#%% PARTIE

class Partie :
    
    def __init__( self ) :
        self.NewJoueurs()   # self.joueurs, creation d'une liste de joueurs
        pepites = [3]*4 + [2]*8 + [1]*16 ; shuffle(pepites)
        self.__pepites = pepites
        
    def NewJoueurs( self ) :
        """Demande a l'utilisateur d'entrer les noms des joueurs de la partie"""
        NBMAX, NBMIN = 10, 3 # nombre maximal et minimal de joueurs
        nomplayers = []
        userInput=''
        print(fg.underline+f"Rentrez le nom des joueurs (minimum {NBMIN}) :\n"+fg.res+"Un joueur par ligne et une ligne vide pour commencer la partie,\n'BOT_' dans un nom pour créer un bot qui joue aléatoirement ($auto$ pour faire jouer 10 bots entre eux)\n")
        while True and len(nomplayers) < NBMAX:
            userInput = input()
            if userInput == '$auto$' : # Pour declencher une partie Automatique a 12 RobOOts
                nomplayers = ['BOT_1', 'BOT_2', 'BOT_3', 'BOT_4', 'BOT_5', 'BOT_6', 'BOT_7', 'BOT_8', 'BOT_9', 'BOT_10']
                break
            if userInput in nomplayers:
                print('Ce joueur existe déjà')
            elif userInput == '':
                if NBMIN <= len(nomplayers) <= NBMAX:
                    break
                else:
                    print("Pas assez de joueurs")
            else: 
                nomplayers.append(userInput)
        self.joueurs = [Joueur(nom,'Defaut',[],[]) for nom in nomplayers if 'BOT_' not in nom] + [RobOOt(nom,'Defaut',[],[]) for nom in nomplayers if 'BOT_' in nom]
        random.shuffle(self.joueurs)
        ecriture(f"Il y aura donc {len(self.joueurs)} joueurs : {'   '.join(f'{c._nom}' for c in self.joueurs)}")
        ecriture("\n(les chercheurs d'or sont communément appelés 'Nains')")
    
    def afficherScores( self ) :
        aff, infosJ, long = '', [], [] # affichage : str, infosJoueurs : list[tuple(scoreActuel, score dans toutes les manches + score Actuel, message)], longueur du message
        
        # pour chaque joueur
        for j in self.joueurs :
            message = f"{j._nom} ({j.role})" # on a le message correspondant
            infosJ.append((sum(j.score),j.score + [sum(j.score)],message)) # on met a jour les infosJoueurs
            long.append(len(message))  # dans le but de savoir quel est le plus long message, on stocke temporairement les longueurs dans un tableau
        # on trie les joueurs par score decroissant
        infosJ.sort(reverse=True)
        nbchar = max(long) ; del long     # longueur de la premiere colonne (plus long message), on peut alors supprimer 'long'
        nbManches = len(infosJ[0][1]) -1  # nombre de manches courantes = longueur de unjoueur.score
        
        
        ligne = "-"*(nbchar-5) + "-+---------"*(nbManches+1) + '\n'
        
        # affichage de l'entete
        aff += " "*(nbchar-5)
        for i in range(nbManches) : aff += " | " + fg.bold + "Manche " + str(i+1) + fg.res
        aff += " | " + "TOTAL" + '\n'
        aff += ligne
        
        n = 0
        for _, sco, mess in infosJ :
            n += 1
            cste = 13
            mess = fg.yellow + str(n) + '- ' + fg.res + mess
            aff += mess + " "*(nbchar - len(mess) + cste)
            for i in range(nbManches+1) : 
                aff += ' | ' + str(sco[i]) + '      '
                if len(str(sco[i])) == 1 :  aff += ' '
            aff += '\n' + ligne
            
        print(aff)
    
    def choisirModeAffichage( self ) :
        ecriture("\nPour cette partie, le plateau peut être affiché avec ou sans les bordures de cartes.\n"+'Souhaitez-vous afficher les parenthèses de bordures de carte sur le plateau ? (o/n) : ')
        UserIn = input()
        return UserIn in ['o','oui','y','yes','O','Oui','Y','Yes']
    
    def jouerPartie( self ) :
        affParentheses = self.choisirModeAffichage()
        clear()
        for numManche in range(3) : # une partie contient 3 manches
            clear()
            print('\n\n' + colors.bold + colors.underline + fg.pink + f"DEBUT de la MANCHE {numManche+1}" + fg.res + colors.res + colors.res + ' \n\n')
            sleep(2)
            mancheEnCours = Manche(self.joueurs, self.__pepites, affParentheses)
            mancheEnCours.jouerManche()
            self.__pepites = mancheEnCours.restePepites # on recupere les pepites restantes
            print('\n\n' + colors.bold + colors.underline + fg.pink + f"SCORES" + fg.res + colors.res + colors.res + ' \n\n')
            self.afficherScores()
            sleep(5)
            del mancheEnCours