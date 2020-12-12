import sys
from copy import deepcopy
import time
import numpy as np
import itertools

fileName = ""
algo = 0
method = 0

# Parameters: None
# Returns: None
# Description: The main structure for the program because begins and ends the different methods to solve the problems

def main():
    listOfLists = fileOperations()
    if(algo == 1):
        matrix = formatMatrix(listOfLists)
        prepareKnapSack(matrix)
    elif(algo == 2):
        prepareSequence(listOfLists)
    else:
        print("Algorithm not recognized")

# Parameters: None
# Returns: A matrix containing all the values read from the file sent as an argument
# Description: Verifies the status of the program when is called, manages the arguments necessary for each problem and determinates 
#              if the -h argument was sent

def fileOperations():
    global fileName, method, algo
    lenArgv = len(sys.argv)
    
    try:
        if(lenArgv == 5):
            argu = getFirstArgu()
            if (argu == "-h"):
                showHelp()
                print("\n")
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
        elif(lenArgv == 2):
            showHelp()
            sys.exit()
        else:
            print("There is a problem with the arguments")
            sys.exit()
    except Exception:
        print("There is a problem with the arguments")
        sys.exit()

# Parameters: None
# Returns: A matrix containing all the values read from the file sent as an argument
# Description: Splits the content of the file sent as an argument based on the commas

def readFile():
    lines = open(fileName, 'r').readlines()
    lines = list(map(removeEndLine, lines))
    listOfLists = []
    for line in lines:
        splittedLine = line.split(",")
        listOfLists.append(splittedLine)
    return listOfLists

# Parameters: None
# Returns: unknown value
# Description: Gets the first element sent by argument to the program

def getFirstArgu():
    return sys.argv[1]

# Parameters: None
# Returns: None
# Description: Prints on console the information to execute the program including the arguments

def showHelp():
    print("Para este programa se pueden resolver 2 problemas de 2 formas, los problemas son:")
    print("     1. Mochila/Contenedores -> Se puede resolver con Fuerza bruta o programación dinámica.")
    print("     2. Alineamiento global de secuencias -> Se puede resolver con Fuerza bruta o programación dinámica.\n")
    print("El número de argumentos son de 3 obligatorios, uno opcional y son:")
    print("     python solver.py [-h] PROBLEMA ALGORITMO ARCHIVO\n")
    print("Los argumentos representan:")
    print("     [-h] Argumento opcional que muestra la guía básica del programa.")
    print("     PROBLEMA valor de 1 o 2, indicando el problema a resolver, 1 contenedor, 2 alineamiento.")
    print("     ALGORITMO valor de 1 o 2, indicando el algoritmo a usar, 1 fuerza bruta, 2 programación dinámica")
    print("     ARCHIVO indica el archivo de entrada donde el programa toma los parámetros del problema y procede a resolverlo con el algoritmo especificado.")


# Parameters: String
# Returns: String
# Description: Removes from a string the end line char

def removeEndLine(line):
    if(line.endswith("\n")):
        return line.replace("\n", "")
    return line

# Parameters: Matrix
# Returns: Matrix
# Description: Removes the signs from the matrix and converts all the values into ints/floats

def formatMatrix(matrix):
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            matrix[row][column] = num(matrix[row][column])
            
    return matrix


# Parameters: s - string that may be an float or int
# Returns: int or float
# Description: converts a string into float or int

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


# Parameters: Matrix
# Returns: None
# Description: Determinates the method to be used (BT, DP) for the Sequence algorithm, runs the functions and displays the results

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


# Parameters: list, list, int, int, list
# Returns: int
# Description: By backtracking resolves the KnapSack problem and returns the best value in the sack

def knapSackBT(val, wt, n, W, items):
    if (W < 0):
        return (-sys.maxsize - 1)

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

# Parameters: int, list, list, int
# Returns: matrix
# Description: By dynamic programming resolves the KnapSack problem and returns the matrix generated

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

# Parameters: matrix, list
# Returns: None
# Description: Displays on console the elements discovered by the BT and DP algorithm of KnapSack

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

# Parameters: list, list, int, int
# Returns: list
# Description: Given the parameters discovers the elements used to get the best result in the KnapSack problem resolved with DP

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

# Parameters: Matrix
# Returns: None
# Description: Determinates the method to be used (BT, DP) for the Sequence algorithm, runs the functions and displays the results

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

        print("Hilera 1: " + str(result[1]))

        print("Hilera 2: " + str(result[2]))

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

        print("Final score: " + str(result[h2Len][h1Len][0]))

        values = determinateSequence(result, h1, h2, h1Len, h2Len)

        print("Hilera 1: " + str(values[0]))

        print("Hilera 2: " + str(values[1]))

        print("Time execution: " + str(end_time))
    else:
        print("Method not recognized")


# Parameters: String, String, int, int, int
# Returns: List
# Description: By backtracking resolves the sequence alignment problem and returns the best finding

def sequenceBT(h1, h2, match, mismatch, gapPenalty):
    h1Len = len(h1)
    h2Len = len(h2)
    k = 0

    if (h1Len >= h2Len):
        k = h1Len * 2
    else:
        k = h2Len * 2

    h1Elements = generateStrings(k, h1)

    h2Elements = generateStrings(k, h2)

    current = [-999,"",""]

    differenceH1 = k - h1Len
    differenceH2 = k - h2Len

    finalDifferenceH1, finalDifferenceH2 = 0, 0

    orderHK = h1Elements
    orderHN = h1Elements

    if (h1Len > h2Len):
        orderHN = h2Elements
        finalDifferenceH2 = differenceH2 - differenceH1

    elif (h1Len < h2Len):
        orderHN = h1Elements
        orderHK = h2Elements
        finalDifferenceH1 = differenceH1 - differenceH2

    for i in range(len(orderHK)):
        currentLen = len(orderHK[i])
        for j in range(currentLen):
            currentLen2 = len(orderHN[i])
            for k in range(currentLen2):
                score = goodnessScore(h1Elements[i + finalDifferenceH1][j], h2Elements[i + finalDifferenceH2][k], match, mismatch, gapPenalty)
                if (current[0] < score):
                    current = [score, h1Elements[i + finalDifferenceH1][j], h2Elements[i + finalDifferenceH2][k]]

    return current

# Parameters: int, string (sequence)
# Returns: Matrix
# Description: Generates N quantity of cases where a GAP can be placed into a string

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

# Parameters: String, String, int, int, int
# Returns: int
# Description: Gives a score between two sequences

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

# Parameters: String, String, int, int, int
# Returns: List
# Description: By dynamic programming resolves the sequence alignment problem and returns the best finding

def sequenceDP(h1, h2, match, mismatch, gapPenalty):
    h1Len = len(h1)
    h2Len = len(h2)
    matrix = [[0 for x in range(h1Len + 1)] for y in range(h2Len + 1)]

    for i in range(h2Len + 1):
        matrix[i][0] = (-2 * i,  [0, 1, 0]) 
    
    for j in range(h1Len + 1):
        matrix[0][j] = (-2 * j,  [0, 0, 1])

    matrix[0][0][1][2] = 0

    for i in range(1, h1Len + 1):
        for j in range (1, h2Len + 1):
            noGap = matrix[j - 1][i - 1][0] + isMatchByIndex(h1, h2, i, j)
            gapH1 = matrix[j - 1][i][0] + gapPenalty
            gapH2 = matrix[j][i - 1][0] + gapPenalty

            values = [noGap, gapH1, gapH2]

            maxValue = max(noGap, max(gapH1, gapH2))

            for ele in range(3):
                if (values[ele] != maxValue):
                    values[ele] = 0
                else:
                    values[ele] = 1
            
            matrix[j][i] = (maxValue, values)

    return matrix

# Parameters: String, String, int, int
# Returns: int
# Description: Determinates if given two indexes there is a match between two chars inside the strings

def isMatchByIndex(h1, h2, i, j):
    if (h1[i - 1] == h2[j - 1]):
        return 1 # aqui deberia el match value
    return -1

# Parameters: matrix, string (sequence), string (sequence), int, int
# Returns: list
# Description: Given a Needleman–Wunsch matrix determinates the strings of the first and second sequence

def determinateSequence(matrix, h1, h2, h1Len, h2Len):
    h1List = []
    h2List = []

    condition =  True

    i, j = h2Len, h1Len
    
    currentI, currentJ = h1Len, h2Len

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

main()