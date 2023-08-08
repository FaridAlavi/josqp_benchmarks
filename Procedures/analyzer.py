from enum import Enum

class Sol_Status(Enum):
    SOLVED     = 1
    INFEASIBLE = 2
    NOT_SOLVED = 3
    SUBOPTIMAL = 4

def getsol(problemName, solver):
    result = {} #{"solution status": "uninitialized", "optimal value": 0.0, "run time": 0.0}
    if solver == "Gurobi":
        problemNameS = problemName.strip()
        filePath = 'Solvers_Logs/Gurobi/QP/' + 'grb_' + problemNameS[0:len(problemNameS)-4] + '.log'
        logFile = open(filePath, 'r')
        logFileLines = logFile.readlines()
        for line in logFileLines:
            if "Optimal objective" in line:
                tokens = line.split('Optimal objective ')
                optObj = float(tokens[1].strip())
                result["solution status"] = Sol_Status.SOLVED
                result["optimal value"]   = optObj
            elif 'solved model in' in line:
                tokens = line.split(' ')
                i = tokens.index('seconds') - 1
                runTime = float(tokens[i])
                result["run time"] = runTime
            elif 'Numerical trouble encountered' in line:
                result['solution status'] = Sol_Status.NOT_SOLVED
            elif 'Sub-optimal termination' in line:
                result['solution status'] = Sol_Status.SUBOPTIMAL
        if len(result) == 0:
            print("Error in parsing the log file ", problemNameS)
    return result

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
    for solver in solvers:
        try:
            sol = getsol(sline, solver)
            print(sol)
        except:
            print("Error in reading the log file of the problem ", sline, " for the solver ", solver)
            print("The analysis aborted!")