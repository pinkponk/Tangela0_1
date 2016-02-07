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

    TO DO
    1)correlation jump, all katekorized to new species...


    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.brainStruct = [20,10,10,1]
        self.nrOfCreatures = 30
        self.targetNrOfSpecies = 3
        self.populationToKeep = 0.5
        self.elitismPercentage = 0.05
        self.mutationChance = 0.05
        self.lowScoreSpeciesRemovalChance = 0.05
        self.shouldDeleteLowScoreSpecies = False
        
        self.species = []                               #A list containing all the current classified species
        self.creatures = []
        self.eliteCreatures = []                          #These will at the end of cycle be the new creatures
        self.speciesCorrelationMargin = 0               #If the correlation of a creature is over the margin then that creature is categorized to that species
        self.creatureIDCounter = 0
        self.speciesEverExisted = 0
        
        file = open("Animal-words.txt")
        self.animalNames = file.readlines()
        self.usedAnimalNames = []
        file.close()
        
        self.createInitPopulation()
        self.speciesCategorization(self.creatures)
        
    
    def determaineSpeciesName(self):
        name = random.choice(self.animalNames)
        name = name.rstrip()
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
        
        self.simulate()
        self.ranking()
        self.elitismAndDiversitySustainabilty(self.elitismPercentage)
        
        self.multipleSpeciesForSameCreatureTest(self.creatures)
        self.multipleSpeciesForSameCreatureTest(self.eliteCreatures)
        
        self.killOffPerSpecies(self.populationToKeep)
        self.reProduce(1)
        self.mutate(self.mutationChance)
        self.speciesCategorization(self.creatures)

        
    def createNewCreature(self):
        newCreature = Creature(self.brainStruct,self.creatureIDCounter)
        self.creatures.append(newCreature)
        self.creatureIDCounter = self.creatureIDCounter+1
        return newCreature
                    
    def createInitPopulation(self):
        '''Creates a initial population with all random weights for the neural brain'''
        for i in range(0,self.nrOfCreatures):
            newCreature=self.createNewCreature()
            newCreature.brain.randomizeAllWeights()
        
    def simulate(self):
        a = 0
        #Just for testing purpose give all random fitness
        for creature in self.creatures:
            creature.fitness = random.random()*100
        
    def ranking(self):

        
        '''Sorts the list of creatures with respect to fitness, highest fitness at the top of the list''' 
        self.creatures=sorted(self.creatures, key=lambda creature: creature.fitness)
        self.creatures.reverse()
        
        '''Also sort the creatures categorized in all the species, highest fitness first'''
        for specie in self.species:
            specie.creatures = sorted(specie.creatures, key=lambda creature: creature.fitness)
            specie.creatures.reverse()
        
    def gaussianTathet(self,x,mu,sigma):
        '''return (1/(sigma*math.sqrt(2*math.pi)))*math.exp(-math.pow(x-mu,2)/(2*math.pow(sigma,2)))'''
        return 0.5*(1+math.erf((x-mu)/(sigma*math.sqrt(2))))
    
    def gaussianTathetABS(self,x,mu,sigma):
        '''Returns the Cumulative distribution function for a abs(gaussian) function'''
        return (1+math.erf((x-mu)/(sigma*math.sqrt(2))))-(1+math.erf((0-mu)/(sigma*math.sqrt(2))))
    
    def calcSigma(self, procent, length):
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

    def killOffPerSpecies(self, popToKeepProcent):
        '''Keeps a certain amount of percentage of the population while the rest is killed. 
        The creatures with lowest fitness will still have a small chance to survive because of
        the gaussian dist used for deciding who gets killed. To preserve species, killing and ranking
        is done internally'''
        
        tempCreatures = []
        tempTopScoreSpecies = []
        
        for specie in self.species:
            tempTopScoreSpecies.append([specie,specie.creatures[0].fitness])
            sigma = self.calcSigma(1-popToKeepProcent,specie.creatures.__len__())
            i = 0
            creaturesToKeep = []
            for creature in specie.creatures:
                if i< abs(round(random.gauss(0, sigma))):
                    creaturesToKeep.append(creature)
                    tempCreatures.append(creature)
                i = i +1
            specie.creatures = creaturesToKeep      #NEED DEEP COPY(will loose performance)? ASK GUSTAV
            
        
        if self.shouldDeleteLowScoreSpecies == True:
            if self.species.__len__()>self.targetNrOfSpecies and random.random()< self.lowScoreSpeciesRemovalChance:
                '''The worst species (the species top creature as benchmark) at the top of list'''    
                tempTopScoreSpecies = sorted(tempTopScoreSpecies, key=lambda tempTopScoreSpecies: tempTopScoreSpecies[1])
                '''Should I delete this species?'''
                #Testing with delete bad species if too many
                print(tempTopScoreSpecies[0][0].name," removed because low score")
                for creature in tempTopScoreSpecies[0][0].creatures:
                    self.creatures.remove(creature)
                self.species.remove(tempTopScoreSpecies[0][0])
                
            
        
        self.creatures = tempCreatures              #Refreshes the list of creatures
        self.ranking()                  #Re-ranks the list of creatures, kill-off mixed the list.
        
            
                
    def elitismAndDiversitySustainabilty(self, procentageToSafeKeep):
        '''Preserve/Copy the best ones from all species for all species to save it from mutation.
        One creature from each species will always be protected/copied if percentage!=0
        The percentage is based on the current number of creatures not the original total amount'''
        
        self.eliteCreatures = []
        self.ranking()                  #Re-ranks the list of creatures, just in case
        for spec in self.species:
            for n in range(0,math.ceil(procentageToSafeKeep*spec.creatures.__len__())):
                newEliteCreature = self.cloneCreature(spec.creatures[n])
                self.eliteCreatures.append(newEliteCreature)
        
        
            
                
                
    def chooseParentRoulette(self,listOfSelectable):
        '''Selects a parent based on the roulette tactic with fitness as weight'''
        
        #Create roulette
        listOfSelectable = sorted(listOfSelectable, key=lambda creature: creature.fitness)
        listOfSelectable.reverse()
        globalMaxFitness = listOfSelectable[0].fitness
        if globalMaxFitness == 0:
            print("ERROR WITH Creature: ",listOfSelectable[0].ID, ", is currently belonging to ", self.findCurrentCorrespondingSpeciesName(listOfSelectable[0]))
        multiplier = 1000/globalMaxFitness          #will ensure good resolution
        roulette = []
        intervalInc = 0
        for creature in listOfSelectable:
            intervalInc = math.ceil(intervalInc + creature.fitness*multiplier)
            roulette.append([creature,intervalInc])
        
        #randomly selects a index within the overall interval
        index = random.randrange(0,math.ceil(intervalInc+1),1)
        
        #Finds the corresponding creature for that index
        n = 0
        while index > roulette[n][1]:
            n = n+1
            
        return roulette[n][0]
    
    def removeEmptySpecies(self):
        '''Clear all the empty species'''
        removeThese = []
        for spec in self.species:
            if spec.creatures.__len__()==0:
                ''' Remove species if no creature is classified to it anymore '''
                print(spec.name," removed! no one left")
                removeThese.append(spec)
                
        for spec in removeThese:
            self.species.remove(spec)
    
    def reProduce(self, crossoverType=1):
        '''First finds two parents by randomly selecting two numbers then depending which intervals
        these numbers the appropriate parents are chosen. Each potential parent has its own interval
        which has its size proportional to its fitness.(roulette-version)'''
        
        elitismCreatures = copy.deepcopy(self.eliteCreatures)   #DO I NEED DEEP COPY?
        self.creatures.extend(elitismCreatures)
        self.speciesCategorization(elitismCreatures)
        self.removeEmptySpecies()
        
        #Chose parents
        newChildren = []
        self.ranking()                  #Re-ranks the list of creatures, just in case

        
        #Will loop until target nr of creatures are refilled
        while (0<(self.nrOfCreatures-self.creatures.__len__()-newChildren.__len__())):
            
            #======================================================
            #Randomly choose a species, low population species are more likely to be chosen
            specToBreed = None
            skip = 0
            #Create roulette
            
            #Lowest length species first
            speciesLengthRanking = sorted(self.species,key=lambda spec: spec.creatures.__len__())
            done = 0
            i = 0
            while done ==0:
                if random.random()>0.5:
                    break
                i = i + 1
            specToBreed = speciesLengthRanking[i%speciesLengthRanking.__len__()]
            #========================================================
            #Breed that species
            parents = [None,None]
            
            if specToBreed.creatures.__len__()<1:
                print("EMPTY SPECES, SHOULD NOT BE POSSIBLE len:", specToBreed.creatures.__len__(), " Name :",specToBreed.name)
                self.printStatus()
            elif specToBreed.creatures.__len__()==1:
                #This species has only one creature or less, later the elitism will be added but
                #this lone creature has no one to breed with so it takes one from another species

                if self.species.__len__()<2:
                    print("LESS THAN TWO SPECIES EXISTS! CANNOT FIND SECOND PARENT")
                    skip = 1
                else:
                    '''Does not reproduce this way if only 1 species left'''
                    parents[0] = specToBreed.creatures[0]
                    topCreatures = []
                    for spec in self.species:
                        if spec is not specToBreed:
                            topCreatures.append(spec.creatures[0])
                    parents[1] = self.chooseParentRoulette(topCreatures)
                    print("TWO SPECIES MATED!")
                
            elif random.random()<0.02:
                #This species has more than one creature, can breed within species but
                #a small chance made it so on creature from this species will breed with a creature
                #from another species
                if self.species.__len__()<2:
                    print("LESS THAN TWO SPECIES EXISTS! CANNOT FIND SECOND PARENT")
                    skip = 1
                else:
                    '''Does not reproduce this way if only 1 species left'''
                    parents[0] = self.chooseParentRoulette(specToBreed.creatures)
                    topCreatures = []
                    for spec in self.species:
                        if spec is not specToBreed:
                            topCreatures.append(spec.creatures[0])
                    parents[1] = self.chooseParentRoulette(topCreatures)
                    print("TWO SPECIES MATED!")
                    
            else:
                #Normal breeding within this species
                parents[0] = self.chooseParentRoulette(specToBreed.creatures)
                parents[1] = None
                while parents[0] is not parents[1]:
                    parents[1] = self.chooseParentRoulette(specToBreed.creatures)
            
            if parents.__len__()!=2:
                print("WARNING: NOT 2 PARENTS")
            elif parents[0] is None or parents[1] is None:
                print("One or Both of parents is None")
                
            
            if crossoverType == 1 and skip is not 1:
                newChildren.append(self.createChildNeuronCrossover(parents))
        
        self.creatures.extend(newChildren)
        
        if self.creatures.__len__() is not self.nrOfCreatures:
            print("REPRODUCTION DID NOT BALANCE TO RIGHT NR OF CREATURES!")
            print("Nr=",self.creatures.__len__())
            print("ElitCre=",self.eliteCreatures.__len__())
            
        
        
    def createChildNeuronCrossover(self,parents):
        child = Creature(self.brainStruct,self.creatureIDCounter)
        self.creatureIDCounter = self.creatureIDCounter+1
        
        for layerIndex in range(0,self.brainStruct.__len__()):
                for neuronIndex in range(0,self.brainStruct[layerIndex]):
                    if random.random()>0.5:
                        child.brain.allLayers[layerIndex][neuronIndex].b = parents[0].brain.allLayers[layerIndex][neuronIndex].b
                        child.brain.allLayers[layerIndex][neuronIndex].k = copy.deepcopy(parents[0].brain.allLayers[layerIndex][neuronIndex].k)
                    else:
                        child.brain.allLayers[layerIndex][neuronIndex].b = parents[1].brain.allLayers[layerIndex][neuronIndex].b
                        child.brain.allLayers[layerIndex][neuronIndex].k = copy.deepcopy(parents[1].brain.allLayers[layerIndex][neuronIndex].k)
        return child

    def mutate(self, howManyProcentage):
        '''Changes the weights by little of already big and by a lot if small, sqrt is used for that'''
        for creature in self.creatures:
            if not self.eliteCreatures.__contains__(creature):
                for layerIndex in range(0,self.brainStruct.__len__()):
                    for neuronIndex in range(0,self.brainStruct[layerIndex]):
                        if random.random()<howManyProcentage:
                            tempb = creature.brain.allLayers[layerIndex][neuronIndex].b
                            temp = abs(tempb**2+2*random.random()-1)
                            creature.brain.allLayers[layerIndex][neuronIndex].b = math.copysign(temp**0.5, tempb)
                        for kIndex in range(0,creature.brain.allLayers[layerIndex][neuronIndex].k.__len__()):
                            if random.random()<howManyProcentage:
                                tempk = creature.brain.allLayers[layerIndex][neuronIndex].k[kIndex]
                                temp = abs(tempk**2+2*random.random()-1)
                                creature.brain.allLayers[layerIndex][neuronIndex].k[kIndex] = math.copysign(temp**0.5, tempk)

    def speciesCategorization(self, creatureVector):
        '''Categorize all the creatures into a target number of species by comparing the angle
        between the genome (all he weights in one long vector) with the help of the dot product'''
        
        ''' Self regulation of how many species are allowed, changes the speciesCorrelationMargin accordingly  '''
        
        initMargin = 0
        for creature in creatureVector:
            weightVector = creature.createWeightVector()
            
            if self.species.__len__()==0:
                '''If no species exist, create the first species'''
                self.species.append(Species(copy.deepcopy(weightVector),self.determaineSpeciesName()))
                self.species[0].creatures.append(creature)
                initMargin = 1
                self.speciesEverExisted = self.speciesEverExisted+1
            else:
                correlation = []
                for spec in self.species:
                    '''Check the correlation with all the known species'''
                    correlation.append([spec, spec.compareWeightVector(weightVector)])
                correlationSorted = sorted(correlation, key=lambda correlation: correlation[1])
                correlationSorted.reverse()
                ''' Highest correlation on top'''
                
                
                '''Create  first guess of what the margin could be, some oscillations could occur 
                before converged to good value'''
                if initMargin == 1:
                    self.speciesCorrelationMargin = correlationSorted[0][1]
                    initMargin = 0
                     
                if self.speciesCorrelationMargin <= correlationSorted[0][1]:
                    #print("Margin:",self.speciesCorrelationMargin,"   curr correlation:",correlationSorted[0])
                    ''' Close enough to be part of that species '''
                    specBelong = correlationSorted[0][0]
                    
                    '''Delete any duplicate creature if not already in correct species and if 
                    new species classification, assign creature new species'''
                    for spec in self.species:
                        if spec.creatures.__contains__(creature)==True and specBelong != spec:
                            spec.creatures.remove(creature)
                        elif spec.creatures.__contains__(creature)==False and specBelong == spec:
                            specBelong.creatures.append(creature)
                        
                    if self.species.__len__()<self.targetNrOfSpecies:
                        self.speciesCorrelationMargin = self.speciesCorrelationMargin*1.1
                    #else:
                     #   self.speciesCorrelationMargin = self.speciesCorrelationMargin*1.00001

                else:
                    ''' Creature has a enough different genome to create a new species '''
                    print("New species Created")
                    newSpecies = Species(copy.deepcopy(weightVector),self.determaineSpeciesName())
                    self.speciesEverExisted = self.speciesEverExisted+1
                    self.species.append(newSpecies)
                    newSpecies.creatures.append(creature)
                    
                    if self.species.__len__()>self.targetNrOfSpecies:
                        self.speciesCorrelationMargin = self.speciesCorrelationMargin*0.9
                    

        self.removeEmptySpecies()
    
    def findCurrentCorrespondingSpeciesName(self,creature):
        for spec in self.species:
            if spec.creatures.__contains__(creature)==True:
                return spec.name
        return "No Species Found"

    def findCurrentCorrespondingSpeciesObject(self,creature):
        for spec in self.species:
            if spec.creatures.__contains__(creature)==True:
                return spec
        return None
        
    
    def printStatus(self):
        for i in range(0,self.creatures.__len__()):
            print(i,": Fitness:",round(self.creatures[i].fitness,4),"\tID=",self.creatures[i].ID,  "Species=",self.findCurrentCorrespondingSpeciesName(self.creatures[i]))
        print("Alive species:")
        for spec in self.species:
            print(spec.name, ", Nr of creatures: ",spec.creatures.__len__())
        print("Nr of Species", self.species.__len__())
        print("New species margin:" , self.speciesCorrelationMargin)
        print("Nr of species ever existed: ",self.speciesEverExisted)
        print("correlation Between Species Num: (the higher, the more diverse)", abs(self.correlationTestBetweenAllCreatures()))
        

    def cloneCreature(self, creature):
        clonedCreature = self.createNewCreature()
        clonedCreature.brain.copyBrainWeights(creature.brain.allLayers)
        clonedCreature.fitness = creature.fitness
        return clonedCreature
    
    def multipleSpeciesForSameCreatureTest(self,creatureList):
        for creature in creatureList:
            for spec in self.species:
                i = 0
                if spec.creatures.__contains__(creature):
                    i=i+1
                if i>1:
                    print(creature," is in multiple species, ERROR!")
                    
    def correlationTestBetweenAllCreatures(self):
        correlationNum = 0
        '''copying self.species and removing elements will remove them in both lists! major error'''
        '''This function takes a LOOOT of time, will slow down the process!'''
        
        '''SOETHING AINT RIGHT WITH THIS?'''
        for creature1 in self.creatures:
            for creature2 in self.creatures:
                if creature1 is not creature2:
                    correlationNum = correlationNum + creature1.compareWeightVector(creature2.createWeightVector())
        return math.log10(correlationNum/(math.factorial(self.creatures.__len__())))
        
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
        self.brainStruct = brainStruct
        self.ID = creatureIDCounter
        self.fitness = 0
        
        # do I need?
        self.species = None
        self.output = 0
        self.nrOfGenerationsPure = 0
        self.correctGuesses = 0
    
    def createWeightVector(self):
        weightVector = []
        for layerIndex in range(0,self.brainStruct.__len__()):
                for neuronIndex in range(0,self.brainStruct[layerIndex]):
                        weightVector.append(self.brain.allLayers[layerIndex][neuronIndex].b)
                        weightVector.extend(self.brain.allLayers[layerIndex][neuronIndex].k)
                        #DO I NEED DEEP COPY?
                        #weightVector.extend(copy.deepcopy(self.brain.allLayers[layerIndex][neuronIndex].k))
                        
        return weightVector
    
    def compareWeightVector(self,creatureVector):
        dotProductValue = numpy.dot(creatureVector,self.createWeightVector())
        normProductValue = numpy.linalg.norm(creatureVector)*numpy.linalg.norm(self.createWeightVector())
        correlation = dotProductValue/normProductValue
        correlation = (correlation+1)/2     #Normalizing the correlation to be in between 0 and 1
        
        '''The correlation ranges from 0: meaning totally different to 1: same direction in vector space'''
        return correlation

        
        
eveLearning = EvoNeuralLearning()
for i in range(0,10000):
    print("Gen Nr: ",i)
    eveLearning.runGeneration()
    eveLearning.printStatus()
print("GEN 1 DONE")