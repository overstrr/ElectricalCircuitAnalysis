#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 19:34:18 2019

@author: ralph
"""
import numpy as np


def polar(z):
    mag = np.abs(z)
    #print(mag)
    real = np.real(z)
    #print(real)
    imag = np.imag(z)
    #print(imag)
    if real != 0:
        angle = np.arctan(imag/real)
    elif imag > 0:
        angle = np.pi/2.0
    elif imag < 0:
        angle = -np.pi/20.
        
        
    print(str(angle/np.pi)+'*pi')
    
    #print(type(z))
    #print(np.absolute(z))
    
    return [mag,angle]

#print(polar(-0.9538756-1.8250323j))

(-0.9538756-1.8250323j)
#print(complex('(-0.9538756-1.8250323j)'))
#print np.log(np.power(np.e,1.0j*np.pi/4.0))
np.exp(5)

#class BasicShape():
#    def __init__(self,lines=[],arcBoxes=[],arcStart=0,arcExtent=0,ovalBoxes=[],
#                 polygons=[],rects=[],textPos=[],endpoints=[]):
#        self.lines = lines
#        self.arcBoxes = arcBoxes
#        self.arcStart = arcStart
#        self.arcExtent = arcExtent
#        self.ovalBoxes = ovalBoxes
#        self.polygons = polygons
#        self.rects = rects
#        self.textPos = textPos
#        self.endpoints = endpoints
#        return
#    
#class Shape():
#    R = BasicShape()
#    lines=[[100.0, 140.0, 100.0, 150.0, 95.0, 
#            155.0, 105.0, 165.0, 95.0, 175.0, 
#            105.0, 185.0, 95.0, 195.0, 105.0, 
#            205.0, 100.0, 210.0, 100.0, 220.0]]
#    textPos = [100+(220-140)/2.0,(140+220)/2.0]
#    endpoints=[100,140,100,220]
#    R.__init__(lines=lines,textPos=textPos,endpoints=endpoints)
#    B = BasicShape()
#    lines = [[100,100,100,120],[80,120,120,120],[90,130,110,130],
#             [80,140,120,140],[90,150,110,150],[100,150,100,170],
#             [86,110,94,110],[90,106,90,114],[86,160,94,160]]
#    textPos = [100+(150-100)/2.0,(100+150)/2.0]
#    endpoints = [100,140,100,220]
#    B.__init__(lines=lines,textPos=textPos,endpoints=endpoints)
#    L = BasicShape()
#    lines = [[100,100,100,110],
#             [100,110,105,110],
#             [100,120,105,120],
#             [100,130,105,130],
#             [100,140,105,140],
#             [100,150,105,150],
#             [100,150,100,160]]
#    arcBoxes = [[100,110,110,120],
#                [100,120,110,130],
#                [100,130,110,140],
#                [100,140,110,150]]
#    arcStart = -90
#    arcExtent = 180
#    textPos = [100+(160-100)/2.0,(100+160)/2.0]
#    endpoints = [100,100,100,160]
#    L.__init__(lines=lines,arcBoxes=arcBoxes,arcStart=arcStart,
#               arcExtent=arcExtent,endpoints=endpoints)
#    
    

    

#sq.crap = 4 
#print sq.crap

#print(super(square))


    


    
