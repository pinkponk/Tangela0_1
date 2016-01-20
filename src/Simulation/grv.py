'''
Created on 15 jan. 2016

@author: Henrik
'''

import numpy
import math
import copy
import time
import random
from scipy.special import erfinv



file = open("Animal-words.txt")
names = file.readlines()
file.close()
print(names.__len__())
choice = random.choice(names)
names.remove(choice)
print(choice.rstrip()+str(2))
print("n")

def thetaNormal(x):
    return math.exp(-0.5*math.pow(x,2))/(math.sqrt(2*math.pi))

def meanFoldedDist(nrOfEle,procentage):
    sigmaNorm = nrOfEle/(erfinv(procentage)*math.sqrt(2))
    muNorm = 0
    muFolded = muNorm*math.sqrt(2/math.pi)*math.exp(-math.pow(muNorm,2)/(2*math.pow(sigmaNorm,2)))-sigmaNorm*math.erf(-muNorm/(math.sqrt(2*math.pow(sigmaNorm,2))))
    return muFolded

def halfNormMean(nrOfEle,procentage):
    sigmaNorm = nrOfEle/(erfinv(procentage)*math.sqrt(2))
    muNorm = 0
    muFolded = sigmaNorm*math.sqrt(2)/math.sqrt(math.pi)
    return muFolded



length = 1000
lista = [1]*length
procentag = 0.8
muFolded= halfNormMean(length,procentag)
muFolded = 500

mu = length*procentag
#(2*length)/(math.sqrt(2)*erfinv(procentag*2))
sigma = length/(erfinv(procentag)*math.sqrt(2))
#sigma = sigma/math.sqrt(1-2/math.pi)
F = math.erf((length-0)/(sigma*math.sqrt(2)))

print("sigma",sigma)
print("muFolded",muFolded)
print("F",F)


i = 0
tot = 0
creaturesToKeep = []
for ele in lista:
    nr = abs(round(random.gauss(0, sigma)))
    tot = tot +nr
    if i <= nr:
        creaturesToKeep.append(ele)
    i = i +1

print(creaturesToKeep.__len__()/length)
print(tot/length)
