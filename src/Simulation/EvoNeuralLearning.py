'''
Created on 14 jan. 2016

@author: Henrik
'''
import numpy
import math
import time
import random

from NeuralNetwork.brain import BrainFullyCon

class EvoNeuralLearning(object):
    '''
    This class is for learning a deep neural network by using a genetic algorithm composed of:
    1) Simulation
    2) Ranking
    3) Species categorization
    4) Kill off
    5) Elitism and Diversity retantion
    6) Reproduce
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.brainStruct = [20,10,10,1]
        self.nrOfCreatures = 40
        self.creatures = []
        self.creatureIDCounter = 0
        
        
        millis = int(round(time.time() * 1000))
        random.seed(millis)
        
        self.createInitPopulation()
    
    def runGeneration(self):
        a = 0
        
    def createNewCreature(self):
        newCreature = Creature(self.brainStruct,self.creatureIDCounter)
        self.creatures.append(newCreature)
        self.creatureIDCounter = self.creatureIDCounter+1
        return newCreature
                    
    def createInitPopulation(self):
        '''Creates a initial population with all random weights for the neural brain'''
        for i in range(0,self.nrOfCreatures):
            newCreature=self.createCreature()
            newCreature.randomizeAllWeights()
        
    def simulate(self):
        a = 0
    def ranking(self):
        a = 0
    def speciesCategorization(self):
        a = 0
    def killOff(self):
        a = 0
    def elitismAndDiversitySustainabilty(self):
        a = 0
    def reProduce(self):
        a = 0
        
    


class Creature():
    '''
    classdocs
    '''
    
    def __init__(self,brainStruct,creatureIDCounter):
        '''
        Constructor
        '''    
        self.brain = BrainFullyCon(brainStruct)
        self.ID = creatureIDCounter
        self.fitness
        
        self.output = 0
        self.nrOfGenerationsPure = 0
        self.correctGuesses = 0
                
        
        
        
        
        
        