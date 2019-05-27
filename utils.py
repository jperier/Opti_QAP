from emplacement import Emplacement
from equipment import Equipment
from random import randint, random
from math import exp


def extract(filepath):
    lines = []
    with open(filepath, 'r') as f:
        for line in f:
            lines.append(line)

    n = int(lines[0].replace(' ', '').replace('\n', ''))

    emplacements = []
    equipments = []

    i = 0
    for line in lines:
        if len(line) > n:
            if i < n:
                emplacements.append(Emplacement(i, line, n))
            else:
                equipments.append(Equipment(i - n, line, n))
            i += 1

    return emplacements, equipments


def voisinage_permut(xi): #TODO
    rand = randint(len(xi))
    equip1 = xi[rand]


# x une solution sous forme de list ou index = emplacement.id et valeur = equipment.id

def recuit(f_voisin, f_obj, x0, t0, n1, n2, mu):
    """
    voisin : fonction de voisinage
    fObj : fonction objectif
    x0 : solution initiale
    t0 : température initiale
    n1 : nombre de changement de température
    n2 : nombre de mouvements à la température tk
    mu : baisse de température ( < 1)
    """

    xmin = x0
    min = f_obj(x0)
    t = t0
    x = x0
    i = 0

    for k in range(n1):
        for l in range(n2):
            y = f_voisin(x)
            obj = f_obj(y)
            deltaf = obj - f_obj(x)

            if deltaf < 0:
                x = y
                if obj < min:
                    xmin = x
                    min = obj
            else:
                p = random()
                expo = exp((-1*deltaf)/t)
                if p < expo:
                    x = y
        t = mu*t
    return xmin


# Fonctions de voisinage :

def v_permute(x):
    rand1 = randint(len(x))
    rand2 = randint(len(x))
    assert len(x) != 1
    while rand1 == rand2:
        rand2 = randint(len(x))
    y = x[:]
    y[rand1] = x[rand2]
    y[rand2] = x[rand1]

    return y


# Fonctions objectifs :

