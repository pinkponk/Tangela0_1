#!/usr/bin/env python

import tkinter as Tk
from tkinter import Canvas
# from tkinter import Tk, Canvas, PhotoImage, mainloop, Frame

SCREEN_DIMENSION = 700;
AspecRatio = 16/9
SCREEN_Height = round(SCREEN_DIMENSION)
SCREEN_Width = round(AspecRatio*SCREEN_DIMENSION)



class GraphicWindow(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.pack()
        self.start()
        
    def start(self):
        self.master.title("My Do-Nothing Application")
        self.master.maxsize(SCREEN_Width, SCREEN_Height)
        # self.pack(expand=1)

        
class PaintCanvas():
    def __init__(self, GraphicWindow=None):
        self.canvas = Canvas(GraphicWindow, width=SCREEN_Width, height=SCREEN_Height, bg="#000")
        self.canvas.pack();
        # self.canvas.create_line(0, 0, 200, 100)
        # self.canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
        # self.canvas.create_rectangle(50, 25, 150, 75, fill="blue")
        
    

 
 
 
root = Tk.Tk()
GW = GraphicWindow(master=root)
PC = PaintCanvas(GraphicWindow=GW)
GW.mainloop()


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