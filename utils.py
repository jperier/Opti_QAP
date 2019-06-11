from emplacement import Emplacement
from equipment import Equipment
from solution import Solution
from random import randint, random
from math import exp, log
from time import process_time

NB_STEPS_SAVE = 25


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


def recuit(f_voisin, f_obj, s, mu, max_time=100, return_stats=False):
    """
    voisin : fonction de voisinage
    fObj : fonction objectif
    s : solution initiale
    t0 : température initiale
    n : nombre de mouvements à la température tk
    mu : baisse de température ( < 1)
    """
    assert max_time > 0

    # Recherche d'une bonne valeur de la température
    deltafs = []
    sol = Solution(s.emplacements, s.equipments)
    voisin = f_voisin(sol)
    deltaf = f_obj(voisin) - f_obj(sol)
    for i in range(500):
        while deltaf < 0:
            sol = Solution(s.emplacements, s.equipments)
            voisin = f_voisin(sol)
            deltaf = f_obj(voisin) - f_obj(sol)
        deltafs.append(deltaf)
    somme = 0
    for d in deltafs:
        somme += d
    mean_deltaf = somme/len(deltafs)
    t = -mean_deltaf/log(0.8)
    print('Temperature =', t)

    # Calcul du nombre de changements de températures
    n1 = int(log(-mean_deltaf/(t*log(0.01))) / log(mu))
    print("n1 =", n1)

    s_min = s.copy()
    f_min = f_obj(s)

    start_time = process_time()
    time = 0

    nb_steps = 0
    value_at_steps = []
    min_at_steps = []

    i = 1
    while time < max_time:

        while time < i*(max_time/n1):
            nb_steps += 1

            y = f_voisin(s)
            new_obj = f_obj(y)
            f = f_obj(s)
            deltaf = new_obj - f

            if deltaf < 0:
                s = y
                if new_obj < f_min:
                    s_min = s.copy()
                    f_min = new_obj
            else:
                p = random()
                expo = exp((-1*deltaf)/t)
                if p < expo:
                    s = y.copy()

            # Stats
            if return_stats:
                if nb_steps % NB_STEPS_SAVE == 0 or nb_steps == 1:
                    value_at_steps.append(f)
                    min_at_steps.append(f_min)

            time = (process_time() - start_time)
        i += 1
        t = mu*t

    return s_min, f_min, nb_steps, value_at_steps, min_at_steps


def tabou(f_voisin, f_obj, s, list_size, max_time=100, return_stats=False):
    assert max_time > 0

    s_min = s.copy()
    f_min = f_obj(s)
    tabu_list = []

    start_time = process_time()

    nb_steps = 0
    value_at_steps = []
    min_at_steps = []

    while (process_time() - start_time) < max_time:
        nb_steps += 1
        s, f_current, permutation = f_voisin(s, f_obj, tabu_list)

        if f_min < f_current:
            tabu_list.append(permutation)
            if len(tabu_list) > list_size:
                tabu_list.pop(0)
        else:
            s_min = s.copy()
            f_min = f_current

        # Stats
        if return_stats:
            if nb_steps % NB_STEPS_SAVE == 0 or nb_steps == 1:
                value_at_steps.append(f_current)
                min_at_steps.append(f_min)

    return s_min, f_min, nb_steps, value_at_steps, min_at_steps


def brute_force(f_obj, s, max_time=100, return_stats=False):
    assert max_time > 0

    s_min = s.copy()
    f_min = f_obj(s)

    start_time = process_time()

    nb_steps = 0
    value_at_steps = []
    min_at_steps = []

    while (process_time() - start_time) < max_time:
        nb_steps += 1
        # New random solution
        s = Solution(s.emplacements, s.equipments)
        f = f_obj(s)

        if f < f_min:
            s_min = s.copy()
            f_min = f

        # Stats
        if return_stats:
            if nb_steps % NB_STEPS_SAVE == 0 or nb_steps == 1:
                value_at_steps.append(f)
                min_at_steps.append(f_min)

    return s_min, f_min, nb_steps, value_at_steps, min_at_steps


def descente(f_voisin, f_obj, s, max_time=100, return_stats=False):
    assert max_time > 0

    s_min_global = s.copy()
    f_min_global = f_obj(s)

    s_min = s.copy()
    f_min = f_obj(s)

    start_time = process_time()

    nb_steps = 0
    value_at_steps = []
    min_at_steps = []
    nb_restart = 0

    while (process_time() - start_time) < max_time:
        nb_steps+=1
        s, f, _ = f_voisin(s, f_obj)

        # Descente
        if f < f_min:
            s_min = s.copy()
            f_min = f
            if f < f_min_global:
                s_min_global = s.copy()
                f_min_global = f

        # Nouveau départ
        else:
            nb_restart+=1
            s = Solution(s.emplacements, s.equipments)
            s_min = s.copy()
            f_min = f_obj(s_min)

        # Stats
        if return_stats:
            if nb_steps % NB_STEPS_SAVE == 0 or nb_steps == 1:
                value_at_steps.append(f)
                min_at_steps.append(f_min_global)

    return s_min_global, f_min_global, nb_steps, value_at_steps, min_at_steps, nb_restart


# Fonctions de voisinage :

def get_best_voisin(s, f_obj, tabu_list=None):

    if tabu_list is None:
        tabu_list = []

    s_min = None
    f_min = float('inf')
    permutation = None

    for i in range(len(s.emplacements)):
        for j in range(i+1, len(s.emplacements)):

            if {i, j} not in tabu_list:

                s2 = s.copy()
                cache = s2.x[i]
                s2.x[i] = s2.x[j]
                s2.x[j] = cache

                obj = f_obj(s2)
                if obj < f_min:
                    f_min = obj
                    s_min = s2
                    permutation = {i, j}

    return s_min, f_min, permutation


def nb_voisins(s):
    nb_voisins = 0
    for i in range(1, len(s.emplacements)):
        nb_voisins += i
    return nb_voisins


def get_best_voisin_small(s, f_obj, tabu_list=None):

    if tabu_list is None:
        tabu_list = []

    rand1 = -1
    rand2 = -1
    s_min = None
    f_min = float('inf')
    permutation = None

    for i in range(1000):
        s2 = s.copy()
        while {rand1, rand2} in tabu_list or {rand1, rand2} == {-1, -1}:
            rand2 = randint(0, len(s2.x) - 1)
            rand1 = randint(0, len(s2.x) - 1)
        cache = s2.x[rand1]
        s2.x[rand1] = s2.x[rand2]
        s2.x[rand2] = cache

        obj = f_obj(s2)
        if obj < f_min:
            f_min = obj
            s_min = s2
            permutation = {rand1, rand2}

    return s_min, f_min, permutation


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
    return sum*2


def obj_simple_2(s: Solution):

    sum = 0

    for emp, eq in s.x.items():
        for emp2, eq2 in s.x.items():
            if not(emp == emp2 or eq == eq2):
                sum += s.emplacements[emp].distances[emp2] * s.equipments[eq].weights[eq2]
    return sum


