'''
Created on 30 dec. 2015

@author: Henrik
'''
import math
import random
import copy
import numpy

class BrainFullyCon(object):
    '''
    classdocs
    Summary: A deep neural network meant to symbolize the brain of in this case a spider but is completely generic
    and can be used for other purposes. The name implies that the sigumd perceptrons are all fully connected in
    between the layers.
    
    "o" -perceptron
    "-" -link
    
                   /o
    input 1 --o-\ /-o       o\
    input 2 --o-----o  ...  o---o---output 1
    input 3 --o-/ \-o       o/
                   \o
    '''

    
    

    def __init__(self, layerStruct):
        '''
        Constructor
        
        ex:
        layerStruc = [4892, 20, 15, 10, 1]   eg. first 4892 neurons (input layer) connected with 
        20 neurons (hidden layer), connected with 15 neurons (hidden layer), connected with 10 
        neurons (hidden layer), connected with 1 neuron (output layer)
        '''
        
        self.allLayers = []
        self.weightVector = []
        self.layerStruct = layerStruct
        
        for layerIndex in range(0,self.layerStruct.__len__()):
            self.allLayers.append([])
            
            if layerIndex==0:
                inputNumber = 1
            else:
                inputNumber = self.layerStruct[layerIndex-1]
                    
            for index2 in range(0,self.layerStruct[layerIndex]):
                self.allLayers[layerIndex].append(perceptron([0]*inputNumber,0))



        
        
    def crunch(self, inputsOriginal):
        inputs = copy.deepcopy(inputsOriginal)
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
                self.allLayers[layerIndex][index2].b = (random.random()*2+-1)
        
        
        
        
    def copyBrainWeights(self,allLayersToCopyFrom):
        #Children
        self.allLayers=copy.deepcopy(allLayersToCopyFrom)
        
    '''def randomizeSomeWeights(self,procentHowMany,procentHowMuch):
        #Mutation
        totalNrWeights = self.layerStruct[0]*2
        for layerIndex in range(1,self.layerStruct.__len__()):
            totalNrWeights=totalNrWeights+self.layerStruct[layerIndex-1]*self.layerStruct[layerIndex]
        
        
        for times in range(0,math.ceil(self.layerStruct[layerIndex]*2*procentHowMany)):
            percept = random.choice(self.allLayers[0])
            
            if random.randrange(0,2,1) == 1:
                percept.k = [percept.k[0]+percept.k[0]*random.randrange(-1,2,2)*procentHowMuch]
            else:
                percept.b = percept.b+percept.b*random.randrange(-1,2,2)*procentHowMuch
            
        
        for layerIndex in range(1,self.layerStruct.__len__()):
            for times in range(0,math.ceil((1+self.layerStruct[layerIndex-1])*self.layerStruct[layerIndex]*procentHowMany)):
                index = random.randrange(0,(1+self.layerStruct[layerIndex-1]),1)
                percept = random.choice(self.allLayers[layerIndex])
                if index == 0:
                    percept.b = percept.b+percept.b*random.randrange(-1,2,2)*procentHowMuch
                else:
                    percept.k[index-1] = percept.k[index-1]+percept.k[index-1]*random.randrange(-1,2,2)*procentHowMuch
                    '''

    def randomizeSomeWeights(self,procentHowMany):
        #Mutation
        
        for times in range(0,math.ceil(self.layerStruct[0]*2*procentHowMany)):
            percept = random.choice(self.allLayers[0])
            
            if random.randrange(0,2,1) == 1:
                percept.k = [(random.random()*2+-1)]
            else:
                percept.b = (random.random()*2+-1)
            
        
        for layerIndex in range(1,self.layerStruct.__len__()):
            for times in range(0,math.ceil((1+self.layerStruct[layerIndex-1])*self.layerStruct[layerIndex]*procentHowMany)):
                index = random.randrange(0,(1+self.layerStruct[layerIndex-1]),1)
                percept = random.choice(self.allLayers[layerIndex])
                if index == 0:
                    percept.b = (random.random()*2+-1)
                else:
                    percept.k[index-1] = (random.random()*2+-1)
        
    
    def updateWeightVector(self):
        self.weightVector = []
        for layer in self.allLayers:
            for percept in layer:
                self.weightVector.append(percept.b)
                self.weightVector.extend(percept.k)
                
        
    def visualizeActivation(self):
        d = 0
        uhcouevh = 0
        
        
        
        
        
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
        t = numpy.dot(inputVector,self.k)+self.b
        outputNumber = 1/(1+math.exp(-t))
       
        
        return outputNumber
        
    '''def dotProduct(self,a,b):
        if (a.__len__() != b.__len__()):
            print("CANNOT MAKE CORRECT DOT PRODUCT, SIZE MISSMATCH")
        c = 0
        for index in range(0,a.__len__()):
            c+=(a[index]*b[index])
        return c'''      
            


'''def print2DMatrix(matrix):

    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))'''
        
        
        