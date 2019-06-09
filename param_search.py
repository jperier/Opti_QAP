from solution import Solution
from utils import extract, obj_simple, obj_simple_2, v_permute_one, recuit, tabou, brute_force, descente, get_best_voisin, get_best_voisin_small, nb_voisins
import json
from os import listdir
from os.path import isfile, join
import os
import datetime
import matplotlib.pyplot as plt


def logprint(*args, sep=' ', end='\n'):

    for a in args:
        s = str(a)
        if log_file is not None:
            log_file.write(s + sep)
        print(s, sep=sep, end='')

    if log_file is not None:
        log_file.write(end)
    print(end=end)


def make_graph(file, nb_steps, value_at_steps, min_at_steps):
    if len(value_at_steps) == 0 or len(min_at_steps) == 0:
        return
    gap = nb_steps/len(value_at_steps)
    axis = [i*gap for i in range(len(value_at_steps))]

    plt.plot(axis, value_at_steps, 'b')
    plt.plot(axis, min_at_steps, 'r')
    plt.ylabel('Fitness')
    plt.xlabel('Step')

    graph_path = 'logs/'+file+'/'
    try:
        os.mkdir(graph_path)
    except FileExistsError:
        pass
    plt.savefig(graph_path + str(now.day)+'_'+str(now.hour)+'h'+str(now.minute)+'.pdf')
    plt.close()


# *********************************************************************************************

TEST_MODE = False
plt.rcParams['figure.figsize'] = [25, 10]   # Pour que ce soit plus grand

conf_path = 'configs/'
files = [f for f in listdir(conf_path) if isfile(join(conf_path, f))]

# Calcul temps total, initialisation des solutions
tps_total = 0
solutions = {}
for f in files:
    with open(conf_path+f, 'r') as file:
        d = json.load(file)
        for t in d['runtimes']:
            if d['algo'] == 'recuit':
                n = len(d['mus'])

            elif d['algo'] == 'tabou':
                n = len(d['list_sizes'])
                if d['f_voisin_small']:
                    n *= 2

            elif d['algo'] == 'descente' and d['f_voisin_small']:
                n = 2

            else:
                n = 1

            tps_total += n*t
        emplacements, equipments = extract('data/'+d['file'])
        solutions[d['file']] = Solution(emplacements, equipments)

print('Total runtime :', tps_total/60, 'mins (', tps_total/3600, 'h )')

now = datetime.datetime.now()

log_file = None

for f in files:

    with open(conf_path+f, 'r') as file:
        d = json.load(file)

        path = 'data/' + d['file']
        s = solutions[d['file']]

        for max_time in d["runtimes"]:

            if log_file is not None:
                log_file.close()
            log_file = open('logs/'+f[:-5]+'.log', 'a')

            now = datetime.datetime.now()
            logprint("\n\n**************************************************")
            logprint(now, '\n')
            if TEST_MODE:
                max_time = 1
                logprint('----- TEST MODE ------')
            logprint('Config : ', f, '\n')
            logprint(d)
            logprint('runtime = ', max_time)
            logprint("Fitness initiale : ", obj_simple(s))
            logprint("Nombre de voisins : ", nb_voisins(s))

            # Recuit
            if d['algo'] == 'recuit':

                for mu in d['mus']:
                    s_recuit, f_min, nb_steps, value_at_steps, min_at_steps = recuit(f_voisin=v_permute_one,
                                                                                     f_obj=obj_simple_2,
                                                                                     s=s,
                                                                                     mu=mu,
                                                                                     max_time=max_time,
                                                                                     return_stats=True)
                    logprint('mu = ', mu)
                    logprint("Fitness recuit : ", f_min)
                    logprint("nb_steps = ", nb_steps)

            # Méthode tabou
            elif d['algo'] == 'tabou':

                for list_size in d['list_sizes']:
                    if d['f_voisin_small']:
                        f_voisin = get_best_voisin_small
                    else:
                        f_voisin = get_best_voisin

                    s_tabou, f_min, nb_steps, value_at_steps, min_at_steps = tabou(f_voisin=f_voisin,
                                                                                   f_obj=obj_simple_2,
                                                                                   s=s,
                                                                                   list_size=list_size,
                                                                                   max_time=max_time,
                                                                                   return_stats=True)
                    logprint('\nlist_size = ', list_size)
                    logprint('f_voisin = ', f_voisin)
                    logprint("Fitness tabou : ", obj_simple_2(s_tabou))
                    logprint("nb_steps = ", nb_steps)

            elif d['algo'] == 'descente':
                if d['f_voisin_small']:
                    f_voisin = get_best_voisin_small
                else:
                    f_voisin = get_best_voisin

                s_d, f_min, nb_steps, value_at_steps, min_at_steps, nb_restart = descente(f_voisin,
                                                                                          obj_simple_2,
                                                                                          s,
                                                                                          max_time=max_time,
                                                                                          return_stats=True)
                logprint('f_voisin = ', f_voisin)
                logprint("Fitness descente: ", f_min)
                logprint("nb_steps = ", nb_steps)
                logprint('nb_restart = ', nb_restart)

            elif d['algo'] == 'brute_force':
                s_brute_force, f_min, nb_steps, value_at_steps, min_at_steps = brute_force(obj_simple_2,
                                                                                           s,
                                                                                           max_time,
                                                                                           return_stats=True)
                logprint("Fitness Brute Force: ", f_min)
                logprint("nb_steps = ", nb_steps)

            # Graphe et libération de la mémoire
            make_graph(f[:-5], nb_steps, value_at_steps, min_at_steps)
            del value_at_steps, min_at_steps

