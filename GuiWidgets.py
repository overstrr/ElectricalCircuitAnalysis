#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 18:56:43 2019

@author: ralph
"""

import Tkinter as tk
import ttk
import circuitGui0 as gui0
import numpy as np

class newCompForm():
    # Class variables
    Type = ''
    Number = -1
    Orientation = ''
    OrientNum = -1.0
    OrientDenom = -1.0
    Angle = 0.0
    Tag = ''
    TakenNums = []
    Value = 0.0

def printData(event,dataList):
    if dataList != None:
        print
        for datum in dataList:
            print(datum.get())
#    print(dataList)
    return
# Radio button handlers do not need an event parameter.
#def handleCompChoice(var,master):
#    choiceStr = var.get()
#    newCompForm.Type = str(choiceStr)
#    orient = newCompForm.Orientation
#    orientChar = 'N'
#    if orient != '':
#        orientChar = orient[0]# First letter, N,E,S,W
#    num = newCompForm.Number
#    if num == -1:
#        num = 1
#        
#    
#    #print('in hCC, choiceStr = '+choiceStr)
#    # addComponent(master,RESISTOR_SHAPE,RESISTOR_ENDPOINTS,tag)
#    oldIdTup = master.find_all()# Remove any old components.
##    print('oldCompId = '+str(oldCompId))
##    print('oldCompId = '+str(oldIdTup))
#    if oldIdTup != ():
#        #print('oldCompId = '+str(oldCompId))
#        idList = list(oldIdTup)
#        for Id in idList:
#            master.delete(Id)
#    tag = 'noTag'
#    shape = []
#    endpoints = []
#    if choiceStr == 'Resistor':
#        tag = 'R'+str(orientChar)+str(num)
#        shape = gui0.RESISTOR_SHAPE
#        endpoints = gui0.RESISTOR_ENDPOINTS
#    elif choiceStr == 'Battery':
#        tag = 'B'+str(orientChar)+str(num)
#        shape = gui0.BATTERY_SHAPE
#        endpoints = gui0.BATTERY_ENDPOINTS
#    newCompForm.Tag = str(tag)
#    gui0.addComponent(master,shape,endpoints,tag)
#    #master.move(resistor,moveX,moveY)
#    coords = master.coords(tag)
#    master.move(tag,-coords[0],-coords[1])
##    c = tk.Canvas(master)
##    print('height = '+str(c.winfo_height()))
#    height = master.winfo_height()
#    width = master.winfo_width()
#    x = width/2.0 -abs(endpoints[2]-endpoints[0])/2.0
#    y  = height/2.0 - abs(endpoints[3]-endpoints[1])/2.0
#    master.move(tag,x,y)
#    # Reflect the component number.
#    if newCompForm.Number != -1:
#        tempVar = tk.StringVar()
#        tempVar.set(newCompForm.Number)
#        #handleCompNumChoice(tk.Event(),tempVar,maste - abs(endpoints[3]-endpoints[1])/2.0)
#    return

def centerComponent(master,endpoints,tag):
    coords = master.coords(tag)
    #print('coords = '+str(coords))
    #print('endpoints = '+str(endpoints))
    x0 = coords[0]# start of lead 0 x
    y0 = coords[1]# Start of lead 0 y
    x1 = x0 + endpoints[2]-endpoints[0]# x span of rotated component
    y1 = y0 + endpoints[3]-endpoints[1]# y span of rotated component
    midX = (x0+x1)/2.0
    midY = (y0+y1)/2.0
    master.move(tag,-midX,-midY)
    height = master.winfo_height()# height and width of the canvas itself
    width = master.winfo_width()
    #print('width = '+str(width))
    #print('height = '+str(height))
    x = width/2.0
    y  = height/2.0
    master.move(tag,x,y)
    return

#def handleCompNumChoice(event,var,master):
#    #print(var.get())
#    #print('newCompForm.Type = '+str(newCompForm.Type))
#    compNum = var.get()
#    compType = newCompForm.Type
#    shape = []
#    endpoints = []
#    compTypeChar = ''
#    if compType == 'Resistor':
#        compTypeChar = 'R'
#        shape = gui0.RESISTOR_SHAPE
#        endpoints = gui0.RESISTOR_ENDPOINTS
#    elif compType == 'Battery':
#        compTypeChar = 'B'
#        shape = gui0.BATTERY_SHAPE
#        endpoints = gui0.BATTERY_ENDPOINTS
#    if compType != '':
#        idTup = master.find_all()
#        idList = list(idTup)
#        labId = idList[-1]# The component label should be the last id.
#        #itemconfigure(item, *options)
#        #print('inhCNC, got here, labId = '+str(labId))
#        if compNum == '':# Make the component number 1 if blank
#            compNum = '1'
#         #gui0.addComponent(master,shape,endpoints,tag)
#        #master.itemconfigure(labId,text=compTypeChar+str(compNum))
#        master.delete(newCompForm.Tag)
#        #lab = compTypeChar+str(compNum)
#        orient = newCompForm.Orientation
#        if orient == '':
#            orient = 'North'
#        orientChar = orient[0]# First letter, N,E,S,W
#        tag = compTypeChar + orientChar + compNum
#        gui0.addComponent(master,shape,endpoints,tag)
#        centerComponent(master,endpoints,tag)
#    if compNum == '':# -1 means that the entry field is empty.
#        newCompForm.Number = -1
#    else:
#        newCompForm.Number = int(compNum)
#    return
#
## Radio button handlers do not need an event parameter.
#def handleCompOrientChoice(var,master):
#    orient = var.get()
#    newCompForm.Orientation = str(orient)
#    if newCompForm.Type != '':# If there is no component, just record and quit.
#        #rotateComponent(master,tag,shape,endpoints,radians)
#        typeChar = newCompForm.Type[0]# First letter of component type string.
#        num = newCompForm.Number
#        orientChar = orient[0]# First letter of orientation string.
#        #oldTag = str(typeChar)+str(num)# The old tag has no orientation character
#        newTag = str(typeChar)+str(orientChar)+str(num)
#        print('in hCOC, tag = '+str(newTag))
#        shape = []
#        endpoints = []
#        if typeChar == 'R':
#            shape = gui0.RESISTOR_SHAPE
#            endpoints = gui0.RESISTOR_ENDPOINTS
#        elif typeChar == 'B':
#            shape = gui0.BATTERY_SHAPE
#            endpoints == gui0.BATTERY_ENDPOINTS
#        angle = setAngle(orient,0.0,1.0)
#        gui0.rotateComponent(master,newTag,shape,endpoints,angle)
#         
#    
#    return

# Has side-effect of setting newCompForm.Angle.
def setAngle(orientation,numerator,denominator):
    angle = 0.0
    if orientation == 'Other':
        angle == float(numerator)*np.pi/float(denominator)
    else:
        if orientation == 'North' or orientation == 'N':
            angle = 0.0
        elif orientation == 'East' or orientation == 'E':
            angle = np.pi/2.0
        elif orientation == 'South' or orientation == 'S':
            angle = np.pi
        elif orientation == 'West' or orientation == 'W':
            angle == 3.0*np.pi/2.0
    newCompForm.Angle == float(angle)
    return angle



#def gotHere(var):
#    print('gotHere')
#    print(var.get())
#    return

def removeOldComp(master):
    oldIdTup = master.find_all()# Remove any old components.
    oldTag = ''
    hadOldComp = True
    if oldIdTup != ():
        #print('oldCompId = '+str(oldCompId))
        idList = list(oldIdTup)
        for Id in idList:# Remove part by part.
            #print('tag = '+str(master.itemcget(Id, option='tag')))
            oldTag = master.itemcget(Id, option='tag')
            master.delete(Id)
    else:
        hadOldComp = False
    #print('oldTag = '+oldTag)
    compTypeChar = ''
    orientChar = ''
    compNumStr = ''
    if oldTag != '':
        compTypeChar = oldTag[0]
        orientChar = oldTag[1]
        compNumStr = oldTag.strip(compTypeChar+orientChar)
    return [hadOldComp,compTypeChar,orientChar,compNumStr]

def changeComp(typeChar,orientChar,numStr,master):
    #newCompForm.Type = str(newType)
    #[hadOldComp,typeChar,orientChar,numStr] = removeOldComp(master)
#    if not hadOldComp:# Default values for the first time.
#        numStr = '1'
#        orientChar = 'N'
    num = int(numStr)
    tag = 'noTag'
    shape = []
    endpoints = []
    if typeChar == 'R':
        tag = 'R'+str(orientChar)+str(num)
        shape = gui0.RESISTOR_SHAPE
        endpoints = gui0.RESISTOR_ENDPOINTS
    elif typeChar == 'B':
        tag = 'B'+str(orientChar)+str(num)
        shape = gui0.BATTERY_SHAPE
        endpoints = gui0.BATTERY_ENDPOINTS
    newCompForm.Tag = str(tag)
    angle = 0.0
    if orientChar == 'N':
        angle = 0.0
    elif orientChar == 'E':
        angle = np.pi/2.0
    elif orientChar == 'S':
        angle = np.pi
    elif orientChar == 'W':
        angle = 3.0*np.pi/2.0
    gui0.addComponent(master,shape,endpoints,tag)
    endpoints = gui0.rotateXYlist(endpoints,angle)
    centerComponent(master,endpoints,tag)  
    return

def handleChange(event,var,change,master):
#    print
#    print('in hC')
#    print('event = '+str(event))
#    print('var.get() = '+str(var.get()))
#    print('change = '+change)
#    print('master = '+str(master))
#    print
    typeChar = ''
    numStr = ''
    orientChar = ''
    if newCompForm.Type == '':
        typeChar = 'R'
    else:
        typeChar = newCompForm.Type[0]
    if newCompForm.Number == -1:
        numStr = '1'
    else:
        numStr = str(newCompForm.Number)
    if newCompForm.Orientation == '':
        orientChar = 'N'
    else:
        orientChar = newCompForm.Orientation[0]        
    # Handle the case where some fields are full and others empty.
    changeValStr = var.get()
    if change == 'comp':
        newCompForm.Type = changeValStr
        typeChar = changeValStr[0]# R or B
    elif change == 'num':
        newCompForm.Number = int(changeValStr)
        numStr = changeValStr
    elif change == 'orient':
        newCompForm.Orientation = changeValStr
        orientChar = changeValStr[0]
    elif change == 'numerator':
        newCompForm.OrientNum = float(changeValStr)
    elif change == 'denom':
        newCompForm.OrientDenom = float(changeValStr)
    elif change == 'val':
        newCompForm.Value = float(changeValStr)
    removeOldComp(master)
    changeComp(typeChar,orientChar,numStr,master)
    return

def newComponentForm(master,bigCanv):
    borderWidth = 5
    fBig = tk.Frame(master,relief=tk.GROOVE,bd=borderWidth)#,bd=5,relief=tk.GROOVE)
    fBig.grid()
    

    fType = tk.Frame(fBig,relief=tk.GROOVE,bd=borderWidth)
    fType.grid(sticky=tk.E+tk.W)
    compTypeLab = tk.Label(fType,text='Component Type',bg='red')
    compTypeLab.grid(sticky=tk.E+tk.W)
    
    compType = tk.StringVar()
#    print(compType.set('3'))
    compList = ['Resistor','Battery']
    for comp in compList:
        typeRB = tk.Radiobutton(fType,text=comp,variable=compType,value=comp,
                                command=lambda : handleChange(tk.Event(),
                                                              compType,'comp',
                                                                  schemCanv))
        typeRB.grid(sticky=tk.W)
        compType.set('0')
    
    fNum = tk.Frame(fBig,relief=tk.GROOVE,bd=borderWidth)
    fNum.grid(sticky=tk.E+tk.W)
    compNumLab = tk.Label(fNum,text='Component Number',bg='blue')#,width=50,height=10,relief=tk.GROOVE)
    compNumLab.grid(sticky=tk.W+tk.E)
    
    compNum = tk.StringVar()
    compNumEntry = tk.Entry(fNum,textvariable=compNum)
    compNum.set('1')
    newCompForm.Number = 1
    compNumEntry.bind(sequence='<KeyRelease>',
                      func=lambda event:handleChange(event,
                                                            compNum,'num',
                                                            schemCanv))
    compNumEntry.grid(sticky=tk.W+tk.E)
    
    fOrient = tk.Frame(fBig,relief=tk.GROOVE,bd=borderWidth)
    fOrient.grid(sticky=tk.E+tk.W)
    compOrientLab = tk.Label(fOrient,text='Component Orientation',bg='orange')#,width=50,height=10,relief=tk.GROOVE)
    compOrientLab.grid(sticky=tk.W+tk.E)
   
    compOrient = tk.StringVar()
    orientList = ['North','East','South','West','Other']
    for orient in orientList:
        RB = tk.Radiobutton(fOrient,text=orient,variable=compOrient,
                            value=orient,
                            command=lambda : handleChange(tk.Event(),
                                                          compOrient,'orient',
                                                                    schemCanv))
        compOrient.set(0)
        RB.grid(sticky=tk.W)
     
    fAngle = tk.Frame(fOrient)
    fAngle.grid()
    
    numeratorText = tk.StringVar()
    numeratorEntry = tk.Entry(fAngle,textvariable=numeratorText,width=3)
    numeratorEntry.bind(sequence='<KeyRelease>',
                      func=lambda event:handleChange(event,numeratorText,
                                                     'numerator',
                                                     schemCanv))
    numeratorEntry.grid()
    numeratorText.set('0')
    
    fracBar = ttk.Separator(fAngle,orient=tk.HORIZONTAL)
    fracBar.grid(sticky=tk.E+tk.W)
    
    denomText = tk.StringVar()
    denomEntry = tk.Entry(fAngle,textvariable=denomText,width=3)
    denomEntry.bind(sequence='<KeyRelease>',
                    func=lambda event:handleChange(event,denomText,'denom',
                                                   schemCanv))
    denomText.set('1')
    denomEntry.grid()
#    numerator = float(numeratorText.get())
#    denom = float(denomText.get())
#    angle = numerator/denom
    
    fVal = tk.Frame(fBig,relief=tk.GROOVE,bd=borderWidth)
    fVal.grid(sticky=tk.W+tk.E)
    compValLab = tk.Label(fVal,text='Component Value',bg='yellow')#,width=50,height=10,relief=tk.GROOVE)
    compValLab.grid(sticky=tk.W+tk.E)
    
    compValText = tk.StringVar()
    compValEntry = tk.Entry(fVal,textvariable=compValText)
    compValEntry.bind(sequence='<KeyRelease>',
                      func=lambda event:handleChange(event,compValText,'val',
                                                     schemCanv))
    compValEntry.grid(sticky=tk.W+tk.E)

    fSchem = tk.Frame(fBig,relief=tk.GROOVE,bd=borderWidth)
    fSchem.grid()
    schemLab = tk.Label(fSchem,text='Schematic Diagram',bg='lightgreen')
    schemLab.grid(sticky=tk.W+tk.E)
    width = height = 160
    schemCanv = tk.Canvas(fSchem,bg='white',width=width,height=height)
    schemCanv.grid()#sticky=tk.N+tk.E+tk.S+tk.W)
    
    #data = [compType,compNum,compOrient,numeratorText,denomText,compValText]
    addCompButton = tk.Button(fBig,text='Add Component',
                              command=lambda : addComp(bigCanv))
    addCompButton.grid()
#    addCompButton.bind(sequence='<Button-1>',
#                       func=lambda event: printData(event,data))
    return [compType,compNum,compOrient,numeratorText,denomText,compValText]

def addComp(bigCanv):
    typeChar = str(newCompForm.Type[0])
    orientChar = str(newCompForm.Orientation[0])
    num = newCompForm.Number
    tag = typeChar+orientChar+str(num)
    shape = []
    endpoints = []
    if typeChar == 'R':
        shape = gui0.RESISTOR_SHAPE
        endpoints = gui0.RESISTOR_ENDPOINTS
    elif typeChar == 'B':
        shape = gui0.BATTERY_SHAPE
        endpoints = gui0.BATTERY_ENDPOINTS
    gui0.globalTagList.append(tag)
    thinTag = gui0.stripOrientationChar([tag])[0]
    gui0.globalValDict[thinTag] = newCompForm.Value
    #gui0.globalValDict[tag] = newCompForm.Value
    gui0.addComponent(bigCanv,shape,endpoints,tag)
    bigCanv.tag_bind(tag,sequence='<B1-Motion>',#Allow to move comp around.
                            func=lambda event ,t = tag:(gui0.moveComponent(bigCanv,
                                                             event,t)))
    return


#func=lambda event ,t = tag:(moveComponent(master,
#                                                             event,t)))
#buttonId.bind(sequence='<Button-1>',func=runFunc)
#root = tk.Tk()
#f = tk.Frame(root)
#f.grid()
#varList = newComponentForm(f)
##print('varList = '+str(varList))
#root.mainloop()

#gui0.addComponent(master,gui0.RESISTOR_SHAPE,gui0.RESISTOR_ENDPOINTS,'RE1')
#tk.StringVar()
#print(str(None))
#print
#for result in resultList:
#    print(result.)
#    print
#a = None
#print(a.__class__)
#def fun():
#    a = 10
#    b = a*c
#    c= 3
#    return
#fun()

