from solution import Solution
from utils import extract, obj_simple, obj_simple_2, v_permute_one, recuit, tabou, brute_force, descente, get_best_voisin, get_best_voisin_small, nb_voisins
import json
import os
import datetime
import matplotlib.pyplot as plt
import numpy as np


def logprint(*args, sep=' ', end='\n'):

    for a in args:
        s = str(a)
        if log_file is not None:
            log_file.write(s + sep)
        print(s, sep=sep, end='')

    if log_file is not None:
        log_file.write(end)
    print(end=end)


def make_graph(means, filename):

    colors = ['b', 'r', 'g', 'y', 'k', 'm']

    title = ''

    for i, k in enumerate(means.keys()):
        x = np.linspace(0, max_time, len(means[k]))
        plt.plot(x, means[k], colors[i])
        title += colors[i] + '=' + k + '  '

    plt.title(title)
    plt.ylabel('Fitness')
    plt.xlabel('Time')

    graph_path = 'logs/main/'
    try:
        os.mkdir(graph_path)
    except FileExistsError:
        pass
    plt.savefig(graph_path + str(now.day)+'_'+str(now.hour)+'h'+str(now.minute)+filename+'.png')
    plt.close()


def compute_mean(min_at_step, algo):
    if means[algo] == []:
        means[algo] = min_at_steps[:]
    else:
        min_len = min(len(means[algo]), len(min_at_step))

        for i in range(min_len):
            means[algo][i] = ((n_test + 1) * means[algo][i] + min_at_step[i]) / (n_test + 2)

        if len(means[algo]) == min_len:
            for i in range(min_len, len(min_at_step)):
                means[algo].append(((n_test + 1) * means[algo][-1] + min_at_step[i]) / (n_test + 2))
        else:
            for i in range(min_len, len(means[algo])):
                means[algo][i] = ((n_test + 1) * means[algo][i] + min_at_step[-1]) / (n_test + 2)


# *********************************************************************************************

TEST_MODE = False
plt.rcParams['figure.figsize'] = [25, 10]   # Pour que ce soit plus grand

conf_path = 'configs/main.json'

log_file = open('logs/main.log', 'a')
logprint("\n\n**************************************************")
logprint("**************************************************")
logprint("**************************************************")

now = datetime.datetime.now()

means = {'recuit': [],
         'tabou': [],
         'descente': [],
         'brute_force': []
         }

with open(conf_path, 'r') as file:
    d = json.load(file)

    emplacements, equipments = extract('data/' + d['file'])

    NB_TESTS = d['nb_tests']  # Nombre de fois où l'on répète l'expérience

    # Calcul temps total
    tps_total = d['runtime']*4*NB_TESTS
    print('Total runtime :', tps_total / 60, 'mins (', tps_total / 3600, 'h )')

    for n_test in range(NB_TESTS):

        s = Solution(emplacements, equipments)

        max_time = d["runtime"]

        now = datetime.datetime.now()

        logprint("\n\n**************************************************")
        logprint(now)
        logprint('Test nb = ', n_test, '\n')
        if TEST_MODE:
            max_time = 1
            logprint('----- TEST MODE ------')
        logprint(d)
        logprint('runtime = ', max_time)
        logprint("Fitness initiale : ", obj_simple(s))
        logprint("Nombre de voisins : ", nb_voisins(s))

        # Recuit
        logprint('\n -- RECUIT -- ')
        s_recuit, f_min, nb_steps, value_at_steps, min_at_steps = recuit(f_voisin=v_permute_one,
                                                                         f_obj=obj_simple_2,
                                                                         s=s,
                                                                         mu=d['mu'],
                                                                         max_time=max_time,
                                                                         return_stats=True)
        logprint('mu = ', d['mu'])
        logprint("Fitness recuit : ", f_min)
        logprint("nb_steps = ", nb_steps)
        compute_mean(min_at_steps, 'recuit')
        del value_at_steps, min_at_steps

        # Méthode tabou
        list_size = d['list_size']
        f_voisin = get_best_voisin

        s_tabou, f_min, nb_steps, value_at_steps, min_at_steps = tabou(f_voisin=f_voisin,
                                                                       f_obj=obj_simple_2,
                                                                       s=s,
                                                                       list_size=list_size,
                                                                       max_time=max_time,
                                                                       return_stats=True)
        logprint('\n -- TABOU -- ')
        logprint('list_size = ', list_size)
        logprint('f_voisin = ', f_voisin)
        logprint("Fitness tabou : ", f_min)
        logprint("nb_steps = ", nb_steps)
        compute_mean(min_at_steps, 'tabou')
        del value_at_steps, min_at_steps

        # Descente
        f_voisin = get_best_voisin

        s_d, f_min, nb_steps, value_at_steps, min_at_steps, nb_restart = descente(f_voisin,
                                                                                  obj_simple_2,
                                                                                  s,
                                                                                  max_time=max_time,
                                                                                  return_stats=True)
        logprint('\n -- DESCENTE -- ')
        logprint('f_voisin = ', f_voisin)
        logprint("Fitness descente: ", f_min)
        logprint("nb_steps = ", nb_steps)
        logprint('nb_restart = ', nb_restart)
        compute_mean(min_at_steps, 'descente')
        del value_at_steps, min_at_steps

        s_brute_force, f_min, nb_steps, value_at_steps, min_at_steps = brute_force(obj_simple_2,
                                                                                   s,
                                                                                   max_time,
                                                                                   return_stats=True)
        logprint('\n -- BRUTE FORCE --')
        logprint("Fitness Brute Force: ", f_min)
        logprint("nb_steps = ", nb_steps)
        compute_mean(min_at_steps, 'brute_force')
        del value_at_steps, min_at_steps

    make_graph(means, ('_' + d['file'][:-4] + '_' + str(d['runtime'])))
log_file.close()
