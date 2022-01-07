import os

INPUT_FILE = "input.txt"
NOT = "-"
OUTPUT_FILE = "output.txt"
INPUT_PATH = "input/"

def getInput(filename):
    with open(filename, 'r') as input:
        alpha = input.readline().split()
        count = alpha.count('OR')
        listAlpha = []
        for _ in range(count):
            alpha.remove('OR')
        for L in alpha:
            if NOT in L:
                temp = [L]
                listAlpha.append(set(temp)) #this is stupid but it works, it wont turn -L into {'-', 'L'}
            else:
                listAlpha.append(set(L))

        nClauses = int(input.readline().rstrip('\n'))
        clauses = []
        for i in range(nClauses):
            clause = input.readline().split()
            count = clause.count('OR')
            for _ in range(count):
                clause.remove('OR')
            clauses.append(set(clause))
    input.close()
    return clauses, listAlpha

def writeOutput(filename, bigList, checkPL):
    with open(filename, 'w') as output:
        for smallList in bigList:
            output.write(str(len(smallList))  + '\n')
            for clause in smallList:
                sortedClause = sortSet2List(clause)
                output.write(convClause2Str(sortedClause))
        if checkPL:
            output.write('YES\n')
        else:
            output.write('0\n')
            output.write('NO\n')
    output.close()

def convClause2Str(clause):
    if not clause:
        return '{}\n'
    else:
        string = clause[0]
        for i in range(1,len(clause)):
            string = string + ' OR ' + clause[i]
        string = string + '\n'
        return string

def sortSet2List(clause):
    negetives = []
    clauseList = list(clause)
    for i,L in enumerate(clauseList):
        if NOT in L:
            negetives.append(L.lstrip(NOT))
            clauseList[i] = L.lstrip(NOT)
    clauseList.sort()
    for i,L in enumerate(clauseList):
        if L in negetives:
            clauseList[i] = NOT + L
    return clauseList
        
def makeNegative(clause):
    clause = list(clause)
    for i,L in enumerate(clause):
        if NOT in L:
            clause[i] = str(L).strip(NOT)
        else:
            clause[i] = NOT + str(L)
    return set(clause)

def PL_Resolve(ci, cj):
    clauses = []
    for l in ci:
        for m in cj:
            if (l == NOT + m) or (m == NOT + l): # if the clause have complimentery literals
                new_clauses = ci.union(cj)
                new_clauses.discard(l)
                new_clauses.discard(m)
                if not new_clauses:
                    clauses.append({})
                elif not any([(NOT + L) in new_clauses for L in new_clauses]): # if the clause doesnt have any more complimentery literals
                    clauses.append(new_clauses)
    return clauses

def PL_Resolution(KB, listAlpha):
    clauses = []
    clauses_pairs = []

    clauses = KB
    for alpha in listAlpha:
        clauses.append(makeNegative(alpha)) # KB ^ not alpha

    new = []
    loopList = []
    count = 0
    while True:
        n = len(clauses)
        for i in range(n):
            for j in range(i+1, n):
                clauses_pairs.append((clauses[i], clauses[j]))

        for (ci, cj) in clauses_pairs:
            resolvents = PL_Resolve(ci, cj)
            if (not all(x in new for x in resolvents) and not all(x in clauses for x in resolvents)) or {} in resolvents:
                new = new + resolvents

        if count < len(new):
            loopList.append(new[-(len(new) - count):]) #contain lists of all new clauses after one KB loop
            count = len(new)

        if {} in new:
            return True, loopList
        if all(x in clauses for x in new):
            return False, loopList
        clauses = clauses + loopList[-1] #only add true clauses

if __name__ == "__main__":
    for file_name in os.listdir(INPUT_PATH):
        input_file = INPUT_PATH + file_name
        KB, alpha = getInput(input_file)
        checkPL, bigList = PL_Resolution(KB, alpha)
        writeOutput(input_file.replace('in', 'out'), bigList, checkPL)
