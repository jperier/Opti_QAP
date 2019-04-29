class Equipment:
    """
    documentation
    """
    def __init__(self, id, line, n):
        self.id = id

        line = line.split(' ')
        weights = {}
        i = 0
        for elt in line:
            if elt != '':
                i+=1
                if i != id:
                    weights[i] = int(elt.replace('\n', ''))
        if len(weights) != n-1:
            print("ERROR: len(weights) != n-1")
        self.weights = weights

        self.emplacement = None
