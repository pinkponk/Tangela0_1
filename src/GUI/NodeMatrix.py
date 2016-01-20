#!/usr/bin/env python
import math
import numpy as np
'''
Created on 8 jan. 2016

@author: Gustav


SpiderWebb is a NodeYCount * NodeXCount * 4 matrix 
Each node has a connection to right up, right, right down, down ( 3 connections).

 0_ _ _ _ _ _ _ _ _ _ _ _n x-dir
0|_|_|_|_|_|_|_|_|_|_|_|_|
 |_|_|_|_|_|_|_|_|_|_|_|_|
 |_|_|_|_|_|_|_|_|_|_|_|_|
 |_|_|_|_|_|_|_|_|_|_|_|_|
 |_|_|_|_|_|_|_|_|_|_|_|_|
 |_|_|_|_|_|_|_|_|_|_|_|_|
n|_|_|_|_|_|_|_|_|_|_|_|_|
y-dir
'''

class SpiderWebb:
    rightup = 0;
    right = 1;
    rightdown = 2;
    down = 3;
    
    
    def __init__(self, NodeXCount, NodeYCount):
        self.NodeXCount = NodeXCount;
        self.NodeYCount = NodeYCount;
        self.Webb = np.zeros((NodeYCount, NodeXCount, 4));
    
    '''
    InsertSpiderThread
    input:
        StartPos = {'x': 3, 'y': 4}
        EndPos = {'x': 4, 'y': 5}
    output:
        SpiderPos after insert
    '''
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
              raise ValueError('Index out of bound. EndPos[''y'']: ' + EndPos['y']);
          else: ## ALL OK
              self.__insert_spider_thread(StartPos, EndPos);
              return EndPos;
        except ValueError as e:
            print(str(e))
            print('Insert had no effect.')
            return StartPos;
          
    def __insert_spider_thread(self, StartPos, EndPos):
        x_dir = EndPos['x'] - StartPos['x'];
        y_dir = EndPos['y'] - StartPos['y'];
        if(x_dir > 0):
            if(y_dir < 0):
                self.Webb[StartPos['y']][StartPos['x']][SpiderWebb.rightup] = 1;
            elif(y_dir == 0):
                self.Webb[StartPos['y']][StartPos['x']][SpiderWebb.right] = 1;
            else:
                self.Webb[StartPos['y']][StartPos['x']][SpiderWebb.rightdown] = 1;
        elif(x_dir == 0):
            if(y_dir < 0):
                self.Webb[EndPos['y']][EndPos['x']][SpiderWebb.down] = 1;
            elif(y_dir == 0):
                raise ValueError('Same index of nodes.');
            else:
                self.Webb[StartPos['y']][StartPos['x']][SpiderWebb.down] = 1;
        else:
            if(y_dir < 0):
                self.Webb[EndPos['y']][EndPos['x']][SpiderWebb.rightdown] = 1;
            elif(y_dir == 0):
                self.Webb[EndPos['y']][EndPos['x']][SpiderWebb.right] = 1;
            else:
                self.Webb[EndPos['y']][EndPos['x']][SpiderWebb.rightup] = 1;     
    
    def IsNodeConnected(WebbNode):
        if(WebbNode[0] == 1 or WebbNode[1] == 1 or WebbNode[2] == 1 or WebbNode[3] == 1):
            return True
        else:
            return False
    
    def ConvertWebbToList(self):
        WebbList = [];
        for yrow in self.Webb:
            for connections in yrow:
                for connection in connections:
                    WebbList.append(connection)
        return WebbList;

    '''
    Webb patterns used for testing
    '''
    def CreateSquarePattern(self):
        TopLeftCorner = {'x' : math.floor(self.NodeXCount/4), 'y' : math.floor(self.NodeYCount/4)};
        BottomLeftCorner = {'x' : math.floor(self.NodeXCount/4), 'y' : math.floor(self.NodeYCount*3/4)}
        BottomRightCorner = {'x' : math.floor(self.NodeXCount*3/4), 'y' : math.floor(self.NodeYCount*3/4)}
        TopRightCorner = {'x' : math.floor(self.NodeXCount*3/4), 'y' : math.floor(self.NodeYCount/4)}

        YLength = BottomLeftCorner['y'] - TopLeftCorner['y']        
        Xlength = TopRightCorner['x'] - TopLeftCorner['x']
        
        '''Insert top line'''
        for col in range(0, Xlength):
            StartPos = {'x': TopLeftCorner['x'] + col, 'y': TopLeftCorner['y']}
            EndPos = {'x': TopLeftCorner['x'] + col + 1, 'y': TopLeftCorner['y']}
            self.InsertSpiderThread(StartPos, EndPos)
        '''Insert bottom line'''
        for col in range(0, Xlength):
            StartPos = {'x': BottomLeftCorner['x'] + col, 'y': BottomLeftCorner['y']}
            EndPos = {'x': BottomLeftCorner['x'] + col + 1, 'y': BottomLeftCorner['y']}
            self.InsertSpiderThread(StartPos, EndPos)
        '''Insert Left vertical line'''
        for row in range(0, YLength):
            StartPos = {'x': TopLeftCorner['x'], 'y': TopLeftCorner['y']+ row}
            EndPos = {'x': TopLeftCorner['x'], 'y': TopLeftCorner['y']+ row + 1}
            self.InsertSpiderThread(StartPos, EndPos)
        '''Insert Right vertical line'''
        for row in range(0, YLength):
            StartPos = {'x': TopRightCorner['x'], 'y': TopRightCorner['y']+ row}
            EndPos = {'x': TopRightCorner['x'], 'y': TopRightCorner['y']+ row + 1}
            self.InsertSpiderThread(StartPos, EndPos)
    
    '''Requires the webb to be square'''
    def CreateCrossPattern(self):
        if(self.NodeXCount == self.NodeYCount):
            TopLeftCorner = {'x' : math.floor(self.NodeXCount/4), 'y' : math.floor(self.NodeYCount/4)};
            BottomLeftCorner = {'x' : math.floor(self.NodeXCount/4), 'y' : math.floor(self.NodeYCount*3/4)}
            BottomRightCorner = {'x' : math.floor(self.NodeXCount*3/4), 'y' : math.floor(self.NodeYCount*3/4)}
            TopRightCorner = {'x' : math.floor(self.NodeXCount*3/4), 'y' : math.floor(self.NodeYCount/4)} 
            
            YLength = BottomLeftCorner['y'] - TopLeftCorner['y']
            '''TopLeft to botton right'''
            for i in range(0,YLength):
                StartPos = {'x' : TopLeftCorner['x'] + i, 'y' : TopLeftCorner['y'] + i}
                EndPos = {'x' : TopLeftCorner['x'] + i + 1, 'y' : TopLeftCorner['y'] + i + 1}    
                self.InsertSpiderThread(StartPos, EndPos)
            '''BottomLeft to top right'''
            for i in range(0, YLength):
                StartPos = {'x' : BottomLeftCorner['x'] + i, 'y' : BottomLeftCorner['y'] - i}
                EndPos = {'x' : BottomLeftCorner['x'] + i + 1, 'y' : BottomLeftCorner['y'] - i - 1}
                self.InsertSpiderThread(StartPos, EndPos)
                
    
    def CreateCirclePattern(self, RadiusRatio):
        Top = {'x' : math.floor(self.NodeXCount/2), 'y': math.floor((self.NodeYCount/2)*(1-RadiusRatio))}
        Bottom = {'x': math.floor(self.NodeXCount/2), 'y': math.floor((self.NodeYCount/2)*(1-RadiusRatio))}
        Left = {'x': math.floor((self.NodeXCount*1/2)*(1-RadiusRatio)), 'y': math.floor(self.NodeYCount*1/2)}
        Right = {'x': math.floor((self.NodeXCount*1/2)*(1+RadiusRatio)), 'y': math.floor(self.NodeYCount*1/2)}
        
        
        YLength = Bottom['y'] - Top['y']        
        Xlength = Right['x'] - Left['x']
        
        Center = {'x': math.floor(self.NodeXCount/2), 'y': math.floor(self.NodeYCount/2)}
        
        '''Left top quarter'''
        '''x-dir = y-dir, y-dir = -x-dir'''
        StartPos = Left
        Stop = False
        while(StartPos['x'] != Top['x'] and StartPos['y']!=Top['y']):
            Dir = {'x': -(StartPos['y']-Center['y']), 'y': -(StartPos['x']-Center['x'])}
            length = math.sqrt(Dir['x']*Dir['x'] + Dir['y']*Dir['y'])
            Dir['x'] = Dir['x']/length
            Dir['y'] = Dir['y']/length
            Diag = {'x': math.sqrt(1/2),'y': -math.sqrt(1/2)}
            Diagscalar = Dir['x']*Diag['x'] + Dir['y']*Diag['y']
            deltaY = abs(Dir['y'])
            deltaX = abs(Dir['x'])
            deltaD = abs(Diagscalar)
            print('deltaY: ' + str(deltaY))
            print('deltaX: ' + str(deltaX))
            print('deltaD: ' + str(deltaD))
            if(deltaY > deltaX):
                if(deltaY > deltaD):
                    self.InsertSpiderThread(StartPos, {'x': StartPos['x'], 'y': StartPos['y'] - 1})
                    StartPos['y'] = StartPos['y'] - 1
                else:
                    self.InsertSpiderThread(StartPos, {'x': StartPos['x'] + 1, 'y': StartPos['y'] - 1})
                    StartPos['y'] = StartPos['y'] - 1
                    StartPos['x'] = StartPos['x'] + 1
            else:
                if(deltaX > deltaD):
                    self.InsertSpiderThread(StartPos, {'x': StartPos['x'] + 1, 'y': StartPos['y']})
                    StartPos['x'] = StartPos['x'] + 1
                else:
                    self.InsertSpiderThread(StartPos, {'x': StartPos['x'] + 1, 'y': StartPos['y'] - 1})
                    StartPos['y'] = StartPos['y'] - 1
                    StartPos['x'] = StartPos['x'] + 1
    '''
    input:  StartPos - {'x': n, 'y': h}
            DirectionWeightVector - [0.1, 0.3, 0.4, 0.12, 0.5, 0.9, 0.01]
    output: EndPos - {'x': n + t, 'y': h+g}
    
        |0|1|2|
        |7|x|3|
        |6|5|4|
    
    '''
    def CalcNextEndPos(StartPos, DirectionWeightVector):
        index = DirectionWeightVector.index(max(DirectionWeightVector))
        if index == 0:
            return {'x' : StartPos['x'] - 1, 'y' : StartPos['y'] - 1}
        elif index == 1:
            return {'x' : StartPos['x'], 'y' : StartPos['y'] - 1}
        elif index == 2:
            return {'x' : StartPos['x'] + 1, 'y' : StartPos['y'] - 1}
        elif index == 3:
            return {'x' : StartPos['x'] + 1, 'y' : StartPos['y']}
        elif index == 4:
            return {'x' : StartPos['x'] + 1, 'y' : StartPos['y'] + 1}
        elif index == 5:
            return {'x' : StartPos['x'], 'y' : StartPos['y'] + 1}
        elif index == 6:
            return {'x' : StartPos['x'] - 1, 'y' : StartPos['y'] + 1}
        elif index == 7:
            return {'x' : StartPos['x'] - 1, 'y' : StartPos['y']}
        else:
            raise ValueError('DirectionWeightVector size incorrect. DirectionWeightVector: ' + str(DirectionWeightVector));
            
class TestSpiderWebb:
    '''
    Test SpiderWebb
    '''
    def Test():
      Webb = SpiderWebb(5,5)
      StartPos = {'x': 0, 'y': 0}
      DirectionWeightVector = [0]*8
      for n in range(1,8):
        index = n-1
        DirectionWeightVector[index] = n
        EndPos = SpiderWebb.CalcNextEndPos(StartPos, DirectionWeightVector)
        Xdir = EndPos['x'] - StartPos['x']
        Ydir = EndPos['y'] - StartPos['y']
        if(index == 0 or index == 6 or index == 7):
          if(Xdir != -1):
            raise ValueError('Invalid output')
        elif(index == 1 or index == 5):
          if(Xdir != 0):
            raise ValueError('Invalid output')
        elif(index == 2 or index == 3 or index == 4):
          if(Xdir != 1):
            raise ValueError('Invalid output')
        
        if(index == 0 or index == 1 or index == 2):
          if(Ydir != -1):
            raise ValueError('Invalid output')
        elif(index == 7 or index == 3):
          if(Ydir != 0):
            raise ValueError('Invalid output')
        elif(index == 6 or index == 5 or index == 4):
          if(Ydir != 1):
            raise ValueError('Invalid output')
      
      Webb.CreateSquarePattern()
      
      print('All tests succeded!')
      
TestSpiderWebb.Test()      
