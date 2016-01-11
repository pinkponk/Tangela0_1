'''
Created on 10 jan. 2016

@author: Henrik
'''

import copy
import random
import math
import time

import NeuralNetwork.brain
from NeuralNetwork.brain import spiderBrainFullyCon

class EvoTest(object):
    '''
    classdocs
    '''


    def __init__(self, numberOfSpiders):
        '''
        Constructor
        '''
        
        millis = int(round(time.time() * 1000))
        random.seed(millis)
        self.startTime = time.time()
        
        self.inputSize = 10
        self.outputSize = 1
        self.spiders = []
        self.numberOfSpiders = numberOfSpiders
        self.brainStruct = [self.inputSize,20,10,2,self.outputSize]
        self.spiderIDCounter = 0
        self.spidersSurvivied = 0
        for i in range(0,self.numberOfSpiders):
            self.spiders.append(Spider(self.brainStruct,self.spiderIDCounter))
            self.spiderIDCounter = self.spiderIDCounter+1
        for spider in self.spiders:
            spider.brain.randomizeAllWeights()
        
        for generation in range(0,1000):
            self.simulate(500)
            print("Gen=",generation,"topScore=", self.spiders[0].correctGuesses, "ID=",self.spiders[0].ID, "SurvPop=",self.spidersSurvivied)
            self.killOff(0.1)  #Keep 10% 100% safe and alive, kill the rest by Gaussian dist
            self.mutate(0.05)  #Don't mutate the top 5% of the survivors, at least one will not mutate i non zero
            self.rePopulate()
        
            
    
    def simulate(self,NrOfTimes):
        for spider in self.spiders:
            spider.correctGuesses = 0
            spider.output = 0
            
        for times in range(0,NrOfTimes):
            sortOrNotSorted = random.random()
            inputVector = []
            for i in range(0,self.inputSize):
                inputVector.append(random.random())

            answer = "random"
            if sortOrNotSorted>0.5:
                answer = "sorted"
                inputVector.sort()
            
            for spider in self.spiders:
                outputTemp = spider.brain.crunch(inputVector)
                if answer == "sorted":
                    spider.output = spider.output + (1-outputTemp[0])
                    if outputTemp[0]>0.5:
                        spider.correctGuesses =spider.correctGuesses+1
                elif answer == "random":
                    spider.output = spider.output + (outputTemp[0])
                    if outputTemp[0]<=0.5:
                        spider.correctGuesses =spider.correctGuesses+1
                else:
                    print("something went wrong")
 

        self.spiders=sorted(self.spiders, key=lambda spider: spider.output)   # lowest has the least error out of NrOfTimes tries

    def killOff(self,procentToSafeKeep):
        i = 0
        spidersToSafeKeep = round(procentToSafeKeep*self.numberOfSpiders)
        newSpiders = []
        for spider in self.spiders:
            if i<spidersToSafeKeep:
                newSpiders.append(spider)
            else:
                if i < (abs(round(random.gauss(0, round((self.numberOfSpiders-spidersToSafeKeep)/3))))+spidersToSafeKeep):
                    newSpiders.append(spider)
            i = i +1
        self.spiders = newSpiders
        self.spidersSurvivied = self.spiders.__len__()
    
    def mutate(self,procentToSafeKeep):
        i = 0
        spidersToSafeKeep = math.ceil(procentToSafeKeep*self.spiders.__len__())
        for spider in self.spiders:
            if i<spidersToSafeKeep:
                spider.nrOfGenerationsPure = spider.nrOfGenerationsPure+1
            else:
                if i < (abs(round(random.gauss(0, round((self.numberOfSpiders-spidersToSafeKeep)/3))))+spidersToSafeKeep):
                    spider.brain.randomizeSomeWeights(0.1,0.5)
                    spider.nrOfGenerationsPure = 0
                else:
                    spider.nrOfGenerationsPure = spider.nrOfGenerationsPure+1
            i = i +1       
        
        
    def rePopulate(self):
        for i in range(self.spiders.__len__(),self.numberOfSpiders):
            newSpider = Spider(self.brainStruct,self.spiderIDCounter)
            self.spiderIDCounter = self.spiderIDCounter+1
            newSpider.brain.randomizeAllWeights()
            self.spiders.append(newSpider)
        if self.spiders.__len__() != self.numberOfSpiders:
            print("SPIDER POPULATION IS CHANGING SIZE")
        
class Spider(object):
    
    def __init__(self,struct,ID):
        self.brain = spiderBrainFullyCon(struct)
        self.output = 0
        self.nrOfGenerationsPure = 0
        self.correctGuesses = 0
        self.ID = ID

        
        
evoTest = EvoTest(1000)
print("elapsed time: ",(time.time()-evoTest.startTime),"[s]")


        