# encoding=windows-1252

"""
Disclaimer : y'a pas tout qui marche des fois �a bug
gentil cr�ateur : Nephty :)
"""

from math import log2


def findParamsSetAssociative(size, bytesPerLine, addressAlignment, sets, fullyAssociative=False):
    if sets == 0:
        raise ValueError("Sets can't be zero")
    elif sets == 1 and not fullyAssociative:
        lines = size / bytesPerLine
        sets = lines
        k = int(log2(sets))
    else:
        lines = size/bytesPerLine
        if fullyAssociative:
            k = 0
        else:
            linesPerSet = lines/sets
            k = int(log2(linesPerSet))      # s'il y a x lignes, il faut savoir repr�senter des entiers jusque x
                                            # pour pouvoir s�lectionner la ligne n r�pr�sent�e en binaire dans l'adresse

    b = int(log2(bytesPerLine))     # s'il y a x octets par ligne, il faut savoir repr�senter des entiers jusque x
                                    # pour pouvoir s�lectionner l'octet n rep�sent� en binaire dans l'adresse
    t = addressAlignment-b-k
    return {"Tag": f"{t} bits",
            "Set": f"{k} bits",
            "Offset": f"{b} bits"}


def findCacheSize(lines, bytesPerLine, addressAlignment, waysAssociative, fullyAssociative=False):
    b = int(log2(bytesPerLine))
    if fullyAssociative:
        k = 0
    else:
        k = int(log2(lines/waysAssociative))
    t = addressAlignment-b-k
    return {"Taille totale": lines*(t+1+bytesPerLine*8),
            "Capacit�": lines*bytesPerLine*8}


# EXAMPLES :

# print(findParamsSetAssociative(512, 8, 32, 4, fullyAssociative=True))
# print(findCacheSize(8, 32, 32, 2, fullyAssociative=False))
