from tkinter.constants import ANCHOR
from fltkModif import *
from deterPiece import *
from echecTrad import *
from copy import deepcopy
import os
import subprocess
import tkinter as tk

# dimensions du jeu
taille_case = 100
largeur_plateau = 12  # Echiquier = 8x8
hauteur_plateau = 8


# Définition des fonction
def case_vers_pixel(case):
    """
    Fonction recevant les coordonnées d'une case du plateau sous la
    forme d'un couple d'entiers (id_colonne, id_ligne) et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case. Ce calcul
    prend en compte la taille de chaque case, donnée par la variable
    globale taille_case.
    :param: case tuple
    :return: float, float

    >>> case_vers_pixel((0,0))
    50, 50
    >>> case_vers_pixel((7, 5))
    750, 550
    """
    i, j = case

    return (i + .5) * taille_case, (j + .5) * taille_case


def recup_case(coorClick, saveEntry):
    """
    Fonction qui récupère la case sur la quelle le joueur a cliquer en
    fonction des coordonnées en pixels du curseurs
    c'est l'inverse de la fonction 'case_vers_pixel'
    :param: coorClick tuple
    :return: tuple

    >>> recup_case((100, 140))
    (1,1)
    >>> recup_case((500, 700))
    (5,7)
    """
    x, y = coorClick

    x = x // 100
    if x > 7:  # Si le clique dans le menue
        click_Menu(coorClick, saveEntry)

    y = y // 100

    return (x, y)  # On retourne les coordonnées de la case en tuple


def click_MenuDebut(menu, coorClick):
    """
    Focntion qui gère les cliques dans le menue qui s'affiche au lancement
    du jeu. On renvoie l'etat du menu
    :param: coorClick tuple
    :return: bool
    """
    x, y = coorClick

    if 45 < x < 1165 and 690 < y < 770:
        menu = False
    if 50 < x < 200 and 550 < y < 580:
        if os.name == 'posix':
            subprocess.call(["open", "aide.txt"])
        elif os.name == 'nt':
            os.startfile("aide.txt")

    return menu


def click_Menu(coorClick, saveEntry):
    """
    Focntion qui gère les cliques dans le menue a coter de l'echiquier lors
    d'une partie
    :param: coorClick tuple
    """
    x, y = coorClick

    if 860 < x < 1150 and 750 < y < 790:
        ferme_fenetre()
    if 950 < x < 1060 and  670 < y < 710:
        save_partie(jeu, saveEntry.get())


def save_partie(jeu, nomFichier):
    """
    Fonction qui sauvegarde la partie dans un fichier texte. Le fichier txt
    peut-être utiliser pour charger la partie plus tard. Il porte le nom entré
    dans le champ de saisie par l'utilisateur dans le menu contextuel
    :param: lstPieces lst
    """
    save = open(os.path.abspath('save/' + nomFichier + '.txt'), 'w', errors='replace')

    save.write('JEU:\n')
    save.write(jeu['nameJ1'] + '\n' + jeu['nameJ2'] + '\n' + 
               str(jeu['scoreJ1']) + '\n' + str(jeu['scoreJ2']) + '\n' +
               str(jeu['nCoup']) + '\n' + jeu['tourDe'])
    save.write('\nROCK:\n')
    for rock, boole in jeu['rock'].items():
        save.write(str(boole) + '\n')
    save.write('PIECE:\n')
    save.write('BLANC:\n')
    for piece, coors in jeu['pieces'].items():
        if piece[1:] == 'white':
            for coor in coors:
                save.write(InfoToEchec(piece, coor) + '\n')
    save.write('NOIR:\n')
    for piece, coors in jeu['pieces'].items():
        if piece[1:] == 'black':
            for coor in coors:
                save.write(InfoToEchec(piece, coor) + '\n')

    save.close()


def charger_partie(jeu, nomFichier):
    """
    Fonction qui charge une partie a partir d'un fichier txt, generer lors
    d'une partie precedante, elle modifie les varible principale du jeu
    :param: nomFichier str
    :return: lst
    """
    save = open(os.path.abspath('save/' + nomFichier + '.txt'), 'r', errors='replace')

    save.readline()  # On sait que la prmière ligne c'est 'JEU:'
    jeu['nameJ1'] = save.readline()[:-1]; jeu['nameJ2'] = save.readline()[:-1]
    jeu['scoreJ1'] = int(save.readline()[:-1])
    jeu['scoreJ2'] = int(save.readline()[:-1])
    jeu['nCoup'] = int(save.readline()[:-1]); jeu['tourDe'] = save.readline()[:-1]

    save.readline()  # On sait que la prmière ligne c'est 'ROCK:' et qu'il y a 4 booleen apres
    for rock in jeu['rock']:
        jeu['rock'][rock] = bool(save.readline()[:-1])

    save.readline() # On attaque les pieces ('PIECES:')
    save.readline() # ('BLANC:')
    color = 'white'
    for ligne in save:
        if ligne[:-1] == 'NOIR:':
            color = 'black'
            continue
        piece, coor = EchecToInfo(ligne, color)
        jeu['pieces'][piece].append(coor)

    save.close()

# Fonction qui gere le deplacement des pieces


def deter_deplacement(moovedPiece, lstPieces, tourDe, rock=None):
    """
    Fonction qui détermine le deplacement d'une piece donné grace au
    module 'deterPiece', et renvoie la liste des déplacement possible
    pour la piece selectioner
    :param: moovedPiece lst, lstPieces dict
    :return: lst

    >>> deter_deplacement(['pwhite', (0,6)], {'pwhite': [(0, 6)]})
    [(0,5), (0, 4)]
    """
    namePiece = moovedPiece[0][0]
    lstMoov = []

    if namePiece == 'p':
        lstMoov = deterP(moovedPiece, lstPieces)
    if namePiece == 't':
        lstMoov = deterT(moovedPiece, lstPieces)
    if namePiece == 'c':
        lstMoov = deterC(moovedPiece, lstPieces)
    if namePiece == 'f':
        lstMoov = deterF(moovedPiece, lstPieces)
    if namePiece == 'd':
        lstMoov = deterD(moovedPiece, lstPieces)
    if namePiece == 'r':
        lstMoov = deterR(moovedPiece, lstPieces, rock)

    return lstMoov


def suppr_echec_moov(moovedPiece, lstPieces, lstMoov, tourDe):
    """
    cette fonction retire de la liste de deplacement possible les deplacement
    qui laisserais le roi en echec.
    :param: moovedPiece lst, lstPieces dict, lstMoov lst, tourDe str
    :return: lst 
    """
    PieceBouger = deepcopy(moovedPiece)
    finalMoov = deepcopy(lstMoov)
    for moov in lstMoov:
        try:
            PieceBouger[2] = moov
        except IndexError:
            PieceBouger.append(moov)

        piecesCopy = deepcopy(lstPieces)  # On créer une copie du dictionaire pour ne pas mofidier le dictionaire principale
        maj_dic(piecesCopy, PieceBouger)  # On met a jour la copie du dictionnaire
        if deter_echec(piecesCopy, tourDe) == tourDe:
            finalMoov.remove(moov)

    return finalMoov


def recup_piece(lstPieces, coorClick):
    """
    Fonction qui regarde si une pieces se trouve sur la case, sur la quelle
    on vient de cliquer, si oui on retourne la piece et son indice, dans la
    listes des pieces, sinon on retourn None
    :param: lstPieces lst, coorClick tuple
    :return: list or bool

    >>> recup_piece({'pwhite': [(0, 0)]}, (0, 0))
    ['pwhite', (0, 0)]
    >>> recup_piece(({'pwhite': [(0, 0)]}, (0, 1))
    None
    """
    for piece, coorPiece in lstPieces.items():
        for coordonne in coorPiece:
            if coordonne == coorClick:
                return [piece, coordonne]  # Donc moovedPiece[0] = son nom, moovedPiece[1] = coordonees

    return None


def deplacer_piece(coorClick, moovedPiece, lstPieces, lstMoov, tourDe):
    """
    Fonction qui regarde si la case sur la quelle on souhaite deplacer la
    piece selectioner est occuper par une piece de meme couleur ou non. Si
    il y a une piece de la meme couleur, c'est cette piece qui devient la
    piece a deplacer, sinon on deplce la piece selectioner au départ.
    Si jamais aucune piece n'est encore selectioner, elle appelle
    recupe_piece
    :param: coorClick tuple, moovedPiece lst or None, lstPieces dict, lstMoov lst
    :return: bool, None or lst

    >>> deplacer_piece((0, 0), None, {'pwhite': [(0, 0)]}, [], 'white')
    False, ['pwhite', (0, 0)]
    >>> deplacer_piece((0, 1), None, {'pwhite': [(0, 0)]}, [], 'white')
    False, None
    >>> deplacer_piece((1, 1), ['pwhite', (0, 6)], {'pwhite': [(0,6)]}, [(0, 5), (0, 4)], 'white')
    False, ['pwhite', (0, 6)]
    >>> deplacer_piece((0, 1), ['pwhite', (0, 6)], 0], {'pwhite': [(0, 6), (0, 1)]}, [(0, 5), (0, 4)], 'white')
    False, ['pwhite', (0, 1)]
    >>> deplacer_piece((0, 4), ['pwhite', (0, 6)], {'pwhite': [(0, 6)]}, [(0, 5), (0, 4)], 'white')
    True, ['pwhite', (0, 4)]
    """
    if moovedPiece is None:  # si aucune piece n'as encore ete selectionne
        moovedPiece = recup_piece(lstPieces, coorClick)
        if moovedPiece is not None and moovedPiece[0][1:] == tourDe:
            return False, moovedPiece
        return False, None

    for piece in lstPieces:
        if coorClick in lstPieces[piece]:
            if moovedPiece[0][1:] == piece[1:]:  # Si les pieces sont de la même couleurs
                moovedPiece = recup_piece(lstPieces, coorClick)  # On recupere alors la piece nouvellement selectioner
                return False, moovedPiece

    if coorClick not in lstMoov:  # On verifie que la case sur la quelle on clique est dans les deplacement legale de la piece
        return False, moovedPiece

    moovedPiece.append(coorClick)
    return True, moovedPiece


def maj_dic(lstPieces, moovedPiece):
    """
    Cette fonction met a jour le dictionaire des pieces avec la piece tout
    juste deplacer
    :param: lstPieces dict, moovedPiece lst
    """
    lstPieces[moovedPiece[0]].remove(moovedPiece[1])  # On retire l'ancienne coordonné
    lstPieces[moovedPiece[0]].append(moovedPiece[2])  # On ajoute la nouvelle
    lstPieces = manger_piece(moovedPiece, lstPieces)  # On mange une piece si il y a une piece a manger


def maj_rock(rock, moovedPiece, lstPieces):
    """
    Met a jour la 'disponibilité' des rocks, si un roi bouge ces deux rock
    sont alors rendu imposible a faire. Si c'est une tour, seul son rock
    est rendu impossible
    :param: rock dict, moovedPiece 
    """
    if moovedPiece[0] == "rwhite":
        rock[(0, 7)] = False
        rock[(7, 7)] = False
    elif moovedPiece[0] == "rblack":
        rock[(0, 0)] = False
        rock[(7, 0)] = False
    elif moovedPiece[0][0] == "t":
        rock[moovedPiece[1]] = False

    deplace_rock(lstPieces, moovedPiece)


def deplace_rock(lstPieces, moovedPiece):
    """
    si jamais un roi fait rock, on bouge alors la tour du rock
    correspondant
    :param: lstPieces dict, moovedPiece lst
    """
    if moovedPiece[0] == "rwhite":
        if moovedPiece[1] == (4, 7) and moovedPiece[2] == (6, 7):
            maj_dic(lstPieces, ["twhite", (7, 7), (5, 7)])
        if moovedPiece[1] == (4, 7) and moovedPiece[2] == (2, 7):
            maj_dic(lstPieces, ["twhite", (0, 7), (3, 7)])
    if moovedPiece[0] == "rblack":
        if moovedPiece[1] == (4, 0) and moovedPiece[2] == (6, 0):
            maj_dic(lstPieces, ["tblack", (7, 0), (5, 0)])
        if moovedPiece[1] == (4, 0) and moovedPiece[2] == (2, 0):
            maj_dic(lstPieces, ["tblack", (0, 0), (3, 0)])


def check_pion_dame(jeu):
    """
    cette fonction regarde si un pion est arriver sur la derniere ligne
    si oui, il se transforme en dame !
    :param: jeu dict
    """
    for coor in jeu['pieces']['pwhite']:
        x, y = coor
        if y == 0:
            jeu['pieces']['pwhite'].remove(coor)
            jeu['pieces']['dwhite'].append(coor)
    for coor in jeu['pieces']['pblack']:
        x, y = coor
        if y == 7:
            jeu['pieces']['pblack'].remove(coor)
            jeu['pieces']['dblack'].append(coor)

def manger_piece(moovedPiece, lstPieces):
    """
    Fonction qui ragarde si la case d'arriver de la piece tout juste deplacer
    contient une piece (obligatoirement de la couleur oppose). si c'est le cas
    on supprime la pieces manger de la listes des pieces, sinon on ne fait rien
    :param: moovedPiece lst, lstPieces dict
    :return: dict

    >>> manger_piece(['pwhite', (1, 1)], {'pwhite': [(0,6), (1,1)], 'pblack': [(1, 2)]})
    {'pwhite': [(0,6), (1,1)], 'pblack': [(1, 2)]}
    >>> manger_piece(['pwhite', (1, 2)], {'pwhite': [(0,6), (1,1)], 'pblack': [(1, 2)]})
    {'pwhite': [(0,6), (1,2)], 'pblack': []}
    """
    for piece, coorP in lstPieces.items():
        for coordonne in coorP:
            if moovedPiece[2] == coordonne and moovedPiece[0] != piece:
                lstPieces[piece].remove(coordonne)

    return lstPieces


def deter_echec(lstPieces, tourDe):
    """
    Fonction qui reagarde si l'un des deux roi est en echec, si oui on renvoie
    la couleur du roi mis en echec
    :param: lstPieces dict, tourDe str
    :return: str or None
    """
    attackColor, echecColor = 'white', 'black'
    for i in range(2):
        for piece, coorPieceLst in lstPieces.items():
            for coorPiece in coorPieceLst:
                coorR = lstPieces['r' + echecColor][0]  # Le roi n'as qu'une seul position
                if piece[1:] == attackColor:
                    lstMoov = deter_deplacement([piece, coorPiece],
                                                lstPieces, tourDe)
                    if coorR in lstMoov:
                        return echecColor
        attackColor, echecColor = 'black', 'white'

    return None


def mat_ou_pat(lstPieces, tourDe, echec):
    """
    Fonction qui regarde si il y a mat ou pat. Pour ça la fonction regarde
    la taille de la liste des pieces, si aucune piece n'as de deplacement
    alors on regarde si le roi est en echecs, si le roi est en echecs, il
    y a mat ! Sinon c'est pat.
    :param: lesPieces dict, tourDe str, echec str
    :return: None or str
    """
    for piece, coorPieceLst in lstPieces.items():
        for coorPiece in coorPieceLst:
            if piece[1:] == tourDe:
                lstMoov = deter_deplacement([piece, coorPiece], lstPieces,
                                            tourDe)
                lstMoov = suppr_echec_moov([piece, coorPiece], lstPieces,
                                            lstMoov, tourDe)

                if len(lstMoov) != 0:
                    return None

    if echec == tourDe:
        return tourDe
    else:
        return 'pat'


# Fonction pour dessiner

def dessiner_echiquier(lstPieces):
    """
    Fonction qui dessine un echequier de 8x8, en prenant soins d'alterner
    correctement la couleur des cases
    """
    efface_tout()

    couleurCase = '#779556'
    for i in range(8):  # pour chaque ligne
        if couleurCase == '#ebecd0':
            couleurCase = '#779556'  # on assure que les couleurs ne se repette pas de la même manière
        elif couleurCase == '#779556':
            couleurCase = '#ebecd0'  # sur tout les lignes (il y a un décallage de 1 a chaque fois)
        for j in range(8):  # pour chaque colone
            x, y = case_vers_pixel((i, j))  # On recupère le centre de la case
            x -= 50  # on vas dans le coins en haut a gauche
            y -= 50  # on vas dans le coins en haut a gauche
            rectangle(x, y, x+100, y+100, remplissage=couleurCase, epaisseur=0)
            if couleurCase == '#779556':
                couleurCase = '#ebecd0'  # on inverse la couleurs des case les unes aprèes les autres
            elif couleurCase == '#ebecd0':
                couleurCase = '#779556'

    dessiner_pieces(lstPieces)


def dessiner_menu(tourDe, nombreCoup, nj1, nj2, sj1, sj2):
    """
    fonction qui dessine le menu a droite de l'echiquier
    """
    # haut du menu
    if tourDe == "white":
        texte(1000, 35, ("Au tour de: " + nj1 + "\n(blanc)" + "    Coup N°" +
                         str(nombreCoup)), ancrage='center')
    else:
        texte(1000, 35, ("Au tour de: " + nj2 + "\n(noir)" + "    Coup N°" +
                         str(nombreCoup)), ancrage='center')
    texte(1000, 100, (nj1 + ": " + str(sj1) + "  " + nj2 + ": " + str(sj2)),
          ancrage='center')

    # bouton save
    saveName = tk.Entry(fenetre.root, bg="lightgrey")
    texte(830, 650, 'nom de la sauvegarde:', ancrage='w', taille=15)
    zoneSaveEntry = fenetre.canvas.create_window(1050, 652, window=saveName,
                                                 anchor='w')
    rectangle(950, 670, 1060, 710, epaisseur=2)
    texte(1005, 690, 'SAVE', ancrage='center')

    # bouton quitter 
    rectangle(860, 750, 1150, 790, epaisseur=5)
    texte(1005, 770, 'QUITTER', ancrage='center')

    return saveName


def dessiner_pieces(lstP):
    """
    Fonction qui represante les pieces sur l'echiquier en fonction de
    la liste des pieces sur le plateau
    :param: lstP dict
    """
    for piece, coorP in lstP.items():
        for coordone in coorP:
            x, y = case_vers_pixel(coordone)
            image(x, y, piece + '.png')


def dessinner_moov(lstMoov):
    """
    Recupere la liste des mouvement possible de la piece selectionner
    et les represente sur l'echiquier par un cercle transparant sur les
    case possible pour la piece
    :param: lstMoov lst
    """
    for moov in lstMoov:
        x, y = case_vers_pixel(moov)
        cercle(x, y, 20, '#ffa800', epaisseur=3, tag='moov')

# Fonction de fin de partie


def restartPartie(jeu, looserName):
    jeu['pieces'] = {'pwhite': [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)],
                     'pblack': [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
                     'twhite': [(0, 7), (7, 7)], 'tblack': [(0, 0), (7, 0)],
                     'cwhite': [(1, 7), (6, 7)], 'cblack': [(1, 0), (6, 0)],
                     'fwhite': [(2, 7), (5, 7)], 'fblack': [(2, 0), (5, 0)],
                     'dwhite': [(3, 7)], 'dblack': [(3, 0)],
                     'rwhite': [(4, 7)], 'rblack': [(4, 0)]}

    jeu['nCoup'] = 1
    jeu['tourDe'] = 'white'
    jeu['nameJ1'], jeu['nameJ2'] = jeu['nameJ2'], jeu['nameJ1']

    if looserName == 'pat':
        jeu['scoreJ1'] += 0.5
        jeu['scoreJ2'] += 0.5
    elif looserName == 'white':
        jeu['scoreJ2'] += 1
    else:
        jeu['scoreJ1'] += 1

    jeu['scoreJ1'], jeu['scoreJ2'] = jeu['scoreJ2'], jeu['scoreJ1']

# Corps du programme


if __name__ == "__main__":
    # Initialisation des variables
    fenetre = cree_fenetre(taille_case * largeur_plateau,  # Création de la fenetre et recuperation de sa reference
                           taille_case * hauteur_plateau)

    pieces = {'pwhite': [],'pblack': [],
              'twhite': [], 'tblack': [],
              'cwhite': [], 'cblack': [],
              'fwhite': [], 'fblack': [],
              'dwhite': [], 'dblack': [],
              'rwhite': [], 'rblack': []}

    rock = {(7, 7): True, (0, 7): True, (7, 0): True, (0, 0): True}  # [petit rock blanc, grand rock blanc, petit rock noir, grand rock noir]

    jeu = {'pieces': pieces, 'nameJ1': '', 'nameJ2': '', 'rock': rock,
           'scoreJ1': 0, 'scoreJ2': 0, 'nCoup': 0, 'tourDe': 'white'}

    nameJ1E = tk.Entry(fenetre.root, bg="lightgrey")
    nameJ2E = tk.Entry(fenetre.root, bg="lightgrey")
    loadE = tk.Entry(fenetre.root, bg="lightgrey")

    menu = True
    while menu is True:  # Menue de début du jeu
        # on dessine le menu
        image(0, 0, "MenuPrincipale.png", "nw")
        zoneEntry1 = fenetre.canvas.create_window(500, 329, window=nameJ1E)
        zoneEntry2 = fenetre.canvas.create_window(500, 383, window=nameJ2E)
        texte(50, 520, ("Nom de la sauvegarde:"), ancrage='w')
        zoneLoadE = fenetre.canvas.create_window(450, 520, window=loadE)
        rectangle(50, 550, 200, 580, epaisseur=2)
        texte(125, 565, 'aide', ancrage='center')

        coorClick = attend_clic_gauche()
        menu = click_MenuDebut(menu, coorClick)

    jeu['nameJ1'] = nameJ1E.get()
    jeu['nameJ2'] = nameJ2E.get()

    load = loadE.get()
    if load != '':
        charger_partie(jeu, load)
    else:
        jeu['pieces'] = {'pwhite': [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)],
                         'pblack': [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
                         'twhite': [(0, 7), (7, 7)], 'tblack': [(0, 0), (7, 0)],
                         'cwhite': [(1, 7), (6, 7)], 'cblack': [(1, 0), (6, 0)],
                         'fwhite': [(2, 7), (5, 7)], 'fblack': [(2, 0), (5, 0)],
                         'dwhite': [(3, 7)], 'dblack': [(3, 0)],
                         'rwhite': [(4, 7)], 'rblack': [(4, 0)]}

    jouer = True
    while jouer is True:  # Boucle de la partie
        # A chaque coup on efface le board et on le redessine avec la nouvelle position des pieces !
        dessiner_echiquier(jeu['pieces'])
        if jeu['tourDe'] == 'white':
            jeu['nCoup'] += 1  # A chaque fois que c'est au blanc de jouer, on incrémante
        saveEntry = dessiner_menu(jeu['tourDe'], jeu['nCoup'], jeu['nameJ1'],
                                      jeu['nameJ2'], jeu['scoreJ1'],
                                      jeu['scoreJ2'])  # On dessine le menu sur le coter de l'echiquier

        echec = deter_echec(jeu['pieces'], jeu['tourDe'])  # On rergarde si il y a echec pour les blanc ou bien les noirs
        matPat = mat_ou_pat(jeu['pieces'], jeu['tourDe'], echec)

        # Si il y a un MAT ou un PAT on reset le board et on cahnge les joueur de coté
        if matPat is not None:
            restartPartie(jeu, matPat)

            dessiner_echiquier(jeu['pieces'])
            tourDe = 'white'
            saveEntry = dessiner_menu(jeu['tourDe'], jeu['nCoup'], jeu['nameJ1'],
                                      jeu['nameJ2'], jeu['scoreJ1'],
                                      jeu['scoreJ2'])

        # Initialisation des variable qui se réinitialise a chaque coup
        validMoov = False
        MoovedPiece = None  # Piece selectioner par le joueurs
        lstMoov = []  # Liste des coup possible pour la piece selectioner

        while validMoov is False:  # Boucle pour le coup du joueur
            coorClick = attend_clic_gauche()
            coorClick = recup_case(coorClick, saveEntry)

            validMoov, MoovedPiece = deplacer_piece(coorClick, MoovedPiece,
                                                    jeu['pieces'], lstMoov, 
                                                    jeu['tourDe'])
            if MoovedPiece is not None:
                lstMoov = deter_deplacement(MoovedPiece, jeu['pieces'],
                                            jeu['tourDe'], rock)
                lstMoov = suppr_echec_moov(MoovedPiece, jeu['pieces'],
                                           lstMoov, jeu['tourDe'])
                efface('moov')
                dessinner_moov(lstMoov)

        maj_rock(rock, MoovedPiece, jeu['pieces'])
        maj_dic(jeu['pieces'], MoovedPiece)
        check_pion_dame(jeu)

        # On met a jour a qui c'est de jouer
        if jeu['tourDe'] == 'white':
            jeu['tourDe'] = 'black'
        else:
            jeu['tourDe'] = 'white'

    attend_fermeture()
