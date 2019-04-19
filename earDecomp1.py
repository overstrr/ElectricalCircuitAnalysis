#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 20:00:24 2019

@author: ralph
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 16:02:21 2018

@author: ralph
"""
import numpy as np

class vertex():
    
    #label = ''# the name of the vertex
    #linked2 = []# list of vertices adjacent to self
    def construct(self,label,linked2):
        self.num = -1
        self.label = label
        self.linked2 = linked2
        self.polarityList = []
        self.parent = None# parent of self in a tree
        self.children = []
        self.descendants = [] #list of vertex objects that decend from self in a tree
        self.rootDist = np.Infinity
        self.compType = ''# type of component or component lead
        self.val = -1*np.Infinity# resistance, voltage, etc
        return
    def toString(self):
        #print('in toString, parent = '+str(self.parent))
        return str(self.label)
    
class edge():
    def makeInstanceVariables(self):
        self.num = -1
        self.endpointsStr = []
        self.endpointsObjs = []
        self.masterEdge = []
        return
    def toString(self):
        return str(self.endpointsStr)

masterEdgeList = [[['BN1', 1], ['RN3', 1]], 
                  [['RN3', 1], ['BS2', 0]], 
                  [['BS2', 1], ['RW2', 1]], 
                  [['BS2', 1], ['RW0', 1]], 
                  [['RW0', 0], ['BN0', 0]],
                  [['BN0', 1], ['BN1', 0]], 
                  [['RW1', 0], ['BN0', 1]], 
                  [['RW1', 1], ['RW2', 0]], 
                  [['RW2', 0], ['RN3', 0]]]

def makeNewEdgeList(oldEdgeList):#Input is an edge list from the circuit GUI. Output is a vertex  list.
    vlist = []
    elist = []
    for e in oldEdgeList:#Each edge has 2 vertices.
        firstVert = ''
        for v in e:
            tagStr = v[0]#Each vertex in the edge list is itself a list.
            tagStr = tagStr.upper()
            vStr = tagStr.replace('N','')# Remove the rotation direction letter.
            vStr = vStr.replace('E','')
            vStr = vStr.replace('S','')
            vStr = vStr.replace('W','')
            if vStr not in vlist:
                vlist.append(vStr)
                newV0 = '0'+vStr
                newV1 = '1'+vStr
                vlist.append(newV0)
                vlist.append(newV1)
                if vStr < newV0:# Alphabetize.
                    newEdge0 = [vStr,newV0]
                else:
                    newEdge0 = [newV0,vStr]
                if vStr < newV1:
                    newEdge1 = [vStr,newV1]
                else:
                    newEdge1 = [newV1,vStr]
                elist.append(newEdge0)
                elist.append(newEdge1)
            leadId = v[1]
            #if leadId == '0':
            newVert = str(leadId)+vStr
            if firstVert == '':
                firstVert = newVert
            else:
                elist.append([firstVert,newVert])
    return [vlist,elist]

def makeVobjsEobjs(V,E,root):# A graph search; makes a linked structure and sets
    #parents and children.
    #vdistlist = [-1 for i in V]
    #vdistlist[V.index(root)] = 0# The root is 0 distance from the root
    adjlist = adjacencyLists(V,E)
    vObjs = []# list of vertex objects. for each vertex label in V, there is a vObj in vObjs.
    eObjs = []# list of edges [v0Obj,v1Obj]
    for v in V:
        newV = enrollVertex(v,adjlist[V.index(v)],None,[])#label,adj,par,children
        vObjs.append(newV)
    #vObjs[V.index(root)].rootDist = 0
    marked = []
    Q = [root]
    while Q != []:
        v = Q.pop(0)
        marked.append(v)
        vIndex = V.index(v)# where v is in V
        for vprime in adjlist[V.index(v)]:# The adjacency list for v.
            if vprime not in marked:
                Q.append(vprime) 
                vprimeIndex = V.index(vprime)# where vprime is in V
                #dist = vdistlist[vprimeIndex] = vdistlist[vIndex] + 1# compute/record root distance
                #vObjs[vprimeIndex].rootDist = dist# store root distance in vertex object
                vObjs[vprimeIndex].parent = vObjs[vIndex]# store parent vertex object
                vObjs[vIndex].children.append(vObjs[vprimeIndex])# add to children list
                if V[vIndex] < V[vprimeIndex]:# Alphabetize edges.
                    eObjs.append(enrollEdge([vObjs[vIndex],vObjs[vprimeIndex]]))#strings
                else:
                    eObjs.append(enrollEdge([vObjs[vprimeIndex],vObjs[vIndex]]))
    return [vObjs,eObjs]
                
def enrollVertex(label,adjacents,parent,children):
    newV = vertex()
    newV.construct(label,adjacents)
    if parent == None:
       # print('in enrollVertex, got here')
        newV.parent = vertex()
        newV.parent.construct('None',[])
    else:
        newV.parent = parent
    #print('in enrollVertex, parent = '+str(newV.parent))
    newV.children = children  
    return newV

def enrollEdge(endpointsObjs):# endpointsObj here is a list of vertex objects [ob0,ob1]
    newE = edge()
    if endpointsObjs[0].label < endpointsObjs[1].label:
        newE.endpointsStr = [endpointsObjs[0].label,endpointsObjs[1].label]# Vertex labels
        newE.endpointsObjs = endpointsObjs
    else:
        newE.endpointsStr = [endpointsObjs[1].label,endpointsObjs[0].label]
        newE.endpointsObjs = [endpointsObjs[1],endpointsObjs[0]]#Vertex list, [vObj0,bObj1]
    return newE

def populateDescendants(cur):#start with the root. cur is the currant vertex
    descendantsList = []
    #print('in popD, cur.label = '+str(cur.label))
    if cur.children == []:# At a leaf. Send a list containing self.label
        return [cur.label]
    else:# Have some children. 
        for c in cur.children:# Visit each child.
            descendantsList = descendantsList + populateDescendants(c)# Collect all of children's decendants.
        cur.descendants = list(descendantsList)# Store self.descendants.
        #print('cur.label, '+str(cur.label)+' descendants = '+str(cur.descendants))
        descendantsList = descendantsList + [cur.label]# After storing, add self.label to the list.
        return list(descendantsList)# Send decendantsList to parent.

def makeWeightDict(edgeList):
    weightDict = {}
    #edgeCnt = len(edgeList)
    randList = [10, 4, 15, 5, 5, 14, 15, 10, 19, 20, 7, 19, 
                   2, 20, 13, 18, 7, 7, 17, 6, 14, 5, 3]
    for i in range(len(edgeList)):
        
        #print('test = '+str(np.random.randint(low=0,high=edgeCnt)))
        #weightDict[tuple([[1],[2]])]='test'
        #print('edg = '+str(edg))
        weightDict[tuple(edgeList[i])] = randList[i]
        #np.random.randint(low=0,high=edgeCnt)
    return weightDict

def Prims(V,wDict):# Takes a list of vertices and a matrix of the weights of edges.
    #print('V = '+str(V))
    T = list()# The edges of the tree to output.
    C = [set([v]) for v in V]# The list of sets of vertices in each subtree.
    cnt = 0
    maxcnt = 20
    while len(C) > 1:# Go until there is only one subtree.
        if cnt == maxcnt:
            break
        #print('len(C) = '+str(len(C)))
        Min = [np.Infinity for i in C]# A list of the minimum edge weight for prospect edges.
        shortest = [[] for i in C]# A list of lowest weight prospect edges.
#        for u in range(len(V)):# Search through each edge combination once.
#            for v in range(u):#The vertices are integers.
        #print
        for eTup in wDict.keys():
            edg = list(eTup)
            #print('edg = '+str(edg))
            #eTup = tuple(edg)
            #print('edg = '+str(edg)+' : eTup = '+str(eTup))
            i = 0#i and j are subtree indices.
            j = 0
            for s in range(len(C)):# Find the subgraph that V[u] and V[v] belong to.
                #print('V[u] = '+str(V[u])+', C[s] = '+str(C[s]))
                if edg[0] in C[s]:
                    i = s
                    #print('u,V[u],v,V[v],s,C[s] = '+str((u,V[u],v,V[v],s,C[s])))
                #print('V[v] = '+str(V[v])+', C[s] = '+str(C[s]))
                if edg[1] in C[s]:
                    j = s
            if i != j:# Sometimes V[u] and V[v] will be in the same subgraph.
                if wDict[eTup] < Min[i]:
                    Min[i] = wDict[eTup]
                    shortest[i] = edg
                if wDict[eTup] < Min[j]:
                    Min[j] = wDict[eTup]
                    shortest[j] = edg
        #print
    #print('shortest = '+str(shortest))
        Ctemp = list()# Assign the shortest edge to the correct subtree.
        setTemp = set([])
        #print
        #print('shortest = '+str(shortest))
        for s in range(len(C)):# Add one vertex from each shortest edge to the corresponding subtree.
            if shortest[s] not in T:
                #print('shortest[s] = '+str(shortest[s]))
                #print
                T.append(list(shortest[s]))# Record the new edge.
                #print('T = '+str(T))
                #print
            #Ctemp is a list of sets of vertices. Shortest[s] is an edge. To be clever,
            # the union of set(a) and set(a,b) is set(a,b), as desired. Here set(a,b) is a
            # set of vertices.
            setTemp = set.union(C[s],set(shortest[s]))
            if setTemp not in Ctemp:
                Ctemp.append(setTemp)#Add the union of the old vertex list for the subgraph and the new
                #vertex, to the list of subgraphs. Remove the old ones later.
        #mergedList = mergeSets(Ctemp)
        mergedList = mergeSets(Ctemp)
        C = list(mergedList)
        #print('len(C) = '+str(len(C)))
        cnt += 1     
    return T# Outputs a list of edges.

def mergeSets(oldSetList):#Takes a list of connected component vertex sets.
    oldList = list(oldSetList)
    workList = list(oldSetList)
    newList = []
    mergeList = [i for i in range(len(oldList))]#tells what to merge with what
    for i in range(len(oldList)):# Consider all combos of sets in oldList
        for j in range(i):
            if set.intersection(oldList[i],oldList[j]) != set([]):#non-empty intersection?
                mergeList[j] = mergeList[i]# merge position i to nothing, and pos j to i
    for i in range(len(mergeList)):
        iset = workList[i]# currant position
        setIndex = mergeList[i]# position of lower index, and location of unioned stuff
        unionS = set.union(iset,workList[setIndex])
        workList[mergeList[i]] = unionS# combine at lower index if different
        if i != mergeList[i]:# if the two sets are from different places, delete the old place.
            workList[i] = []
    for s in workList:
        if (s not in newList) and (s != []):
            newList.append(s)
    #print('newList = '+str(newList))
    return newList

def findDif(first,second):# [[a,b],[c,d]] -  [[a,b]] = [[c,d]]
    # alphabetize both lists of edges
    alphafirst = []
    alphasecond = []
    dif = []
    for e in first:
        e0 = e[0]
        e1 = e[1]
        if str(e0) > str(e1):
            alphafirst.append([e1,e0])
        else:
            alphafirst.append([e0,e1])
    for e in second:
        e0 = e[0]
        e1 = e[1]
        if str(e0) > str(e1):
            alphasecond.append([e1,e0])
        else:
            alphasecond.append([e0,e1])
    for e in alphafirst:
        if e not in alphasecond:
            dif.append(e)
    return dif

#
def adjacencyLists(V,E):# Given G(V,E), make a list of adjacent vertices for each vertex.
    aListList = []# A list of adjacency lists for each vertex
    for v in V:
        aList = []
        for e in E:
            if v == e[0]:
                aList.append(e[1])# v is e[0], so e[1] is adjacent to v
            elif v == e[1]:
                aList.append(e[0])
            else:
                pass
        aListList.append(list(aList))
            
    return aListList

# For each vertex in the spanning tree, set v.num to preorder dfs cnt.
def setPreorderNums(rootObj,cnt):# Recursive preorder depth first
    #cnt += 1
#    print(rootObj.toString())
#    print('cnt = '+str(cnt))
#    print
    rootObj.num = cnt# Set num
    #cnt += 1
    childList = list(rootObj.children)
    if childList != []:# At a leaf yet?
        for child in childList:
            cnt = setPreorderNums(child,cnt+1)
            #cnt += 1
    return cnt

def setNteEarNums(nteStrs,vStrs,vObjs):
    nteObjs = []
    for nteStr in nteStrs:
        vObj0 = vObjs[vStrs.index(nteStr[0])]
        vObj1 = vObjs[vStrs.index(nteStr[1])]
        nteObj = enrollEdge([vObj0,vObj1])
        lcaObj = lca(vObj0,vObj1)
        dist = lcaDist(lcaObj)
        nteObj.num = dist
        nteObjs.append(nteObj)
#    print('in sNEN, nteNums = ')
#    for nte in nteObjs:
#        print(nte.toString()+' : '+str(nte.num))
#    print
    nteObjs.sort(cmp=compareNteNums)
    for i in range(len(nteObjs)):
        nteObjs[i].num = i+1
#    print('in sNEN, nteNums = ')
#    for nte in nteObjs:
#        print(nte.toString()+' : '+str(nte.num))
#    print
    return nteObjs
    
def compareNteNums(nteObj0,nteObj1):
    if nteObj0.num < nteObj1.num:
        return -1
    else:
        return 1
    
def setNumsVertsIncidentNtes(nteObjs):
    vIncid = []
    for nteObj in nteObjs:# List all vertices that are incident of an nte.
        for i in [0,1]:
            vObj = nteObj.endpointsObjs[i]
            if vObj not in vIncid:
                vIncid.append(vObj)
#    print('in sNVIN, vObjs in vIncid ')
#    for vObj in vIncid:
#        print(vObj.label)
#    print
    for vObj in vIncid:# Update the incident vertex.num with min nte.num
        minNum = np.Infinity
        for nteObj in nteObjs:# Check each nte
            for i in [0,1]:# see if any of nte endpoints are vObj
                if nteObj.endpointsObjs[i] == vObj:
                    #print('in sNVIN, got here 0')
                    if nteObj.num < minNum:# find the min nte.num
                        minNum = nteObj.num
                        vObj.num = minNum # Update with the new min
    return

def setTreeEdgeNums(root,vStrs,vObjs,eObjs):
    eObjDict = {}
    for eObj in eObjs:# Id by endpoints. tuple(vObj,vObj'). Both orders accepted.
        eObjDict[(eObj.endpointsObjs[0],eObj.endpointsObjs[1])] = eObj
        eObjDict[(eObj.endpointsObjs[1],eObj.endpointsObjs[0])] = eObj
    def traverse(cur):#Traverse along the vertices of the spanning tree.
        descendantsNumList = [int(cur.num)]
        if cur.children == []:# Leaf
            return [int(cur.num)]
        else:# Not a leaf
            for child in cur.children:# List of child vertex objects
                childsDescs = traverse(child)# Child Vertex
                eObjDict[(cur,child)].num = int(min(childsDescs))# update edge.num
                descendantsNumList = descendantsNumList + childsDescs
            #cur.num = int(min(descendantsLabelList))
            return list(descendantsNumList)
    descNumList = traverse(root)
    print('descNumList = '+str(descNumList))
    return

def renumNte1(nteObjs):
    for nteObj in nteObjs:
        if nteObj.num == 1:
            nteObj.num = 0
            break
    return
    
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

# Also find the distance between the lca and the root.
#Lowest Common Ancestor.
def lca(uObj,vObj):#Supply 2 vertex objects of a tree with decendant lists.
    #uStr = uObj.label
    vStr = vObj.label
    lca = None
    # One of these vertices might : have no parent, or have no decendants.
    cur = uObj
    cnt = 0
    while cnt < 1000000:# runaway safe
        #print('cur = '+str(cur.label))
        if cur.parent.label == 'None':# At the root
            lca = cur
            break
        elif vStr in cur.descendants:# Is v a decendant of u or u's ancestor
            lca = cur# Stop. this is the lca
            break
        elif vStr == cur.label:#This allows a vertex to be its own ancestor (??)
            lca = cur
            break
        else:
            cur = cur.parent
        cnt += 1# runaway count
    
    return lca# Outputs a vertex object, the lowest common ancestor

# we already have the root dist, so this function is not needed.
def lcaDist(lca):# Find the distance between the lca and the root. Takes a vertex object.
    print('lca = '+lca.toString())
    d = 0 # Start distance at 0.
    cur = lca
    while True:
        if cur.parent.label == 'None':# At the root
            print('if, cur = '+cur.toString())
            break
        else:
            print('else, cur = '+cur.toString())
            cur = cur.parent
            d += 1 # Distance increases as we have travelled along another edge.
    print
    return d

#print(np.random.randint(low=0,high=10))
#print(tuple([1,2,3,4]))
[vStrList,eStrList] = makeNewEdgeList(masterEdgeList)
#print('vStrList = ')
#print
#print(vStrList)
#print
#print('eStrList = ')
#print
#print(eStrList)
#print
#print('weightDict = ')
#print
wDict = makeWeightDict(eStrList)
#print(wDict)
T = Prims(vStrList,wDict)
#print('len(T) = '+str(len(T)))
print
print('T =')
print
print(T)
nteStrs = findDif(eStrList,T)
print
print("nte's = "+str(nteStrs))
print
rootStr = vStrList[0]
[vObjs,eObjs] = makeVobjsEobjs(vStrList,T,rootStr)
#print('vObjs = ')
#for vObj in vObjs:
#    print(vObj.toString())
#print
#print('eObjs = ')
#for eObj in eObjs:
#    print(eObj.toString())
root = vObjs[0]
#print
#print('children = ')
#for vObj in vObjs:
#    print(vObj.toString()+' : '+str([child.toString() for child in vObj.children]))
#print
populateDescendants(root)
#print('descendants = ')
#print
#for vObj in vObjs:
#    print(vObj.toString()+' : '+str(vObj.descendants))
#print
#print('root = '+str(root.toString()))
#print(vObjs[3].toString()+' '+vObjs[6].toString())
#lcaV = lca(vObjs[3],vObjs[6])
#print(lcaV.toString())
#print
setPreorderNums(root,0)
#numList = []
#for vObj in vObjs:
#    print(vObj.toString()+' num = '+str(vObj.num))
#    numList.append(vObj.num)
#numList.sort()
#print('numList = '+str(numList))
##Note: The parent and children need to be set relative to the three,
## not the graph search function.
#print
#print('linked2 = ')
#for vObj in vObjs:
#    print(vObj.linked2)

# 

#print(lca(nte))
#print('len(eStrList) = '+str(len(eStrList)))
#print(list(np.random.randint(0,len(eStrList),size=len(eStrList))))
#print np.random.randint(low=0,high=10)
#print('parents = ')
#for vObj in vObjs:
#    print(vObj.toString()+' : '+str(vObj.parent.toString()))
#print
nteObjs = setNteEarNums(nteStrs,vStrList,vObjs)
print('nte ear nums = ')
for eObj in nteObjs:
    print(eObj.toString()+' : '+str(eObj.num))
setNumsVertsIncidentNtes(nteObjs)
print
print('vObjs after updating according to nte nums ')
for vObj in vObjs:
    print(vObj.toString()+' : '+str(vObj.num))
print
setTreeEdgeNums(root,vStrList,vObjs,eObjs)    
print
print('eObjs.num')
for eObj in eObjs:
    print(eObj.toString()+' : '+str(eObj.num))
print
renumNte1(nteObjs)
print('nteObjs.num = ')
for nteObj in nteObjs:
    print(nteObj.toString()+' : '+str(nteObj.num))


