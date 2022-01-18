import os

import numpy as np
from NQueensACO import NQueensACO as ACO

from ACO.ResultsSaver import ResultsSaver
from ACO.running_sets import *


class ACO_Runner:
    def __init__(self, num_of_iterations, save_to_files):
        self.num_of_iterations = num_of_iterations
        self.results_per_n = dict()
        self.results_saver = ResultsSaver()
        self.save_to_files = save_to_files

    def run(self, lst_of_running_sets):
        for running_set in lst_of_running_sets:
            results_per_n = []
            aco = None
            print(f"-------------------- Running: {running_set} --------------------")
            for i in range(self.num_of_iterations):
                print(f"---------- Iteration number {i} ------------")
                aco = ACO(**running_set)
                result = aco.run()
                for path in result:
                    if path not in results_per_n:
                        results_per_n.append(path)
                print(f"N={running_set.get('n')}: iteration {i} -> {len(result)} paths found")
            print(f"N={running_set.get('n')}: total of {len(results_per_n)} paths found")
            self.results_per_n[running_set.get("n")] = results_per_n.copy()
            if self.save_to_files:
                pheromones = aco.pheromones.get_normalized_edge_to_phero_by_column()
                self.results_saver.save_results_to_files(results_per_n, running_set, pheromones)
        self.print_results()

    def simple_run(self, running_set):
        print(f"-------------------- Running: {running_set} --------------------")
        aco = ACO(**running_set)
        result = aco.run()
        self.results_per_n[running_set.get("n")] = result
        self.print_results()

    def print_results(self):
        print("----------------- Total Results -------------------")
        print(self.results_per_n)
        for n, results_per_n in self.results_per_n.items():
            print(f"N={n}: {len(results_per_n)} paths")

    # not implemented
    def plot_results_from_json_file(self, n):
        solutions = self.results_saver.get_results_by_n(n)
        for solution in solutions:
            self.__plot_solution(solution)

    def __plot_solution(self, solution):
        pass


if __name__ == '__main__':
    runner = ACO_Runner(ITERATIONS, SAVE_TO_FILES)
    runner.run(running_sets)
    # runner.simple_run(N16)
