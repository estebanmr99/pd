import sys
from copy import deepcopy
import time
import numpy as np
import itertools

fileName = ""
algo = 0
method = 0

def main():
    listOfLists = fileOperations()
    if(algo == 1):
        matrix = formatMatrix(listOfLists)
        prepareKnapSack(matrix)
    elif(algo == 2):
        prepareSequence(listOfLists)
    else:
        print("Algorithm not recognized")

def prepareSequence(listOfLists):
    global method
    match = num(listOfLists[0][0])
    mismatch = num(listOfLists[0][1])
    gapPenalty = num(listOfLists[0][2])
    h1 = listOfLists[1][0]
    h2 = listOfLists[2][0]
    h1Len = len(h1)
    h2Len = len(h2)

    if (method == 1):
        #Backtracking case
        print("Sequence alignment with backtracking")

        start_time = time.time()
        result = sequenceBT(h1, h2, match, mismatch , gapPenalty)
        
        print("Final score: " + str(result[0]))

        print("Hilera1: " + str(result[1]))

        print("Hilera2: " + str(result[2]))

        end_time =  time.time() - start_time
        print("Time execution: " + str(end_time))
    elif(method == 2):
        #DP case
        print("Sequence alignment with dynamic programing")

        start_time = time.time()
        result = sequenceDP(h1, h2, match, mismatch , gapPenalty)
        end_time =  time.time() - start_time

        for row in result:
            print(' '.join(map(str,row)))

        print("Final score: " + str(result[h1Len][h2Len][0]))

        values = determinateSequence(result, h1, h2, h1Len, h2Len)

        print("Hilera1: " + str(values[0]))

        print("Hilera2: " + str(values[1]))

        print("Time execution: " + str(end_time))
    else:
        print("Method not recognized")


def sequenceBT(h1, h2, match, mismatch, gapPenalty):
    h1Len = len(h1)
    h2Len = len(h2)
    k = 0

    if (h1Len >= h2Len):
        k = h1Len * 2
    else:
        k = h2Len * 2

    test1 = generateStrings(k, h1)

    test2 = generateStrings(k, h2)

    current = [-999,"",""]

    for i in range(len(test1)):
        currentLen = len(test1[i])
        for j in range(currentLen):
            currentLen2 = len(test1[i])
            for k in range(currentLen2):
                score = goodnessScore(test1[i][j], test2[i][k], match, mismatch, gapPenalty)
                if (current[0] < score):
                    current = [score, test1[i][j], test2[i][k]]


    return current

def goodnessScore(h1, h2, match, mismatch, gapPenalty):
    score = 0
    GAP = "_"
    for i in range(len(h1)):
        if (h1[i] == h2[i] and (h1 != GAP and h2[i] != GAP)):
            score += match
        elif (h1[i] == GAP or h2[i] == GAP):
            score += gapPenalty
        else:
            score += mismatch

    return score


def generateStrings(k, string):

    cases = [[string]]
    
    stringRange =  k - len(string)

    for i in range(stringRange):
        current = []
        someLen = len(cases[i])
        for j in range(someLen):
            currentLen = len(cases[i][j])
            for k in range((currentLen + 1)):
                modifiedString = cases[i][j][:k] + "_" + cases[i][j][k:]
                if (len(current) == 0):
                    current.append(modifiedString)
                elif(len(current) != 0 and current[-1] != modifiedString):
                    current.append(modifiedString)

        cases.append(current)
    
    return cases

def insertChar(mystring, position, chartoinsert ):
    mystring   =  mystring[:position] + chartoinsert + mystring[position:] 
    return mystring  

def determinateSequence(matrix, h1, h2, h1Len, h2Len):
    h1List = []
    h2List = []

    condition =  True

    i, j, currentI, currentJ = h1Len, h2Len, h1Len, h2Len

    count = 0

    while(condition):
        if(matrix[i][j][1][0] == 1):
            h1List.insert(0, h1[currentI - 1])
            h2List.insert(0, h2[currentJ - 1])
            currentI -= 1
            currentJ -= 1
            i -= 1
            j -= 1
        elif (matrix[i][j][1][1] == 1):
            h1List.insert(0, "_")
            h2List.insert(0, h2[currentJ - 1])
            currentJ -= 1
            i -= 1
        elif (matrix[i][j][1][2] == 1):
            h1List.insert(0, h1[currentI - 1])
            h2List.insert(0, "_")
            currentI -= 1
            j -= 1
        else:
            print("There is an error with the directions")
            sys.exit()
        
        if(i == 0 and j == 0):
            condition = False
        count += 1

    return [''.join(h1List), ''.join(h2List)]


def sequenceDP(h1, h2, match, mismatch, gapPenalty):
    h1Len = len(h1)
    h2Len = len(h2)
    maxAlign = [[0 for x in range(h1Len + 1)] for y in range(h2Len + 1)]

    for q in range(h1Len + 1):
        maxAlign[q][0] = (-2 * q,  [0, 1, 0]) 
    
    for r in range(h2Len + 1):
        maxAlign[0][r] = (-2 * r,  [0, 0, 1])

    maxAlign[0][0][1][2] = 0

    for i in range(1, h1Len + 1):
        for j in range (1, h2Len + 1):
            leaveIt = maxAlign[j - 1][i - 1][0] + f(h1, h2, i, j, match, mismatch)
            addGapH1 = maxAlign[j - 1][i][0] + gapPenalty
            addGapH2 = maxAlign[j][i - 1][0] + gapPenalty

            values = [leaveIt, addGapH1, addGapH2]

            maxValue = max(leaveIt, max(addGapH1, addGapH2))

            for ele in range(3):
                if (values[ele] != maxValue):
                    values[ele] = 0
                else:
                    values[ele] = 1
            
            maxAlign[j][i] = (maxValue, values)

    return maxAlign


def f(h1, h2, i, j, match, mismatch):
    if (h1[i - 1] == h2[j - 1]):
        return 1 # aqui deberia el match value
    return -1
        
def prepareKnapSack(matrix):
    global method
    val = [matrix[i][1] for i in range(1, len(matrix)) for x in range(matrix[i][2])]
    wt = [matrix[i][0] for i in range(1, len(matrix)) for x in range(matrix[i][2])]
    W = matrix[0][0]
    n = len(val)
    
    elemts = []

    if (method == 1):
        #Backtracking case
        print("KnapSack with backtracking")

        start_time = time.time()
        result = knapSackBT(val, wt, n - 1, W, elemts) 
        end_time =  time.time() - start_time

        print(result)

        printElements(matrix, elemts)

        print("Time execution: " + str(end_time))
    elif(method == 2):
        #DP case
        print("KnapSack with dynamic programing")

        start_time = time.time()
        V = knapSackDP(W, wt, val, n)
        end_time =  time.time() - start_time

        print(V[n][W])

        elemts = findElements(V, W, n, wt)

        printElements(matrix, elemts)

        print("Time execution: " + str(end_time))
    else:
        print("Method not recognized")


def printElements(matrix, elemts):
    groupElements = [ (i, matrix[i][2]) for i in range(1, len(matrix))]

    presentElements = [0] * len(groupElements)
    for i in range(len(elemts)):
        current = elemts[i]
        for j in range(len(groupElements)):
            current -= groupElements[j][1]
            if(current <= 0):
                presentElements[groupElements[j][0] - 1] += 1
                break

    for i in range(len(presentElements)):
        if(presentElements[i] == 0):
            continue
        print(str(i + 1) + ", " + str(presentElements[i]))


def knapSackBT(val, wt, n, W, items):
    if (W < 0):
        return -sys.maxsize - 1

    if (n < 0 or W == 0):
        return 0
    
    originalItems = deepcopy(items)

    items.append(n + 1)
    include = val[n] + knapSackBT(val, wt, n - 1, W - wt[n], items)

    exclude = knapSackBT(val, wt, n - 1, W, originalItems)

    if (include > exclude):
        return include
    else:
        items.clear()
        items.extend(originalItems)
        return exclude


def findElements(V, W, n, wt):
    k = W
    elemts = []
    for i in range(n, 0, -1):
        if (V[i][k] != V[i - 1][k]):
            elemts.append(i)
            i -= 1
            k -= wt[i]
        else:
            i -= 1
    return elemts


def fileOperations():
    global fileName, method, algo
    lenArgv = len(sys.argv)
    
    try:
        if(lenArgv == 5):
            argu = getFirstArgu()
            if (argu == "-h"):
                showHelp()
                algo = int(sys.argv[2])
                method = int(sys.argv[3])
                fileName = sys.argv[4]
                return readFile()
            else:
                print("There is a problem with the arguments")
                sys.exit()

        elif(lenArgv == 4):
            algo = int(getFirstArgu())
            method = int(sys.argv[2])
            fileName = sys.argv[3]
            return readFile()
        else:
            sys.exit()
    except:
        print("There is a problem with the arguments")
        sys.exit()


def readFile():
    lines = open(fileName, 'r').readlines()
    lines = list(map(removeEndLine, lines))
    listOfLists = []
    for line in lines:
        splittedLine = line.split(",")
        listOfLists.append(splittedLine)
    return listOfLists

def getFirstArgu():
    return sys.argv[1]

def showHelp():
    print("Hello")

def removeEndLine(line):
    if(line.endswith("\n")):
        return line.replace("\n", "")
    return line

def formatMatrix(matrix):
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            matrix[row][column] = num(matrix[row][column])
            
    return matrix

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def knapSackDP(W, wt, val, n): 
    V = []

    for i in range(n + 1):
        V.append([0] * (W + 1))

    for i in range(1, n + 1): 
        for w in range(W + 1): 
            if (wt[i - 1] > w):
                V[i][w] = V[i - 1][w]
            elif (val[i - 1] + V[i - 1][w - wt[i - 1]] > V[i - 1][w]):
                V[i][w] = val[i - 1] + V[i - 1][w - wt[i - 1]]
            else: 
                V[i][w] = V[i - 1][w]
  
    return V

main()