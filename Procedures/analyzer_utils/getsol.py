from analyzer_utils.common_def import *

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