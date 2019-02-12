#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 16:02:21 2018

@author: ralph
"""
import numpy as np

class vertex():
    label = 0
    linked2 = []
    children = []
    def construct(self,label,linked2):
        self.label = label
        self.linked2 = linked2
    def toString(self):
        return 'vertex : '+str(self.label)+ \
        ' linked to '+str([self.linked2[i].label for i in range(len(self.linked2))])
class edge():
    endpoints = []
    
y = np.Infinity

De1 = [0] + [8,y,4,11,y,y,y,y,y]
De2 = [0,0] + [7,y,13,9,y,y,y,y]
De3 = [0,0,0] + [y,y,12,11,y,y,y]
De4 = [0,0,0,0] + [14,y,y,17,y,y]
De5 = [0,0,0,0,0] + [10,y,13,5,y]
De6 = [0,0,0,0,0,0] + [9,y,6,2]
De7 = [0,0,0,0,0,0,0] + [y,y,10]
De8 = [0,0,0,0,0,0,0,0] + [3,y]
De9 = [0,0,0,0,0,0,0,0,0] + [12]
De10= [0,0,0,0,0,0,0,0,0,0] + []

A = np.matrix([De1,De2,De3,De4,De5,De6,De7,De8,De9,De10])
B = np.matrix.transpose(A)
De = A+B
    
'''Turn an edge matrix, m, into an edge list'''
def matrix2list(m):
    edgeList = []
    for i in range(len(m)):
        for j in range(i):
            if m[i,j] != np.Infinity:
                edgeList.append([i,j])
    return edgeList

'''Turn an edge list into a linked graph.'''
def list2graph(edges):
    vList = []
    vObjs = []
    for e in edges:# Obtain a list of vertices
        if e[0] not in vList:
            vList.append(e[0])
            v0 = vertex()           #Make a new linked vertex, if needed.
            v0.construct(e[0],[])
            vObjs.append(v0)
        if e[1] not in vList:
            vList.append(e[1])
            v1 = vertex()           #Make a new linked vertex, if needed.
            v1.construct(e[1],[])
            vObjs.append(v1)
    #print(vList)
    #print([x.label for x in vObjs])
    vObjs.sort(cmp = compareVertexObj)# sort by label
    #print([x.label for x in vObjs])
    eObjs = []
    for e in edges:
        e0 = edge()#Make an edge object out e, which is a list of 2 integers.
        e0.endpoints = [vObjs[e[0]],vObjs[e[1]]]#List of vertex objects, assuming vertices are in order.
        if e0 not in eObjs:
            eObjs.append(e0)# Store new edge object.
            vObjs[e[0]].linked2.append(vObjs[e[1]])#Add vertex object at the other end of the edge.
            vObjs[e[1]].linked2.append(vObjs[e[0]])
    '''
    for v in vObjs:
        for j in range(len(v.linked2)):
            print v.linked2[j].label
        print
    for e in eObjs:
        print([e.endpoints[0].label,e.endpoints[1].label])
   '''
    return vObjs, eObjs

def compareVertexObj(x,y):
    if x.label < y.label:
        return -1
    else:
        return 1
'''
v1 = vertex()
v2 = vertex()
v2.construct(1,[v1])
v1.construct(0,[v2,v1])
print(v1.toString())
print(v2.toString())
'''
def manualTraverse(vStart):
    stop = False
    vCur = vStart
    while not stop:
        print('You are at vertex '+str(vCur.label))
        print('Would you like to continue? Answer 1 for yes and 0 for no.')
        answer0 = 5
        while answer0 != 1 and answer0 != 0:
            answer0 = input()
        if answer0 == 0:
            break
        print('You can go to vertices '+str([vCur.linked2[i].label for i in range(len(vCur.linked2))]))
        print('Where would you like to go?')
        answer1 = -np.Infinity
        #print('list = '+str([v.label for v in vCur.linked2]))
        while (answer1 not in [v.label for v in vCur.linked2]) or (answer1 == -np.Infinity):
            answer1 = input()
        for i in range(len(vCur.linked2)):
            #print('i = '+str(i))
            #print('len of vCur.linked2 = '+str(len(vCur.linked2)))
            if answer1 == vCur.linked2[i].label:
                vCur = vCur.linked2[i]
                break
    return

#print(list2graph(matrix2list(De)))
#x = input()
#print(x)
V,E = list2graph(matrix2list(De))
#print V
manualTraverse(V[0])
