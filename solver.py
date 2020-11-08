import sys
from copy import deepcopy

def main():
    listOfLists = fileOperations()
    createOutputFile()

def fileOperations():
    lines = open(getFileName(), 'r').readlines()
    lines = list(map(removeEndLine, lines))
    listOfLists = []
    for line in lines:
        splittedLine = line.split(",")
        listOfLists.append(splittedLine)
    return listOfLists

def getFileName():
    return sys.argv[1]

def removeEndLine(line):
    if(line.endswith("\n")):
        return line.replace("\n", "")
    return line

def createOutputFile():
    fileName = getFileName()
    global outputFileName
    outputFileName = fileName.replace(".txt", "_solution.txt")
    open(outputFileName, 'w+')

main()