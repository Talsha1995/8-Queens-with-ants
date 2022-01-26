from Graph.Edge import Edge
from Graph.Vertex import Vertex
from running_sets import DEBUG

class PheromonesData:
    def __init__(self, edges, n, alpha, beta, initial_pheromone=1, max_pheromone=25):
        self.edges = edges
        self.edge_to_phero = {edge: initial_pheromone for edge in edges}
        self.n = n
        self.init_phero = initial_pheromone
        self.max_phero = max_pheromone
        self.alpha = alpha
        self.beta = beta

    def update_pheromones_and_get_results(self, lst_of_paths):
        """
        :param lst_of_paths: all paths found, each path is list of Edges
        :return: paths that made no penalties
        """
        perfect_paths = []
        # path_score_tuples = self.__get_path_to_score_list(lst_of_paths)
        # path_score_tuples = sorted(path_score_tuples, key=lambda x: x[1], reverse=True)
        # best_size = len(path_score_tuples)//4

        best_len = 0
        best_paths = []
        for path in lst_of_paths:
            vertices, threats = self.__count_threats(path)
            if threats == 0:
                perfect_paths.append(path)
                continue
            # else:
            #     if len(path) == best_len:
            #         best_paths.append(path)
            #     elif len(path) > best_len:
            #         best_paths = [path]
            #         best_len = len(path)
            for edge in path:
                # todo: check adding (n-threats_in_path) to pheromones
                self.edge_to_phero[edge] = self.edge_to_phero[edge] + (self.n - threats//2)/100
        return perfect_paths if perfect_paths else best_paths

    def __get_path_to_score_list(self, lst_of_paths):
        for i in range(len(lst_of_paths)):
            path = lst_of_paths[i]
            max_group_no_threats = self.__get_max_group_no_threats(path)
            lst_of_paths[i] = (path, len(max_group_no_threats))

        return lst_of_paths

    def __get_max_group_no_threats(self, path):
        sum_of_threads = 1
        max_group_in_path = path
        while sum_of_threads > 0:
            vertices, sum_of_threads = self.__count_threats(max_group_in_path)
            vertices = sorted(vertices, key=lambda vertex: vertex.threats, reverse=True)
            bad_vertex = vertices.pop(0)
            if bad_vertex.threats == 0:
                break
            max_group_in_path = [edge for edge in max_group_in_path if edge.source != bad_vertex and edge.dest != bad_vertex]
        return max_group_in_path

    def __count_threats(self, path):
        # get vertices in path
        s = set()
        for edge in path:
            s.update({edge.source, edge.dest})
        vertices = list(s)
        # reset threats in vertices
        for vertex in vertices:
            vertex.threats = 0

        length = len(vertices)
        sum_of_threats = 0
        for i in range(length):
            for j in range(i+1, length):
                sum_of_threats += self.__check_edge_penalty(vertices[i], vertices[j])
        return vertices, sum_of_threats

    def __check_edge_penalty(self, source: Vertex, dest: Vertex):
        """ returning True if this edge is breaking the rules. False if it good edge. """
        if source.row == dest.row or source.col == dest.col or abs(source.row - dest.row) == abs(source.col - dest.col):
            source.threats += 1
            dest.threats += 1
            return 2
        return 0

    def get_edges_with_probabilities_from_given_column(self, threats, source_col_index, source_row_index=None):
        """
        returning dict of {.., edge: probability, ...} for all edges from given vertex indexes.
        if source_row_index not given, it will take all vertices from source_col_index.
        in case of first column, source_row_index is not needed(because we don't know the source_row_index).
        """
        if DEBUG:
            print("@@@")
        sum_of_phero = 0
        edges = dict()
        all_same = True
        for edge, phero in self.edge_to_phero.items():
            if phero != 0.1:
                all_same = False
            if source_row_index is not None:
                if edge.source.row == source_row_index and edge.source.col == source_col_index:
                    edge_p = phero ** self.alpha  # * (1/threats[edge.dest.row][edge.dest.col]) ** self.beta
                    edges[edge] = edge_p
                    sum_of_phero += edge_p

            elif edge.source.col == source_col_index:
                edges[edge] = phero
                sum_of_phero += phero
        if all_same:
            print("@@@@")
        # for edge, p in edges.items():
        #     print(f"@ {edge}: {p}")
        # print(sum_of_phero)
        return {edge: phero/sum_of_phero for edge, phero in edges.items()}

    def get_normalized_edge_to_phero_by_column(self):
        edge_to_phero = dict()
        for i in range(self.n):
            for j in range(self.n):
                edge_to_phero.update(self.get_edges_with_probabilities_from_given_column(i, j))
        return edge_to_phero

    def make_evaporation(self, rho):
        """ evaporating """
        min_phero = self.init_phero
        for edge, phero in self.edge_to_phero.items():
            self.edge_to_phero[edge] = max(self.edge_to_phero[edge]*rho, 0.1)
