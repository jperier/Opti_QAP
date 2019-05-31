from emplacement import Emplacement
from equipment import Equipment
from solution import Solution
from random import randint, random
from math import exp
from tqdm import tqdm


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


def recuit(f_voisin, f_obj, s, t, n1, n2, mu):
    """
    voisin : fonction de voisinage
    fObj : fonction objectif
    s : solution initiale
    t0 : température initiale
    n1 : nombre de changement de température
    n2 : nombre de mouvements à la température tk
    mu : baisse de température ( < 1)
    """

    s_min = s.copy()
    f_min = f_obj(s)

    for k in tqdm(range(n1)):
        for l in range(n2):
            y = f_voisin(s)     # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
            new_obj = f_obj(y)
            deltaf = new_obj - f_obj(s)

            if deltaf < 0:
                s = y
                if new_obj < f_min:
                    s_min = s.copy()
                    f_min = new_obj
            else:
                p = random()
                expo = exp((-1*deltaf)/t)
                if p < expo:
                    s = y
        t = mu*t
    return s_min


def tabou(f_voisin, f_obj, s, list_size, max_iter):

    s_min = s.copy()
    f_min = f_obj(s)
    tabu_list = []

    for i in tqdm(range(max_iter)):
        voisins = f_voisin(s)
        s = min(voisins, lambda x: f_obj(x))
        deltaf = f_min - f_obj(s)

        if deltaf > 0:
            tabu_list.append(find_permute()) #s_old



# Fonctions de voisinage :

def find_permute(s1, s2):
    permut = set()
    for i in range(len(s1.emplacements)):
        if s1.x[i] != s2.x[i]:
            permut.add(i)
            if len(permut) == 2:
                return permut

def v_permute_all(s):
    voisins = []
    for i in range(len(s.emplacements)):
        for j in range(i, s.emplacements):
            s2 = s.copy()
            cache = s2.x[i]
            s2.x[i] = s2.x[j]
            s2.x[j] = cache
            voisins.append(s2)
    return voisins


def v_permute_100(s):
    voisins = []
    deja_fait = []
    for i in range(100):
        s2 = s.copy()
        rand1 = randint(0, len(s2.x) - 1)
        rand2 = randint(0, len(s2.x) - 1)
        assert len(s2.x) != 1
        while rand1 == rand2 and ((rand1, rand2) in deja_fait or (rand2, rand1) in deja_fait):
            rand2 = randint(0, len(s2.x) - 1)
        cache = s2.x[rand1]
        s2.x[rand1] = s2.x[rand2]
        s2.x[rand2] = cache
        voisins.append(s2)
    return voisins


def v_permute_one(s):
    s2 = s.copy()
    rand1 = randint(0, len(s2.x) - 1)
    rand2 = randint(0, len(s2.x) - 1)
    assert len(s2.x) != 1
    while rand1 == rand2:
        rand2 = randint(0, len(s2.x) - 1)
    cache = s2.x[rand1]
    s2.x[rand1] = s2.x[rand2]
    s2.x[rand2] = cache
    return s2


# Fonctions objectifs :

def obj_simple(s: Solution):

    sum = 0
    deja_fait = []

    for emp, eq in s.x.items():
        deja_fait.append(emp)

        for emp2, eq2 in s.x.items():
            if not emp2 in deja_fait:
                sum += s.emplacements[emp].distances[emp2] * s.equipments[eq].weights[eq2]
    return sum


