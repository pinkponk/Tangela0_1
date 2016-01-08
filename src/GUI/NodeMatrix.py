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
    #     StartPos = {'x': 3, 'y': 4}
    #     EndPos = {'x': 4, 'y': 5}
    def InsertSpiderThread(self, StartPos, EndPos):
        try:
          Xlength = abs(EndPos['x'] - StartPos['x'])
          Ylength = abs(EndPos['y'] - StartPos['y'])
          if (Xlength > 1 or Ylength > 1 or (Xlength == 0 and Ylength == 0)):
              raise ValueError('Invalid node connection. Xlength: ' + str(Xlength) + ", Ylength: " + str(Ylength));
          elif (StartPos['x'] < 0 or StartPos['x'] > (self.NodeXCount-1)):
              raise ValueError('Index out of bound. StartPos[''x'']: ' + StartPos['x']);
          elif (StartPos['y'] < 0 or StartPos['y'] > (self.NodeYCount-1)):
              raise ValueError('Index out of bound. StartPos[''y'']: ' + StartPos['y']);
          elif (EndPos['x'] < 0 or EndPos['x'] > (self.NodeXCount-1)):
              raise ValueError('Index out of bound. EndPos[''x'']: ' + EndPos['x']);
          elif (EndPos['y'] < 0 or EndPos['y'] > (self.NodeYCount-1)):
              raise ValueError('Index out of bound. StartPos[''x'']: ' + StartPos['x']);
          else: ## ALL OK
              self.__insert_spider_thread(StartPos, EndPos);
        except ValueError as e:
            print(str(e))
            print('Insert had no effect.')
          # self.Webb
          
    def __insert_spider_thread(self, StartPos, EndPos):
        x_dir = EndPos['x'] - StartPos['x'];
        y_dir = EndPos['y'] - StartPos['y'];
        if(x_dir > 0):
            if(y_dir < 0):
                self.Webb[StartPos['x']][StartPos['y']][SpiderWebb.rightup] = 1;
            elif(y_dir == 0):
                self.Webb[StartPos['x']][StartPos['y']][SpiderWebb.right] = 1;
            else:
                self.Webb[StartPos['x']][StartPos['y']][SpiderWebb.rightdown] = 1;
        elif(x_dir == 0):
            if(y_dir < 0):
                self.Webb[EndPos['x']][EndPos['y']][SpiderWebb.down] = 1;
            elif(y_dir == 0):
                raise ValueError('Same index of nodes.');
            else:
                self.Webb[StartPos['x']][StartPos['y']][SpiderWebb.down] = 1;
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
    
                
Webb = SpiderWebb(5, 5)
# Webb.Webb[0][0][0] = 3
# print (Webb.Webb[99][0][0])
Webb.InsertSpiderThread({'x':1, 'y':1}, {'x':1, 'y':2})
Webb.InsertSpiderThread({'x':1, 'y':1}, {'x':1, 'y':1})
#print (Webb.Webb)
Webb.ConvertWebbToList();