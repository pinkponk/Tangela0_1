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



length = 100
lista = []
for n in range(0,length):
    lista.append(random.randrange(0,100))
lista.sort(key=None, reverse=True)
print(lista)
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


def calcSigma(procent, length):
    ''' Calculates the necessary sigma for a half gaussian distribution such that
    an even distribution from 0 to "length" will have "percent" % of it's numbers 
    above multiple calls from the gaussian.'''
    
    p1 =      -1.969
    p2 =       1.977
    q1 =      -4.431
    q2 =       4.883
    q3 =     0.06092
    
    x = procent
    sigmaNorm = (p1*x+p2)/(x*x*x+q1*x*x+q2*x+q3)
    sigma = sigmaNorm*length
    return sigma


sigma = calcSigma(1-0.3,length)
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
print(creaturesToKeep)



'''
class Spider(object):

    def __init__(self):
        self.ID = random.randrange(0,100)
        
        
        
A = []  
B = []  
import weakref


def callback(reference):
    """Invoked when referenced object is deleted"""
    print('callback(', reference, ')')
    

for i in range(0,10):
    tempObject = Spider()
    A.append(tempObject)
    B.append(weakref.ref(tempObject,callback))

for spider in A:
    print(spider.ID,end=" ")
print(" ")
for spider in B:
    print(spider().ID,end=" ")
    

A.pop(0)

print(" ")
for spider in A:
    print(spider.ID,end=" ")
print(" ")
for spider in B:
    if spider() is not None:
        print(spider().ID,end=" ")
    else:
        print("No", end=" ")

B = [x for x in B if x() is not None]

print(" ") 
for spider in B:
    if spider() is not None:
        print(spider().ID,end=" ")
    else:
        print("No", end=" ")
print(" ")
print(B)'''

       
        