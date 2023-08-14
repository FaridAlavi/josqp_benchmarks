from analyzer_utils.common_def import *
import os.path

def getsol(problemName, solver):
    result = {}
    problemNameS = problemName.strip()
    if solver == "Gurobi":
        filePath = 'Solvers_Logs/Gurobi/QP/' + 'grb_' + problemNameS[0:len(problemNameS)-4] + '.log'
        if not os.path.isfile(filePath):
            result['log file status'] = File_Status.NOT_FOUND
            return result
        else:
            result['log file status'] = File_Status.FOUND
        logFile = open(filePath, 'r')
        logFileLines = logFile.readlines()
        for line in logFileLines:
            if "Optimal objective" in line:
                tokens = line.split('Optimal objective ')
                optObj = float(tokens[1].strip())
                result["solution status"] = Sol_Status.SOLVED
                result["optimal value"]   = optObj
            elif 'Sub-optimal termination - objective' in line:
                tokens = line.split('Sub-optimal termination - objective')
                optObj = float(tokens[1].strip())
                result["solution status"] = Sol_Status.SUBOPTIMAL
                result["optimal value"]   = optObj
                if 'seconds' in prevLine:
                    tokens = prevLine.split(' ')
                    i = tokens.index('seconds') - 1
                    runTime = float(tokens[i])
                    result['run time'] = runTime
            elif 'I ' in line:
                tokens = line.split(' ')
                optObj = float(tokens[1].strip())
                result['solution status'] = Sol_Status.SUBOPTIMAL
                result['optimal value']   = optObj
                if 'seconds' in prevLine:
                    tokens = prevLine.split(' ')
                    i = tokens.index('seconds') - 1
                    runTime = float(tokens[i])
                    result['run time'] = runTime
            elif 'solved model in' in line:
                tokens = line.split(' ')
                i = tokens.index('seconds') - 1
                runTime = float(tokens[i])
                result["run time"] = runTime
            elif 'Numerical trouble encountered' in line:
                result['solution status'] = Sol_Status.NOT_SOLVED
            elif 'Sub-optimal termination' in line:
                result['solution status'] = Sol_Status.SUBOPTIMAL
            prevLine = line
        if len(result) == 0:
            print("Error in parsing the log file ", problemNameS)
    elif solver == "OSQP":
        filePath = 'Solvers_Logs/OSQP/QP/' + 'osqp_' + problemNameS[0:len(problemNameS)-4] + '.log'
        if not os.path.isfile(filePath):
            result['log file status'] = File_Status.NOT_FOUND
            return result
        else:
            result['log file status'] = File_Status.FOUND
        logFile = open(filePath, 'r')
        logFileLines = logFile.readlines()
        for line in logFileLines:
            if line.find('status:') == 0:
                tokens = line.split(' ')
                if tokens[len(tokens)-1].strip() == 'solved':
                    result['solution status'] = Sol_Status.SOLVED
                elif tokens[len(tokens)-1].strip() == 'infeasible':
                    result['solution status'] = Sol_Status.INFEASIBLE
                elif tokens[len(tokens)-1].strip() == 'inaccurate':
                    result['solution status'] = Sol_Status.SUBOPTIMAL
            elif line.find('optimal objective:') == 0:
                tokens = line.split(' ')
                result['optimal value'] = float(tokens[len(tokens)-1].strip())
            elif line.find('run time:') == 0:
                tokens = line.split(' ')
                timeStr = tokens[len(tokens)-1].strip()
                timeStr = timeStr[0:len(timeStr)-1]
                result['run time'] = float(timeStr.strip())
    elif solver == "JOSQP":
        filePath = 'Solvers_Logs/JOSQP/QP/' + 'josqp_' + problemNameS[0:len(problemNameS)-4] + '.log'
        if not os.path.isfile(filePath):
            result['log file status'] = File_Status.NOT_FOUND
            return result
        else:
            result['log file status'] = File_Status.FOUND
        logFile = open(filePath, 'r')
        logFileLines = logFile.readlines()
        for line in logFileLines:
            if line.find('Status:') != -1:
                tokens = line.split()
                status = tokens[len(tokens)-1].strip()
                if status == 'SOLVED':
                    result['solution status'] = Sol_Status.SOLVED
            elif line.find('Optimal obj:') != -1:
                tokens = line.split()
                objStr = tokens[len(tokens)-1].strip()
                result['optimal value'] = float(objStr)
            elif line.find('Run time (s):') != -1:
                tokens = line.split()
                timeStr = tokens[len(tokens)-1].strip()
                result['run time'] = float(timeStr)
    return result
