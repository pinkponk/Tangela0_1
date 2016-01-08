'''
Created on 30 dec. 2015

@author: Henrik
'''
import random

import NeuralNetwork.brain

if __name__ == '__main__':

    #hej =(NeuralNetwork.brain.spiderBrainFullyCon([3,2,1]))
    #hej.randomizeAllWeights()
    #print(hej.crunch([1,1,1]))
    #print("Hello World!")
    
    p = []
    for i in range(0,1000):
        p.append(NeuralNetwork.brain.spiderBrainFullyCon([400,20,15,1]))
        p[i].randomizeAllWeights()
        input2 = [random.random()]*400
        #print(p[i].crunch(input2))
        print(i)
    pass