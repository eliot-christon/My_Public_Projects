"""
Created on Tue Oct 25 20:44:05 2022
@author: CHRISTON Eliot, LEVEQUE Robin, PETARD Adrien
"""

import sys
import random
from abc import ABC,abstractmethod
from time import sleep

from couleurs import fg,colors
from clearConsole import clear
from affichageLent import ecriture
from .Ext_ClassesCarte import *
from .Ext_stockageSabOOters import dicoCartesAction,dicoCartesChemin,dicoRoles
from .Ext_ClassesJoueur import Joueur,RobOOt

#%% PLATEAU
class Plateau:
    
    def __init__(self, tableau_de_cartes = [[]], posStart = [0,0], parentheses = False):
        self.__C = len(tableau_de_cartes[0])    # nb de colonnes du tableau
        self.__L = len(tableau_de_cartes)       # nb de lignes du tableau
        self.table = tableau_de_cartes          # tableau de cartes
        self.posStart = posStart                # position de la carte de depart
        self.positionsPossibles = []            # liste d'emplacements libres relies a la carte START
        self.parentheses = parentheses          # le plateau peut etre affiche avec ou sans parentheses
    
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
                affichage += str(lignes[k%2]*i) + ' '*(2-len(str(lignes[k%2]*i))) +"|"
                for j in range(1,self.__C-1):
                    affichage += self.table[i][j].visuColor(k, self.parentheses )
                affichage += '\n'
        affichage += "--+" + (self.__C-2)*5*"-"
        return affichage
    
    @property
    def C(self):
        return self.__C
    
    @property
    def L(self):
        return self.__L
    
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
        random.shuffle( ordre )
        table = [] # future grille du plateau contenant les cartes
        for i in range(lignes+2) :
            table.append([])
            for _ in range(colonnes+2) :
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
    
    def checkEmplacementCarte( self, carte, ligne, colonne ) :
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
        
        zero_co_cmpt = 0 # nombre d'absence de connections (mur contre mur) ou (chemin vers vide/fin_non_devoilee)
        connect = (0,0)
        for i in range(4) : # car 4 cartes voisines, U, R, D, L
            l, c = ligne + (i-1)*((i+1)%2), colonne + (2-i)*(i%2)
            
            if not(0 <= l < self.__L) or not(0 <= c < self.__C) : # si bord adjacent alors absence de connexion
                carte_voisine = CarteVide( )
            else :
                carte_voisine = self.table[l][c]
                connect = (abs(carte._logic[i]), abs(carte_voisine._logic[(i+2)%4]))
            
            if connect == (0,0) or isinstance(carte_voisine, CarteVide) \
            or ( isinstance(carte_voisine, CarteFin) and not(carte_voisine.visible)):
                zero_co_cmpt += 1
            elif connect[0] == 0 or connect[1] == 0 :
                return "Chemins incompatibles"
        
        if zero_co_cmpt == 4 :      return "Pas de chemin connecté"
        return "Placement valide"
    
    def poserCarte( self, carte, ligne, colonne, typeJoueur) :
        """ CarteChemin -> String * bool
        Methode qui effectue la pose d'une carte sur un plateau et renvoie la statut de la pose
        Elle s'appuie sur checkEmplacementCarte()
        On verifie toutes les possibilites de pose de cette carte et s'il en
        existe plusieurs on demande a l'utilisateur laquelle il prefere
        """
        C1 = CarteChemin( carte._nom, carte._visuel, carte._logic )
        C2 = CarteChemin( carte._nom, carte._visuel, carte._logic )
        C2.flip()
        
        mess1 = self.checkEmplacementCarte( C1, ligne, colonne )
        mess2 = self.checkEmplacementCarte( C2, ligne, colonne )
        
        if mess1 != "Placement valide" and mess2 != "Placement valide":
            return(mess1, False) # placement invalide
        elif mess1 == "Placement valide" and mess2 == "Placement valide" and C1._visuel != C2._visuel :
            if typeJoueur == 'joueur': # Permet de séparer les joueurs humains des ordinateurs
                print("Deux choix possibles")
                deuxChoix = ListeCartes([C1 , C2])
                print( deuxChoix ,end='')
                print("\n1 ou 2 : " ,end='')
                choice = deuxChoix.choisirCarte()
            if typeJoueur == 'RobOOt': choice = random.choice([C1 , C2]) # Si le joue n'est pas humain on mets une valeur par défaut et on ne demande pas d'input
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
    
    def trouverCoordsStartEchelles( self ) : # Renvoie la liste des coordonnees des cartes Start et Echelles
        coords = [self.posStart]
        for l in range(self.__L) :
            for c in range(self.__C) :
                if 'E' in self.table[l][c]._nom and self.table[l][c]._nom != 'END' : 
                    coords.append([l,c])
        return coords
    
    def quiPeutPasser( self, chemin ) : # Renvoie la liste des joueurs qui peuvent passer par chaque chemin vers la fin (portes)
        res = " " + fg.green+"NainVert"+fg.res + " " +fg.blue+"NainBleu"+fg.res
        for coord in chemin :
            nom = self.table[coord[0]][coord[1]]._nom
            if 'V' in nom : res = res.replace('NainBleu','')
            if 'B' in nom : res = res.replace('NainVert','')
        return res
    
    def distanceEnd( self, x, y ) :
        """distance au carre entre la carte END centrale et une carte de coordonnee x, y"""
        xEND, yEND = self.posStart[0] - 1, self.posStart[1] + 7
        return ( (x-xEND)**2 + (y-yEND)**2 )
        
    def addAccessFromCoord( self, coord ) :
        """renvoie tous les chemins possibles entre une carte de coordonnee coord et la carte END sinon liste vide
        et modifie self.positionsPossibles pour ajouter les emplacements disponibles"""
        ## init
        AFFICHER_DETAILS = False # pour mieux analyser, mettre a True
        coord_non_visitees = [(coord[0], coord[1], -1)]# liste de coordonnees non visitees par la direction (0,1,2,3 pour U,R,D,L)
        chemin_courant = [(coord[0], coord[1])]
        mem_chemins = [chemin_courant + []]
        victoires = []
        ## recherche en profondeur
        # on va parcourir en profondeur l'arbre des connections. En partant des coordonnees en input
        while len(coord_non_visitees) > 0 :    # tant qu'il y a des coordonnees a visiter
            l, c, dir = coord_non_visitees[-1][0], coord_non_visitees[-1][1], coord_non_visitees[-1][2] # on prend le dernier ajout dans la liste
            dir = (dir + 2) % 4                # on visite la carte a partir de cette direction U <=> D, R <=> L
            coord_non_visitees.pop(-1)         # elle ne sont donc plus "a visiter"
            carte_courante = self.table[l][c]  # changement de carte courante
            
            if AFFICHER_DETAILS : print("\n"+colors.bold +"actual : "+ colors.res,l,c," dans la direction : ",dir);print(fg.pink + carte_courante._nom + fg.res, end='')
            
            ## update de chemin_courant
            demi_tour = True
            indi = 0
            while demi_tour :
                if len( chemin_courant ) == 0 : 
                    chemin_courant = mem_chemins[indi] + []
                    indi += 1
                    # print("len = 0")
                elif ( [l,c] == coord ) :
                    demi_tour = False
                elif ( [(l-1, c), (l, c+1), (l+1, c), (l, c-1)][dir] == (chemin_courant[-1]) ) and ( len(chemin_courant) < 2 or not(chemin_courant[-1] in chemin_courant[:-2] and chemin_courant[-2] in chemin_courant[:-2]) ):
                    chemin_courant.append((l,c))
                    demi_tour = False
                else : chemin_courant.pop(-1)
            
            if AFFICHER_DETAILS : print("\nchemin courant : ", chemin_courant, end='')
            
            ## is chemin nouveau
            newChemin = True
            # print("\nmemoire de chemins : ",mem_chemins, end ='')
            for che in mem_chemins :
                if newChemin == False : break
                for i in range( len(che)-1 ) :
                    if newChemin == False : break
                    if che[:i+1] == chemin_courant :
                        newChemin = False
                        # print("\nle chemin est connu ! ", end = '')
                        
            ## ajout en memoire d'un nouveau chemin
            if newChemin and not isinstance(carte_courante, CarteVide):
                mem_chemins.append(chemin_courant + [])
            
            ## ajout d'un chemin victorieux
            if isinstance(carte_courante, CarteFin) and not(carte_courante.visible) :
                self.positionsPossibles.append((l,c))
                carte_courante.decouvrir( self )
            if carte_courante._nom == "END" : 
                if AFFICHER_DETAILS : print("\nC'est bien un chemin vers la fin !")
                victoires.append( chemin_courant + [] )
            
            ## exploration du prochain chemin
            if not isinstance(carte_courante, CarteVide) and ('+' in carte_courante._nom or 'ST' in carte_courante._nom or 'E' in carte_courante._nom) :
                # si ce n'est pas une carte vide et qu'elle contient au moins une connection ('+' dans le nom)
                for k in range(4) : # On regarde les cartes voisines
                    other_l, other_c = l + (k-1)*((k+1)%2), c + (2-k)*(k%2)
                    if AFFICHER_DETAILS : print("\ntest   : ",other_l, other_c," dans la direction : ", k, "logic : ",self.table[l][c]._logic[k], end="")
                    if self.table[l][c]._logic[k] > 0 and newChemin and not(carte_courante._nom == "END") and not(self.table[other_l][other_c]._nom == "START")\
                            and ( ( self.table[l][c]._logic[k] == self.table[l][c]._logic[dir] and dir != k ) or len(chemin_courant) == 1 ) :
                        # s'il y a un chemin vers une carte, mais pas ajoutee a la liste des coordonnees a visiter
                        if AFFICHER_DETAILS : print("   OK, on l'ajoute aux cartes a visiter", end='')
                        coord_non_visitees.append( (other_l, other_c, k) ) # on l'ajoute a cette liste
            
            ## update la table des emplacements libres
            elif isinstance(carte_courante, CarteVide) :
                self.positionsPossibles.append((l,c))
            
        return victoires # chemins victorieux
    
    def updateAccess( self ) :
        """update l'attribut self.positionsPossibles, qui est un tableau de booleens qui indiquent 
        les emplacements vides qui sont reliees a la carte de coordonnees coord
        renvoie le nom des roles qui gagnent la manche"""
        
        self.positionsPossibles = []
        coords = self.trouverCoordsStartEchelles()
        chemins = []
        for c in coords :
            chemins += self.addAccessFromCoord( c )
        
        # on trie les emplacements disponibles du plus proche de la carte END du milieu au plus lointain
        # choix arbitraire pour les RobOOts
        self.positionsPossibles = sorted(self.positionsPossibles, key=lambda pos: self.distanceEnd(pos[0], pos[1]))
        
        if len(chemins) > 0 : res = fg.blue+"Bo"+fg.green+"ss"+fg.res  # il y a au moins une facon d'arriver a END => Boss est un role gagnant
        else :                res = fg.red+"Saboteur"+fg.res           # pas de connection jusqu'a la pepite de fin => Saboteur est un role gagnant
        
        for che in chemins :
            res += self.quiPeutPasser( che ) # ajout du nom des roles qui peuvent passer par chaque chemin
        
        return res




#%% MANCHE

class Manche :
    """Chaque partie est constituee de 3 manches. Dans chaque manche il y a les joueurs de la partie, un nouveau plateau, un nouveau deck de cartes,
    et le reste des cartes or = pepites restantes. On decide egalement de garder en memoire les roles qui n'ont pas ete distribues dans le cas d'un changement de role"""
       
    def __init__( self, listeDeJoueurs, affParentheses = False ) :
        self.joueurs = listeDeJoueurs
        self.celuiQuiJoue = listeDeJoueurs[0]
        self.plateau = Plateau(parentheses=affParentheses) ; self.plateau.config_initiale()
        self.NewDeck() # self.deck # creation d'un deck
        self.rolesRestants = []
        for role,nfois in dicoRoles().items() : self.rolesRestants += [role]*nfois

    def NewDeck( self ):
        """Methode qui cree un nouveau deck"""
        deck = []
        for k, v in dicoCartesChemin().items() :
            for _ in range(v[1]):
                deck.append(CarteChemin(k, v[0], v[2]))
            
        for k, v in dicoCartesAction().items() :
            for _ in range(v[1]):
                if k[-1] == "+" :    deck.append( CarteDEF(k, v[0]) )
                elif k[-1] == "x" :  deck.append( CarteATT(k, v[0]) )
                elif k == "MAP" :    deck.append( CarteMap(k, v[0]) )
                elif k == "RoF" :    deck.append( CarteRoF(k, v[0]) )
                elif k == "CdR" :    deck.append( CarteCdR(k, v[0]) )
                elif k == "CdM" :    deck.append( CarteCdM(k, v[0]) )
                elif k == "VuR" :    deck.append( CarteVuR(k, v[0]) )
                elif "Vol" in k :    deck.append( CarteVol(k, v[0]) )
                else : print("Erreur : Carte Action sans sous-classe")
                
        random.shuffle(deck)
        self.deck = ListeCartes(deck[:-10]) # dans l'extension on enleve 10 cartes du deck

    def distribuerMains( self ) :
        """On distribue 6 cartes a chaque joueur en debut de manche"""
        nb_cartes = 6
        
        # Piocher dans le deck et ajouter a la main d'un joueur
        for joueurCourant in self.joueurs:
            joueurCourant.main = ListeCartes([])
            joueurCourant.banc = ListeCartes([])
            for _ in range(nb_cartes):
                # hyp: len(deck) > 0 a chaque iteration
                joueurCourant.piocher( self.deck )
    
    def assignerRoles( self ) :
        """Chaque joueur se voit assigner un nouveau role"""
        random.shuffle(self.rolesRestants) # on melange les roles
        for joueurCourant in self.joueurs : 
            joueurCourant.role = self.rolesRestants[0] # on attribue les roles
            self.rolesRestants.pop(0)
    
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
    
    def gainScore( self, rolesgagnants ) :
        nbCristaux = 0
        joueursGagnants, geologues, voleurs = [], [], []
        
        # compte les cristaux
        for l in range( self.plateau.L ) :
            for c in range( self.plateau.C ) :
                if 'C' in self.plateau.table[l][c]._nom : nbCristaux += 1
        
        # dans quel camp est chaque joueur
        for j in self.joueurs :
            j.score.append(0) # nouveau score de manche dans l'attribut joueur.score (liste des scores)
            estVoleur, enPrison = False, False
            for carte in j.banc :
                if carte._nom == "Vol#" : estVoleur = True
                elif carte._nom == "Prix" : enPrison = True ; estVoleur = False ; break
            if   j.role in rolesgagnants and not(enPrison) : joueursGagnants.append(j)
            elif "Géologue"  in j.role   and not(enPrison) : geologues.append(j)
            elif "Profiteur" in j.role   and not(enPrison) : joueursGagnants.append(j)
            # else : perdant
            if estVoleur : voleurs.append(j)
            
        for geo in geologues :
            geo.score[-1] += round((49*nbCristaux)/(50*len(geologues))) # arrondir par defaut sans utiliser math.floor()

        # les joueurs gagnants ont des points
        for j in joueursGagnants :
            if j.role == fg.blue+"Bo"+fg.green+"ss"+fg.res : # c'est un Boss
                if len(joueursGagnants) <= 4 : j.score[-1] += 1 + 4 - len(joueursGagnants)
            elif "Profiteur" in j.role :
                if len(joueursGagnants) <= 3 : j.score[-1] += 1 + 3 - len(joueursGagnants)
            else : # tout autre role gagnant hors geologue
                if len(joueursGagnants) <= 5 : j.score[-1] += 1 + 5 - len(joueursGagnants)
                else :                         j.score[-1] += 1
        
        # au tour des voleurs de voler des points a ceux qui en ont
        for v in voleurs :
            # construction de la liste des joueurs qui peuvent etre voles par v
            ListeJoueursOkVol = []
            for cejoueur in self.joueurs :
                if sum(cejoueur.score) != 0 and cejoueur != v : ListeJoueursOkVol.append(cejoueur)
            if len(ListeJoueursOkVol) > 0 :
                print(f"Joueur {v._nom}, vous pouvez voler un point à quelqu'un !")
                # choix d'un joueur
                self.celuiQuiJoue = v # c'est le voleur qui choisit le joueur a voler
                joueurCible = self.choisirJoueur(ListeJoueursOkVol)
                joueurCible.score[-1] -= 1
                v.score[-1] += 1
            else : print(f"Joueur {j._nom}, vous êtes voleur mais personne ne peut être volé..")

    def nbJoueursQuiPeuventJouer( self ) : # Nombre de joueur qui ont encore des cartes dans leur main
        res = 0
        for j in self.joueurs :
            if len(j.main) != 0: res += 1
        return res
    
    def jouerManche( self ) :
        self.assignerRoles()
        self.distribuerMains()
        print("Voici la grille de jeu\n")
        print(self.plateau)
        fin_manche, quiGagne = False, fg.red+"Saboteur"+fg.res
        while not fin_manche:
            for joueurCourant in self.joueurs:
                
                print(fg.underline + "Au tour de :" + fg.res + f" {joueurCourant._nom}, ({joueurCourant.role})")
                self.celuiQuiJoue = joueurCourant # stockage du joueur courant en attribut de la Manche
                
                mess, tourOK = '', False
                if len(joueurCourant.main) == 0 : tourOK = True ; print(colors.bold + "Vous n'avez plus de carte..." + colors.res)
                
                while (not tourOK) : # tant que le tour n'a pas pu etre effectue
                    print("Quelle carte voulez vous jouer ?")
                    if len(joueurCourant.banc) > 0 : print(joueurCourant.banc)
                    
                    # piocher cartes speciales
                    joueurCourant.piocher( CarteDefausser() )        # on donne au joueurCourant une CarteDefausser
                    if joueurCourant.estBloque() and len(joueurCourant.main) >= 2 : # s'il est bloque
                        joueurCourant.piocher( CarteEnleverMalus() ) # - on donne au joueurCourant une CarteEnleverMalus
                        
                    # choisir une carte dans la main
                    print(joueurCourant.main)
                    if joueurCourant.who()=='joueur': # Permet de séparer les joueurs humains des ordinateurs
                        carteChoisie = joueurCourant.main.choisirCarte() # on lui demande de choisir une carte (dont les nouvelles cartes)
                    elif joueurCourant.who()=='RobOOt': # Si le joue n'est pas humain on mets une valeur par défaut et on ne demande pas d'input
                        carteChoisie = random.choice(joueurCourant.main)
                    
                    # defausse des cartes speciales
                    if joueurCourant.estBloque() and len(joueurCourant.main) >= 2 :  # s'il est bloque
                        joueurCourant.defausser( CarteEnleverMalus())# - on lui retire la CarteEnleverMalus
                    joueurCourant.defausser( CarteDefausser() )      # on lui retire la CarteDefausser pour qu'il ne la defausse pas
                                                                     # et pour qu'elle soit a nouveau a la fin de sa main au tour suivant
                    
                    print(f"Carte choisie : {carteChoisie._nom}")
                    
                    if isinstance( carteChoisie, CarteChemin ) and joueurCourant.estBloque() :  # un joueur bloqué ne peut pas poser de chemin
                        mess = "Choisissez une autre carte, vous êtes bloqué."
                        tourOK = False
                    
                    elif isinstance( carteChoisie, CarteChemin ):                   # si c'est une CarteChemin
                        if joueurCourant.who()=='joueur': # Permet de séparer les joueurs humains des ordinateurs
                            l,c = self.plateau.askForLC()                               # on lui demande de choisir une ligne et une colonne
                        if joueurCourant.who()=='RobOOt': # Si le joueur n'est pas humain on met une valeur par défaut et on ne demande pas d'input
                            if len(self.plateau.positionsPossibles)>0:
                                l,c = self.plateau.positionsPossibles[0] # le bot choisit la meilleure position possible (voir self.updateAccess())
                            else: l,c = 0,0 # Aucune position possible, plateau.poserCarte renverra tourOk = False
                        mess, tourOK = self.plateau.poserCarte( carteChoisie, l, c, joueurCourant.who())# puis on tente de poser la carte
                        if tourOK : self.plateau.checkAgrandir(l,c) ; print( self.plateau )
                        quiGagne = self.plateau.updateAccess()
                        
                    elif isinstance(carteChoisie,CarteAction):      # si c'est une CarteAction
                        mess, tourOK = carteChoisie.action( self )  # on tente de faire l'action
                    
                    print( colors.bold + mess + colors.res)
                
                if  not isinstance(carteChoisie, CarteCdM) and \
                    not isinstance(carteChoisie, CarteDefausser)and \
                    not isinstance(carteChoisie, CarteEnleverMalus):
                    joueurCourant.defausser( carteChoisie )
                    joueurCourant.piocher( self.deck )
                
                if joueurCourant.who() == 'joueur' : sleep(2)
                clear()
                
                print("Cartes restantes dans le deck :",len(self.deck))
                print("###"+("#"*(self.plateau.C-2)*5))
                print(self.plateau)   # on affiche le plateau
                
                if quiGagne != fg.red+"Saboteur"+fg.res : fin_manche = True ; break
                if self.nbJoueursQuiPeuventJouer() == 0 : fin_manche = True ; break
        
        
        self.gainScore(quiGagne)




#%% PARTIE

class Partie :
    
    def __init__( self ) :
        self.NewJoueurs() # self.joueurs, creation d'une liste de joueurs
        
    def NewJoueurs( self ) :
        NBMAX, NBMIN = 12, 2 # nombre maximal et minimal de joueurs
        nomplayers = []
        userInput=''
        print(fg.underline+f"Rentrez le nom des joueurs (minimum {NBMIN}) :\n"+fg.res+"Un joueur par ligne et une ligne vide pour commencer la partie,\n'BOT_' dans un nom pour créer un bot qui joue aléatoirement ($auto$ pour faire jouer 12 bots entre eux)\n")
        while True and len(nomplayers) < NBMAX:
            userInput = input()
            if userInput == '$auto$' : # Pour declencher une partie Automatique a 12 RobOOts
                nomplayers = ['BOT_1', 'BOT_2', 'BOT_3', 'BOT_4', 'BOT_5', 'BOT_6', 'BOT_7', 'BOT_8', 'BOT_9', 'BOT_10', 'BOT_11', 'BOT_12']
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
        ecriture(f"Il y aura donc {len(self.joueurs)} joueurs : {'   '.join(f'{c._nom} ({fg.yellow+c.who()+fg.res})' for c in self.joueurs)}")
        sleep(2)
        
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
            if fg.blue+"Bo"+fg.green+"ss"+fg.res in mess : cste += 5; # si c'est un Boss, alors il y a deux decalages de 5 characteres, dus a l'ajout de deux couleurs
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
            mancheEnCours = Manche(self.joueurs, affParentheses)
            mancheEnCours.jouerManche()
            print('\n\n' + colors.bold + colors.underline + fg.pink + f"SCORES" + fg.res + colors.res + colors.res + f" (Manches jouées : {numManche + 1}/3) \n")
            self.afficherScores()
            sleep(5)
            del mancheEnCours