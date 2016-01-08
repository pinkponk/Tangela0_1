'''
Created on 30 dec. 2015

@author: Henrik
'''
import math
import random

class spiderBrainFullyCon(object):
    '''
    classdocs
    '''


    
    

    def __init__(self, layerStruct):
        '''
        Constructor
        
        ex:
        layerStruc = [4892, 20, 15, 10, 1]   eg. first 4892 neurons (input layer) connected with 20 neurons (hidden layer), connected with 15 neurons (hidden layer), connected with 10 neurons (hidden layer), connected with 1 neuron (output layer)
        '''
        
        self.allLayers = []
        self.layerStruct = layerStruct
        for layerIndex in range(0,self.layerStruct.__len__()):
            self.allLayers.append([])
            
            if layerIndex==0:
                inputNumber = 1
            else:
                inputNumber = self.layerStruct[layerIndex-1]
                    
            for index2 in range(0,self.layerStruct[layerIndex]):
                self.allLayers[layerIndex].append(perceptron([0]*inputNumber,0))





        '''self.webState=[[[0]*self.xSize]*self.ySize]*self.neighbours
        self.webWeights = [[0]*self.xSize]*self.ySize
        self.webBias = [0]*self.neighbours
        
        self.timeWeight = 0
        self.timeBias = 0
        
        
        print(self.webState)
        print(self.webState[0][0][0])
        print([[[0]*self.ySize]*2]*2)
        
        print("whatsup")'''
        
        
    def crunch(self, inputs):
        if inputs.__len__()==self.layerStruct[0]:
            i = 0
            for layer in self.allLayers:
                outputs = []
                if i == 0:
                    for percept in layer:
                        outputs.append(percept.activate([inputs.pop()]))
                    inputs = outputs
                    i = i+1
                else:
                    for percept in layer:
                        outputs.append(percept.activate(inputs))
                    inputs = outputs            
            
        else:
            print("Wrong input size")
        return outputs

        
    def randomizeAllWeights(self):
        for layerIndex in range(0,self.layerStruct.__len__()):
            
            if layerIndex==0:
                inputNumber = 1
            else:
                inputNumber = self.layerStruct[layerIndex-1]
                
            for index2 in range(0,self.layerStruct[layerIndex]):
                for index3 in range(0,inputNumber):
                    #'sets all k to a value between -1 and 1'
                    self.allLayers[layerIndex][index2].k[index3]= (random.random()*2+-1)
                #'sets b to a value between 0 and 1'
                self.allLayers[layerIndex][index2].b = random.random()
        
        
        
        
    def copyBrainWeights(self,allLayersToCopyFrom):
        #Children
        a = 0
        
    def randomizeSomeWeights(self):
        #Mutation
        d = 0
        
    def visualizeActivation(self):
        d = 0
        
        
        
        
        
        
class perceptron(object):
    '''
    classdocs
    '''
    k = []
    b = 0


    def __init__(self, kInput,bInput):
        '''
        Constructor
        '''
        self.k = kInput
        self.b = bInput
        
    def activate(self, inputVector):
        t = self.dotProduct(inputVector,self.k)+self.b
        outputNumber = 1/(1+math.exp(-t))
       
        
        return outputNumber
        
    def dotProduct(self,a,b):
        if (a.__len__() != b.__len__()):
            print("CANNOT MAKE CORRECT DOT PRODUCT, SIZE MISSMATCH")
        c = 0
        for index in range(0,a.__len__()):
            c+=(a[index]*b[index])
        return c           
            


def print2DMatrix(matrix):

    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))
        
        
        