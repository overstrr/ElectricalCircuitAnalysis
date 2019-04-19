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

freq = 1000

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
    Prefix = ''
    
class voltageSource():
    def __init__(self,Vrms=0.0,freq=0.0,phase=0.0,lab=''):
        self.Vp = Vrms*np.sqrt(2.0)
        self.Vpp = 2.0*Vrms*np.sqrt(2.0)
        self.Vrms = Vrms
        self.freq = freq
        self.phase = phase
        self.rect = self.Vp*np.cos(self.phase)+1.0j*self.Vp*np.sin(self.phase)
        self.lab = lab
        return

def printData(event,dataList):
    if dataList != None:
        print
        for datum in dataList:
            print(datum.get())
#    print(dataList)
    return

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
    master.move(tag+'a',-midX,-midY)
    height = master.winfo_height()# height and width of the canvas itself
    width = master.winfo_width()
    #print('width = '+str(width))
    #print('height = '+str(height))
    x = width/2.0
    y  = height/2.0
    master.move(tag,x,y)
    master.move(tag+'a',x,y)
    return

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

def prefix2mult(prefixStr):
    prefix = prefixStr.upper()
    #print('in GW,p2m, prefix = '+str(prefix))
    mult = 1.0
    if prefix == 'TERA':
        mult = np.power(10.0,12.0)
    elif prefix == 'GIGA':
        mult = np.power(10.0,9.0)
    elif prefix == 'MEGA':
        mult = np.power(10.0,6.0)
    elif prefix == 'KILO':
        mult = np.power(10.0,3.0)
    elif prefix == 'UNIT':
        mult = 1.0
    elif prefix == 'MILLI':
        mult = np.power(10.0,-3.0)
    elif prefix == 'MICRO':
        mult = np.power(10.0,-6.0)
    elif prefix == 'NANO':
        mult = np.power(10.0,-9.0)
    elif prefix == 'PICO':
        mult = np.power(10.0,-12.0)
    return mult

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
#    shape = []
#    endpoints = []
    shapeObj = None
    if typeChar == 'R':
        tag = 'R'+str(orientChar)+str(num)
        #shape = gui0.RESISTOR_SHAPE
        #endpoints = gui0.RESISTOR_ENDPOINTS
        shapeObj = gui0.Shape.R
    elif typeChar == 'B':
        tag = 'B'+str(orientChar)+str(num)
        #shape = gui0.BATTERY_SHAPE
        #endpoints = gui0.BATTERY_ENDPOINTS
        shapeObj = gui0.Shape.B
    elif typeChar == 'L':
        tag = 'L'+str(orientChar)+str(num)
        shapeObj = gui0.Shape.L
    elif typeChar == 'C':
        tag = 'C'+str(orientChar)+str(num)
        shapeObj = gui0.Shape.C
    elif typeChar == 'V':
        tag = 'V'+str(orientChar)+str(num)
        shapeObj = gui0.Shape.V
    newCompForm.Tag = str(tag)
#    angle = 0.0
#    if orientChar == 'N':
#        angle = 0.0
#    elif orientChar == 'E':
#        angle = np.pi/2.0
#    elif orientChar == 'S':
#        angle = np.pi
#    elif orientChar == 'W':
#        angle = 3.0*np.pi/2.0
    #gui0.addComponent(master,shape,endpoints,tag)
    #print('orientChar = '+str(orientChar))
    rads = orientChar2rads(orientChar)
    #print('got to changeComp, after set rads = '+str(rads))
    gui0.addComponent2(master,shapeObj,tag,rads)
    endpoints = gui0.rotateXYList1(shapeObj.endpoints[0],shapeObj.endpoints[1],
                                   shapeObj.endpoints,rads)
    centerComponent(master,endpoints,tag)  
    return

def handleChange(event,var,change,master):
#    print('hC, got here')
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
        if changeValStr.isalpha():
            newCompForm.Type = changeValStr
            typeChar = changeValStr[0]# R or B
    elif change == 'num':
        if changeValStr.isdigit():
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
        val = 0.0
        try:
            val = complex(changeValStr)
        except:
            pass
        newCompForm.Value = val
    elif change == 'prefix':
        newCompForm.Prefix = str(changeValStr)
        #print('in GW,hC, prefix = '+str(changeValStr))
    val = newCompForm.Value    
#    if typeChar == 'L':
#                val = 2.0*np.pi*freq*val
#                newCompForm.Value = val
    #print('in hC, val = '+str(val))
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
    compList = ['Resistor','Battery','Inductor','Capacitor','Voltage Source']
    compChar = ['R','B','L','C','V']
    for comp in compList:
        typeRB = tk.Radiobutton(fType,text=comp,variable=compType,
                                value=compChar[compList.index(comp)],
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
    
    prefixChoice = tk.StringVar()
    prefixList = ['Tera','Giga','Mega','Kilo','unit','milli','micro','nano','pico']
    for prefix in prefixList:
        RB = tk.Radiobutton(fVal,text=prefix,variable=prefixChoice,
                            value=prefix,
                            command=lambda : handleChange(tk.Event(),
                                                          prefixChoice,'prefix',
                                                                    schemCanv))
        prefixChoice.set('unit')
        RB.grid(sticky=tk.W)

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
    #shape = []
    #endpoints = []
    shapeObj = None
    if typeChar == 'R':
        #shape = gui0.RESISTOR_SHAPE
        #endpoints = gui0.RESISTOR_ENDPOINTS
        shapeObj = gui0.Shape.R
    elif typeChar == 'B':
        #shape = gui0.BATTERY_SHAPE
        #endpoints = gui0.BATTERY_ENDPOINTS
        shapeObj = gui0.Shape.B
    elif typeChar == 'L':
        shapeObj = gui0.Shape.L
    elif typeChar == 'C':
        shapeObj = gui0.Shape.C
    elif typeChar == 'V':
        shapeObj = gui0.Shape.V
    gui0.globalTagList.append(tag)
    #print('GW,aC,global tag list = '+str(gui0.globalTagList))
    thinTag = gui0.stripOrientationChar([tag])[0]
    #print('thinTag = '+str(thinTag))
    #print('GW,aC,newCompForm.Type = '+str(newCompForm.Type))
    if newCompForm.Type[0] == 'L':
        gui0.globalValDict[thinTag] = newCompForm.Value*\
            prefix2mult(str(newCompForm.Prefix))*2.0*np.pi*freq*1.0j
        #print('GW,aC, got here '+str(gui0.globalValDict[thinTag]))
    elif newCompForm.Type[0] == 'C':
        try:
            gui0.globalValDict[thinTag] = -1.0j/(newCompForm.Value*\
                              prefix2mult(str(newCompForm.Prefix))*\
                              2.0*np.pi*freq)
            #print('in GW,aC, valDict = '+str(-1.0j/(newCompForm.Value*2.0*np.pi*freq)))
        except:
            pass
    else:
        gui0.globalValDict[thinTag] = newCompForm.Value*\
            prefix2mult(str(newCompForm.Prefix))
    #print('in GW,aC, newCompForm.Prefix = '+str(newCompForm.Prefix))
    #print('gui0.globalValDict : '+str(gui0.globalValDict[thinTag]))
    #gui0.globalValDict[thinTag] = gui0.globalValDict[thinTag] *\
        
    #print('globalValDict 2nd : '+str(gui0.globalValDict[thinTag]))
    #print('GW,aC,global val dict = '+str(gui0.globalValDict))
    #gui0.globalValDict[tag] = newCompForm.Value
    #gui0.addComponent(bigCanv,shape,endpoints,tag)
    gui0.addComponent2(bigCanv,shapeObj,tag,orientChar2rads(orientChar))
#    bigCanv.tag_bind(tag,sequence='<B1-Motion>',#Allow to move comp around.
#                            func=lambda event ,t = tag:(gui0.moveComponent(bigCanv,
#                                                             event,t)))
    bigCanv.tag_bind(tag,sequence='<B1-Motion>',#Allow to move comp around.
                            func=lambda event ,t = [tag,tag+'a']:(gui0.moveComponent(bigCanv,
                                                             event,t)))
    bigCanv.tag_bind(tag+'a',sequence='<B1-Motion>',#Allow to move comp around.
                            func=lambda event ,t = [tag,tag+'a']:(gui0.moveComponent(bigCanv,
                                                             event,t)))
    return

def orientChar2rads(orientChar):
    rads = 0.0
    if orientChar == 'N':
        rads = 0.0
    elif orientChar == 'E':
        rads = np.pi/2.0
        #print('east, rads = '+str(rads)+' : '+str(np.pi/2.0))
    elif orientChar == 'S':
        rads = np.pi
    elif orientChar == 'W':
        rads = 3.0*np.pi/2.0
    #print('in oC2r, rads = '+str(rads))
    return rads


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

gui0.globalTagList