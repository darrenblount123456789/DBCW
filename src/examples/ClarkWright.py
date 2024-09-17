import sys
import os

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_dir, 'src'))

from vrp_solvers import ClarkWright
from input_CMT_dataset import *


problem, graph = create_vrp_problem(r"C:\Users\darre\Desktop\Quantum Research\DBCW\D-Wave-VRP-master_Time\D-Wave-VRP-master\tests\CMT\CMT1.vrp")
solver = ClarkWright(problem)
#print("Solution1 : ", solution.solution)
solution2 = solver.solveWithoutTime()
#print("Solution2 : ", solution2.solution)
plot_all_solutions(graph, solution2.solution)
print("Solution : ", solution2.solution) 
print("Total cost : ", solution2.total_cost())
print("Weights : ", solution2.all_weights())
# print("Vehicles : ", len(problem.capacities))


# from dimod import BinaryQuadraticModel

# bqm = BinaryQuadraticModel('BINARY')

# pumps = [0,1,2,3]
# costs = [
#     [36, 27],
#     [54, 67],
#     [53, 12],
#     [90, 78]
# ]
# time = [0,1]
# demand = 20
# flow = [2, 7, 3, 8]

# x = [[f'P{p}_AM', f'P{p}_PM'] for p in pumps]



# #sum_p sum_t costpt (bias) * xpt (binary variable)

# #objective
# for p in pumps:
#     for t in time:
#         bqm.add_variable(x[p][t], costs[p][t]) #adds if doesnt exist


# #Every pump runs at lesast once per day
# for p in pumps:
#     c1 = [(x[p][t], 1) for t in time]
#     bqm.add_linear_inequality_constraint(c1, lb = 1, ub = len(time), lagrange_multiplier=5, label = 'c1_pump_'+str(p))

# # #At most 3 pumps per time slot
# # for t in time:
# #     c2 = [(x[p][t], 1) for p in pumps]
# #     bqm.add_linear_inequality_constraint(c2, constant = -3, lagrange_multiplier=5, label = 'c2_time_'+str(t))

# # #Satisfy daily demand
# # c3 = [(x[p][t], flow[p]) for t in time for p in pumps]
# # bqm.add_linear_equality_constraint(c3, constant = -demand, lagrange_multiplier=20)



# print(bqm)










