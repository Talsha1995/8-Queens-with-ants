# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 09:42:08 2018
Updated on Tue Jan 7 20:30:01 2020
@author: ofersh@telhai.ac.il
Based on code by <github/Akavall>
"""
import numpy as np
from HelperMethods import getDistanceMatrix

"""
A class for defining an Ant Colony Optimizer for TSP-solving.
The c'tor receives the following arguments:
    Graph: TSP graph 
    Nant: Colony size
    Niter: maximal number of iterations to be run
    rho: evaporation constant
    alpha: pheromones' exponential weight in the nextMove calculation
    beta: heuristic information's (\eta) exponential weight in the nextMove calculation
    seed: random number generator's seed
"""


class AntforTSP(object):
    def __init__(self, n, Nant, Niter, rho, alpha=1, beta=1, seed=None):
        self.N = n
        self.Nant = Nant
        self.Niter = Niter
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.pheromone = np.ones((n, n ** 2))
        self.local_state = np.random.RandomState(seed)
        """
        This method invokes the ACO search over the TSP graph.
        It returns the best tour located during the search.
        Importantly, 'all_paths' is a list of pairs, each contains a path and its associated length.
        Notably, every individual 'path' is a list of edges, each represented by a pair of nodes.
        """

    def run(self):
        # Book-keeping: best tour ever
        shortest_path = None
        best_path = ("TBD", np.inf)
        for i in range(self.Niter):
            all_paths = self.constructColonyPaths()
            # print(all_paths)
            self.depositPheronomes(all_paths)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if (i + 1) % 100 == 0:
                print(i + 1, ": cur path- ", shortest_path[1], ", best path- ", best_path[1])
            if shortest_path[1] < best_path[1]:
                best_path = shortest_path
            self.pheromone * self.rho  # evaporation
            if shortest_path[1] == self.N:
                return best_path, i + 1
        return best_path, self.Niter

        """
        This method deposits pheromones on the edges.
        Importantly, unlike the lecture's version, this ACO selects only 1/4 of the top tours - and updates only their edges, 
        in a slightly different manner than presented in the lecture.
        """

    def depositPheronomes(self, all_paths):
        all_paths.sort(key=lambda x: x[1])
        for path, path_threats in all_paths[:self.Nant // 4]:
            for queen in range(len(path)):
                row = path[queen][0]
                col = path[queen][1]
                self.pheromone[queen][row * self.N + col] += 1 / path_threats

        """
        This method generates paths for the entire colony for a concrete iteration.
        The input, 'path', is a list of edges, each represented by a pair of nodes.
        Therefore, each 'arc' is a pair of nodes, and thus Graph[arc] is well-defined as the edges' length.
        """

    def evalTour(self, path, threats):
        res = 0
        for queen in path:
            row = queen[0]
            column = queen[1]
            res += threats[row][column]
        return res
        #

    def updatedThreats(self, row, column, threats):
        for j in range(self.N):
            if j != column:
                threats[row][j] += 1  # update row
            if j != row:
                threats[j][column] += 1  # update col
            if j == 0:
                continue
            if row + j < self.N and column + j < self.N:  # update upper diagonal
                threats[row + j][column + j] += 1
            if 0 < row - j < self.N and column + j < self.N:  # update lower diagonal
                threats[row - j][column + j] += 1
            if 0 < row - j < self.N and 0 < column - j < self.N:
                threats[row - j][column - j] += 1
            if row + j < self.N and 0 < column - j < self.N:
                threats[row + j][column - j] += 1

        """
        This method generates a single Hamiltonian tour per an ant, starting from node 'start'
        The output, 'path', is a list of edges, each represented by a pair of nodes.
        """

    def constructSolution(self):
        # visited = [start]
        path = []
        visited = [0, (self.N - 1) * self.N, (self.N - 1) * self.N + self.N - 1,
                   self.N - 1]  # huristic not alloc queen on the corners
        threats = np.ones((self.N, self.N))
        for i in range(self.N):
            (row, col) = self.nextMove(self.pheromone[i], threats, visited)
            visited.append((row * self.N + col))
            self.updatedThreats(row, col, threats)
            path.append((row, col))
        # while len(visited) < len(self.Graph[0]):
        #     next_vertex = self.nextMove(self.pheromone[cur_vertex], self.Graph[cur_vertex], visited)
        #     path.append((cur_vertex, next_vertex))
        #     cur_vertex = next_vertex
        #     visited.append(cur_vertex)
        # path.append((cur_vertex, start))
        return path, threats

        """
        This method generates 'Nant' paths, for the entire colony, representing a single iteration.
        """

    def constructColonyPaths(self):
        # rand_starts = np.random.randint(0, 149, size=(150, 0))
        all_path = []
        for ant in range(self.Nant):
            (path, threats) = self.constructSolution()
            all_path.append((path, self.evalTour(path, threats)))
        return all_path

        """
        This method probabilistically calculates the next move (node) given a neighboring 
        information per a single ant at a specified node.
        Importantly, 'pheromone' is a specific row out of the original matrix, representing the neighbors of the current node.
        Similarly, 'dist' is the row out of the original graph, associated with the neighbors of the current node.
        'visited' is a set of nodes - whose probability weights are constructed as zeros, to eliminate revisits.
        The random generation relies on norm_row, as a vector of probabilities, using the numpy function 'choice'
        """

    def nextMove(self, pheromone, threats, visited):
        threats = np.copy(threats).reshape(self.N * self.N)
        pheromone = np.copy(pheromone)  # Careful: python passes arguments "by-object"; pheromone is mutable
        pheromone[list(visited)] = 0

        squares_prob = pheromone ** self.alpha * ((1.0 / threats) ** self.beta)
        norm_squares_prob = squares_prob / squares_prob.sum()

        move = self.local_state.choice(range(self.N ** 2), 1, p=norm_squares_prob)[0]
        return move // self.N, move % self.N


def main():
    # 30 ants and rho 85
    n = 8
    Niter = 10 ** 3
    aco = AntforTSP(n, 150, Niter, 0.85, alpha=1, beta=2)
    print(aco.run())


main()
