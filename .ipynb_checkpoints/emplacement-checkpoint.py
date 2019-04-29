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
                i+=1
                if i != id:
                    distances[i] = int(elt.replace('\n', ''))
        if len(distances) != n-1:
            print("ERROR: len(distances) != n-1")
        self.distances = distances

        self.equipment = None