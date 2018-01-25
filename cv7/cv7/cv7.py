import random
from numpy.core.defchararray import lower
import numpy
import sys
import string
import re

filename = input("Enter matrix filename (for determinant and inverse): ")
rowsize = input("Enter row size (for determinant and inverse): ")

try:
	matrix = numpy.matrix(numpy.loadtxt(filename, dtype=int, usecols=range(int(rowsize))))
except:
    print("Matrix load failed.")
    sys.exit()

print("Matrix:\n%s\n" % matrix)
print("\nDeterminant: %s\n" %str(numpy.linalg.det(matrix)))
try:
	print("\nInverse: \n%s\n" % numpy.linalg.inv(matrix))
except np.linalg.LinAlgError:
	print("Unable to compute inverse matrix.")

filename = input("Enter matrix filename (for equations): ")
rowsize = input("Enter row size (for equations): ")

try:
    sols = numpy.matrix(numpy.loadtxt(filename, dtype=int, usecols=int(rowsize) - 1))
    solutions = numpy.array(sols.T)
    coefficients = numpy.matrix(numpy.loadtxt(filename, dtype=int, usecols=range(int(rowsize) -1)))
except:
    print("Matrix load failed.")
    sys.exit()
print("Loaded coefficients:\n%s\n" % coefficients)
print("Loaded results:\n%s\n" % solutions)
try:
    print("Solution is: \n%s\n" % numpy.linalg.solve(coefficients, solutions))
except:
    print("Unable to find solution.")
    sys.exit()

allLines = []
keys = []
filename = input("Enter filename (for nice equations): ")
with open(filename, "r") as f:  

    line = f.readline()
    while line:
        line = line.replace(" ", "")
        line = line.replace("\n", "")
        line = line.lower()
        if(line.startswith('-') == False):
            line = '+' + line
        singleLine = {}
        regex = re.compile(r"([+-]{1}\d+\w|=\d+)", re.IGNORECASE)
        for match in regex.finditer(line):  
            if(match.group(1).startswith('+')) or (match.group(1).startswith('-')):
                letter = re.search(r'[a-z]', match.group(1)).group()
                number = int(re.search(r'[+-]{1}\d+', match.group(1)).group())
            if(match.group(1).startswith('=')):
                letter = '='
                number = int(re.search(r'([+-])?\d+', match.group(1)).group())
            if(letter in singleLine):
                singleLine[letter] += number
            else:
                singleLine[letter] = number
            if((letter in keys) == False):
                keys.append(letter)
        allLines.append(singleLine)
        line = f.readline()

#convert into arrays
allArrs = []
keyValues = []
for dct in allLines:
    singleArr = []
    for key in keys:
        if key == '=':
            keyValues.append(dct[key])
        else:
            if key in dct:
                singleArr.append(dct[key])
            else:
                singleArr.append(0)
    allArrs.append(singleArr)

#pretty print
for i in range(len(allArrs)):
    for j in range(len(allArrs[i])):
        if allArrs[i][j] > 0:
            print('+ %d %s ' % (allArrs[i][j], keys[j]), end='')
        else:
            print('- %d %s ' % (abs(allArrs[i][j]), keys[j]), end='')
    if keyValues[i] > 0:
        print('= %d' % (keyValues[i]))
    else:
        print('= - %d' % (keyValues[i]))

matrix = numpy.matrix(allArrs)
try:
    res = numpy.linalg.solve(matrix, keyValues)
    res = res.tolist()
    print("solution: ", end="")
    for i in range(len(res)):
        print("(%s = %d)" % (keys[i], res[i]), end="")
        if(i != len(res)):
            print(", ", end="")
        else:
            print("")
except:
    print("Unable to find solution.")
    sys.exit()

