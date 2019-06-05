from emplacement import Emplacement
from equipment import Equipment
from solution import Solution
from utils import extract, obj_simple, obj_simple_2, v_permute_one, recuit, tabou, brute_force, descente, get_best_voisin
from time import perf_counter
path = "data/tai12a.dat"


emplacements, equipments = extract(path)
s = Solution(emplacements, equipments)  # init random
print("Fitness initiale :", obj_simple(s))

max_time = 10


s_recuit = recuit(f_voisin=v_permute_one,
                  f_obj=obj_simple_2,
                  s=s,
                  t=5,
                  n=50,
                  mu=0.9,
                  max_time=max_time)
print("Fitness recuit :", obj_simple_2(s_recuit))


s_tabou = tabou(f_voisin=get_best_voisin,
                f_obj=obj_simple_2,
                s=s,
                list_size=50,
                max_time=max_time)
print("Fitness tabou :", obj_simple_2(s_tabou))


s_optimale = Solution(emplacements, equipments, [8,1,6,2,11,10,3,5,9,7,12,4])
print("Fitness opt :", obj_simple(s_optimale))


s_d = descente(obj_simple_2, s, max_time=max_time)
print(obj_simple_2(s_d))


s_brute_force = brute_force(obj_simple_2, s, max_time)
print(obj_simple_2(s_brute_force))