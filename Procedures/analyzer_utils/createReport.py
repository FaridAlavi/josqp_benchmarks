def createReport(solCollectionDict):
    report  = '\t|\t\t|               Optimal objecive                |               Run time\t\n'
    report += 'Check\t|Test\t\t|-----------------------------------------------|------------------------------------\n'
    report += '\t|\t\t|Gurobi\t\tOSQP\t\tJOSQP\t\t|Gurobi\t\tOSQP\t\tJOSQP\n'
    report += '-----\t----\t\t------         ----            -----            ------         ----            -----\n'
    for probName, solDict in solCollectionDict.items():
        attentionReq = False
        line = '\t|{}\t|'.format(probName)
        objKeyName = 'optimal value'
        runTimeKeyName = 'run time'
        if 'Gurobi' in solDict.keys():
            sol = solDict['Gurobi']
            if objKeyName in sol.keys():
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
        if attentionReq:
            attention = '*\t'
        else:
            attention = '\t'
        # Adjusting the length of strings
        probName     = adjLen(probName)
        grbObj       = adjLen(grbObj)
        osqpObj      = adjLen(osqpObj)
        josqpObj     = adjLen(josqpObj)
        grbRunTime   = adjLen(grbRunTime)
        osqpRunTime  = adjLen(osqpRunTime)
        josqpRunTime = adjLen(josqpRunTime)
        line = '{}|{}|{}{}{}{}{}{}\n'.format(attention, probName, grbObj, osqpObj, josqpObj, grbRunTime, osqpRunTime, josqpRunTime)
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