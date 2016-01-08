#!/usr/bin/env python


class SpiderNode:
    # '''Class variable used to identify a node'''
    # '''Increments by one for each node created'''
    # nextNodeId = 0
    # input: index : {x: int, y: int} (index in node)
    x = 0
    y = 1
    
    
    def __init__(self, index):
        self.index = { 'x' : index['x'], 'y' : index['y']}
        self.neighbours = []
        
    