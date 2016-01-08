#!/usr/bin/env python
import numpy as np

'''
Created on 8 jan. 2016

@author: Gustav


SpiderWebb is a NodeXCount * NodeYCount * 4 matrix 
Each node has a connection to right up, right, right down, down ( 3 connections).

'''

class SpiderWebb:
    rightup = 0;
    right = 1;
    rightdown = 2;
    down = 3;
    
    
    def __init__(self, NodeXCount, NodeYCount):
        self.NodeXCount = NodeXCount;
        self.NodeYCount = NodeYCount;
        self.Webb = np.zeros((NodeXCount, NodeYCount, 4));
        
    #InsertsThread
    #input:
    #     Node1Pos = {'x': 3, 'y': 4}
    #     Node2Pos = {'x': 4, 'y': 5}
    #output:
    #     SpiderPos after insert
    def InsertSpiderThread(self, Node1, Node2):
        try:
          Xlength = abs(EndPos['x'] - Node1Pos['x'])
          Ylength = abs(EndPos['y'] - Node1Pos['y'])
          if (Xlength > 1 or Ylength > 1 or (Xlength == 0 and Ylength == 0)):
              raise ValueError('Invalid node connection. Xlength: ' + str(Xlength) + ", Ylength: " + str(Ylength));
          elif (Node1Pos['x'] < 0 or Node1Pos['x'] > (self.NodeXCount-1)):
              raise ValueError('Index out of bound. Node1Pos[''x'']: ' + Node1Pos['x']);
          elif (Node1Pos['y'] < 0 or Node1Pos['y'] > (self.NodeYCount-1)):
              raise ValueError('Index out of bound. Node1Pos[''y'']: ' + Node1Pos['y']);
          elif (EndPos['x'] < 0 or EndPos['x'] > (self.NodeXCount-1)):
              raise ValueError('Index out of bound. EndPos[''x'']: ' + EndPos['x']);
          elif (EndPos['y'] < 0 or EndPos['y'] > (self.NodeYCount-1)):
              raise ValueError('Index out of bound. Node1Pos[''x'']: ' + Node1Pos['x']);
          else: ## ALL OK
              self.__insert_spider_thread(Node1Pos, EndPos);
              return EndPos;
        except ValueError as e:
            print(str(e))
            print('Insert had no effect.')
            return Node1Pos;
          # self.Webb
          
    def __insert_spider_thread(self, Node1Pos, EndPos):
        x_dir = EndPos['x'] - Node1Pos['x'];
        y_dir = EndPos['y'] - Node1Pos['y'];
        if(x_dir > 0):
            if(y_dir < 0):
                self.Webb[Node1Pos['x']][Node1Pos['y']][SpiderWebb.rightup] = 1;
            elif(y_dir == 0):
                self.Webb[Node1Pos['x']][Node1Pos['y']][SpiderWebb.right] = 1;
            else:
                self.Webb[Node1Pos['x']][Node1Pos['y']][SpiderWebb.rightdown] = 1;
        elif(x_dir == 0):
            if(y_dir < 0):
                self.Webb[EndPos['x']][EndPos['y']][SpiderWebb.down] = 1;
            elif(y_dir == 0):
                raise ValueError('Same index of nodes.');
            else:
                self.Webb[Node1Pos['x']][Node1Pos['y']][SpiderWebb.down] = 1;
        else:
            if(y_dir < 0):
                self.Webb[EndPos['x']][EndPos['y']][SpiderWebb.rightdown] = 1;
            elif(y_dir == 0):
                self.Webb[EndPos['x']][EndPos['y']][SpiderWebb.right] = 1;
            else:
                self.Webb[EndPos['x']][EndPos['y']][SpiderWebb.rightup] = 1;

    def ConvertWebbToList(self):
        WebbList = [];
        for yrow in self.Webb:
            for connections in yrow:
                for connection in connections:
                    WebbList.append(connection)
        return WebbList;
        
    def CalcNextEndPos(Node1Pos, )  
    
                
Webb = SpiderWebb(5, 5)
# Webb.Webb[0][0][0] = 3
# print (Webb.Webb[99][0][0])
Webb.InsertSpiderThread({'x':1, 'y':1}, {'x':1, 'y':2})
Webb.InsertSpiderThread({'x':1, 'y':1}, {'x':1, 'y':1})
#print (Webb.Webb)
Webb.ConvertWebbToList();