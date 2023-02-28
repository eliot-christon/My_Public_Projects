"""
Created on Tue Oct 25 20:44:05 2022
@author: CHRISTON Eliot, LEVEQUE Robin, PETARD Adrien
"""
from .Ext_ClassesCarte import *
from .Ext_stockageSabOOters import *

from time import sleep
from couleurs import *
from affichageLent import ecriture
from clearConsole import clear

def regles ( ) :
    
    # Principe du jeu
    Principe_du_jeu = "\n"+colors.underline+fg.bold+"Principe du jeu"+fg.res+colors.res+"\n\n\
Dans cette extension, les joueurs vont découvrir de nouveaux rôles à prendre : le "+fg.blue+"Bo"+fg.green+"ss"+fg.res + ", \
le "+fg.darkgrey+"Profiteur"+fg.res+", le "+fg.cyan+"Géologue"+fg.res+" (voir plus bas), ainsi que de nouvelles actions et d'autres cartes \
Chemin. Il y a toujours des "+fg.blue+"Cherc"+fg.green+"heurs"+fg.res+" d'or mais ils sont dorénavant divisés en 2 équipes : \
les "+fg.blue+"bleus"+fg.res+" et les "+fg.green+"verts"+fg.res+".\nComme précédemment, ces prospecteurs cherchent à construire un chemin \
jusqu'au "+fg.bold+"trésor"+fg.res+". Mais ils ne sont plus seuls : ils vont devoir coopérer avec leurs collègues pour y parvenir. \
\nComme pour le jeu de base, le joueur ayant récolté le plus de pépites après 3 manches consécutives \
gagne la partie. \n\
Les principes de jeu restent globalement les mêmes, hormis les changements et compléments ci-après.\n\n"
    
    # Preparation
    Preparation = "\n"+colors.underline+fg.bold+"Préparation"+fg.res+colors.res+"\n\n\
• Remplacer les cartes Rôle du jeu de base par les nouvelles.\n\
• Placez la carte de départ et les 3 cartes Arrivée comme indiqué dans la règle de base.\n\
• Mélangez ensemble toutes les cartes Chemin et Action (du jeu de base et de l'extension) et placez \
les en pile face cachée. \n  Au début de chaque manche retirez et écartez les 10 premières cartes de \
cette pile sans les regarder : elles ne seront pas utilisées.\n\
• Mélangez les 15 cartes Rôle de l'Extension et distribuez en une à chaque joueur, face cachée, \
indépendamment du nombre de joueurs.\n\
• Distribuez 6 cartes à chacun, indépendamment du nombre de joueurs.\n\
Chaque joueur regarde sa carte Rôle puis la repose devant lui, face cachée, en prenant soin de ne pas \
la révéler.\nLes cartes Rôle restantes ne sont pas distribuées et sont mises de côté : les rôles non attribués \
restent donc inconnus de tous !\n\
Le joueur le plus jeune commence. Puis on joue dans le sens horaire.\n\n"
    
    # Les nouvelles cartes Roles et leurs conditions de victoire
    LesNouvellesCartesRolesEtLeursConditionsDeVictoire = "\n"+colors.underline+fg.bold+"Les nouvelles cartes Rôles et leurs conditions de victoire"+fg.res+colors.res+"\n\n"
    ChercheursDor = fg.bold+"1 Chercheurs d'or "+fg.blue+"bleus"+fg.res+fg.bold+" et "+fg.green+"verts"+fg.res+" (4 cartes par équipe dans le jeu) \n   \
Les 2 équipes essaient de creuser un chemin vers le trésor mais sont en compétition. \n   \
C'est toujours l'équipe qui établit la connexion qui gagne. \n   Si la connexion avec le trésor passe par une porte, seule l'équipe portant la couleur de la porte gagne. \n   \
"+fg.red+"Cas spécial : si un joueur Bleu crée un chemin vers le trésor et que ce chemin est bloqué par une porte Verte, \n   alors l'équipe Verte gagne. Et inversement."+fg.res+"\n\n"
    Boss = fg.bold+"2 Le "+fg.blue+"Bo"+fg.green+"ss"+fg.res+" (1 dans le jeu) \n   \
Construit des tunnels pour l'équipe "+fg.blue+"Bleue"+fg.res+" comme pour l'équipe "+fg.green+"Verte"+fg.res+". \n   Il gagne à chaque fois qu'une de ces équipes gagne, \
mais toujours une pépite de moins que les "+fg.blue+"Cherc"+fg.green+"heurs"+fg.res+".\n\n"
    Profiteur = fg.bold+"3 Le "+fg.darkgrey+"Profiteur"+fg.res+" (1 dans le jeu) \n   \
Profite de chaque situation : il est toujours gagnant, que ce soit les "+fg.blue+"Cherc"+fg.green+"heurs"+fg.res+" ou les "+fg.red+"Saboteurs"+fg.res+" qui l'emportent. \n   \
Il peut même gagner seul. Mais lors du partage, il prend 2 pépites de moins que les autres.\n\n"
    Geologues = fg.bold+"4 Les "+fg.cyan+"Géologues"+fg.res+" (2 dans le jeu) \n   \
Creusent pour leur propre compte. Ils ne sont pas particulièrement intéressés par l'or. \n   \
Lors du partage du trésor, les "+fg.cyan+"Géologues"+fg.res+" reçoivent autant de pépites qu'il y a de cristaux visibles dans le labyrinthe.\n   \
S'il y a 2 "+fg.cyan+"Géologues"+fg.res+" lors d'une manche ils se partagent équitablement ce butin,\n   en arrondissant au nombre inférieur si le nombre de cristaux est impair.\n\n"
    FinRoles = "Quand un "+fg.blue+"Bo"+fg.green+"ss"+fg.res+", un "+fg.cyan+"Géologue"+fg.res+" ou un "+fg.darkgrey+"Profiteur"+fg.res+" crée la connexion avec le trésor : \n   \
• s'il n'y a aucune porte sur le chemin qui mène au trésor, les deux équipes de "+fg.blue+"Cherc"+fg.green+"heurs"+fg.res+" gagnent.\n   \
• s'il y a une porte sur le chemin, seule l'équipe de la couleur de la porte gagne.\n   \
• s'il y a deux portes de couleurs différentes, le "+fg.blue+"Bo"+fg.green+"ss"+fg.res+" gagne seul. S'il n'y a pas de "+fg.blue+"Bo"+fg.green+"ss"+fg.res+", les "+fg.red+"Saboteurs"+fg.res+" gagnent.\n\n"
    LesNouvellesCartesRolesEtLeursConditionsDeVictoire += ChercheursDor + Boss + Profiteur + Geologues + FinRoles
    
    # Deroulement d'une partie
    Deroulement1Partie = "\n"+colors.underline+fg.bold+"Déroulement d'une partie"+fg.res+colors.res+"\n\n \
A leur tour les joueurs doivent faire au choix l'une des 4 actions suivantes : \n   \
• poser une carte Chemin dans le labyrinthe, puis piocher 1 carte ; \n   \
• jouer une carte Action, puis piocher 1 carte ; \n   \
• se défausser de 2 cartes de sa main pour pouvoir retirer une carte posée devant soi, puis piocher 1 seule carte ; \n   \
• passer et se défausser (face cachée) d'1 à 3 cartes de sa main, puis piocher 1 à 3 cartes; \n\
c'est ensuite le tour du joueur suivant. \n\
Quand la pioche est épuisée, les joueurs ne piochent plus mais doivent jouer au moins une carte. \n\
Quand un joueur n'a plus de carte en main, il passe son tour jusqu'à la fin de la manche.\n\n"
    
    # nouvelles cartes chemin
    nouvellesCartesChemin = "\n"+colors.underline+fg.bold+"Les nouvelles cartes Chemin :"+fg.res+colors.res+"\n\n"

    Pont = fg.bold+"Carte Chemin avec un Pont"+fg.res+" (2 par jeu)"
    c = ListeCartes([CarteChemin("UD+RL+",dicoCartesChemin()["UD+RL+"][0],dicoCartesChemin()["UD+RL+"][2])])
    Pont += '\n' + c.__str__() + '\n' +"   Cette carte montre 2 chemins droits qui ne sont pas connectés entre eux. \n   \
Vous ne pouvez tourner ni à gauche ni à droite avec cette carte. \n   \
Au moins l'un des 2 chemins doit être connecté avec à la carte Départ.\n\n"

    Echelle = fg.bold+"Carte Chemin avec une Echelle"+fg.res+" (4 dans le jeu, indiquant des directions différentes)"
    c = ListeCartes([CarteChemin("UR+E",dicoCartesChemin()["UR+E"][0],dicoCartesChemin()["UR+E"][2]), \
                       CarteChemin("UL+E",dicoCartesChemin()["UL+E"][0],dicoCartesChemin()["UL+E"][2]), \
                       CarteChemin("UxE",dicoCartesChemin()["UxE"][0],dicoCartesChemin()["UxE"][2]), \
                       CarteChemin("RxE",dicoCartesChemin()["RxE"][0],dicoCartesChemin()["RxE"][2])])
    Echelle += '\n' + c.__str__() + '\n' + "   Le chemin sur cette carte peut être connecté à la carte de Départ et à toutes les autres cartes ayant une échelle ; \n   \
il doit toujours toucher une carte Chemin et ne peut donc pas être placé à côté d'une carte Arrivée. \n   \
Ces cartes permettent de poursuivre le tunnel depuis une carte Echelle, même si la connexion avec la case de départ est supprimée.\n   \
Une porte qui se trouve entre deux échelles n'est plus prise en compte, ces échelles établissant un raccourci.\n\n"

    DoubleCourbe = fg.bold+"La Double Courbe"+fg.res+" (2 dans le jeu, indiquant des directions différentes)"
    c = ListeCartes([CarteChemin("UR+DL+",dicoCartesChemin()["UR+DL+"][0],dicoCartesChemin()["UR+DL+"][2]), \
                       CarteChemin("UL+RD+",dicoCartesChemin()["UL+RD+"][0],dicoCartesChemin()["UL+RD+"][2])])
    DoubleCourbe += '\n' + c.__str__() + '\n' + "   Cette carte a elle aussi 2 chemins qui ne sont pas connectés, \n   et au moins l'un de ces 2 chemins doit être connecté avec à la carte Départ.\n\n"

    Porte = fg.bold+"Carte Chemin avec une Porte"+fg.res+" (3 de chaque couleur dans le jeu)"
    c = ListeCartes([CarteChemin("UD+B",dicoCartesChemin()["UD+B"][0],dicoCartesChemin()["UD+B"][2]), \
                       CarteChemin("UR+B",dicoCartesChemin()["UR+B"][0],dicoCartesChemin()["UR+B"][2]), \
                       CarteChemin("RL+B",dicoCartesChemin()["RL+B"][0],dicoCartesChemin()["RL+B"][2]), \
                       CarteChemin("UL+V",dicoCartesChemin()["UL+V"][0],dicoCartesChemin()["UL+V"][2]), \
                       CarteChemin("RL+V",dicoCartesChemin()["RL+V"][0],dicoCartesChemin()["RL+V"][2]), \
                       CarteChemin("UD+RxV",dicoCartesChemin()["UD+RxV"][0],dicoCartesChemin()["UD+RxV"][2])])
    Porte += '\n' + c.__str__() + '\n' + "   Au moment de la connexion avec le trésor, un chemin avec une porte ("+fg.green+"Verte"+fg.res+" ou "+fg.blue+"Bleue"+fg.res+") n'est accessible que par les membres \n   \
de l'équipe de la couleur correspondante.\n   \
Le "+fg.blue+"Bo"+fg.green+"ss"+fg.res+" est considéré comme "+fg.blue+"bleu"+fg.res+" et "+fg.green+"vert"+fg.res+", le Profiteur : "+fg.blue+"bleu"+fg.res+" ou "+fg.green+"vert"+fg.res+" (quand la manche est terminée, il choisit sa couleur).\n\n"

    Cristaux = fg.bold+"Cartes Chemin avec des cristaux"+fg.res+" (10 dans le jeu)"
    c = ListeCartes([CarteChemin("URDL+C",dicoCartesChemin()["URDL+C"][0],dicoCartesChemin()["URDL+C"][2]), \
                       CarteChemin("URD+LxC",dicoCartesChemin()["URD+LxC"][0],dicoCartesChemin()["URD+LxC"][2]), \
                       CarteChemin("URL+DxC",dicoCartesChemin()["URL+DxC"][0],dicoCartesChemin()["URL+DxC"][2]), \
                       CarteChemin("RL+UxC",dicoCartesChemin()["RL+UxC"][0],dicoCartesChemin()["RL+UxC"][2]), \
                       CarteChemin("URD+C",dicoCartesChemin()["URD+C"][0],dicoCartesChemin()["URD+C"][2]), \
                       CarteChemin("URL+C",dicoCartesChemin()["URL+C"][0],dicoCartesChemin()["URL+C"][2]), \
                       CarteChemin("UxC",dicoCartesChemin()["UxC"][0],dicoCartesChemin()["UxC"][2]), \
                       CarteChemin("RxC",dicoCartesChemin()["RxC"][0],dicoCartesChemin()["RxC"][2])])
    Cristaux += '\n' + c.__str__() + '\n' + "   Ces cartes ne changent rien aux connexions entre les autres cartes, mais seront bien utiles aux "+fg.cyan+"Géologues"+fg.res+" !\n\n"

    nouvellesCartesChemin += Pont + Echelle + DoubleCourbe + Echelle + Cristaux + "\n"
    
    # Nouvelles cartes Action
    nouvellesCartesAction = "\n"+colors.underline+fg.bold+"Nouvelles cartes Action"+fg.res+colors.res+"\n\n\
Comme dans le jeu de base, on ne peut poser qu'une seule carte Action de même type devant un joueur.\n"

    Inspection = fg.bold+"Inspection"+fg.res+" (2 dans le jeu)"
    c = ListeCartes([CarteVuR("VuR",dicoCartesAction()["VuR"][0])])
    Inspection += '\n' + c.__str__() + '\n' + "   Le joueur qui joue cette carte peut regarder secrètement la carte Rôle de n'importe quel autre joueur.\n   \
Puis il défausse la carte «Inspection».\n\n"

    CdR = fg.bold+"Changement de Rôle"+fg.res+" (2 dans le jeu)"
    c = ListeCartes([CarteCdR("CdR",dicoCartesAction()["CdR"][0])])
    CdR += '\n' + c.__str__() + '\n' + "   Celui qui pose cette carte choisit un joueur (il peut se choisir lui-même) qui doit piocher une nouvelle carte Rôle.\n   \
Ce joueur se défausse secrètement de son ancienne carte Rôle, puis pioche au hasard une nouvelle carte Rôle \n   parmi celles qui n'ont pas été distribuées au début. \
La carte Action est ensuite défaussée.\n\n"

    CdM = fg.bold+"Changer de main"+fg.res+" (2 dans le jeu)"
    c = ListeCartes([CarteCdM("CdM",dicoCartesAction()["CdM"][0])])
    CdM += '\n' + c.__str__() + '\n' + "   Le joueur qui joue cette carte choisit un autre joueur et échange sa main avec lui.\n   \
Les autres ne doivent pas voir ces cartes. L'échange est autorisé même avec un joueur qui n'a pas le même nombre de cartes en main. \n   \
Puis la carte Action est défaussée et c'est au tour de l'autre joueur de piocher une nouvelle carte.\n\n"

    Voleur = fg.bold+"Voleur"+fg.res+" (4 dans le jeu)"
    c = ListeCartes([CarteVol("Vol#",dicoCartesAction()["Vol#"][0])])
    Voleur += '\n' + c.__str__() + '\n' + "   Le joueur pose cette carte, face visible, devant lui. \n   \
A la fin de la manche, après le partage, il pourra voler un 1 point au joueur de son choix.\n   \
Note : vous ne pouvez pas voler de pépite si vous êtes emprisonné au moment du partage.\n\n"

    PasTouche = fg.bold+"Pas Touche"+fg.res+" (3 dans le jeu)"
    c = ListeCartes([CarteVol("Vol-",dicoCartesAction()["Vol-"][0])])
    PasTouche += '\n' + c.__str__() + '\n' + "   Le joueur qui joue cette carte peut retirer une carte Voleur qui a été posée précédemment.\n   \
Les 2 cartes sont défaussées.\n\n"

    EnPrison = fg.bold+"En Prison !"+fg.res+" (3 dans le jeu)"
    c = ListeCartes([CarteATT("Prix",dicoCartesAction()["Prix"][0])])
    EnPrison += '\n' + c.__str__() + '\n' + "   Le joueur pose cette carte, face visible, devant le joueur de son choix: celui-ci est alors emprisonné et ne peut plus jouer normalement. \n   \
A leur tour, les joueurs emprisonnés ne peuvent pas jouer de carte Chemin, mais ils peuvent jouer d'autres cartes Action, \n   \
ou changer les cartes de leur main pour tenter de trouver une carte « Enfin libre », \n   ou encore se défausser de 2 cartes pour se libérer (voir plus bas).\n   \
Les joueurs qui sont emprisonnés au moment de la répartition du trésor ne comptent pas et ne reçoivent aucune pépite. \n   Ils ne peuvent pas voler non plus.\n\n"
    
    EnfinLibre = fg.bold+"Enfin Libre"+fg.res+" (4 dans le jeu)"
    c = ListeCartes([CarteDEF("Pri+",dicoCartesAction()["Pri+"][0])])
    EnfinLibre += '\n' + c.__str__() + '\n' + "   Le joueur pose cette carte, face visible, devant le joueur de son choix: celui-ci est alors emprisonné et ne peut plus jouer normalement. \n   \
A leur tour, les joueurs emprisonnés ne peuvent pas jouer de carte Chemin, mais ils peuvent jouer d'autres cartes Action, \n   \
ou changer les cartes de leur main pour tenter de trouver une carte « Enfin libre », \n   ou encore se défausser de 2 cartes pour se libérer (voir plus bas).\n   \
Les joueurs qui sont emprisonnés au moment de la répartition du trésor ne comptent pas et ne reçoivent aucune pépite. \n   Ils ne peuvent pas voler non plus.\n\n"

    nouvellesCartesAction += Inspection + CdR + CdM + Voleur + PasTouche + EnPrison + EnfinLibre + "\n"
    
    # Se défausser de 2 cartes
    SeDfausserDe2Cartes = "\n"+colors.underline+fg.bold+"Se défausser de 2 cartes."+fg.res+colors.res+"\n\n\
En se défaussant de 2 cartes, un joueur peut retirer n'importe quelle carte qui se trouve devant lui. \n\
Attention : il ne pioche qu'une carte à la fin de son tour et réduit donc son nombre de cartes en main.\n\n"
    
    # Passer
    Passer = "\n"+colors.underline+fg.bold+"Passer"+fg.res+colors.res+"\n\n\
Si un joueur ne peut ou ne veut pas poser de carte, il passe et se défausse d'1, 2 ou 3 cartes, mais faces cachées.\n\
Il pioche ensuite le même nombre de cartes.\n\n"
    
    # Fin d'une manche
    Fin1Manche = "\n"+colors.underline+fg.bold+"Fin d'une manche"+fg.res+colors.res+"\n\n\
Une manche se termine quand un chemin ininterrompu est créé entre la carte Départ et la carte Trésor,\n\
ou quand aucun joueur ne peut plus jouer de carte.\n\n"

    # Partage de tresor
    PartageDuTresor = "\n"+colors.underline+fg.bold+"Partage du trésor"+fg.res+colors.res+"\n\n\
Il y a plusieurs jetons « Pépite d'Or » ayant chacun une valeur de 1, 2 ou 5 pépites.\n\
Le ou les "+fg.cyan+"Géologue(s)"+fg.res+" reçoivent d'abord autant de pépites qu'il y a de cristaux visibles sur le labyrinthe. \n\
S'il y a 2 "+fg.cyan+"Géologues"+fg.res+", ils partagent en deux parties égales, en arrondissant au nombre inférieur si le total est impair.\n\
Ensuite, selon la continuité ou non du chemin entre le départ et le trésor, on détermine qui des "+fg.red+"Saboteurs"+fg.res+" \
ou des "+fg.blue+"Cherc"+fg.green+"heurs"+fg.res+" a remporté la manche. Si le chemin est continu mais bloqué par une porte, seuls les \
"+fg.blue+"Cherc"+fg.green+"heurs"+fg.res+" propriétaires de cette porte (en fonction de sa couleur) sont gagnants. \
On détermine enfin le nombre de joueurs (hors "+fg.cyan+"Géologues"+fg.res+") qui vont se partager le butin, en ajoutant \
éventuellement aux "+fg.blue+"Cherc"+fg.green+"heurs"+fg.res+" gagnants le "+fg.blue+"Bo"+fg.green+"ss"+fg.res+" et/ou le "+fg.darkgrey+"Profiteur"+fg.res+", ou bien en ajoutant aux "+fg.red+"Saboteurs"+fg.res+" \
l'éventuel "+fg.darkgrey+"Profiteur"+fg.res+". Ce nombre de gagnants influe sur la part de chacun : \n   \
1 gagnant  5 pépites pour le "+fg.blue+"Cherc"+fg.green+"heur"+fg.res+" ou le "+fg.red+"Saboteurs"+fg.res+" (4 pour le "+fg.blue+"Bo"+fg.green+"ss"+fg.res+" ou 3 pour le "+fg.darkgrey+"Profiteur"+fg.res+")\n   \
2 gagnants 4 pépites par "+fg.blue+"Cherc"+fg.green+"heur"+fg.res+" ou "+fg.red+"Saboteurs"+fg.res+" (3 pour le "+fg.blue+"Bo"+fg.green+"ss"+fg.res+", 2 pour le "+fg.darkgrey+"Profiteur"+fg.res+")\n   \
3 gagnants 3 pépites par "+fg.blue+"Cherc"+fg.green+"heur"+fg.res+" ou "+fg.red+"Saboteurs"+fg.res+" (2 pour le "+fg.blue+"Bo"+fg.green+"ss"+fg.res+", 1 pour le "+fg.darkgrey+"Profiteur"+fg.res+")\n   \
4 gagnants 2 pépites par "+fg.blue+"Cherc"+fg.green+"heur"+fg.res+" ou "+fg.red+"Saboteurs"+fg.res+" (1 pour le "+fg.blue+"Bo"+fg.green+"ss"+fg.res+", rien pour le "+fg.darkgrey+"Profiteur"+fg.res+")\n   \
5 gagnants ou + 1 pépite par "+fg.blue+"Cherc"+fg.green+"heur"+fg.res+" ou "+fg.red+"Saboteurs"+fg.res+" (rien pour le "+fg.blue+"Bo"+fg.green+"ss"+fg.res+" ou le "+fg.darkgrey+"Profiteur"+fg.res+")\n\
Les joueurs placent les jetons récoltés, faces cachées, devant eux. \n\
Les voleurs peuvent alors détrousser les autres. C'est le joueur qui a posé sa carte «Voleur» en dernier \
qui se sert en premier : il prend un jeton pépite de valeur 1 dans le butin du joueur de son choix puis \
les voleurs suivants (dans le sens des aiguilles d'une montre) se servent ensuite de la même manière. \
Pour ajuster les paiements, les joueurs « volés » peuvent préalablement faire de la monnaie avec leurs jetons. \n\n\
"+fg.red+fg.underline+"Exemple de distribution des pépites à la fin d'une manche :"+fg.res+fg.red+" \n\n\
Jouent : 1 Chercheur Bleu et 2 Verts, 1 Boss, 1 Profiteur et 2 Saboteurs \n\
Le Boss a complété le chemin jusqu'au trésor. Le chemin est bloqué par une porte bleue. Les deux Saboteurs \
ont une carte Voleur devant eux. Un Saboteur a été emprisonné (il a donc la carte « En prison ! » devant lui).\n\
Le trésor est réparti comme suit :\n   \
• Le Chercheur d'or bleu a gagné (ainsi que le Boss et le Profiteur)\n     \
Nombre de gagnants : 3 (1 Chercheur bleu, 1 Boss, 1 Profiteur). Le Chercheur Bleu reçoit 3 pépites;\n     \
le Boss reçoit 3-1=2 pépites, le Profiteur reçoit 3-2=1 pépite.\n   \
• Le Saboteur qui a joué la carte Voleur et qui n'est pas emprisonné prend 1 jeton de 1 Pépite dans\n     \
le butin du joueur de son choix. L'autre Saboteur qui a une carte Voleur mais qui est emprisonné\n     \
ne reçoit rien.\n\n"+fg.res
    
    # Debut d'un nouveau tour
    DebutNouveauTour = "\n"+colors.underline+fg.bold+"Début d'un nouveau tour"+fg.res+colors.res+"\n\n\
Placer les cartes Départ et Arrivée de nouveau à leur place. Mélanger toutes les cartes Action et Chemin, \
y compris les 10 cartes mises de côté au tour précédent, et empilez-les, faces cachées. Retirer les 10 \
premières cartes et les mettre de côté. Distribuez 6 cartes de la pile à chaque joueur.\n\
Mélangez également à nouveau les 15 cartes Rôle et distribuez-en une par joueur.\n\
Le joueur assis à la gauche de celui qui a joué la dernière carte de la manche précédente entame la nouvelle manche.\n\n"
    
    # Fin de partie
    Fin2Partie = "\n"+colors.underline+fg.bold+"Fin de partie"+fg.res+colors.res+"\n\n\
Le jeu se termine après 3 manches. Le ou les joueur(s) ayant récolté le plus de pépites gagnent la partie.\n\n"

    Tout = Principe_du_jeu + Preparation + LesNouvellesCartesRolesEtLeursConditionsDeVictoire + Deroulement1Partie + nouvellesCartesChemin + nouvellesCartesAction + SeDfausserDe2Cartes + Passer + Fin1Manche + PartageDuTresor + DebutNouveauTour + Fin2Partie

    dico = {
        0   :   "Exit",
        1   :   Tout,
        2   :   Principe_du_jeu,
        3   :   Preparation,
        4   :   LesNouvellesCartesRolesEtLeursConditionsDeVictoire,
        5   :   Deroulement1Partie,
        6   :   nouvellesCartesChemin,
        7   :   nouvellesCartesAction,
        8   :   SeDfausserDe2Cartes,
        9   :   Passer,
        10  :   Fin1Manche,
        11  :   PartageDuTresor,
        12  :   DebutNouveauTour,
        13  :   Fin2Partie
    }
    
    #Menu
    mess = ""
    affMenu = '\n' + colors.underline + "Voici le menu des règles de l'extension !\n" + colors.res +"\
    1    :   Toutes les regles\n\
    2    :   Principe du jeu\n\
    3    :   Preparation\n\
    4    :   Les nouvelles cartes Roles et leurs conditions de victoire\n\
    5    :   Deroulement d'une partie\n\
    6    :   Les nouvelles cartes chemin\n\
    7    :   Les nouvelles cartes action\n\
    8    :   Se défausser de deux cartes\n\
    9    :   Passer\n\
    10   :   Fin d'une manche\n\
    11   :   Partage du trésor\n\
    12   :   Debut d'un nouveau tour\n\
    13   :   Fin de partie\n\
    Autre:   Jouons maintenant !\n"
    
    while mess != "Exit" :
        print(affMenu)
        try : # on demande des valeurs entieres a l'utilisateur
            UserIn = int(input("Veuillez choisir les règles à afficher : "))
        except : 
            UserIn = 0 # Exit
        if 0 < UserIn < 14 :
            mess = dico[UserIn]
            ecriture(mess)
            sleep(2)
        else :
            mess = "Exit"
