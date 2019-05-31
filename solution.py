from equipment import Equipment
from emplacement import Emplacement
from random import shuffle


class Solution:

    def __init__(self, emplacements, equipments, init: dict=None):
        self.emplacements = tuple(emplacements)
        self.equipments = tuple(equipments)

        if init:
            assert len(emplacements) == len(init) == len(equipments)
            self.x = init
        # Random initialization
        else:
            l = [e.id for e in equipments]
            shuffle(l)
            self.x = {}
            for i, emp in enumerate(emplacements):
                self.x[emp.id] = l[i]

    def __str__(self):
        return str(self.x)

    def __repr__(self):
        return str(self.x)

    def copy(self):
        return Solution(self.emplacements, self.equipments, self.x.copy())
