# This example shows using SolutionPartitioningSolver with FullQuboSolver.
# It makes solving cvrp possible with using FullQuboSolver.

import sys
import os

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_dir, 'src'))

from vrp_solvers import SolutionPartitioningSolver, FullQuboSolver
from vrp_solvers import TabuSolver
import DWaveSolvers
from input import *

if __name__ == '__main__':

    graph_path = os.path.join(project_dir, 'graphs/small.csv')

    # Parameters for solve function.
    only_one_const = 10000000.
    order_const = 1.

    for t in ['example_small1', 'example_small2', 'example_small3']:
        print("Test : ", t)

        # Reading problem from file.
        path = os.path.join(project_dir, 'tests/cvrp/' + t + '.test')
        problem = read_full_test(path, graph_path, capacity = True)

        # Solving problem on SolutionPartitioningSolver.
        solver = SolutionPartitioningSolver(problem, FullQuboSolver(problem))
        solution = solver.solve(only_one_const, order_const, solver_type = 'cpu')

        # Checking if solution is correct.
        if solution == None or solution.check() == False:
            print("Solver hasn't find solution.\n")
            continue

        print("Solution : ", solution.solution) 
        print("Total cost : ", solution.total_cost())
        print("Weights : ", solution.all_weights())
        print("\n")


        # Solving problem on SolutionPartitioningSolver.
        solver = TabuSolver(problem, anti_noiser = False, max_len = 25)
        solution = solver.solve(only_one_const, order_const, solver_type = 'qpu')

        # Checking if solution is correct.
        if solution == None or solution.check() == False:
            print("Tabu Solver hasn't find solution.\n")
        else:
            print("Tabu Solution : ", solution.solution) 
            print("Tabu Total cost : ", solution.total_cost())
            print("\n")
