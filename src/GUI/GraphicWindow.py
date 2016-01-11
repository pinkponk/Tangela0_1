#!/usr/bin/env python

import tkinter as Tk
from tkinter import Canvas, Button
from NodeMatrix import SpiderWebb



class GraphicWindow(Tk.Frame):
    SCREEN_DIMENSION = 700;
    AspecRatio = 16/9
    SCREEN_Height = round(SCREEN_DIMENSION)
    SCREEN_Width = round(AspecRatio*SCREEN_DIMENSION)
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.pack()
        self.start()
        
    def start(self):
        self.master.title("My Do-Nothing Application")
        self.master.maxsize(GraphicWindow.SCREEN_Width, GraphicWindow.SCREEN_Height)
        self.pack(expand=1)

        
class WebbCanvas():
    sideoffset = 25
    
    def __init__(self):
        self.root = Tk.Tk()
        self.GraphicWindow = GraphicWindow(master=self.root)
        self.canvas = Canvas(self.GraphicWindow, width=GraphicWindow.SCREEN_Width, height=GraphicWindow.SCREEN_Height, bg="#000")
        self.canvas.pack();
        
    def __Loop(self):
        self.root.mainloop()

    def PaintSpiderNodes(self, SpiderWebb):
      NodeXCount = SpiderWebb.NodeXCount
      NodeYCount = SpiderWebb.NodeYCount;
      NodeXDistance = (GraphicWindow.SCREEN_Width - (2*WebbCanvas.sideoffset))/(NodeXCount)
      NodeYDistance = (GraphicWindow.SCREEN_Height - (2*WebbCanvas.sideoffset))/(NodeYCount)
      NodeXSize = NodeXDistance/4;
      NodeYSize = NodeYDistance/4;
      
      NextNodeXpos = WebbCanvas.sideoffset
      NextNodeYpos = WebbCanvas.sideoffset
      
      for yrow in SpiderWebb.Webb:
        NextNodeXpos = WebbCanvas.sideoffset
        for xrow in yrow:
          self.canvas.create_rectangle(NextNodeXpos, NextNodeYpos, NextNodeXpos+NodeXSize, NextNodeYpos+NodeYSize, fill="blue")
          NextNodeXpos += NodeXDistance
        NextNodeYpos += NodeYDistance
      self.root.update();
class TestWebbCanvas:
  '''
  Test SpiderCanvas
  '''
  def HandleClick(self):
    self.WebbPainter.PaintSpiderNodes(self.Webb)

  def Test(self):      
    self.WebbPainter = WebbCanvas()
    self.Webb = SpiderWebb(5,5)
    Button(self.WebbPainter.root, text='Show next webb', command=HandleClick).pack()
    self.WebbPainter.__Loop()
    self.WebbPainter.PaintSpiderNodes(Webb)
 
  
 
 
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