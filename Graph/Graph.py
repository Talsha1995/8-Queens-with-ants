from ACO.Graph.Edge import Edge
from ACO.Graph.Vertex import Vertex


class Graph:
    def __init__(self, n: int):
        self.n = n
        self.vertex_lst = [Vertex(i, j) for i in range(n) for j in range(n)]
        self.edges_lst = self.__build_edges_lst()

    def __build_edges_lst(self):
        """ building edges list without bad edges. """
        edges_lst = []
        for source in self.vertex_lst:
            for dest in self.vertex_lst:

                # not adding corners
                if dest.row == dest.col == self.n-1 or source.row == source.col == 0:
                    continue
                if (source.row == self.n-1 and source.col == 0) or (dest.row == 0 and dest.col == self.n-1):
                    continue
                # not adding diagonal edges
                if abs(source.row - dest.row) == abs(source.col - dest.col):
                    continue
                # not adding edges in same row and edges with difference that is not one.
                if dest.col - source.col != 1 or source.row == dest.row:
                    continue
                edges_lst.append(Edge(source, dest))

        return edges_lst

    def plot_solution(self, path):
        """
        :param path: list of Edges
        plotting the solution on standard output as a board.
        """
        vertices = [edge.source for edge in path]
        vertices.append(path[-1].dest)
        print("----------------------------------------")
        print("   ", end="")
        for i in range(self.n):
            print(i, end=" ")
        print()
        for i in range(self.n):
            print(f"{i} ", end="")
            for j in range(self.n):
                print("|", end="")
                if Vertex(i, j) in vertices:
                    print("X", end="")
                else:
                    print(" ", end="")
            print()
        print("----------------------------------------")

Graph(4)
