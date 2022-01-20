from Graph.Vertex import Vertex


class Edge:
    def __init__(self, source: Vertex, dest: Vertex):
        self.source = source
        self.dest = dest

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return other.source == self.source and other.dest == self.dest

    def __str__(self):
        return f"{self.source} -> {self.dest}"

    def __repr__(self):
        return self.__str__()
