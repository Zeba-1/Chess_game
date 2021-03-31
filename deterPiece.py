#Module contenant tout les fonction pour determiner les deplacement possible des pieces

def regarde_piece(coorDeplacement, lstPieces, needPieces = False):
    """
    Fonction qui check si une piece se trouve sur la case demander,
    si il y'en a une on renvoie False, sinon on renvois True. On peut
    aussi récuperer la piece qui se trouve sur la case si il y'en a une
    :param: coorDeplacement tuple, lstPieces dict, needPieces bool
    :return: bool, None or lst

    >>> reagarde_piece((0, 4), {'pwhite': [(0,6), (1,1)], 'pblack': [(1, 2)]})
    False
    >>> reagarde_piece((0, 4), {'pwhite': [(0,6), (1,1)], 'pblack': [(0, 4)]}, True)
    False, ['pblack', (0,4)]
    >>> reagarde_piece((0, 3), {'pwhite': [(0,6), (1,1)], 'pblack': [(1, 2)]})
    True, None
    """
    x, y = coorDeplacement
    if (0 > x or x > 7) or (0 > y or y > 7):
        return False, None

    for piece, coorPiece in lstPieces.items():
        for coordonne in coorPiece:
            if coorDeplacement == coordonne:
                if needPieces:
                    return False, [piece, coordonne]
                else:
                    return False
    
    return True, None

def deterPintermediaire(coorP, colorP, startLigne, direction, lstPieces):
    """
    Cette fonction determiner le deplacement possible pour un pioin en faisant la difference 
    entre pion blanc et pion noir
    """
    lstMoov = []
    xP, yP = coorP

    if yP == startLigne:
            if regarde_piece((xP, yP + 1 * direction), lstPieces):
                lstMoov.append((xP, yP + 1 * direction))
                if regarde_piece((xP, yP + 2 * direction), lstPieces):
                    lstMoov.append((xP, yP + 2 * direction))
    else:
        if regarde_piece((xP, yP + 1 * direction), lstPieces):
            lstMoov.append((xP, yP + 1 * direction))

    for i in range(-1, 2, 2):
        havePiece, attackPiece = regarde_piece((xP - i, yP + 1 * direction), lstPieces, True)
        if havePiece == False:
            if attackPiece != None and attackPiece[0][1:] != colorP:
                lstMoov.append(attackPiece[1])

    return lstMoov


def deterP(piece, lstPieces):
    """
    Fonction qui calcule les coup possible pour un pion, noir ou blanc.
    Il prend en conte le deplacement double possible a la position de 
    départ et la prise en diagonale

    >>> deterP([['pwhite', (0,6)], 0], [['pwhite', (0,6)]])
    [(0,5), (0, 4)]
    >>> deterP([['pwhite', (0,5)], 0], [['pwhite', (0,6)]])
    [(0, 4)]
    >>> deterP([['pwhite', (0,5)], 0], [['pwhite', (0,6)], ['pblack', (1, 4)]])
    [(0, 4), (1, 4)]
    """
    lstMoov = []

    if piece[0][1:] ==  'white':
        lstMoov = deterPintermediaire(piece[1], 'white', 6, -1, lstPieces)

    elif piece[0][1:] ==  'black':
        lstMoov = deterPintermediaire(piece[1], 'black', 1, 1, lstPieces)

    return lstMoov

def deterT(piece, lstPieces):
    """
    Fonction qui calcule les coup possible pour une Tour, noir ou blanc.
    :param: piece lst, lstPieces dict
    :return: lst
    """
    lstMoov = []
    lstMoov += deterLignediag(piece[1], piece[0][1:], (0, -1), lstPieces)
    lstMoov += deterLignediag(piece[1], piece[0][1:], (0, 1), lstPieces)
    lstMoov += deterLignediag(piece[1], piece[0][1:], (1, 0), lstPieces)
    lstMoov += deterLignediag(piece[1], piece[0][1:], (-1, 0), lstPieces)

    return lstMoov

def deterC(piece, lstPieces):
    """
    Fonction qui calcule les coup possible pour un Cavalier, noir ou blanc.
    :param: piece lst, lstPieces dict
    :return: lst
    """
    lstMoov = []
    xP, yP = piece[1]

    for x in range(-2, 3):
        for y in range(-2, 3):
            if x == y: continue  # On regarde pas quand les x et y sont egale (pas de diagonale pour le fou)
            if -1*x == y: continue  # On regarde pas quand les x et y sont egale (pas de diagonale pour le fou)
            if x == -1*y: continue  # On regarde pas quand les x et y sont egale (pas de diagonale pour le fou)
            if x == 0 or y == 0: continue  #le fou se deplace au moins de 1 sur x ou y
            xt = xP + x  # on ajoute les coordone du cavalier pour calculer par rappoer a sa position
            yt = yP + y

            moovOk, attackPiece = regarde_piece((xt, yt), lstPieces, True)
            if moovOk or (attackPiece != None and attackPiece[0][1:] != piece[0][1:]):
                lstMoov.append((xt, yt))

    return lstMoov

def deterF(piece, lstPieces):
    """
    Fonction qui calcule les coup possible pour un Fou, noir ou blanc.
    :param: piece lst, lstPieces dict
    :return: lst
    """
    lstMoov = []
    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            lstMoov += deterLignediag(piece[1], piece[0][1:], (i, j), lstPieces)

    return lstMoov

def deterD(piece, lstPieces):
    """
    Fonction qui calcule les coup possible pour une Dame, noir ou blanc.
    :param: piece lst, lstPieces dict
    :return: lst
    """
    lstMoov = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            lstMoov += deterLignediag(piece[1], piece[0][1:], (i, j), lstPieces)

    return lstMoov

def deterR(piece, lstPieces, rock):
    """
    Fonction qui calcule les coup possible pour un Roi, noir ou blanc.
    :param: piece lst, lstPieces dict
    :return: lst
    """
    lstMoov = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            lstMoov += deterLignediag(piece[1], piece[0][1:], (i, j), lstPieces, True)

    lstMoov = deterRock(piece, lstPieces, rock, lstMoov)
                
    return lstMoov

def deterRock(piece, lstPieces, rock, lstMoov):
    """
    determine si le roi a la posibilite de rocker ou non, si oui, elle ajoute
    le mouvement a la liste des coup possible
    :param: piece lst, lstPieces dict, rock dict, lstMoov lst
    :return: lst
    """
    if piece[0][1:] == "white" and rock != None:
        if rock[(0, 7)] == True:
            if regarde_piece((2, 7), lstPieces) and regarde_piece((1, 7), lstPieces) and (3, 7) in lstMoov: 
                lstMoov.append((2, 7))
        if rock[(7, 7)] == True:
            if regarde_piece((6, 7), lstPieces) and (5, 7) in lstMoov: 
                lstMoov.append((6, 7))
    elif piece[0][1:] == "black" and rock != None:
        if rock[(0, 0)] == True:
            if regarde_piece((2, 0), lstPieces) and regarde_piece((1, 0), lstPieces) and (3, 0) in lstMoov: 
                lstMoov.append((2, 0))
        if rock[(7, 0)] == True:
            if regarde_piece((6, 0), lstPieces) and (5, 0) in lstMoov: 
                lstMoov.append((6, 0))

    return lstMoov

def deterLignediag(coorP, colorP, direction, lstPieces, doOnce = False):
    """
    Foncrion permetant qui determine les deplacement en diagonal et les
    deplacement sur les lignes. elle ne peut determiner qu'une seul direction
    a la fois !!!!!!! il faut donc appeller la fonction 8 fois pour determiner
    toute les lignes de la dames ou du roi !
    Pour le roi on utilise 'doOnce' pour calculer suelement une fois dans la
    direction voulue
    :param: coorP tuple, colorP stringn, direction int, lstPieces dict, 
    doOnce bool
    :return: lst
    """
    lstMoov = []
    xP, yP = coorP
    x, y = direction
    attackPiece = None

    xP += x
    yP += y
    moovOk, attackPiece = regarde_piece((xP, yP), lstPieces, True)
    while moovOk:
        lstMoov.append((xP, yP))
        xP += x
        yP += y
        if doOnce: 
            moovOk = False
            break
        moovOk, attackPiece = regarde_piece((xP, yP), lstPieces, True)

    if attackPiece != None:
        if attackPiece[0][1:] != colorP:
            lstMoov.append((xP, yP))

    return lstMoov
