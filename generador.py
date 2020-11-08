import sys
from copy import deepcopy
import random

knapsack = "mochila"
nw = "secuencia"
outputFileName = ""

def main():
    fileOperations()

def fileOperations():
    algo = determinateAlgo()

    if (algo == knapsack):
        createOutputFile(knapsack)
        createKnapsackExp(getArguments(10))
    elif(algo == nw):
        createOutputFile(nw)
        createNWExp(getArguments(4))
    else:
        print("ID-PROBLEMA not recognized")
        sys.exit()
    
def determinateAlgo():
    return sys.argv[1]

def getArguments(argvRange):
    arguments = []
    for i in range (2,argvRange):
        try:
            arguments.append(int(sys.argv[i]))
        except:
            print("There is a problem with the arguments")

    return arguments

def createOutputFile(fileName):
    global outputFileName
    outputFileName = fileName + "_experiment.txt"
    open(outputFileName, 'w+')


def createKnapsackExp(argv):
    writeInOuputFile(str(argv[0]))

    n =  argv[1]
    minPeso = argv[2]
    maxPeso = argv[3]
    minBeneficio = argv[4]
    maxBeneficio = argv[5]
    minCantidad = argv[6]
    maxCantidad = argv[7]

    for i in range(n):
        line = str(random.randrange(minPeso,maxPeso)) + "," + str(random.randrange(minBeneficio, maxBeneficio)) + "," + str(random.randrange(minCantidad, maxCantidad))
        writeInOuputFile(line)


def createNWExp(argv):
    letters = "ATCG"
    largoH1 = argv[0]
    largoH2 = argv[1]

    match = "1"
    mismatch = "-1"
    gap = "-2"

    seque1 = ""
    seque2 = ""

    for i in range(largoH1):
        seque1 += random.choice(letters)

    for i in range(largoH2):
        seque2 += random.choice(letters)

    writeInOuputFile(match + "," + mismatch + "," + gap)
    writeInOuputFile(seque1)
    writeInOuputFile(seque2)

    return

def writeInOuputFile(text):
    file = open(outputFileName, "a")
    file.write(text + '\n')
    file.close
    print(text)

main()