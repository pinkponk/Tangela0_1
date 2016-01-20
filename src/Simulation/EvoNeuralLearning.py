'''
Created on 14 jan. 2016

@author: Henrik
'''
import numpy
import math
import copy
import time
import random
from scipy.special import erfinv

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
        self.targetNrOfSpecies = 5
        self.creaturesToKeep = 0.5
        
        self.creatureIDCounter = 0
        self.speciesNameCounter = ['A','A','A','A']     #use "".join(list) to print, and chr/ord to increment
        self.species = []                               #A list containing all the current classified species
        self.speciesCorrelationMargin = 0               #If the correlation of a creature is over the margin then that creature is categorized to that species
        
        self.killOffSigma = self.getKillOffSigma(self.creaturesToKeep)
        
        millis = int(round(time.time() * 1000))
        random.seed(millis)
        
        file = open("Animal-words.txt")
        self.animalNames = file.readlines()
        self.usedAnimalNames = []
        file.close()
        
        self.createInitPopulation()
    
    def getKillOffSigma(self,creaturesToKeep):
        error = 1
        x = self.nrOfCreatures
        mu = 0
        sigma = self.nrOfCreatures/3
        while(abs(error)<0.01):
            error = creaturesToKeep-self.gaussianTathetABS(x,mu,sigma)
            sigma = sigmaOld - 
            
            newtonrapson
            
        return sigma
        
    
    def determaineSpeciesName(self):
        name = random.choice(self.animalNames)
        name = name.rsptrip()
        if self.usedAnimalNames.__contains__(name):
            i = 0
            nameClean = name
            while(self.usedAnimalNames.__contains__(name)):
                i = i +1
                name = nameClean + str(i)
            self.usedAnimalNames.append(name)
        else:
            self.usedAnimalNames.append(name)
        return name
    
    def runGeneration(self):
        #Do we need a thread do make the simulation so that the GUI can show the results as they come along?
        #If so what kind of structure should we use?
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
        '''Sorts the list of creatures with respect to fitness, highest fitness at the top of the list''' 
        self.creatures=sorted(self.creatures, key=lambda creature: creature.fitness)
        self.creatures.reverse()
        
    def gaussianTathet(self,x,mu,sigma):
        '''return (1/(sigma*math.sqrt(2*math.pi)))*math.exp(-math.pow(x-mu,2)/(2*math.pow(sigma,2)))'''
        return 0.5*(1+math.erf((x-mu)/(sigma*math.sqrt(2))))
    
    def gaussianTathetABS(self,x,mu,sigma):
        '''Returns the Cumulative distribution function for a abs(gaussian) function'''
        return (1+math.erf((x-mu)/(sigma*math.sqrt(2))))-(1+math.erf((0-mu)/(sigma*math.sqrt(2))))
    
    def getSigmaForGaussianABS(self,nrOfElements, survivialRate):
        '''Returns what sigma which should be used in order to get a 
            certain amount of survivials
            F = math.erf((x-mu)/(sigma*math.sqrt(2)))
            sigma = (x-mu)/(erfinv(F)*math.sqrt(2))
            survivialRate = math.erf((nrOfElements-0)/(sigma*math.sqrt(2)))'''
        return nrOfElements/(erfinv(survivialRate)*math.sqrt(2))
        
        
    def killOff(self,populationToKeepProcent):
        '''Keeps at least a certain percentage of the population as well as some creatures that by 
        chance (gaussian(mu, sigma) dist) also will survive'''
        nrOfCreaturesToKeep = round(populationToKeepProcent*self.nrOfCreatures)
        sigma = round((self.nrOfCreatures-nrOfCreaturesToKeep)/3)
        i = 0
        creaturesToKeep = []
        for creature in self.creatures:
            if i<=nrOfCreaturesToKeep:
                creaturesToKeep.append(creature)
            else:
                if i < (abs(round(random.gauss(0, sigma)+nrOfCreaturesToKeep))):
                    creaturesToKeep.append(creature)
            i = i +1
        self.creatures = creaturesToKeep
        self.creaturesSurvivied = self.creatures.__len__() 
        
    def elitismAndDiversitySustainabilty(self):
        a = 0
    def reProduce(self):
        a = 0
    def mutate(self):
        a=0
    def speciesCategorization(self):
        '''Categorize all the creatures into a target number of species by comparing the angle
        between the genome (all he weights in one long vector) with the help of the dot product'''
        for creature in self.creatures:
            creature.updateWeightVector()
            
            if self.species.__len__()==0:
                '''If no species exist, create the first species'''
                self.species.append(Species(copy.deepcopy(creature.weightVector),self.determaineSpeciesName()))
                self.species[0].creatures.append(creature)
            else:
                correlation = []
                for spec in self.species:
                    '''Check the correlation with all the known species'''
                    correlation.append(spec.compareWeightVector(creature.weightVector))
                correlationSorted = correlation.sort()
                correlationSorted.reverse()
                ''' Highest correlation on top'''
                if self.speciesCorrelationMargin <= correlationSorted[0]:
                    ''' Close enough to be part of that species '''
                    indexOfSpecies = correlation.index(correlationSorted[0])
                    specBelong = self.species[indexOfSpecies]
                    
                    '''Delete any duplicate creature if not already in correct species and if 
                    new species classification, assign creature new species'''
                    for spec in self.species:
                        if spec.creatures.__contains__(creature)==True and specBelong != spec:
                            spec.remove(creature)
                            specBelong.append(creature)
                            if spec.creatures.__len__()==0:
                                ''' Remove species if no creature is classified to it anymore '''
                                self.species.remove(spec)
                            break
                        elif spec.creatures.__contains__(creature)==False and specBelong == spec:
                            specBelong.append(creature)
                            break

                else:
                    ''' Creature has a enough different genome to create a new species '''
                    newSpecies = Species(copy.deepcopy(creature.weightVector),self.determaineSpeciesName())
                    self.species.append(newSpecies)
                    newSpecies.creatures.append(creature)
                    
                ''' Self regulation of how many species are allowed, changes the speciesCorrelationMargin accordingly  '''
                if self.creatures.__len__()==self.targetNrOfSpecies:
                    self.speciesCorrelationMargin = correlationSorted[0]
                elif self.creatures.__len__()>self.targetNrOfSpecies:
                    self.speciesCorrelationMargin = self.speciesCorrelationMargin*0.8
                elif self.creatures.__len__()<self.targetNrOfSpecies:
                    self.speciesCorrelationMargin = self.speciesCorrelationMargin*1.2
                
                

        
        
        
        
        
class Species():
    
    def __init__(self,templateVector,speciesName):
        self.creatures = []
        self.templateVector = templateVector  
        self.name = speciesName
        

    def compareWeightVector(self,creatureVector):
        dotProductValue = numpy.dot(creatureVector,self.templateVector)
        normProductValue = numpy.linalg.norm(creatureVector)*numpy.linalg.norm(self.templateVector)
        correlation = dotProductValue/normProductValue
        correlation = (correlation+1)/2     #Normalizing the correlation to be in between 0 and 1
        
        '''The correlation ranges from 0: meaning totally different to 1: same direction in vector space'''
        return correlation



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
        
        # do I need?
        self.output = 0
        self.nrOfGenerationsPure = 0
        self.correctGuesses = 0
                
        
        
        
        
        
        