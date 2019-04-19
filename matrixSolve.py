#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 19:30:29 2019

@author: ralph
"""

import numpy as np

''' Here are some functions that do basic RREF steps to solve an augmented matrix'''

m0 = [[1,2,3],
     [4,5,6],
     [7,8,9]]

m1 = [[0,1,2,3],
      [0,0,4,5],
      [0,6,7,8]]

m2 = [[0,0,0,0],
      [0,0,0,0],
      [0,0,1,2],
      [0,0,0,1]]

m3 = [[0,3,-6,6,4,-5],
      [3,-7,8,-5,8,9],
      [3,-9,12,-9,6,15]]
#
#m4 = [['R4+R2+R3','-R3','R2+R3','0'],
#      ['-R3','R8+R7+R3+R1+R0','-R8-R7-R3','B0'],
#      ['R2+R3','-R3-R7-R8','R2+R3+R7+R8+R6+R5','0']]

#numMat = [[12.0, -4.0, 7.0, 0.0], 
#          [-4.0, 20.0, -13.0, -10.0], 
#          [7.0, -13.0, 21.0, 0.0]]

numMat = [[43.0, -10.0, 0.0, 8.0], 
          [-10.0, 32.0, 0.0, 6.0], 
          [0.0, 0.0, 47.0, 26.0]]

numMat = [[1.1234+1.0j,1.0-1.0j,1.0+2.0j,10.0],
          [1.0+3.0j,3.0-4.0j,5.0+1.0j,15.0],
          [5.0+1.0j,6.0-4.0j,8.0-3.0j,20.0]]

def firstLRNonzeroPos(m,prevPiv):
    pos = [-1,-1]# init
    I = len(m)
    J = len(m[0])
    for cnt in range(I*J):
        i = int(np.mod(cnt,I))
        j = int(np.floor((1.0*cnt/(1.0*I))))
        if i > prevPiv and j > prevPiv and m[i][j] != 0:
            pos = list([int(i),int(j)])
            break
    return pos


def exchangeRows(m,r0,r1):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if i == r0:
                temp = m[i][j]
                m[i][j] = m[r1][j]
                m[r1][j] = temp          
    return 

def replaceRow(m,repRow,multRow,mult):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if i == repRow:
                m[i][j] = m[i][j] + m[multRow][j] * mult
    return

def scaleRow(m,row,mult):
    for j in range(len(m[row])):# Go through each column of row row.
        m[row][j] = m[row][j]*1.0*mult
    return

def pivot2top(m,pos,prevPos):# move the pivot row to the top of the submatrix
    # containing the pivot. It starts at pivCol,pivCol.
    pivRow = -1
    choiceList = []
    for i in range(len(m)):
        if i > prevPos[0] and m[i][pos[1]] != 0:# prevPivRow, pivCol. Consider stuff at or below pivot
            choiceList.append(np.abs(m[i][pos[1]]))# pivCol. Choose the max
        else:
            choiceList.append((-1)*np.Infinity)# At a row above the pivot
    #print('choiceList = '+str(choiceList))
    Max = max(choiceList)
    #print('Max = '+str(Max))
    pivRow = choiceList.index(Max)
    #print('in p2t, pivRow = '+str(pivRow))
    exchangeRows(m,prevPos[0]+1,pivRow)# Bring pivot to top.
    pos = [prevPos[0]+1,pos[1]]# Next row, same column.
    return pos

def zerosBelowPivot(m,pos):
    pivot = 0.0
    for i in range(len(m)):
        below = 0.0
        factor = 0.0
        if i == pos[0]:# The row. Gets here before elif.
            pivot = m[i][pos[1]]# The column.
        elif i > pos[0]:# Row
            below = m[i][pos[1]]# Column
            factor = (-1.0*below/pivot)
            replaceRow(m,i,pos[0],factor) 
    return

def zerosAbovePivot(m,pos):
    pivot = 0.0
    rows = len(m)
    for i in range(rows):
        row =  rows - i - 1
        #print('row = '+str(row))
        above = 0.0
        factor = 0.0
        if row == pos[0]:
            pivot = m[row][pos[1]]
        elif row < pos[0]:
            above = m[row][pos[1]]
            factor = (-1.0*above/pivot)
            replaceRow(m,row,pos[0],factor)
    return

def scale(m,pivPosList):
    for pivPos in pivPosList:
        scaleRow(m,pivPos[0],1.0/m[pivPos[0]][pivPos[1]])# Divide row by pivot.
    return

def forwardPhaseRREF(m):
    pos = [-1,-1]# init
    prevPos = [-1,-1]
    pivPosList = []
    while True:
        pos = firstLRNonzeroPos(m,pos[1])
        #print('pos 0 = '+str(pos))
        if pos[1] == -1:
            break
        else:
            pos = pivot2top(m,pos,prevPos)
            pivPosList.append(list(pos))
            #print('pos 1 = '+str(pos))
            #display(m)
            zerosBelowPivot(m,pos)
            #display(m)
        prevPos = list(pos)# Update prev pos.
    return pivPosList

def reversePhaseRREF(m,pivPosList):
    pivs = len(pivPosList)
    for i  in range(pivs):
        #print(pivPosList[pivs-i-1])
        zerosAbovePivot(m,pivPosList[pivs-i-1])# Right to left.
    return

def RREF(m):
    pivPosList = forwardPhaseRREF(m)
    reversePhaseRREF(m,pivPosList)
    scale(m,pivPosList)
    return

def display(m):
    print
    spaceSize = 30
    for i in range(len(m)):
        displayStr = ''
        for j in range(len(m[i])):
            element = np.round(m[i][j],spaceSize/2)
            displayStr += str(element)
            for k in range(spaceSize - len(str(element))):
                displayStr += ' '
        print(displayStr)
    print
    return

#print(findLeftNonzeroCol(m2))
#m = numMat
#print(m)
#exchangeRows(m,0,2)
#pivCol = -1# Init.
#pivCol = findLeftNonzeroCol(m,pivCol)
#print('pivCol = '+str(pivCol))
#pivot2top(m,pivCol)
#zerosBelowPivot(m,pivCol)
#pivCol = findLeftNonzeroCol(m,pivCol)
#print('pivCol = '+str(pivCol))
#pivot2top(m,pivCol)
#zerosBelowPivot(m,pivCol)
#pivCol = findLeftNonzeroCol(m,pivCol)
#print('pivCol = '+str(pivCol))
#pivot2top(m,pivCol)
#zerosBelowPivot(m,pivCol)
#pivCol = findLeftNonzeroCol(m,pivCol)
#print('pivCol = '+str(pivCol))
#pivot2top(m,pivCol)
#zerosBelowPivot(m,pivCol)

#display(m)
#pivot2top(m,[1,0],[-1,-1])
#forwardPhaseRREF(m)
#zerosAbovePivot(m,1)
#print
#zerosAbovePivot(m,4)
#pivPosList = forwardPhaseRREF(m)

#zerosAbovePivot(m,pivPosList[-1])
#reversePhaseRREF(m,pivPosList)
#print(round((1.0/3),6))
#display(m)
#scaleRow(m,0,10)
#scale(m,pivPosList)
#RREF(m)

#print
#print(str([[m[i][j] for j in range(len(m[i]))] for i in range(len(m))]))
#print
#display(m)

#print(np.zeros([3,4],dtype = int))

#display(numMat)
#RREF(numMat)
#display(numMat)
#print np.round(5.123456j,3)
#import numpy as np

#print(np.round(4.7+8.3j))

#print(-0-0j == 0.0)
    
#m = [[1,-2,0,0,7,-3],
#     [0,1,0,0,-3,1],
#     [0,0,0,1,5,-4],
#     [0,0,0,0,0,0]]
#display(m)
#RREF(m)
#display(m)


    