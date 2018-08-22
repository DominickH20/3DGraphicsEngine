class graph:
    #edge list chosen for practicality of drawing links
    edges = []
    name = ""

    def __init__(self, name):
        self.name = name

    def addEdge(self,v1,v2):
        edges.append(edge(v1,v2))
        v1.addAdj(v2)
        v2.addAdj(v1)

class vertex:

    adjacencies = []

    def __init__(self,data):
        self.data = data

    def addAdj(self,otherVertex):
        self.adjancencies.append(other)

    def __repr__(self):
        return self.data

class edge:

    def __init__(self,v1,v2):
        self.vertex1 = v1
        self.vertex2 = v2

    def __repr__(self):
        return "[" + str(self.vertex1) + "," + str(self.vertex2) + "]"
