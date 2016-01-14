'''
Created on 10 jan. 2016

@author: Henrik
'''

import copy
import random
import math
import time

import NeuralNetwork.brain
from NeuralNetwork.brain import BrainFullyCon

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
        
        self.inputSize = 3
        self.outputSize = 1
        self.spiders = []
        self.topScoreSpiders = []
        self.spiderChildren = []
        self.numberOfSpiders = numberOfSpiders
        self.brainStruct = [self.inputSize,30,30,self.outputSize]
        self.spiderIDCounter = 0
        self.spidersSurvivied = 0
        self.spidersPure = 0
        self.staticInput = []
        self.staticAnswer = []
        
        for i in range(0,self.numberOfSpiders):
            self.spiders.append(Spider(self.brainStruct,self.spiderIDCounter,[self.spiderIDCounter,self.spiderIDCounter]))
            self.spiderIDCounter = self.spiderIDCounter+1
            
        for spider in self.spiders:
            spider.brain.randomizeAllWeights()
                    
        self.generateStaticInput(3, 30)
        for generation in range(0,100):
            nrOfSims = 10000
            self.simpleSimulate()
            #self.simulate(nrOfSims)
            #self.categorizeSpecies()
            print("---------------------------------------------")
            print("Gen=",generation, "SurvPop=",self.spidersSurvivied, "PurePop=", self.spidersPure)
            for i in range(0,10):
                print(i,": Fitness:",round(self.spiders[i].fitness,4),"\tCorrectGuesses=",round(self.spiders[i].correctGuesses/30*100,2),"%", "\tID=",self.spiders[i].ID, "Parents ID=",self.spiders[i].parentsID, "NrOfGenPure=",self.spiders[i].nrOfGenerationsPure)
            self.killOff(0.5)  #Keep 10% alive, kill the rest by Gaussian dist
            print("Killoff: complete")
            self.safeKeepTopScoreSpiders(0.10)
            print("Elistism: complete")
            self.crossOver1()
            print("CrossOver: complete")
            self.mutate(0.05)  #Don't mutate the top 5% of the survivors, at least one will not mutate if non zero
            print("Mutate: complete")
            
    def generateStaticInput(self,length,number):
        for i in range(0,number):
            self.staticInput.append([])
            for ii in range(0,length):
                self.staticInput[i].append(random.random())
            if random.random()>0.5:
                self.staticInput[i].sort()
                self.staticAnswer.append(1)
            else:
                self.staticAnswer.append(0)
                while(sorted(self.staticInput[i])==self.staticInput[i]):
                        random.shuffle(self.staticInput[i])
        
        
    def simpleSimulate(self):
        for spider in self.spiders:
            spider.correctGuesses = 0
            spider.output = 0
            
            for i in range(0,self.staticAnswer.__len__()):
                outputTemp = spider.brain.crunch(self.staticInput[i])
                #print(outputTemp)
                if self.staticAnswer[i] == 1:
                    spider.output = spider.output + (1-outputTemp[0])
                    if outputTemp[0]>0.5:
                        spider.correctGuesses =spider.correctGuesses+1
                elif self.staticAnswer[i] == 0:
                    spider.output = spider.output + (outputTemp[0])
                    if outputTemp[0]<=0.5:
                        spider.correctGuesses =spider.correctGuesses+1
                else:
                    print("something went wrong")
                        
            spider.fitness = 0.5/(spider.output/self.staticAnswer.__len__())
            
            self.spiders=sorted(self.spiders, key=lambda spider: spider.correctGuesses)
            self.spiders.reverse()           
            
    
    def simulate(self,NrOfTimes):
        for spider in self.spiders:
            spider.correctGuesses = 0
            spider.output = 0
        
            for times in range(0,NrOfTimes):
                sortOrNotSorted = random.randrange(0,2,1)
                inputVector = []
                for i in range(0,self.inputSize):
                    inputVector.append(random.random())
    
                if sortOrNotSorted==1:
                    answer = "sorted"
                    inputVector.sort()
                else:
                    answer = "random"
                    while(sorted(inputVector)==inputVector):
                        random.shuffle(inputVector)
                
                                
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
                        
            spider.fitness = 0.5/(spider.output/NrOfTimes)
            
        self.spiders=sorted(self.spiders, key=lambda spider: spider.output)   # lowest has the least error out of NrOfTimes tries
    

    def killOff(self,procentToSafeKeep):
        i = 0
        spidersToSafeKeep = round(procentToSafeKeep*self.numberOfSpiders)
        newSpiders = []
        for spider in self.spiders:
            if i<=spidersToSafeKeep:
                newSpiders.append(spider)
            else:
                if i < (abs(round(random.gauss(0, round((self.numberOfSpiders-spidersToSafeKeep)/3))))+spidersToSafeKeep):
                    newSpiders.append(spider)
            i = i +1
        self.spiders = newSpiders
        self.spidersSurvivied = self.spiders.__len__()
    
    def categorizeSpecies(self):
        '''Will categorize all spiders into species and give each species a letter code
        If the checked spider's weights are too different from the all the existing species
        then a new species is created with a letter code following simple rules:
        if mutated from spider species which letter code was
        -CAAAAA then use CAAAAB 
        if completely new random spider then use 
        -CUSAA then use CUTAA
        -etc
        
        
        '''
        b = 0    
    
    def safeKeepTopScoreSpiders(self,procentToSafeKeep):
        self.topScoreSpiders = []
        spidersToSafeKeep = math.ceil(self.spiders.__len__()*procentToSafeKeep)
        i = 0
        for spider in self.spiders:
            if i<spidersToSafeKeep:
                spiderCopy = self.copySpider(spider,self.brainStruct,spider.ID)
                spider.ID = self.spiderIDCounter 
                self.spiderIDCounter = self.spiderIDCounter+1
                self.topScoreSpiders.append(spiderCopy)
                spiderCopy.nrOfGenerationsPure = spider.nrOfGenerationsPure+1
                
                #self.spiders.remove(spider)
            else:
                break
            i = i +1
        
    def copySpider(self, spiderOriginal,brainStruct,spiderIDCounter):
        spiderCopy = Spider(brainStruct,spiderIDCounter,spiderOriginal.parentsID)
        spiderCopy.brain.copyBrainWeights(spiderOriginal.brain.allLayers)
        return spiderCopy
        
        
        
    def crossOver1(self):
    #Finds two parents by random with the fitness as weight. Then takes the genes from 
    #both parents and combines them into a new child
        self.spiderChildren = []
        
        for k in range(0,self.numberOfSpiders-(self.spiders.__len__()+self.topScoreSpiders.__len__())):
            spiderParents = []
            runAgain = 1
            while runAgain == 1:
                roulette = []
                intervalInc = 0
                for spider in self.spiders:
                    intervalInc = intervalInc + spider.fitness*100
                    roulette.append([spider,intervalInc])
                if intervalInc<self.spiders.__len__():
                    print("WARNING BAD ROULETT RESOLUTION")
                index = random.randrange(0,math.ceil(intervalInc+1),1)
                                
                n = 0
                while index > math.ceil(roulette[n][1]):
                    n = n+1
                if spiderParents.__len__()==0:
                    spiderParents.append(roulette[n][0])
                elif spiderParents[0]!=roulette[n][0]:
                        spiderParents.append(roulette[n][0])
                        runAgain = 0
            if spiderParents.__len__()!=2:
                print("WARNING: NOT 2 PARENTS")  
            spiderChild = Spider(self.brainStruct,self.spiderIDCounter,[spiderParents[0].ID,spiderParents[1].ID])
            self.spiderIDCounter = self.spiderIDCounter+1
            
            for layerIndex in range(0,self.brainStruct.__len__()):
                for neuronIndex in range(0,self.brainStruct[layerIndex]):
                    spiderChild.brain.allLayers[layerIndex][neuronIndex].b = spiderParents[0].brain.allLayers[layerIndex][neuronIndex].b
                    spiderChild.brain.allLayers[layerIndex][neuronIndex].k = copy.deepcopy(spiderParents[0].brain.allLayers[layerIndex][neuronIndex].k)
                else:
                    spiderChild.brain.allLayers[layerIndex][neuronIndex].b = spiderParents[1].brain.allLayers[layerIndex][neuronIndex].b
                    spiderChild.brain.allLayers[layerIndex][neuronIndex].k = copy.deepcopy(spiderParents[1].brain.allLayers[layerIndex][neuronIndex].k)
            self.spiderChildren.append(spiderChild)
            
        self.spiders.extend(self.spiderChildren)
        

    def mutate(self,procentHowMuch):
        for spider in self.spiders:
            spider.nrOfGenerationsPure = 0
            spider.brain.randomizeSomeWeights(procentHowMuch)
            
        self.spiders.extend(self.topScoreSpiders)
        self.spidersPure = self.topScoreSpiders.__len__()
        
        if self.spiders.__len__() != self.numberOfSpiders:
            print("SPIDER POPULATION IS CHANGING SIZE")

        
        
class Spider(object):
    
    def __init__(self,struct,ID,parentsID):
        self.brain = BrainFullyCon(struct)
        self.output = 0
        self.nrOfGenerationsPure = 0
        self.correctGuesses = 0
        self.ID = ID
        self.fitness = 0
        self.parentsID = parentsID
        


        
        
evoTest = EvoTest(30)

print("elapsed time: ",(time.time()-evoTest.startTime),"[s]")


        