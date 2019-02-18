#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 20:15:31 2019

@author: ralph
"""
"""
ASSUMPTIONS:
1. Each component has a tag that starts with a letter to designate its 
type. Not case sensitive. B = battery. R = resistor.
2. Tags have the form XYZ...Z, where X is the type, Y is the rotation, 
such as N,E,S,W for north/0 rads, east/pi/2 rads, south/pi rads,(why clockwise?)
west/3pi/2 rads. And Z...Z is the component number such as R0,R1,R1,B1,B2 ect.

"""
from Tkinter import *

import numpy as np
#m = np.matrix([[1,2,3],[4,5,6],[7,8,9]])
#print m
#r = np.rot90(m)
#print r
#print np.sin(np.pi/2)

#rotMatrix = np.matrix([[np.cos, -1.0*np.sin],[np.sin, np.cos]])
#print rotMatrix

global leadSelection
#global leadSelection1
leadSelection = []
#leadSelection1 = []
global globalTagList
globalTagList = []
global globalValDict
globalValDict = {}# keys are components, values are component values, 
#ohms, volts ...
global masterEdgeList
masterEdgeList = []
global RESISTOR_SHAPE,BATTERY_SHAPE,CURRENT_SOURCE_SHAPE
#RESISTOR_SHAPE = [[0,40,10,40,15,45,25,35,35,45,
#                       45,35,55,45,65,35,70,40,80,40]]#horiontal
#RESISTOR_SHAPE = [[0.0, 40.0, 0.0, 50.0, -5.0, 55.0, #vertical
#                   5.0, 65.0, -5.0, 75.0, 5.0, 85.0,
#                   -5.0, 95.0, 5.0, 105.0, 0.0, 110.0,
#                   0.0, 120.0]]
RESISTOR_SHAPE = [[100.0, 140.0, 100.0, 150.0, 95.0, #vertical and offset to see better
                   155.0, 105.0, 165.0, 95.0, 175.0, 
                   105.0, 185.0, 95.0, 195.0, 105.0, 
                   205.0, 100.0, 210.0, 100.0, 220.0]]
#print([x+100 for x in RESISTOR_SHAPE[0]])
BATTERY_SHAPE = [[100,100,100,120],[80,120,120,120],[90,130,110,130],
                 [80,140,120,140],[90,150,110,150],[100,150,100,170],
                 [86,110,94,110],[90,106,90,114],[86,160,94,160]]
global RESISTOR_ENDPOINTS, BATTERY_ENDPOINTS
#RESISTOR_ENDPOINTS = [0,40,80,40]
RESISTOR_ENDPOINTS = [100,140,100,220]
BATTERY_ENDPOINTS = [100,100,100,170]

def createCanvas(master,width,height,bg):
    canvas = Canvas(master, width=width, height=height, bg=bg, closeenough=5)
    #canvas.pack()
    canvas.grid(column=0,row=0)
    return canvas

def addResistor(master):
    resistor = master.create_line(0,40,10,40,15,45,25,35,35,45,
                       45,35,55,45,65,35,70,40,80,40)
    return resistor

def addBattery(master,tag):
    
    #f = Frame(master, borderwidth=2, relief=RAISED)
    #c = Canvas(f,width = 100,height=100,bg='white')
    c = master
    c.create_line(100,100,100,120,tag = tag)# Bat
    c.create_line(80,120,120,120,tag = tag)
    c.create_line(90,130,110,130,tag = tag)
    c.create_line(80,140,120,140,tag = tag)
    c.create_line(90,150,110,150,tag = tag)
    c.create_line(100,150,100,170,tag = tag)
    
    c.create_line(86,110,94,110,tag = tag)#Plus
    c.create_line(90,106,90,114,tag = tag)
    
    c.create_line(86,160,94,160,tag = tag)#Minus
    #f.pack()
    #c.pack()
    
    return

def addComponent(master,shape,endpoints,tag):
    tag = tag.upper()
    for line in shape:
        master.create_line(line,tag=tag)
    #canvas.create_text(350,150, text='text', fill='yellow', font=('verdana', 36))
    #For text position
#    dx = endPoints[2] - endPoints[0]
#    dy = endPoints[3] - endPoints[1]
#    x = endPoints[0] + dy * 3.0/4.0
#    y = endPoints[1] + dx * 3.0/4.0
    
    dx = endpoints[2] - endpoints[0]
    dy = endpoints[3] - endpoints[1]
    x = endpoints[0] + (dx+dy)/2.0
    y = endpoints[1] + (dx+dy)/2.0
    
    text = tag#Remove the rotation direction
    text = text.replace('N','')
    text = text.replace('E','')
    text = text.replace('S','')
    text = text.replace('W','')  
    master.create_text(x,y,text=text, tag = tag)
    pi = np.pi
    rot = tag[1]
    if rot == 'N':
        pass
    elif rot == 'E':
        rotateComponent(master,tag,shape,endpoints,pi/2.0)
    elif rot == 'S':
        rotateComponent(master,tag,shape,endpoints,pi)
    elif rot == 'W':
        rotateComponent(master,tag,shape,endpoints,3.0*pi/2.0)
    return

def rotateResistor(master,resistor):
    ptList = master.coords(resistor)#[x0,y0,x1,y1,x2,y2,...]
    firstPt = [ptList[0],ptList[1]]
    rotPtList = []#A new list of points starting at (0,0) with the same shape.
    for i in range(len(ptList)):
        if divmod(i,2)[1] == 0:
            x = ptList[i]-firstPt[0]
            rotPtList.append(x)
        else:
            y = ptList[i]-firstPt[1]
            rotPtList.append(y)
    for j in range(len(rotPtList)/2):#Take points 2 at a time.
        swapX = rotPtList[2*j]
        swapY = rotPtList[2*j+1]
        rotPtList[2*j] = swapY + firstPt[0]#Switch x and y and add back the offset.
        rotPtList[2*j+1] = swapX + firstPt[1]
    newResistor = master.create_line(rotPtList)
    return newResistor

def rotateXYlist(xyList,radians):#rotate (clockwise?) relative to ref (??)
    refX = xyList[0]
    refY = xyList[1]
    newList = []#[x0,y0,x1,y1,...]
    for i in range(len(xyList)/2):#Assume the list has even length
        oldX = xyList[2*i] - refX
        oldY = xyList[2*i+1] -refY
        newX = round(np.cos(radians)*oldX - np.sin(radians)*oldY)
        newY = round(np.sin(radians)*oldX + np.cos(radians)*oldY)
        newList.append(newX+refX)
        newList.append(newY+refY)
    return newList

def locateCompEnds(master,tag):
    tag = tag.upper()#Make sure the tag is all caps, leave numbers alone
    coor = master.coords(tag)# end0 is here but not edn 1
    typeLetter = tag[0]
    rotLetter = tag[1]
    shapeEnds = []
    if  typeLetter== 'B':#alfabetical
        shapeEnds = BATTERY_ENDPOINTS
        
    elif typeLetter == 'R':
        shapeEnds = RESISTOR_ENDPOINTS
    else:
        pass
    pi = np.pi
    instanceOffset = []#The amount that the component end 0 is offset from the shape of it,
    #taking in to account the rotation of the compnent. Although, end 0 does not rotate.
    #instanceOffset1 = []#Offset of end 1 given the rotation.
    shapePos0 = []# The coords of the 0 end of the shape.
    shapePos1 = []# The [x,y] of the 1 end of the shape.
    instancePos0 = []# The [x,y] of the 0 end of the component instance.
    instancePos1 = []# [x,y] of the 1 end of the component instance.
    rotShapeEnds = []
    if rotLetter == 'N':
        rotShapeEnds = shapeEnds
        pass
    if rotLetter == 'E':
        rotShapeEnds = rotateXYlist(shapeEnds,pi/2.0)
    elif rotLetter == 'S':
        rotShapeEnds = rotateXYlist(shapeEnds,pi)
    elif rotLetter == 'W':
        rotShapeEnds = rotateXYlist(shapeEnds,3.0*pi/2.0)
    else:
        pass
    shapePos0 = [rotShapeEnds[0],rotShapeEnds[1]]
    shapePos1 = [rotShapeEnds[2],rotShapeEnds[3]]
    instancePos0 = [coor[0],coor[1]]
    instanceOffset = [instancePos0[0] - shapePos0[0],instancePos0[1] - shapePos0[1]]
    instancePos1 = [shapePos1[0] + instanceOffset[0], shapePos1[1] + instanceOffset[1]]
    #master.create_oval(instancePos0[0]-2,instancePos0[1]-2,instancePos0[0]+2,instancePos0[1]+2)
    #master.create_oval(instancePos1[0]-1,instancePos1[1]-1,instancePos1[0]+1,instancePos1[1]+1)
    return [instancePos0,instancePos1]

#print('lghR123G'.upper())
def rotateComponent(master,tag,shape,endpoints,radians):
    newEndpoints = []# Rotate endpoints appropriately.
    if tag[1] == 'N':
        newEndpoints = endpoints
    elif tag[1] == 'E':
        newEndpoints = rotateXYlist(endpoints,np.pi/2.0)
    elif tag[1] == 'S':
        newEndpoints = rotateXYlist(endpoints,np.pi)
    elif tag[1] == 'W':
        newEndpoints = rotateXYlist(endpoints,3*np.pi/2.0)
    else:
        print('in rotC, Tag Not Found')
        pass
    endpoints = newEndpoints
    ptList = master.coords(tag)#Returns some line from this component
    shapeOffset = [shape[0][0],shape[0][1]]#Some point in the shape to center on.
    realLifeOffset = [ptList[0],ptList[1]]#Some point in the component instance in use on the canvas.
    origenRefList = []#The list of lists of points with offset subtracted from each point.
    for i in range(len(shape)):#Subtract off the offset and create a new list, origenRefList.
        newLine = []
        for j  in range(len(shape[i])/2):
            newX = shape[i][2*j] - shapeOffset[0]
            newLine.append(newX)
            newY = shape[i][2*j+1] - shapeOffset[1]
            newLine.append(newY)
        origenRefList.append(newLine)
    rotList = []
    for i in range(len(origenRefList)):
        newLine = []
        for j in range(len(origenRefList[i])/2):
            oldX = origenRefList[i][2*j]
            oldY = origenRefList[i][2*j+1]
            newX = round(np.cos(radians)*oldX-np.sin(radians)*oldY)+realLifeOffset[0]
            newLine.append(newX)
            newY = round(np.sin(radians)*oldX+np.cos(radians)*oldY)+realLifeOffset[1]
            newLine.append(newY)
        rotList.append(newLine)      
    #Delete the old component.
    master.delete(tag)
    #Redraw the component.
    for line in rotList:
       # print(line)
        master.create_line(line,tag=tag)
        #print('line '+str(line))
    print
    #Set the text and compute the position.
    text = tag
    text = text.replace('N','')
    text = text.replace('E','')
    text = text.replace('S','')
    text = text.replace('W','')
    dx = endpoints[2] - endpoints[0]
    dy = endpoints[3] - endpoints[1]
    x = realLifeOffset[0] + (dx+dy)/2.0
    y = realLifeOffset[1] + (dx+dy)/2.0
    master.create_text(x,y,text = text, tag = tag)#Switch x and y, to rotate.
    #Now draw the rotated component.    
    return
#def moveResistor(event):
    #.move(resistor,50,50)
#root = Tk()
#canvasMain = createCanvas(root,1000,1000,'white')
#f = Frame(root, borderwidth=2, relief=RAISED)
#canvasMain.create_rectangle(405,10,500,105, outline='white', canvasMain.tag_bind('b1',sequence='<B1-Motion>',func=lambda event:(moveComponent(canvasMain,event,'b1')))
#fill='gray50')
#resistor0 = addResistor(canvasMain)

#resistor1 = addResistor(canvasMain)

#resistor2 = addResistor(canvasMain)
#resistor3 = rotateResistor(canvasMain,resistor2)

#addBattery(canvasMain,'b')

#B for battery, R for resistor, N,E,S,W for rotation, 0,1,2,3,.. as in R2 or B1
#addComponent(canvasMain,BATTERY_SHAPE,BATTERY_ENDPOINTS,'BN0')
#addComponent(canvasMain,RESISTOR_SHAPE,RESISTOR_ENDPOINTS,'RN0')
#addComponent(canvasMain,RESISTOR_SHAPE,RESISTOR_ENDPOINTS,'RE1')
#addComponent(canvasMain,RESISTOR_SHAPE,RESISTOR_ENDPOINTS,'RS2')
#addComponent(canvasMain,RESISTOR_SHAPE,RESISTOR_ENDPOINTS,'RW3')
#addComponent(canvasMain,BATTERY_SHAPE,BATTERY_ENDPOINTS,'BN0')
#addComponent(canvasMain,BATTERY_SHAPE,BATTERY_ENDPOINTS,'BE1')
#addComponent(canvasMain,BATTERY_SHAPE,BATTERY_ENDPOINTS,'BS2')
#addComponent(canvasMain,BATTERY_SHAPE,BATTERY_ENDPOINTS,'BW3')
#rotateComponent(canvasMain,'RN0',RESISTOR_SHAPE,RESISTOR_ENDPOINTS,0)
#rotateComponent(canvasMain,'RE1',RESISTOR_SHAPE,RESISTOR_ENDPOINTS,np.pi/2.0)
#rotateComponent(canvasMain,'RS2',RESISTOR_SHAPE,RESISTOR_ENDPOINTS,np.pi)
#rotateComponent(canvasMain,'RW3',RESISTOR_SHAPE,RESISTOR_ENDPOINTS,3.0*np.pi/2.0)
#canvasMain.move('RN0',500,500)
#canvasMain.move('RE1',500,500)
#canvasMain.move('RS2',500,500)
#canvasMain.move('RW3',500,500)


#rotateComponent(canvasMain,'BN0',BATTERY_SHAPE,BATTERY_ENDPOINTS,np.pi/2.0)
#canvasMain.move('b1',300,0)
#canvasMain.move('R4',300,100)
 
#rotateComponent(canvasMain,'b1',BATTERY_SHAPE,BATTERY_ENDPOINTS,np.pi)

#tag_bind(tagOrId, sequence=None, function=None, add=None)
#coords(item, x0, y0, x1, y1, ..., xn, yn)
def moveResistor(master,event,resistor):
    coor = master.coords(resistor)
    #mouse2resistorX = event.x - coor[0]
    #mouse2resistorY = event.y - coor[1]
    moveX = event.x - coor[0]
    moveY = event.y - coor[1]
    master.move(resistor,moveX,moveY)
    return

def moveComponent(master,event,tag):
    #tag = tag.capitalize()
    #print('in movC, tag = '+tag)
    coor = master.coords(tag)
    moveX = event.x - coor[0]
    moveY = event.y - coor[1]
    master.move(tag,moveX,moveY)
    return

def userCreateComponents(master,mouseDist):
    global globalTagList
    print('Input a list of component tags, such as RN0, BW1, etc.')
    usersCompStr = input()
   # print(usersCompStr)
    usersCompStr = usersCompStr.upper()
    usersCompList = usersCompStr.split(',')
    #print(usersCompList)
    for tag in usersCompList:
        tag = tag.upper()
        globalTagList.append(tag)# For storing tags to use create comp form.
        compType = tag[0]
        if compType == 'B':#Add the component.
            addComponent(master,BATTERY_SHAPE,BATTERY_ENDPOINTS,tag)
        elif compType == 'R':
            addComponent(master,RESISTOR_SHAPE,RESISTOR_ENDPOINTS,tag)
        else:
            pass
        master.tag_bind(tag,sequence='<B1-Motion>',#Allow to move comp around.
                            func=lambda event ,t = tag:(moveComponent(master,
                                                             event,t)))
    master.bind('<Double-Button-1>',#Allow making connections.
                    func=lambda event:(makeConnection(master,
                                                      event,usersCompList,
                                                      mouseDist)))      
    return usersCompList

def stripOrientationChar(usersCompList):
    compList = []
    for thick in usersCompList:
        thin = thick.replace('N','')
        thin = thin.replace('E','')
        thin = thin.replace('S','')
        thin = thin.replace('W','')
        compList.append(str(thin))
    return compList

def userSetCompVals(compList):
    global globalValDict
    compValList = []
    print('For each component, please give the value in the desired units.')
    for comp in compList:
        print(comp+'?')
        userStr = input()
        val = float(userStr)
        compValList.append(val)
        globalValDict[comp] = val
    print('Done with component value inputs.')
    return compValList
#userCreateComponents(canvasMain,10)

#moveComponent(canvasMain,4,'b')
#canvas.bind('<B1-Motion>',lambda event, c = canvas:
#    (c.move(resistor,event.x/100.0,event.y/100.0)))
#canvasR0.bind('<B1-Motion>',moveResistor)
    
#canvasMain.tag_bind(resistor0,sequence='<B1-Motion>' ,func=lambda event, master=canvasMain,r=resistor0:(moveResistor(master,event,r)))
#canvasMain.tag_bind(resistor1,sequence='<B1-Motion>' ,func=lambda event, master=canvasMain,r=resistor1:(moveResistor(master,event,r)))
#canvasMain.tag_bind(resistor2,sequence='<B1-Motion>' ,func=lambda event, master=canvasMain,r=resistor2:(moveResistor(master,event,r)))
#canvasMain.tag_bind(resistor3,sequence='<B1-Motion>' ,func=lambda event, master=canvasMain,r=resistor3:(moveResistor(master,event,r)))

#canvasMain.tag_bind('b',sequence='<B1-Motion>',func=lambda event:(moveComponent(canvasMain,event,'b')))
#canvasMain.tag_bind('RN0',sequence='<B1-Motion>',func=lambda event:(moveComponent(canvasMain,event,'RN0')))
#canvasMain.tag_bind('RE1',sequence='<B1-Motion>',func=lambda event:(moveComponent(canvasMain,event,'RE1')))
#canvasMain.tag_bind('RS2',sequence='<B1-Motion>',func=lambda event:(moveComponent(canvasMain,event,'RS2')))
#canvasMain.tag_bind('RW3',sequence='<B1-Motion>',func=lambda event:(moveComponent(canvasMain,event,'RW3')))
#
#canvasMain.tag_bind('BN0',sequence='<B1-Motion>',func=lambda event:(moveComponent(canvasMain,event,'BN0')))
#canvasMain.tag_bind('BE1',sequence='<B1-Motion>',func=lambda event:(moveComponent(canvasMain,event,'BE1')))
#canvasMain.tag_bind('BS2',sequence='<B1-Motion>',func=lambda event:(moveComponent(canvasMain,event,'BS2')))
#canvasMain.tag_bind('BW3',sequence='<B1-Motion>',func=lambda event:(moveComponent(canvasMain,event,'BW3')))


def makeWire(master,event,componentList,mouseDist):#bind to double click: <Double-Button-1>
    #print('got here -1')
    global leadSelection0,leadSelection1
    newEdge = []
    comp = -1#Component to connect to.
    pos = []#x,y for component 0.
    end = -1# 0 for first end of that component, 1 for second end.
    hit = False
    for component in componentList:
        coor = master.coords(component)
        compX0 = coor[0]
        compX1 = coor[-2]
        compY0 = coor[1]
        compY1 = coor[-1]
        if abs(event.x - compX0) < mouseDist and abs(event.y - compY0) < mouseDist:#mouse close to end 0
             comp = component
             pos = [compX0,compY0]
             end = 0
             #print('got here 0')
             hit = True
        elif abs(event.x - compX1) < mouseDist and abs(event.y - compY1) < mouseDist:
            comp = component
            pos = [compX1,compY1]
            end = 1
            #print('got here 1')
            hit = True
        else:
           pass
      
    if hit:
        if leadSelection0 == []:# First end of wire.
            leadSelection0 = [comp,pos,end]
        else:
            [comp0,pos0,end0] = leadSelection0
            leadSelection0 = []
            [comp1,pos1,end1] = [comp,pos,end]
            x0 = pos0[0]# x coord
            y0 =pos0[1] # y coord
            x1 = pos1[0]
            y1 = pos1[1]
            newEdge = [[comp0,end0],[comp1,end1]]
            master.create_line(x0,y0,x1,y1)
            print(newEdge)
    return newEdge

def makeConnection(master,event,tagList,mouseDist):
    global globalTagList
    global masterEdgeList
    #printDoubleClickCoords(master,event)
    #print('got here -1')
    global leadSelection
    tagList = globalTagList
    newEdge = []
    comp = ''#Component to connect to.
    pos = []#x,y for component 0.
    end = -1# 0 for first end of that component, 1 for second end.
    hit = False
    for component in tagList:# Identify each component by its tag.
        component = component.upper()
        [[compEnd0x,compEnd0y],[compEnd1x,compEnd1y]] = locateCompEnds(master,component)       
        if abs(event.x - compEnd0x) < mouseDist and \
            abs(event.y - compEnd0y) < mouseDist:#mouse close to end 0
             comp = component
             pos = [compEnd0x,compEnd0y]
             end = 0
             hit = True
        elif abs(event.x - compEnd1x) < mouseDist and \
            abs(event.y - compEnd1y) < mouseDist:
            comp = component
            pos = [compEnd1x,compEnd1y]
            end = 1
            hit = True
        else:
           pass
        #print
    if hit:
        if leadSelection == []:# First end of wire.
            leadSelection = [comp,pos,end]
            master.itemconfigure(tagOrId=comp,fill='red')
        else:
            [comp0,pos0,end0] = leadSelection#Last round
            leadSelection = []
            master.itemconfigure(tagOrId=comp0,fill='black')
            [comp1,pos1,end1] = [comp,pos,end]#This round
            if comp0 != comp1:#Do not allow connecting a component to itself.
                x0 = pos0[0]# x coord
                y0 =pos0[1] # y coord
                x1 = pos1[0]
                y1 = pos1[1]
                newEdge = [[comp0,end0],[comp1,end1]]
                #master.create_line(x0,y0,x1,y1)
                drawSquareWire(master,[x0,y0],[x1,y1])
                #print(newEdge)
                masterEdgeList.append(newEdge)
    return newEdge

def getComponentEndpoints(tag):
    endpoints = []
    letter = tag[0]
    #letter = letter.capitalize()
    if letter == 'B':
        endpoints = BATTERY_ENDPOINTS
    elif letter == 'R':
        endpoints = RESISTOR_ENDPOINTS
    else:
        print('In getComponentEndpoints - tag does not specify an ' +\
              'existing type of component.')
    return endpoints



def drawSquareWire(master,pt0,pt1):
    [x0,y0] = pt0
    [x1,y1] = pt1
    hvLine=[x0,y0,x1,y0,x1,y1]
    vhLine=[x0,y0,x0,y1,x1,y1]

    master.create_line(hvLine,fill='red',tag='redLine')#hor then vert
    master.create_line(vhLine,fill='blue',tag='blueLine')#vert then hor
    master.tag_bind('redLine',sequence='<Double-Button-1>',func=lambda event,
                    t='redLine',m=master,l=hvLine:(chooseSquareWire(m,event,t,l)))
    master.tag_bind('blueLine','<Double-Button-1>',func=lambda event,
                    t='blueLine',m=master,l=vhLine:(chooseSquareWire(m,event,t,l)))
    return

def chooseSquareWire(master,event,tag,line):
    otherTag = 'blueLine'
    if tag == 'blueLine':
        otherTag = 'redLine'
    elif tag == 'redLine':
        otherTag = 'blueLine'
    else:
        print('in cSW, else, tag = '+tag)
    #line = master.coords(otherTag)
    #line = l
#    master.delete(tag)
#    master.delete(otherTag)
    
    #print('tag = '+tag)
    #print('otherTag = '+otherTag)
    #print
    #print('line = '+str(line))
   # print('tag coords = '+str((master.coords(tag))))
    #print('otherTag coords '+str(master.coords(otherTag)))
    #print
    master.create_line(master.coords(otherTag))
    master.delete(tag)
    master.delete(otherTag)
    return

def printDoubleClickCoords(master,event):
    #master.create_text(x,y,text=tag, tag = tag)
    master.create_text(event.x,event.y,text=str((event.x,event.y)))
    return

def printMouseOverCoords():
    
    return

def addComputeButton(root,master,runFunc):
    buttonId = Button(master,text='Analyse Circuit')
    buttonId.grid()#in_=master)
    buttonId.bind(sequence='<Button-1>',func=runFunc)
    return

def addArrow(master,compTag,direction,currentNum,level):# Level is the number
    # of parrell arrows away from the component.
    colorList = ['black','brown','red','orange','yellow','green','blue','violet','gray','pink']
    endpoints = locateCompEnds(master,compTag)
    endpoints = [endpoints[0][0],endpoints[0][1],endpoints[1][0],endpoints[1][1]]
    #print('in aa, endpoints = '+str(endpoints))
    dx = abs(endpoints[2] - endpoints[0])
    dy = abs(endpoints[3] - endpoints[1])
#    moveBy = (dx+dy)/3.0
    # Start at the component endpoint 0 and make a shaft and 2 barbs.
    # Then rotate the correct amount.
    arrowLen = np.sqrt(dx*dx+dy*dy)# Hypotenuse of component
    # tail-------shaft---------->>barb>>
    barbFrac = 8.0 # The fraction of the arrow length that is the length of the barb.
    offset = arrowLen/barbFrac*level# the level of the parallel arrows.
    startX = endpoints[0]+2.0*dy/barbFrac+offset
    startY = endpoints[1]+2.0*dx/barbFrac+offset
    endX = startX
    endY = startY + arrowLen# Make the arrow straight down, then rotate.
    shaft = [startX,startY,endX,endY]
    barbY = endY - arrowLen/barbFrac
    barbLeftX = endX - arrowLen/barbFrac
    barbRightX = endX + arrowLen/barbFrac
    barb = [barbLeftX,barbY,endX,endY,barbRightX,barbY]# Up then down
    #The current number, text.
    textFrac = 12.0# Distance from arrow tail.
    textX = startX
    textY = startY - arrowLen/textFrac
    textPos = [textX,textY]
    # Rotate all lines about (startX,startY)
    shaft = [startX,startY] + shaft # Temporary. 
    barb = [startX,startY] + barb
    textPos = [startX,startY] + textPos
    #Determine the angle to rotate the arrow.
    color = ''
    angle = 0
    orientLetter = compTag[1].upper()
    if orientLetter == 'N' :
        color = 'red'
        angle = 0
        pass
    elif orientLetter == 'E' :
        color = 'yellow'
        angle = np.pi/2.0
    elif orientLetter == 'S':
        color = 'blue'
        angle = np.pi
    elif orientLetter == 'W':
        color = 'purple'
        angle = 3.0*np.pi/2.0
    # Rotate stuff by the correct angle.
    shaft = rotateXYlist(shaft,angle)
    barb = rotateXYlist(barb,angle)
    textPos = rotateXYlist(textPos,angle)
    # Strip the start position after rotating around it.
    shaft.pop(0)
    shaft.pop(0)
    barb.pop(0)
    barb.pop(0)
    textPos.pop(0)
    textPos.pop(0)
    # Filp ?
    if direction == [0,1]:#Defalt. Point from lead 0 to lead 1.
        pass
    elif direction == [1,0]:# Reverse the arrow direction.
        midX = (shaft[0] + shaft[2])/2.0
        midY = (shaft[1] + shaft[3])/2.0
        midPos = [midX,midY]
        angle = np.pi
        barb = rotateXYlist(midPos+barb,angle)
        shaft = rotateXYlist(midPos+shaft,angle)
        textPivot = [shaft[0],shaft[1]]# The tail of the arrow.
        textPos=rotateXYlist(textPivot+textPos,angle)
        # Strip the mid position after rotating around it.
        shaft.pop(0)
        shaft.pop(0)
        barb.pop(0)
        barb.pop(0)
        textPos.pop(0)
        textPos.pop(0)
    color = colorList[np.mod(currentNum,len(colorList))]
    master.create_line(shaft, fill=color)
    master.create_line(barb,fill=color)
    Id = master.create_text(textPos,text=str(currentNum))
#    master.itemconfigure(Id, fill = 'pink')
#    if direction == [0,1]:
#        master.create_line([newEnds[2],newEnds[3],newEnds[2]+(-dx+dy)/4.0,newEnds[3]+(dx-dy)/4.0])
#        master.create_line([newEnds[0],newEnds[1],newEnds[0]-(-dx+dy)/4.0,newEnds[1]-(dx-dy)/4.0])
    return

def arrowList2arrows(arrowList,compTagList,master):
    compDict = {}
    # compTag has the orientation character, comp does not.
    for compTag in compTagList:
        comp = str(compTag)
        comp = comp.replace('N','')# Remove the rotation direction letter.
        comp = comp.replace('E','')
        comp = comp.replace('S','')
        comp = comp.replace('W','')
        compDict[comp] = compTag
    for i in range(len(arrowList)):
        for j in range(len(arrowList[i])):
            [comp,direction,current] = arrowList[i][j]
            addArrow(master,compDict[comp],direction,current,current)
            
    return
    
#def pushit(event):
#    print('You pushed me.')
#    return
#locateCompEnds(canvasMain,'RN0')
#locateCompEnds(canvasMain,'RE1')
#locateCompEnds(canvasMain,'RS2')
#locateCompEnds(canvasMain,'RW3')
#r = RESISTOR_ENDPOINTS`
#print(r)
#print(rotateXYlist(r,np.pi/2))
#print(rotateXYlist(r,np.pi))
#print(rotateXYlist(r,3*np.pi/2))

#compList = [resistor0,resistor1,resistor2,resistor3]
#canvasMain.bind('<Double-Button-1>',func=lambda event,master=canvasMain,
#                componentList=compList,mouseDist=5:(makeWire(master,event,
#                              componentList,mouseDist)))
#tagList = ['RN0','RE1','RS2','RW3','BN0','BE1','BS2','BW3']
#canvasMain.bind('<Double-Button-1>',func=lambda event:(makeConnection(canvasMain,event,
 #                             tagList,5)))
#R0

#canvasMain.bind('<Double-Button-1>',func=lambda event:
#    (printDoubleClickCoords(canvasMain,event)))
#curList = 'BN0,RW0,RW1,RN2,RN3,RN4,RW5,RW6,RW7,RW8'
#curList = 'BN0,BN1,BS2,RE0,RE1,RE2,RN3'
#root.mainloop()
#print('masterEdgeList = '+str(masterEdgeList))

#[[['BN0', 0], ['RW0', 0]], [['RW0', 1], ['RW1', 0]], [['RW1', 1], 
#  ['RN2', 0]], [['RW1', 1], ['RN3', 0]], [['RN3', 1], ['RW7', 1]], 
#    [['RN2', 1], ['RN4', 0]], [['RN4', 1], ['RW7', 1]], [['RW7', 0], ['RW8', 1]], 
#    [['RW8', 0], ['BN0', 1]], [['RW6', 0], ['RW8', 0]], [['RW6', 1], ['RW5', 0]], 
#    [['RW5', 1], ['RN4', 0]]]