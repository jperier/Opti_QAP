class Emplacement:
    """
    documentation
    """
    def __init__(self, id, line, n):
        self.id = id

        line = line.split(' ')
        distances = {}
        i = 0
        for elt in line:
            if elt != '':
                if i != id:
                    distances[i] = int(elt.replace('\n', ''))
                i += 1
        if len(distances) != n-1:
            print("ERROR: len(distances)", len(distances), " != n-1")
        self.distances = distances

        self.equipment = None

    def __str__(self):
        string = 'Emplacement id = ' + str(self.id) + '\n'
        string += '\tDistances:' + str(self.distances) + '\n'
        string += '\tEquipment:' + str(self.equipment.id) + '\n'

        return string

