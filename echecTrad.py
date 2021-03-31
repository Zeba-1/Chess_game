# Module qui traduit les coordoné des pièces en notatoin échiquéenne
# et inversement

dicoX = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
dicoY = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}


def InfoToEchec(nomPiece, coordonee):
    x, y = coordonee
    return (nomPiece[0].upper() + dicoX[x] + dicoY[y])


def EchecToInfo(piece, couleur):
    return (piece[0].lower() + couleur), (trouve_cle(piece[1], dicoX), trouve_cle(piece[2], dicoY))


def trouve_cle(cle, dic): 
    for k, val in dic.items(): 
        if cle == val: 
            return k