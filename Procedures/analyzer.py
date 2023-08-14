from analyzer_utils.common_def   import *
from analyzer_utils.getsol       import *
from analyzer_utils.createReport import *

solvers = ['Gurobi', 'OSQP', 'JOSQP']

qp_list_file_name = 'Procedures/qp_problem_list.txt'
file = open(qp_list_file_name, 'r')
lines = file.readlines()
file.close()
solCollectionDict = {}
probCnt = 0
for line in lines:
    sline = line.strip()
    # skip the comments
    if sline[0] == '*':
        continue
    # skip the lines that are not QPS files
    if sline[len(sline)-4:len(sline)] != '.qps':
        continue
    # at this point, we are sure that the line represents a valid QP problem
    probCnt += 1
    problemName = sline[0:len(sline)-4]
    #print("Processing results of ", problemName)
    solDict= {}
    for solver in solvers:
        try:
            sol = getsol(sline, solver)
            solDict[solver] = sol
        except:
            print("Error in reading the log file of the problem ", sline, " for the solver ", solver)
            print("The analysis aborted!")
    solCollectionDict[problemName] = solDict
print('Finished processing {} test cases.'.format(probCnt))

# Writing the report
createReport(solCollectionDict)
