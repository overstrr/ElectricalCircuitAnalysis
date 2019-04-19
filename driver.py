#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 08:00:43 2019

@author: ralph
"""

from circuitGui0 import *
from earDecomp import *
from stringEqns import *
from matrixSolve import *
from GuiWidgets import *

import numpy as np

#masterEdgeList = [[['BN1', 1], ['RN3', 1]], 
#                  [['RN3', 1], ['BS2', 0]], 
#                  [['BS2', 1], ['RW2', 1]], 
#                  [['BS2', 1], ['RW0', 1]], 
#                  [['RW0', 0], ['BN0', 0]],
#                  [['BN0', 1], ['BN1', 0]], 
#                  [['RW1', 0], ['BN0', 1]], 
#                  [['RW1', 1], ['RW2', 0]], 
#                  [['RW2', 0], ['RN3', 0]]]
#!!!ERROR-----2 batteries and a resistor all in parallel is not computed right.
# Or maybe this is indeterminate.
# It is indeterminant because the resistance is 0 so the current is infinite.
# If a cycle has 0 impedence and nonzero voltage source sums, tell user.

def makeCircuitSolveNumeric():
#    print('Be prepared to enter a circuit with labels and values.')
#    print
    # circuitGui0
    root = Tk()
    f0 = Frame(root)
    f0.grid()
    f1 = Frame(f0)
    f1.grid(row=0,column=0)
    f2 = Frame(f0)
    f2.grid(row=0,column=1)
    mouseDist = 10
    canvasMain = createCanvas(f1,1000,1000,'white',mouseDist)
    canvasMain.bind('<Double-Button-1>',#Allow making connections.
                    func=lambda event:(makeConnection(canvasMain,
                                                      event,globalTagList,
                                                      mouseDist)))
    #addComponent2(canvasMain,Shape.V,'VN1',0.0)
    #addComponent2(canvasMain,Shape.C,'CN1',np.pi)
    
    #addInductor(canvasMain,'L')
    
    #addComponent1(canvasMain,Shape().R,'RN5')
    
    #rotateComponent1(canvasMain,Shape.R,'RN5',0.0*3.0*np.pi/2.0)
    #addComponent2(canvasMain,Shape.B,'LW5',3.0*np.pi/2.0)
    #canvasMain = createCanvas(root,1000,1000,'white')
    if False:
        orientCompStrs = userCreateComponents(canvasMain,mouseDist)
        compStrs = stripOrientationChar(orientCompStrs)
        compVals = userSetCompVals(compStrs)
        print('compStrs = '+str(compStrs))
        print('compVals = '+str(compVals))
    #strEqnList = []
    #m = []
    def analyseCircuit(event):
        
        print(masterEdgeList)
        
        # Have a function here that is called by a button in circuitGui0.
        # earDecomp
        compStrs = []
        compVals = []
        for comp in globalValDict.keys():
            compStrs.append(comp)
            compVals.append(globalValDict[comp])
        print('compStrs = '+str(compStrs))
        print('compVals = '+str(compVals))
        e = masterEdgeList
        [v,e] = makeGraph(e)
        print('v = '+str(v))
        we = addWeights(e)
        m = weightedEdgeList2distMatrix(v,we)
        spanTree = Prims(v,m)
        nontreeEdgeList = findDif(e,spanTree)
        distlist,vObjs,eObjs = graphSearchDist(v,spanTree,v[0])
        populateDecendants(vObjs[0])
        eCycles = findCycleList(v,vObjs,eObjs,nontreeEdgeList)
        vCycleList = cycle2vObjsList(eCycles)
        arrows = setPolarities(v,vObjs,vCycleList)
        #  arrowList2arrows(arrowList,compTagList)
        #arrowList2arrows(arrows,orientCompStrs,canvasMain)
        arrowList2arrows(arrows,globalTagList,canvasMain)
        print
        print('arrows = '+str(arrows))
        print
        eqnList = eqStrWrite(vCycleList)
        strEqnList = list(eqnList)
        # stringEqns
        #compStrs = ['R0','R1','R2','R3','B0','B1','B2']
        #compVals = [47,22,33,10,12,6,8]
        print(eqnList)
        print
        strMat = strEqns2strMatrix(eqnList)
#        compVals = []
#        for comp in compStrs
        numMat = strMat2numMat(compStrs,compVals,strMat)
        print('numMat = ')
        print(numMat)
        # matrixSolve
        m = numMat
        display(m)
        RREF(m)
        display(m)
        compCurDict = makeCompCurDict(compStrs,v,vObjs,m,arrows)
        print('compCurDict = '+str(compCurDict))
        print
        compVoltDict = makeCompVoltDict(compCurDict,compStrs,compVals)
        print('compVoltDict = '+str(compVoltDict))
        #compCurDict = makeCompCurDict(m,compStrs,strEqnList,v,vObjs)
#        print
#        print('compCurDict = '+str(compCurDict))
#        print
        # Add stuff to the gui after computing
        #addArrow(master,compEnds,direction,currentNum)
#        for compStr in orientCompStrs:
#            direction = [0,1]
#            offset = 0
##            if compStr[0] == 'B':
##                direction = [1,0]
##                offset = 3
#            for i in range(4):
#                offset = i
#                direction = [np.mod(i,2),np.mod(i+1,2)]
#                addArrow(canvasMain,compStr,direction,i,offset)
        return 
    newComponentForm(f2,canvasMain)
    addComputeButton(root,f2,analyseCircuit)# Bind analyseCir to computeButton
#    noval = Pmw.EntryField(root, labelpos=W, label_text='No validation',
#validate = None)
#    e = StringVar()
#    Entry(f2, width=40, textvariable=e).grid(row=1,column=1)
#    e.set("'A shroe! A shroe! My dingkom for a shroe!'")
#    
#    var = IntVar()
#    f3 = Frame(f2,borderwidth=2,relief=GROOVE,bg='red')
#    f3.grid(row=2,column=2)
#    for text, value in [('Passion fruit', 1), ('Loganberries', 2),
#        ('Mangoes in syrup', 3), ('Oranges', 4),
#        ('Apples', 5),('Grapefruit', 6)]:
#        Radiobutton(f2, text=text, value=value, variable=var).grid(column=1)
#    var.set(3)
    #addComputeButton(root,canvasMain,analyseCircuit)
    #makeCompCurDict(numMat,compStrs,compVals,strEqnList)

   
    root.mainloop()
    
    return

#print(bytes('r'))
#list(bytearray('abc'))
#print('abc'.encode())

makeCircuitSolveNumeric()

someEdges = [[['BN0', 0], ['RE1', 1]], 
             [['RE1', 1], ['RE2', 1]], 
             [['RE2', 0], ['RE7', 0]], 
             [['RE1', 0], ['RE4', 1]], 
             [['RE4', 0], ['RE7', 1]], 
             [['RE7', 0], ['BS1', 1]], 
             [['BN0', 1], ['RE5', 1]], 
             [['RE5', 0], ['BS1', 0]], 
             [['RN3', 1], ['RE5', 1]], 
             [['RN6', 1], ['RE5', 0]], 
             [['RE1', 0], ['RN3', 0]], 
             [['RN6', 0], ['RE7', 1]]]

#print(np.complex.conjugate(4+5j))

