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
                if i != id:
                    weights[i] = int(elt.replace('\n', ''))
                i += 1
        if len(weights) != n-1:
            print("ERROR: len(weights)", len(weights), "!= n-1")
        self.weights = weights

        self.emplacement = None

    def __str__(self):
        string = 'Equipment id = ' + str(self.id) + '\n'
        string += '\tWeights:' + str(self.weights) + '\n'
        string += '\tEmplacement:' + str(self.emplacement.id) + '\n'

        return string

    def __repr__(self):
        return str(self)
