import numpy as np

def createReport(solCollectionDict):
    report  = '\t|\t\t|               Optimal objecive                |               Run time\t\n'
    report += 'Check\t|Test\t\t|-----------------------------------------------|------------------------------------\n'
    report += '\t|\t\t|Gurobi\t\tOSQP\t\tJOSQP\t\t|Gurobi\t\tOSQP\t\tJOSQP\n'
    report += '-----\t----\t\t------         ----            -----            ------         ----            -----\n'
    runTimes = {'Gruobi': [], 'OSQP': [], 'JOSQP': []}
    for probName, solDict in solCollectionDict.items():
        attentionReq = False
        line = '\t|{}\t|'.format(probName)
        objKeyName = 'optimal value'
        runTimeKeyName = 'run time'
        if 'Gurobi' in solDict.keys():
            sol = solDict['Gurobi']
            if objKeyName in sol.keys():
                grbObjAux = sol[objKeyName]
                grbObj = '{:.3e}'.format(sol[objKeyName])
            else:
                grbObj = '-'
                attentionReq = True
            if runTimeKeyName in sol.keys():
                grbRunTime = '{:.2f}'.format(sol[runTimeKeyName])
            else:
                grbRunTime = '-'
                attentionReq = True
        else:
            grbObj = '-'
            grbRunTime = '-'
            attentionReq = True
        if 'OSQP' in solDict.keys():
            sol = solDict['OSQP']
            if objKeyName in sol.keys():
                osqpObjAux = sol[objKeyName]
                osqpObj = '{:.3e}'.format(sol[objKeyName])
            else:
                osqpObj = '-'
                attentionReq = True
            if runTimeKeyName in sol.keys():
                osqpRunTime = '{:.2f}'.format(sol[runTimeKeyName])
            else:
                osqpRunTime = '-'
                attentionReq = True
        else:
            osqpObj = '-'
            osqpRunTime = '-'
            attentionReq = True
        if 'JOSQP' in solDict.keys():
            sol = solDict['JOSQP']
            if objKeyName in sol.keys():
                josqpObjAux = sol[objKeyName]
                josqpObj = '{:.3e}'.format(sol[objKeyName])
            else:
                josqpObj = '-'
                attentionReq = True
            if runTimeKeyName in sol.keys():
                josqpRunTime = '{:.2f}'.format(sol[runTimeKeyName])
            else:
                josqpRunTime = '-'
                attentionReq = True
        else:
            josqpObj = '-'
            josqpRunTime = '-'
            attentionReq = True
        # If the optimal points found by the solvers do not match, raise attentionReq flag.
        if not attentionReq:
            relTol = 1e-1
            if not grbObjAux == 0.0:
                if abs((osqpObjAux - grbObjAux) / grbObjAux) > relTol or abs((josqpObjAux - grbObjAux) / grbObjAux) > relTol:
                    attentionReq = True
            else:
                if abs(osqpObjAux - grbObjAux) > relTol or abs(josqpObjAux - grbObjAux) > relTol:
                    attentionReq = True
        if attentionReq:
            attention = '*\t'
        else:
            attention = ' \t'
        # Adjusting the length of strings
        probName     = adjLen(probName)
        grbObj       = adjLen(grbObj)
        osqpObj      = adjLen(osqpObj)
        josqpObj     = adjLen(josqpObj)
        grbRunTime   = adjLen(grbRunTime)
        osqpRunTime  = adjLen(osqpRunTime)
        josqpRunTime = adjLen(josqpRunTime)
        line = '{}|{}|{}{}{}{}{}{}\n'.format(attention, probName, grbObj, osqpObj, josqpObj, grbRunTime, osqpRunTime, josqpRunTime)
        # updating the run times
        if not attentionReq:
            runTimes['Gruobi'].append(float(grbRunTime))
            runTimes['OSQP'].append(float(osqpRunTime))
            runTimes['JOSQP'].append(float(josqpRunTime))
        report += line

    sh = 10
    nValidRslts = len(runTimes['Gruobi'])
    if nValidRslts > 0:
        grbRunTimeShifted    = np.add(runTimes['Gruobi'], sh)
        grbRunTimeGeoMean    = pow(np.prod(grbRunTimeShifted),   1.0 / nValidRslts) - sh
        grbRunTimeArthMean   = np.sum(runTimes['Gruobi']) / nValidRslts
        osqpRunTimeShifted   = np.add(runTimes['OSQP'],   sh)
        osqpRunTimeGeoMean   = pow(np.prod(osqpRunTimeShifted),  1.0 / nValidRslts) - sh
        osqpRunTimeArthMean  = np.sum(runTimes['OSQP']) / nValidRslts
        josqpRunTimeShifted  = np.add(runTimes['JOSQP'],  sh)
        josqpRunTimeGeoMean  = pow(np.prod(josqpRunTimeShifted), 1.0 / nValidRslts) - sh
        josqpRunTimeArthMean = np.sum(runTimes['JOSQP']) / nValidRslts
        
        minGeoMean = min(grbRunTimeGeoMean, min(osqpRunTimeGeoMean, josqpRunTimeGeoMean))
        grbRunTimeShiftedGeoMean   = grbRunTimeGeoMean   / minGeoMean
        osqpRunTimeShiftedGeoMean  = osqpRunTimeGeoMean  / minGeoMean
        josqpRunTimeShiftedGeoMean = josqpRunTimeGeoMean / minGeoMean

        fullDashLine = '-------------------------------------------------------------------------------------------------------------\n'
        report += fullDashLine
        line = '\t\t\t\t\t\tArithmetic mean\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\n'.format(grbRunTimeArthMean, osqpRunTimeArthMean, josqpRunTimeArthMean)
        report += line
        line = '\t\t\t\t\t Shifted geometric mean\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\n'.format(grbRunTimeShiftedGeoMean, osqpRunTimeShiftedGeoMean, josqpRunTimeShiftedGeoMean)
        report += line

    reportFile = open('Results/report.txt', 'w')
    reportFile.writelines(report)
    reportFile.close()

def adjLen(str):
    if len(str) >= 7:
        str += '\t'
    else:
        str += '\t\t'
    return str