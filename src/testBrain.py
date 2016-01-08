'''
Created on 30 dec. 2015

@author: Henrik
'''
from NeuralNetwork.brain import spiderBrainFullyCon
from GUI.NodeMatrix import SpiderWebb

if __name__ == '__main__':
    Webb = SpiderWebb(5, 5)
    SpiderBrain = spiderBrainFullyCon([100, 10, 10, 1])
    SpiderBrain.randomizeAllWeights();
    print(Webb.ConvertWebbToList().__len__());
    number = SpiderBrain.crunch(Webb.ConvertWebbToList())
    print(number)
 
# Webb = SpiderWebb(5, 5)
# # Webb.Webb[0][0][0] = 3
# # print (Webb.Webb[99][0][0])
# Webb.InsertSpiderThread({'x':1, 'y':1}, {'x':1, 'y':2})
# Webb.InsertSpiderThread({'x':1, 'y':1}, {'x':1, 'y':0})
# #print (Webb.Webb)
# Webb.ConvertWebbToList(); 