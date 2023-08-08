from analyzer_utils.common_def import *
from analyzer_utils.getsol     import *

solvers = ['Gurobi', 'OSQP', 'JOSQP']

qp_list_file_name = 'Procedures/qp_problem_list.txt'
file = open(qp_list_file_name, 'r')
lines = file.readlines()
for line in lines:
    sline = line.strip()
    # skip the comments
    if sline[0] == '*':
        continue
    # skip the lines that are not QPS files
    if sline[len(sline)-4:len(sline)] != '.qps':
        continue
    print(sline)
    for solver in solvers:
        try:
            sol = getsol(sline, solver)
            print(solver, '\t', sol)
        except:
            print("Error in reading the log file of the problem ", sline, " for the solver ", solver)
            print("The analysis aborted!")