import numpy as np

from ACO.Graph.Edge import Edge
from ACO.Graph.Graph import Graph
from ACO.Graph.PheromonesData import PheromonesData
from tqdm import tqdm
from ACO.running_sets import DEBUG


class NQueensACO:
    def __init__(self, n, Nant, Niter, rho, init_pheromone, max_pheromone, seed=None,
                 ):
        self.n = n
        self.Nant = Nant
        self.Niter = Niter
        self.rho = rho
        self.graph = Graph(n)
        self.pheromones = PheromonesData(self.graph.edges_lst, n, init_pheromone, max_pheromone)
        self.local_state = np.random.RandomState(seed)

    def run(self):
        """
        This method invokes the ACO search over the TSP graph.
        It returns the best tour located during the search.
        Importantly, 'all_paths' is a list of pairs, each contains a path and its associated length.
        Notably, every individual 'path' is a list of edges, each represented by a pair of nodes.
        """

        perfect_paths = []
        for _ in tqdm(range(self.Niter)):
            all_paths = self.constructColonyPaths()
            non_penalty_paths = self.pheromones.update_pheromones_and_get_results(all_paths)
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
        prev_row = None
        if DEBUG:
            print("---------------------------------------")
        for col in range(self.n - 1):
            move = self.nextMove(prev_row, col)
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

    def nextMove(self, source_row_index, source_col_index) -> Edge:
        """
        This method probabilistically calculates the next move (node) given a neighboring
        information per a single ant at a specified node.
        Importantly, 'pheromone' is a specific row out of the original matrix, representing the neighbors of the current node.
        Similarly, 'dist' is the row out of the original graph, associated with the neighbors of the current node.
        'visited' is a set of nodes - whose probability weights are constructed as zeros, to eliminate revisits.
        The random generation relies on norm_row, as a vector of probabilities, using the numpy function 'choice'
        """
        edge_to_p = self.pheromones.get_edges_with_probabilities_from_given_column(source_col_index, source_row_index)
        if DEBUG:
            for edge, p in edge_to_p.items():
                print(f"{edge}: {p}")
        edges = []
        probabilities = []
        for edge, prob in edge_to_p.items():
            edges.append(edge)
            probabilities.append(prob)
        move = self.local_state.choice(edges, 1, p=probabilities)[0]
        if DEBUG:
            print(f"chosen: {move}")
        return move

