"""
Created on Tue Oct 25 20:44:05 2022
@author: CHRISTON Eliot, LEVEQUE Robin, PETARD Adrien
"""
from .ClassesCarte import *
from .ClassesPartie import Plateau
from .stockageSabOOters import *

from time import sleep
from couleurs import *
from affichageLent import ecriture
from clearConsole import clear

def regles ( ) :
    
    # Principe du jeu
    Principe_du_jeu = "\n"+colors.underline+fg.bold+"Principe du jeu"+fg.res+colors.res+"\n\n\
Chacun joue soit le rôle d'un "+fg.green+"Chercheur d'or"+fg.res+", soit le rôle d'un "+fg.red+"Saboteur"+fg.res+" qui entrave la prospection. Mais \
personne ne connaît le rôle des autres joueurs !\n\
Les deux groupes s'affrontent donc sans savoir qui fait quoi.\nLorsqu'arrive le partage de l'or, chacun \
révèle son rôle : si les "+fg.green+"Chercheurs d'or"+fg.res+" sont arrivés au trésor, ils gagnent des pépites et les "+fg.red+"Saboteurs"+fg.res+" ne \
gagnent rien ;\nmais si les "+fg.green+"Chercheurs"+fg.res+" sont bredouilles, les "+fg.red+"Saboteurs"+fg.res+" raflent le butin !\nAprès 3 manches, \
le joueur qui a gagné le plus de pépites remporte la partie.\n\n"

    plateauEx = Plateau() ; plateauEx.config_initiale()
    # Preparation
    Preparation = "\n"+colors.underline+fg.bold+"Préparation"+fg.res+colors.res+"\n\n\
Les cartes Or, Rôle, Chemin et Action, sont triées en 3 paquets distincts. \
On utilise un nombre différent de "+fg.green+"Chercheurs"+fg.res+" et de "+fg.red+"Saboteurs"+fg.res+" en fonction du nombre de joueurs : \n\
• à 3 joueurs : 1 "+fg.red+"Saboteur"+fg.res+" et 3 "+fg.green+"Chercheurs"+fg.res+" \n\
• à 4 joueurs : 1 "+fg.red+"Saboteur"+fg.res+" et 4 "+fg.green+"Chercheurs"+fg.res+" \n\
• à 5 joueurs : 2 "+fg.red+"Saboteurs"+fg.res+" et 4 "+fg.green+"Chercheurs"+fg.res+" \n\
• à 6 joueurs : 2 "+fg.red+"Saboteurs"+fg.res+" et 5 "+fg.green+"Chercheurs"+fg.res+" \n\
• à 7 joueurs : 3 "+fg.red+"Saboteurs"+fg.res+" et 5 "+fg.green+"Chercheurs"+fg.res+" \n\
• à 8 joueurs : 3 "+fg.red+"Saboteurs"+fg.res+" et 6 "+fg.green+"Chercheurs"+fg.res+" \n\
• à 9 joueurs : 3 "+fg.red+"Saboteurs"+fg.res+" et 7 "+fg.green+"Chercheurs"+fg.res+" \n\
• à 10 joueurs : toutes les cartes Rôle (4 "+fg.red+"Saboteurs"+fg.res+" et 7 "+fg.green+"Chercheurs"+fg.res+"). \n\
Les cartes non utilisées sont remises dans la boîte. \n\
Les cartes "+fg.green+"Chercheurs"+fg.res+" et "+fg.red+"Saboteurs"+fg.res+" sont mélangées et distribuées, faces cachées, aux joueurs. Chaque \
joueur reçoit une carte qu'il regarde et repose devant lui, sans dévoiler quel est son rôle pour cette \
manche. La carte non utilisée est écartée, face cachée.\nLes rôles ne seront révélés qu'à la fin de la manche. \
Parmi les 44 cartes Chemin, il y a une carte de départ et 3 cartes \
Arrivée. Sur une carte Arrivée on peut voir un trésor, sur les deux autres ce sont des \
pierres. Les cartes Arrivée sont mélangées et posées faces cachées sur la table. On pose ensuite la carte \
de départ en respectant le schéma ci-après.\n" + plateauEx.__str__() + "\n\
Au cours de la partie, un labyrinthe va se constituer à partir \
de la carte de départ.\nLes cartes Chemin pourront alors être posées au-delà des limites du schéma.\n\
Les 40 autres cartes Chemin et toutes les cartes Action sont mélangées et on les distribue : \n\
• de 3 à 5 joueurs, chaque joueur reçoit 6 cartes. \n\
• de 6 à 7 joueurs, chacun reçoit 5 cartes. \n\
• de 8 à 10 joueurs, chacun reçoit 4 cartes. \n\
Les cartes restantes forment une pioche qui reste sur la table, \
faces cachées.\n\n"

    # Deroulement d'une partie
    DeroulementPartie = "\n"+colors.underline+fg.bold+"Déroulement d'une partie"+fg.res+colors.res+"\n\n\
Le joueur dont c'est le tour doit poser une carte :\n\
• soit une carte Chemin dans le labyrinthe ;\n\
• soit une carte Action devant lui ou en face d'un adversaire ;\n\
• soit il passe et se défausse d'une carte, face cachée, à coté de la pioche.\n\
Ensuite, le joueur doit piocher une carte pour compléter sa main : son tour est terminé et passe au \
suivant.\n\
Lorsque la pioche est épuisée, on ne prend plus de carte à la fin de son tour.\n\n"

    # Jouer une carte chemin
    JouerUneCarteChemin = "\n"+colors.underline+fg.bold+"Jouer une carte chemin"+fg.res+colors.res+"\n\n\
A l'aide de ses cartes, on va créer un chemin entre la carte de Départ et \
les cartes Arrivée.\nUne carte Chemin doit être posée à coté d'une autre \
carte Chemin.\nDe plus, tous les chemins doivent se connecter à la carte \
adjacente et les cartes Chemin doivent toujours être posées dans le \
même sens.\nLes "+fg.green+"Chercheurs d'or"+fg.res+" tentent de créer une liaison ininterrompue entre la \
carte de Départ et une carte Arrivée.\nLes "+fg.red+"Saboteurs"+fg.res+" tentent de les en empêcher.\nIls ne \
doivent cependant pas le faire de manière trop évidente pour ne pas être démasqués !\n\n"


    c1 = ListeCartes([CarteATT("Lix",dicoCartesAction()["Lix"][0]),\
                      CarteATT("Px",dicoCartesAction()["Px"][0]),\
                      CarteATT("Wx",dicoCartesAction()["Wx"][0])])
    c2 = ListeCartes([CarteATT("Li+",dicoCartesAction()["Li+"][0]),\
                      CarteATT("P+",dicoCartesAction()["P+"][0]),\
                      CarteATT("W+",dicoCartesAction()["W+"][0])])
    c3 = ListeCartes([CarteATT("LiP+",dicoCartesAction()["LiP+"][0]),\
                      CarteATT("LiW+",dicoCartesAction()["LiW+"][0]),\
                      CarteATT("PW+",dicoCartesAction()["PW+"][0])])
    c4 = CarteRoF("RoF",dicoCartesAction()["RoF"][0])
    c5 = CarteMap("MAP",dicoCartesAction()["MAP"][0])
    # Jouer une carte action
    JouerUneCarteAction = "\n"+colors.underline+fg.bold+"Jouer une carte action"+fg.res+colors.res+"\n"\
+ """
Les cartes Action sont posées, face visible, devant un joueur. On peut poser devant soi ou devant un 
adversaire. Grâce aux cartes Action, les joueurs peuvent s'aider ou se gêner les uns les autres, retirer des 
cartes du labyrinthe ou obtenir des informations sur les cartes Arrivée. 
""" + '\n' + c1.__str__() + '\n' + """
Si l'une de ces 3 cartes Outil Brisé est posée devant un adversaire, 
celui-ci ne peut plus poser de cartes Chemin tant que cette carte reste 
devant lui. Il lui est néanmoins toujours possible de jouer une carte 
Action ou de passer. Il ne peut y avoir, au maximum, que 3 cartes 
devant un même joueur, et qu'une seule carte du même type. Un 
joueur ne peut poser une carte Chemin dans le labyrinthe que si, au 
début de son tour, il n'y a aucune carte de ce genre devant lui. 
""" + '\n' + c2.__str__() + '\n' + """
Ces 3 cartes permettent de réparer les cartes outil brisé qui se 
trouvent devant un joueur. Elles doivent être jouées sur une carte 
qui se trouve devant soi ou devant un adversaire. Dans les deux cas, 
les deux cartes sont ensuite posées sur la pile de défausse. On ne 
peut retirer une carte qu'à l'aide d'une carte de même type : par 
exemple, un wagonnet défectueux ne peut être écarté qu'à l'aide 
d'un wagonnet en bon état. 
""" + '\n' + c3.__str__() + '\n' + """
Il existe aussi des cartes avec 2 objets. Lorsqu'une telle carte est 
jouée, elle permet de réparer l'un des deux objets indiqués. 
""" + '\n' + c4.__str__() + '\n' + """
Cette carte «éboulement» permet de retirer du labyrinthe une carte Chemin de son 
choix, à l'exception de la carte Départ ou d'une carte Arrivée ; la carte retirée et la carte 
éboulement vont sur la pile de défausse. 
Avec cette carte, un """+fg.red+"Saboteur"+fg.res+""" peut par exemple couper une liaison avec la carte de Départ. 
Autre exemple: un """+fg.green+"Chercheur d'or"+fg.res+""" peut retirer du labyrinthe une carte Chemin avec un 
cul-de-sac. Les trous ainsi formés pourront ensuite être à nouveau remplis à l'aide de cartes 
Chemins appropriées. 
Attention, il est impossible de poursuivre un chemin qui n'est plus relié à la carte de départ : 
il faut d'abord réparer la galerie avant de poursuivre vers une arrivée. 
""" + '\n' + c5.__str__() + '\n' + """
La carte «plan secret» permet à celui qui la joue de prendre connaissance de l'une des 3 
cartes Arrivée : il la regarde secrètement puis la remet à sa place et défausse ensuite la carte 
« plan secret ».\n\n
"""
    
    # Passer
    Passer = "\n"+colors.underline+fg.bold+"Passer"+fg.res+colors.res+"\n\n\
Si un joueur ne peut ou ne veut pas poser de carte, il passe et se défausse d'1 carte, mais face cachée.\n\
Il pioche ensuite une carte.\n\n"

    # Fin d'une manche
    FinManche = "\n"+colors.underline+fg.bold+"Fin d'une manche"+fg.res+colors.res+"\n\n\
Une manche se termine quand un chemin ininterrompu est créé entre la carte Départ et la carte Trésor,\n\
ou quand aucun joueur ne peut plus jouer de carte.\n\n"
        
    # Partage de tresor
    PartageDuTresor = "\n"+colors.underline+fg.bold+"Partage du trésor"+fg.res+colors.res+"\n\n\
Les "+fg.green+"Chercheurs d'or"+fg.res+" ont gagné si le chemin est ininterrompu entre la carte de Départ et la carte \
Arrivée avec le trésor.\nOn pioche alors autant de cartes Or qu'il y a de joueurs autour de la table.\nPar \
exemple, s'il y a 5 joueurs, on pioche 5 cartes Or. Ces cartes ont une valeur de 1, 2 ou 3 pépites.\nLe \
joueur qui a atteint le trésor prend toutes les cartes Or à répartir et en choisit une ; bien sûr, il prendra la \
plus forte valeur possible.\nIl passe ensuite les cartes restantes au prochain "+fg.green+"Chercheur"+fg.res+" (pas au "+fg.red+"Saboteur"+fg.res+"), \
dans le sens inverse des aiguilles d'une montre, qui choisit à son tour une carte, et ainsi de suite jusqu'à \
ce que toutes les cartes Or aient été récupérées.\nLors de ce partage, certains "+fg.green+"Chercheurs"+fg.res+" peuvent donc \
récolter plus de cartes Or que d'autres." + \
"Les "+fg.red+"Saboteurs"+fg.res+" ont gagné si la carte Arrivée sur laquelle figure le trésor n'est pas atteinte.\nS'il n'y \
a qu'un seul "+fg.red+"Saboteur"+fg.res+", il reçoit des cartes Or pour une valeur de 4 pépites.\nS'il y a 2 ou 3 "+fg.red+"Saboteurs"+fg.res+", \
chacun d'entre eux en reçoit pour une valeur de 3 pépites.\nEt s'il y a 4 "+fg.red+"Saboteurs"+fg.res+", ils reçoivent chacun \
2 pépites.\nLes joueurs conservent ensuite secrètement leurs cartes Or pendant les manches suivantes, \
jusqu'à la fin de la partie.\n\n"

    # Deuxieme et Troisieme Manches
    ManchesSuivantes = "\n"+colors.underline+fg.bold+"Manches suivantes"+fg.res+colors.res+"\n" +\
"""
Lorsque les cartes Or ont été réparties, une nouvelle manche commence (se reporter au chapitre \
« Préparation du Jeu »).\nLe joueur assis à la gauche de celui qui a joué la dernière carte de la manche 
précédente commence la nouvelle manche.\n\n
"""

# Fin de partie
    FinPartie = "\n"+colors.underline+fg.bold+"Fin de partie"+fg.res+colors.res+"\n\n\
Le jeu se termine après 3 manches. Le ou les joueur(s) ayant récolté le plus de pépites gagnent la partie.\n\n"

# Conseils
    Conseils = "\n"+colors.underline+fg.bold+"Conseils"+fg.res+colors.res+"\n\n\
Même si vous gagnez plus d'or en arrivant en premier, n'oubliez pas que "+fg.red+"Saboteur"+fg.res+" est un jeu de \
coopération !\nIl est souvent plus avantageux de réparer les outils brisés de vos camarades que de garder \
ces cartes.\nNaturellement il faut être sûr de ses camarades… \
Pour les "+fg.red+"Saboteurs"+fg.res+" : ne révélez pas votre identité en jouant des culs-de-sacs trop tôt.\nPlus vous attendrez, \
plus le suspense sera intense !\n\n"
    
    Tout = Principe_du_jeu + Preparation + DeroulementPartie + JouerUneCarteChemin + JouerUneCarteAction + Passer + FinManche + PartageDuTresor + ManchesSuivantes + FinPartie + Conseils

    dico = {
        0   :   "Exit",
        1   :   Tout,
        2   :   Principe_du_jeu,
        3   :   Preparation,
        4   :   DeroulementPartie,
        5   :   JouerUneCarteChemin,
        6   :   JouerUneCarteAction,
        7   :   Passer,
        8   :   FinManche,
        9   :   PartageDuTresor,
        10  :   ManchesSuivantes,
        11  :   FinPartie,
        12  :   Conseils,
    }
    
    #Menu
    mess = ""
    affMenu = '\n' + colors.underline + "Voici le menu des règles de l'extension !\n" + colors.res +"\
    1    :   Toutes les regles\n\
    2    :   Principe du jeu\n\
    3    :   Preparation\n\
    4    :   Deroulement d'une partie\n\
    5    :   Jouer une carte chemin\n\
    6    :   Jouer une carte action\n\
    7    :   Passer\n\
    8    :   Fin d'une Manche\n\
    9    :   Partage du tresor\n\
    10   :   Manches suivantes\n\
    11   :   Fin de la Partie\n\
    12   :   Conseils\n\
    Autre:   Jouons maintenant !\n"
    
    while mess != "Exit" :
        print(affMenu)
        try : # on demande des valeurs entieres a l'utilisateur
            UserIn = int(input("Veuillez choisir les règles à afficher : "))
        except : 
            UserIn = 0 # Exit
        if 0 < UserIn < 13 :
            mess = dico[UserIn]
            ecriture(mess)
            sleep(2)
        else :
            mess = "Exit"