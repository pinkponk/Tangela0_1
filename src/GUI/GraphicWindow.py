#!/usr/bin/env python
import math
import tkinter as Tk
from tkinter import Canvas, Button
from NodeMatrix import SpiderWebb



class GraphicWindow(Tk.Frame):
    SCREEN_DIMENSION = 700;
    AspecRatio = 1
    SCREEN_Height = round(SCREEN_DIMENSION)
    SCREEN_Width = round(AspecRatio*SCREEN_DIMENSION)
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.pack()
        self.start()
        
    def start(self):
        self.master.title("My Do-Nothing Application")
        #self.master.maxsize(GraphicWindow.SCREEN_Width, GraphicWindow.SCREEN_Height)
        self.pack(expand=1)

        
class WebbCanvas():
    sideoffset = 25
    
    def __init__(self):
        self.root = Tk.Tk()
        self.GraphicWindow = GraphicWindow(master=self.root)
        self.canvas = Canvas(self.GraphicWindow, width=GraphicWindow.SCREEN_Width, height=GraphicWindow.SCREEN_Height, bg="#000")
        self.canvas.pack();
        
    def Loop(self):
        self.root.mainloop()

    def PaintSpiderNodes(self, spiderWebb):
      NodeXCount = spiderWebb.NodeXCount
      NodeYCount = spiderWebb.NodeYCount;
      NodeXDistance = (GraphicWindow.SCREEN_Width - (2*WebbCanvas.sideoffset))/(NodeXCount)
      NodeYDistance = (GraphicWindow.SCREEN_Height - (2*WebbCanvas.sideoffset))/(NodeYCount)
      NodeXSize = NodeXDistance/4;
      NodeYSize = NodeYDistance/4;
      NextNodeXpos = WebbCanvas.sideoffset
      NextNodeYpos = WebbCanvas.sideoffset
      
      for yrow in spiderWebb.Webb:
        NextNodeXpos = WebbCanvas.sideoffset
        for SpiderNode in yrow:
          color = "blue"
          if(SpiderWebb.IsNodeConnected(SpiderNode)==True):
              color = "green"
              
          self.canvas.create_rectangle(NextNodeXpos, NextNodeYpos, NextNodeXpos+NodeXSize, NextNodeYpos+NodeYSize, fill=color)
          self.PaintConnectionSpiderNode(SpiderNode, NextNodeXpos + math.floor(NodeXSize/2), NextNodeYpos + math.floor(NodeYSize/2), NodeXDistance, NodeYDistance)
          NextNodeXpos += NodeXDistance
        NextNodeYpos += NodeYDistance
      self.root.update();
    
    def PaintConnectionSpiderNode(self, SpiderNode, NodeXCenterPos, NodeYCenterPos, NodeXDistance, NodeYDistance):
        '''UpRight'''
        if(SpiderNode[0]==1):
            self.canvas.create_line(NodeXCenterPos, NodeYCenterPos, NodeXCenterPos + NodeXDistance, NodeYCenterPos - NodeYDistance, fill="red")
        '''Right'''
        if(SpiderNode[1]==1):
            self.canvas.create_line(NodeXCenterPos, NodeYCenterPos, NodeXCenterPos + NodeXDistance, NodeYCenterPos + 0, fill="red")
        '''RightDown'''
        if(SpiderNode[2]==1):
            self.canvas.create_line(NodeXCenterPos, NodeYCenterPos, NodeXCenterPos + NodeXDistance, NodeYCenterPos + NodeYDistance, fill="red")
        '''Down'''
        if(SpiderNode[3]==1):
            self.canvas.create_line(NodeXCenterPos, NodeYCenterPos, NodeXCenterPos + 0, NodeYCenterPos + NodeYDistance, fill="red")
            
            
class TestWebbCanvas:
  '''
  Test SpiderCanvas
  '''
  def HandleClick(self):
    self.WebbPainter.PaintSpiderNodes(self.Webb)

  def Test(self):      
    self.WebbPainter = WebbCanvas()
    self.Webb = SpiderWebb(25,25)
    self.Webb.CreateSquarePattern()
    self.Webb.CreateCrossPattern()
    self.Webb.CreateCirclePattern(0.7)
    Button(self.WebbPainter.root, text='Show next webb', command=None).pack()
    self.WebbPainter.PaintSpiderNodes(self.Webb)
    self.WebbPainter.Loop()
 
  
TestObject = TestWebbCanvas()
TestObject.Test()

# from tkinter import Tk, Canvas, PhotoImage, mainloop
# from math import sin

# WIDTH, HEIGHT = 640, 480

# window = Tk()
# canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
# canvas.pack()
# img = PhotoImage(width=WIDTH, height=HEIGHT)
# canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

# for x in range(4 * WIDTH):
    # y = int(HEIGHT/2 + HEIGHT/4 * sin(x/80.0))
    # img.put("#ffffff", (x//4,y))

# mainloop()



# from Tkinter import *

# master = Tk()

# w = Canvas(master, width=200, height=100)
# w.pack()

# w.create_line(0, 0, 200, 100)
# w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

# w.create_rectangle(50, 25, 150, 75, fill="blue")

# mainloop()