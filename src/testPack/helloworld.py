'''
Created on 30 dec. 2015

@author: Henrik
'''
import random
import time
import math

import NeuralNetwork.brain

if __name__ == '__main__':
    
    millis = int(round(time.time() * 1000))
    random.seed(millis)
    hej =(NeuralNetwork.brain.spiderBrainFullyCon([10,100,100,8]))
    hej.randomizeAllWeights()
    
    output = hej.crunch([1,1,1,1,1,1,1,1,1,1])
    max_value = max(output)
    max_index = output.index(max_value)
    print("max_value = ",round(max_value,3)," max_index = ", max_index)

    
    print("Hello World!")
    
    '''p = []
    for i in range(0,1000):
        p.append(NeuralNetwork.brain.spiderBrainFullyCon([400,20,15,1]))
        p[i].randomizeAllWeights()
        input2 = [random.random()]*400
        #print(p[i].crunch(input2))
        print(i)
        '''
    pass