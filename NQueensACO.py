import numpy as np

from Graph.Edge import Edge
from Graph.Graph import Graph
from Graph.PheromonesData import PheromonesData
from tqdm import tqdm
from running_sets import DEBUG


class NQueensACO:
    def __init__(self, n, Nant, Niter, rho, init_pheromone, max_pheromone, seed=None, alpha=1, beta=0
                 ):
        # todo: check with beta <= alpha  &  check beta = 0
        self.n = n
        self.Nant = Nant
        self.Niter = Niter
        self.rho = rho
        self.graph = Graph(n)
        self.pheromones = PheromonesData(self.graph.edges_lst, n, alpha, beta, init_pheromone, max_pheromone)
        self.local_state = np.random.RandomState(seed)

    def run(self):
        """
        This method invokes the ACO search over the TSP graph.
        It returns the best tour located during the search.
        Importantly, 'all_paths' is a list of pairs, each contains a path and its associated length.
        Notably, every individual 'path' is a list of edges, each represented by a pair of nodes.
        """

        perfect_paths = []
        for i in tqdm(range(self.Niter)):
            # todo: check state after 1000 iterations
            if i >= 500:
                print("HERE")
            all_paths = self.constructColonyPaths()
            non_penalty_paths = self.pheromones.update_pheromones_and_get_results(all_paths)
            # todo: add paths to perfect_paths even if not perfect
            for path in non_penalty_paths:
                if path not in perfect_paths:
                    perfect_paths.append(path)
                    print(f"Found new path: {path}")
                    print(f"Total paths found so far: {len(perfect_paths)}")
            self.pheromones.make_evaporation(self.rho)
        for path in perfect_paths:
            self.graph.plot_solution(path)
        return perfect_paths

    def constructSolution(self):
        """
        This method generates a single Hamiltonian tour per an ant, starting from node 'start'
        The output, 'path', is a list of edges, each represented by a pair of nodes.
        """
        path = []
        threats = 1 # np.ones((self.n, self.n))
        prev_row = None
        if DEBUG:
            print("---------------------------------------")
        for col in range(self.n - 1):
            move = self.nextMove(prev_row, col, threats)
            path.append(move)
            prev_row = move.dest.row
        if DEBUG:
            print("---------------------------------------")
        return path

    def constructColonyPaths(self):
        """
        This method generates 'Nant' paths, for the entire colony, representing a single iteration.
        """
        return [self.constructSolution() for _ in range(self.Nant)]

    # def updatedThreats(self, row, column, threats):
    #     """
    #     this method update threats on board (on the next columns -->.. ) that the new queen, that placed in (row, col)
    #     is threat on.
    #     """
    #     for j in range(1, self.n - column):
    #         threats[row][column + j] += 1  # update row
    #         if row + j < self.n:  # update upper diagonal
    #             threats[row + j][column + j] += 1
    #         if row - j < self.n and row - j >= 0:  # update lower diagonal
    #             threats[row - j][column + j] += 1

    def nextMove(self, source_row_index, source_col_index, threats) -> Edge:
        """
        This method probabilistically calculates the next move (node) given a neighboring
        information per a single ant at a specified node.
        Importantly, 'pheromone' is a specific row out of the original matrix, representing the neighbors of the current node.
        Similarly, 'dist' is the row out of the original graph, associated with the neighbors of the current node.
        'visited' is a set of nodes - whose probability weights are constructed as zeros, to eliminate revisits.
        The random generation relies on norm_row, as a vector of probabilities, using the numpy function 'choice'
        """
        edge_to_p = self.pheromones.get_edges_with_probabilities_from_given_column(threats, source_col_index, source_row_index)
        if DEBUG:
            for edge, p in edge_to_p.items():
                print(f"{edge}: {p}")
        edges = []
        probabilities = []
        for edge, prob in edge_to_p.items():
            edges.append(edge)
            probabilities.append(prob)
        # print(f"---------------{source_col_index + 1}")
        # print(probabilities)
        # print()
        move = self.local_state.choice(edges, 1, p=probabilities)[0]
        # if source_col_index == 0: #case of fisrt move so we need to update threate of 2 queens
        #     self.updatedThreats(move.source.row, 0, threats)
        # self.updatedThreats(move.dest.row, move.dest.col, threats)
        if DEBUG:
            print(f"chosen: {move}")
        return move

