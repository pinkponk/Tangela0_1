'''
Created on 30 dec. 2015

@author: Henrik
'''

class spiderBrain(object):
    '''
    classdocs
    '''
    webState = []
    
    neighbours = 8
    xSize = 100
    ySize = 100
    
    'weights and bias'
    webWeights = []
    webBias = []
    
    timeWeight = 0
    timeBias = 0
    

    def __init__(self, params):
        '''
        Constructor
        '''

        self.webState=[[[0]*self.xSize]*self.ySize]*self.neighbours
        self.webWeights = [[0]*self.xSize]*self.ySize
        self.webBias = [0]*self.neighbours
        
        self.timeWeight = 0
        self.timeBias = 0
        
        
        print(self.webState)
        print(self.webState[0][0][0])
        print([[[0]*self.ySize]*2]*2)
        
        print("whatsup")
        
        
        
        
        
        
        
        
class perceptron(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
        