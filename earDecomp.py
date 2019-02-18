#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 16:02:21 2018

@author: ralph
"""
import circuitGui0 as cg
import numpy as np
# I don't understand step 5. It seems that there can only be one master
# edge for the whole graph. ??
'''Jobs needed to accomplish ear decomposition:'''
#1. Take the edge list from the circuit GUI and add edges and vertices
#   for the component itself, and to connect the component leads to the
#   component one both sides. (makeGraph)

#2. Add weights to each edge. The first edge can be weighted 1, the next one
#   2, and so on till the last edge. (addWeights)

#3. Find spanning tree and output the edge list of the tree. (Prims)

#4. Determine, for each edge uv that is not part of the tree, the distance
#   between the root and the lowest common ancestor of u and v.
#
#   4a.  Assign a root and assign distances of each vertex from the root.
#        Use the graph search algorithm to assign distances. (graphSearchDist)
#
#   4b.  Make a function to determine lowest common ancestors given 4a.
#        Find the distance between the lca and the root. (lowestCommonAncestor)
#        (lcaDist, v.rootDist, findDif)
#
#5. For each edge uv that is part of the tree, find the corresponding
#   "master edge", a non-tree edge wx such that the cycle formed by 
#   adding wx to the tree passes through uv and such that, among such edges,
#   w and x have a lowest common ancestor that is as close to the root as 
#   possible (with ties broken by edge identifiers).
#
#   5a. For a given edge uv, find each non-tree edge, wx, that forms a 
#       cycle passing through uv.
#
#   5b. For each set of non-tree edges, such as wx, in 5a, find the one
#       with the lowest (as close to the root as possible) 
#       lowest common ancestor.
#
#   5c. Add a master attribute to the edge class. For each tree edge,
#       set the master edge attribute.

#6. Form an ear for each non-tree edge, consisting of it and the tree edges
#   for which it is the master, and order the ears by their master edges'
#   distance from the root (with the same tie braking rule).

class vertex():
    
    #label = ''# the name of the vertex
    #linked2 = []# list of vertices adjacent to self
    def construct(self,label,linked2):
        self.label = label
        self.linked2 = linked2
        self.polarityList = []
        self.parent = None# parent of self in a tree
        self.children = []
        self.decendants = [] #list of vertex objects that decend from self in a tree
        self.rootDist = np.Infinity
        self.compType = ''# type of component or component lead
        self.val = -1*np.Infinity# resistance, voltage, etc
        return
    def toString(self):
        #print('in toString, parent = '+str(self.parent))
        return str(self.label)
class edge():
    def makeInstanceVariables(self):
        self.endpointsStr = []
        self.endpointsObjs = []
        self.masterEdge = []
        return
    def toString(self):
        return str(self.endpointsStr)

#e=[[['BN0', 0], ['RW0', 0]], [['RW0', 1], ['RW1', 0]], 
#   [['RW1', 1], ['RN2', 0]], [['RW1', 1], ['RN3', 0]], 
#   [['RN3', 1], ['RW7', 1]], [['RN2', 1], ['RN4', 0]], 
#   [['RN4', 1], ['RW7', 1]], [['RW7', 0], ['RW8', 1]], 
#   [['RW8', 0], ['BN0', 1]], [['RW6', 0], ['RW8', 0]], 
#   [['RW6', 1], ['RW5', 0]], [['RW5', 1], ['RN4', 0]]]
#
#e=[[['BN0', 0], ['RE0', 1]],
#   [['BN0', 1], ['BN1', 0]], 
#   [['BN1', 1], ['RN3', 1]], 
#   [['RN3', 1], ['BS2', 0]], 
#   [['BS2', 1], ['RE2', 0]], 
#   [['RN3', 0], ['RE2', 1]], 
#   [['RN3', 0], ['RE1', 0]], 
#   [['RE1', 1], ['BN0', 1]], 
#   [['RE0', 0], ['RE2', 0]]]

#a = vertex()
#b = vertex()
#a.children = [0]
#b.children = [1]
#
#print(a.children == b.children)

#1.

def makeGraph(oldEdgeList):#Input is an edge list from the circuit GUI. Output is a vertex  list.
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
                newEdge0 = [vStr,newV0]
                newEdge1 = [vStr,newV1]
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

def addWeights(edgeList):
    weightedList = []
    cnt = 0
    for e in edgeList:
        weightedList.append([e,cnt])
        cnt = cnt + 1
    return weightedList

def weightedEdgeList2distMatrix(vList,weightElist):
    row = [np.Infinity for i in range(len(vList))]
    rows = [list(row) for i in range(len(vList))]
    m = np.matrix(rows)
    #print('m = '+str(m))
    vDict = {}# Dictionary, keys are vertex strings, values are indices in the distance matrix.
    #weightList = []
    #indexVlist = []# A list of vertices and their index in the distance matrix.
    cnt = 0
    for v in vList:
        #indexVlist.append([v,cnt])
        vDict[v] = cnt
        cnt +=1
    for item in weightElist:
        e = item[0]# Unpacking.
        v0 = e[0]
        v1 = e[1]
        w = item[1]
        index0 = vDict[v0]
        index1 = vDict[v1]
        m[index0,index1] = w
        m[index1,index0] = w
    return m# Outputs a distance matrix

def displayMatrix(m,v):# Takes a matrix, m, and a vertex list, v.
    space = '   '#  spaces
    _space = '___'
    pipeSpace = ' | '
    print # Top seperator
    for i in [-1]+range(len(m)):# Num rows + the vertex label
        rowStr = ''
        for j in [-1]+range(len(m)):#Square matrix, so num columns + vertex label.
            weightStr = ''
            weight = np.Infinity
            if i == -1 and j == -1:
                weightStr = space
            elif i == -1:# left vertical vertex labels
                weightStr = str(v[j])
                #print('got here i, v[j] = |'+str(v[j])+'|')
            elif j == -1:# top horizontal vertex labels
                weightStr = str(v[i])
            else:
                weight = m[i,j] # the distance of the edge.
                lowerTriangle = i > j
                #lowerTriangle = True
                if weight != np.Infinity and lowerTriangle:# Remove the inf's, lower triangle,
                    weightStr = str(int(round(weight)))# Get rid of the .0's .
                else:
                    if np.mod(i,3) == 2:
                        weightStr = _space
                    elif np.mod(i,3) == 1 and np.mod(j,3) == 2:
                        weightStr = pipeSpace
                    else:
                        weightStr = str(space)
            rowStr += weightStr# Add the weights.
            for k in range(len(space)-len(weightStr)):
                if np.mod(i,3) == 2:
                    rowStr += '_'
                else:
                    rowStr += ' '
            if np.mod(i,3) == 2:
                rowStr += '_'
            else:
                rowStr += ' '
        print(rowStr)
    print# Bottom seperator.
    return

def Prims(V,De):# Takes a list of vertices and a matrix of the weights of edges.
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
        for u in range(len(V)):# Search through each edge combination once.
            for v in range(u):#The vertices are integers.
                i = 0#i and j are subtree indices.
                j = 0
                for s in range(len(C)):# Find the subgraph that V[u] and V[v] belong to.
                    #print('V[u] = '+str(V[u])+', C[s] = '+str(C[s]))
                    if V[u] in C[s]:
                        i = s
                        #print('u,V[u],v,V[v],s,C[s] = '+str((u,V[u],v,V[v],s,C[s])))
                    #print('V[v] = '+str(V[v])+', C[s] = '+str(C[s]))
                    if V[v] in C[s]:
                        j = s
                if i != j:# Sometimes V[u] and V[v] will be in the same subgraph.
                    if De[u,v] < Min[i]:
                        Min[i] = De[u,v]
                        shortest[i] =[V[v],V[u]]
                    if De[u,v] < Min[j]:
                        Min[j] = De[u,v]
                        shortest[j] = [V[v],V[u]]
        #print('shortest = '+str(shortest))
        Ctemp = list()# Assign the shortest edge to the correct subtree.
        setTemp = set([])
        for s in range(len(C)):# Add one vertex from each shortest edge to the corresponding subtree.
            if shortest[s] not in T:
                T.append(list(shortest[s]))# Record the new edge.
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

def graphSearchDist(V,E,root):# Run graph search assign distances to vertices from root.
    vdistlist = [-1 for i in V]
    vdistlist[V.index(root)] = 0# The root is 0 distance from the root
    adjlist = adjacencyLists(V,E)
    vObjs = []# list of vertex objects. for each vertex label in V, there is a vObj in vObjs.
    eObjs = []# list of edges [v0Obj,v1Obj]
    for v in V:
        newV = enrollVertex(v,adjlist[V.index(v)],None,[])#label,adj,par,children
        vObjs.append(newV)
    vObjs[V.index(root)].rootDist = 0
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
                dist = vdistlist[vprimeIndex] = vdistlist[vIndex] + 1# compute/record root distance
                vObjs[vprimeIndex].rootDist = dist# store root distance in vertex object
                vObjs[vprimeIndex].parent = vObjs[vIndex]# store parent vertex object
                vObjs[vIndex].children.append(vObjs[vprimeIndex])# add to children list
                if V[vIndex] < V[vprimeIndex]:# Alphabetize edges.
                    eObjs.append(enrollEdge([vObjs[vIndex],vObjs[vprimeIndex]]))#strings
                else:
                    eObjs.append(enrollEdge([vObjs[vprimeIndex],vObjs[vIndex]]))
    return vdistlist,vObjs,eObjs
                
    #print('vOrder = '+str(vOrder))
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
    newE.endpointsStr = [endpointsObjs[0].label,endpointsObjs[1].label]# Vertex labels
    newE.endpointsObjs = endpointsObjs#Vertex list, [vObj0,bObj1]
    return newE

'''Turn an graph, G(V,E) into a linked graph.'''
def list2graph(vertices,edges):
    #vList = []
    #vObjs = []
    eObjs = []# list of edge objects
    vObjsDict = {}#keys are vertex strings, values are vertex objects
    for v in vertices:
        vOb = vertex()
        vOb.construct(v,[])#label,linked2
        vObjsDict[v] = vOb
    for e in edges:
        eOb = edge()#Make an edge object out of e, which is a list of 2 vertices.
        #e0.endpoints = [vObjs[e[0]],vObjs[e[1]]]#List of vertex objects, assuming vertices are in order.
        eOb.endpointsObjs = [vObjsDict[e[0]],vObjsDict[e[1]]]
        if eOb not in eObjs:
            eObjs.append(eOb)# Store new edge object.
            vObjsDict[e[0]].linked2.append(vObjsDict[e[1]])#Add vertex object at the other end of the edge.
            vObjsDict[e[1]].linked2.append(vObjsDict[e[0]])
            
    return vObjsDict.values(), eObjs

def compareVertexObj(x,y):
    if x.label < y.label:
        return -1
    else:
        return 1
    
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
    
def populateDecendants(cur):#start with the root. cur is the currant vertex
    decendantsList = []
    #print('in popD, cur.label = '+str(cur.label))
    if cur.children == []:# At a leaf. Send a list containing self.label
        return [cur.label]
    else:# Have some children. 
        for c in cur.children:# Visit each child.
            decendantsList = decendantsList + populateDecendants(c)# Collect all of children's decendants.
        cur.decendants = list(decendantsList)# Store self.decendants.
        #print('cur.label, '+str(cur.label)+' decendants = '+str(cur.decendants))
        decendantsList = decendantsList + [cur.label]# After storing, add self.label to the list.
        return list(decendantsList)# Send decendantsList to parent.

# Also find the distance between the lca and the root.
def lowestCommonAncestor(uObj,vObj):#Supply 2 vertex objects of a tree with decendant lists.
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
        elif vStr in cur.decendants:# Is v a decendant of u or u's ancestor
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
    d = 0 # Start distance at 0.
    cur = lca
    while True:
        if cur.parent.label == 'None':# At the root
            break
        else:
            cur = cur.parent
            d += 1 # Distance increases as we have travelled along another edge.
    return d



def findCycle(V,vObjs,edgeObj,nteStr):#Takes a tree edge object and 
    #a non tree edge list of string names of vertices, ['v0','v1'].
    #cycle = []# The output. Contains the cycle of vertex objects 
    #we are looking for if possible. Or empty otherwise.
    # Given a list of strings, ['v0','v1'], enroll a vertex objects.
#    nteObj = None# non-tree edge object.
    
#    if nteStr[0] < nteStr[1]:# Alphabetize. Make edge
#        nteObj = enrollEdge([vObjs[V.index(nteStr[0])],vObjs[V.index(nteStr[1])]])
#    else:
#        nteObj = enrollEdge([vObjs[V.index(nteStr[1])],vObjs[V.index(nteStr[0])]])
    vObjsWork = []
    for vObj in vObjs:# a copy of vObjs with all new objects.
        new = enrollVertex(str(vObj.label),list(vObj.linked2),None,[])
        vObjsWork.append(new)
        
#    for i in range(len(vObjsWork)):
##        print(vObjsWork[i] is vObjs[i])
##        print(vObjsWork[i] == vObjs[i])
##        print(vObjsWork[i],vObjs[i])
#        print(vObjsWork[i].linked2 is vObjs[i].linked2)
    #ntev0 = edgeObj.endpointsObjs[0].label# First vertex string
    #ntev1 = edgeObj.endpointsObjs[1].label# Second vertex string
    ntev0 = nteStr[0]# the label of non-tree edge[0], the first vertex
    ntev1 = nteStr[1]# the label of the second vertex, non-tree edge[1]
#    for vObj in vObjs:
#        print('in fC before, vObj.label = '+str(vObj.label))
#        print('adjacents = '+str([vStr for vStr in vObj.linked2]))
#        print
    vObjsWork[V.index(ntev0)].linked2.append(ntev1)# Add the nte vertices 
                                                   # to the adjacency lists.
    vObjsWork[V.index(ntev1)].linked2.append(ntev0)
#    for vObj in vObjs:
#        print('in fC after, vObj.label = '+str(vObj.label))
#        print('adjacents = '+str([vStr for vStr in vObj.linked2]))
#        print
        
#    print('ntev0 = '+str(ntev0))
#    print('ntev1 = '+str(ntev1))
#    print('added linked2, = '+str(vObjsWork[V.index(ntev0)].linked2))
#    print('added linked2, = '+str(vObjsWork[V.index(ntev1)].linked2))
    # Traverse the graph from the edge[0] vertex depth first.
    # Maintain a path list of vertices from edge[0] to each currant vertex.
    # If the path list contains any vertex twice, stop. That is a cycle. 
    # If the cycle contains edge[0] and edge[1], and if it contains edge[0]
    # twice, that is the cycle we are looking for. findMaster will determine that.
    # If the process ends without finding a cycle, it should still end. But, 
    # this should not happen.
    # 
    # how to go in a circle when children is in one direction only???
    def traverse(prev,cur,startVert,partner,pathVerts,pathEdges):# Recursive
        #print('cur.label = '+str(cur.label))
        retVal = []
        paths = []
        #print('pathEdges top = '+str([e.endpointsStr for e in pathEdges]))
        #print('pathVerts top = '+str([v.label for v in pathVerts]))
        tempPathVerts = list(pathVerts)# Use for calc and discard.
        for vObj in pathVerts:# Detect any cycle
            #print('tempPathVerts, before = '+str([v.label for v in tempPathVerts]))
            tempPathVerts.remove(vObj)
            #print('tempPathVerts, after = '+str([v.label for v in tempPathVerts]))
            if vObj in tempPathVerts:# Does tempPathVerts contain vObj twice?
                # Found some cycle. Break for loop.
                
# Somehow we need to store all possible cycles, not just the first found.
# But, how many cycles can there be? I thought only one.                
                
                if vObj == startVert and partner in tempPathVerts:# must pass through both.
                    # The cycle we want. And the master edge
                                     # is nontreeEdge./ maybe not ?
                    #print('pathEdges if = '+str([e.endpointsStr for e in pathEdges]))
                    #return pathEdges
                    if pathEdges not in paths:
                        paths.append(pathEdges)# Store all the possible cycles going
                                           # through startVert.
                    if len(paths) > 1:
                        print('in traverse, paths = '+str(paths))
                    return pathEdges
                                
                else:# A cycle but, not the one we want.
                   # print('got to first else')
                    return [] # This tree edge has a master edge different from
                              # nontreeEdge.
                    pass
                
            else:# Not yet a cycle.
                tempPathVerts.append(vObj)# Else put back vObj and continue for loop.
                #print('got to second else')
        # Not yet cycle. Record and traverse.
        # go through adjacentcy list, not child list.
        for adjStr in cur.linked2:# Need depth first. Go to each child in turn.
            adjObj = vObjsWork[V.index(adjStr)]
            if adjObj != prev:# If just been that way, don't go that way
                pathVerts.append(adjObj)
                if cur.label < adjObj.label:# Alphabetize. Create new edges. should(?)
                    #pathEdges.append(enrollEdge([cur,adjObj]))
                    pathEdges.append(enrollEdge([vObjs[V.index(cur.label)],
                                                       vObjs[V.index(adjObj.label)]]))
                else:
                    #pathEdges.append(enrollEdge([adjObj,cur]))
                    pathEdges.append(enrollEdge([vObjs[V.index(adjObj.label)],
                                                       vObjs[V.index(cur.label)]]))
                #print('pathEdges recurse = '+str([e.endpointsStr for e in pathEdges]))
                retVal = traverse(cur,adjObj,startVert,partner,pathVerts,pathEdges)
                if retVal != []:
                    break
                # When returning from any traverse call, i.e. when you are here,
                # pop one vertex and one edge from the end of their respective lists.
                # Whenever you are returning from a chain ending at a leaf, you
                # no longer need to remember those places. They do not lead to 
                # the startVert, and so can be taken out of the path.
                pathVerts.pop(-1)# remove the last in. This is used in the
                pathEdges.pop(-1)# remove the last in. remainder of the for loop
        #print('at end of taverse, pathEdges = '+str(pathEdges))
        return retVal
            
#    startVert = vObjsWork[V.index(ntev0)]# vObj
    startVert = vObjsWork[V.index(edgeObj.endpointsObjs[0].label)]# vObj, the edge sent to this function.
    partner = vObjsWork[V.index(edgeObj.endpointsObjs[1].label)]# Other end of the supplied edge.
    cur = startVert# the first vertex of nontreeEdge.
    prev = None# the previous vertex
    pathVerts = [cur]# path of vertices.
    pathEdges = []# empty path of edges

    path = traverse(prev,cur,startVert,partner,pathVerts,pathEdges)# Compute the cycle if possible.
    #print('pathEdges bottom = '+str([e.endpointsStr for e in pathEdges]))
    return path# Output a list of edges in the cycle.

def findMasters(V,vObjs,eObjs,nteStrs):
    #findCycle(V,vObjs,edgeObj,nteStr)
    #print(nteStrs)
    lcaDistList = []
    for nte in nteStrs:
        vObj0 = vObjs[V.index(nte[0])]
        vObj1 = vObjs[V.index(nte[1])]
        lcaObj = lowestCommonAncestor(vObj0,vObj1)
        lcaDis = lcaDist(lcaObj)
        lcaDistList.append(lcaDis)
    treeEnum = 16
    nteNum = 2
    print('eObj[?] = '+str(eObjs[treeEnum].toString()))
    print('nteStrs[?] = '+str(nteStrs[nteNum]))
    cycle = findCycle(V,vObjs,eObjs[treeEnum],nteStrs[nteNum])
    print('cycle = '+str([edg.toString() for edg in cycle]))
    #print('lcaDistList = '+str(lcaDistList))
    masterEdges = []
    #cycleList = []
    for edgeObj in eObjs:
        #print('edgeObj = '+str(edgeObj.toString()))
        cycleList = []
        for nte in nteStrs:
            #print('nte = '+str(nte))
            cycle = findCycle(V,vObjs,edgeObj,nte)
            #print('cycle = '+str([edg.toString() for edg in cycle]))
            cycleList.append(list(cycle))
#            if tempList != []:# Find the master edge
#                break# and go to the next edge.
#        print('cycleList = '+str([str([e.toString() for e in cc])+str("----------") for cc in cycleList]))
#        print'|\n|'
#        print
        for c in range(len(cycleList)):
            pass
        masterEdges.append(list(nte))# Record the master edge for each edge
#        if tempList not in cycleList:
#            cycleList.append(tempList)# Keep a list of the cycles found.
    #print('masterEdges = '+str(masterEdges))
   # print
    #print('cycleList = '+str(cycleList))
    return [masterEdges,cycleList]

def findCycleList(V,vObjs,eObjs,nteStrs):
    #findCycle(V,vObjs,edgeObj,nteStr)
#    for vObj in vObjs:
#        print('in findCycL, vObj.label = '+str(vObj.label))
#        print('adjacents = '+str([vStr for vStr in vObj.linked2]))
#        print
    cycleList = []
    for nte in nteStrs:
#        print(nte)
        eObj = enrollEdge([vObjs[V.index(nte[0])],vObjs[V.index(nte[1])]])
        cycle = findCycle(V,vObjs,eObj,nte)
        cycleList.append(list(cycle))
#        verts = []
#        print
#        for edg in cycle:
#            for i in [0,1]:
#                if edg.endpointsObjs[i] not in verts:
#                    verts.append(edg.endpointsObjs[i])
#        for vert in verts:
#            print('in findCL, vert.label = '+str(vert.label))
#            print('adjacents = '+str([vstr for vstr in vert.linked2]))
#            print
#    for vObj in vObjs:
#        print('in findCycL, vObj.label = '+str(vObj.label))
#        print('adjacents = '+str([vStr for vStr in vObj.linked2]))
#        print
        
    
    return cycleList

# Assumes the edge list is in order for the cycle.
def cycle2vObjsList(eCycles):# Takes a list of edge objects forming a cycle.
    #print('in c2ObjL, eCycles = '+str(eCycles))
    vCycleList = []    
    for eCycle in eCycles:
        # Find the correct start vertex.
        if len(eCycle) > 1:# Find the starting vertex; it is not in the next edge.
            startVert = None# which of the first edge, is not in the 2nd edge?
            if eCycle[0].endpointsObjs[0] in eCycle[1].endpointsObjs:
                startVert = eCycle[0].endpointsObjs[1]
            elif eCycle[0].endpointsObjs[1] in eCycle[1].endpointsObjs:
                startVert = eCycle[0].endpointsObjs[0]
        vObjsList = [startVert]# Start with startVert.
        for edg in eCycle:
            v0 = edg.endpointsObjs[0]
            v1 = edg.endpointsObjs[1]
            if v0 not in vObjsList:
                vObjsList.append(v0)
            if v1 not in vObjsList:
                vObjsList.append(v1)
        vCycleList.append(list(vObjsList))# an ordered list of vertex objects.
    return vCycleList# Outputs a list of vertex cycles

def setPolarities(V,vObjs,vCycleList):
    # ['-','+'] means that lead 0 is negative relative to current Ix
    # ['+','-'] means that lead 0 is negative relative to current Ix
    
    #print('in setP, len(vCycleList) = '+str(len(vCycleList)))
    for vObj in vObjs:# Set the polarity list 
        for i in range(len(vCycleList)):# according to the number of cycles
            vObj.polarityList.append([])
        #print('len vObj.polarityList = '+str(len(vObj.polarityList)))
   # vCycleList = [cycle2vObjsList(c) for c in vcycleList]
    bigTemp = []# need to use the same vertex objects as vObjs
    for vcycle in vCycleList:
        temp = []
        for vert in vcycle:
           # print('vert.label = '+vert.label)
            temp.append(vObjs[V.index(vert.label)])
        bigTemp.append(list(temp))
    vCycleList = list(bigTemp)
    arrowListList = [] # list of components, arrow directions, and current numbers
    for i in range(len(vCycleList)):# Each cycle.
        arrowListList.append([])
        for j in range(len(vCycleList[i])):# Each vertex
            vObj = vCycleList[i][j]# vertex
            vStr = vObj.label
            compId = vStr[0]
            compId = compId.upper()
            if compId.isalpha():
                vObjPrev = vCycleList[i][j-1]# Previous vertex in the vCycle
                leadStr = vObjPrev.label
                leadNum = leadStr[0]# leftmost char is either 0 or 1.
                #print('i,j = '+str((i,j))+' polarityList = '+str(vObj.polarityList))
                if compId == 'B':# batteries keep thier polarity
                    if leadNum == '0':# Came to positive side first.
                        vObj.polarityList[i] = ['+','-']
                    elif leadNum == '1':# Came to negative side first.
                        vObj.polarityList[i] = ['-','+']
                elif compId == 'R':# Not a battery, so must be a resistor
                    #vObj.polarityList[i] = ['-','+']#Foward relative to I for this cycle.
                                                    # But that's always the case. (?)
                    if leadNum == '0':# came to lead 0 first
                        vObj.polarityList[i] = ['-','+']# lead 0 is neg, lead 1 is pos
                                                        # for that current
                    elif leadNum == '1':# came to lead 1 first
                        vObj.polarityList[i] = ['+','-']# lead 0 is pos, lead 1 is neg
                    
                else:
                    print('in setP, got here 0')
                direction = []
                current = i
                if leadNum == '0': # previous vertex is lead 0: Direction is [0,1].
                    direction = [0,1]
                elif leadNum == '1':
                    direction = [1,0]
                arrowListList[i].append([vStr,direction,current])
    return arrowListList

def eqStrWrite(vCycles):# Takes a list of vObjs with polarities set.
    eqnlist = []
    for i in range(len(vCycles)):
        eqnstr = ''
        for j in range(len(vCycles[i])):
            newstr = ''
            vObj = vCycles[i][j]
            polars = list(vObj.polarityList)
            lab = str(vObj.label)
            lab = lab.upper()
            first = lab[0]
            if first.isalpha():# vObj is a component, not  a lead.
                prev = vCycles[i][j-1]# The lead of the component.
                leadNumStr = prev.label[0]# leftmost char is '0' or '1' for the lead
                if first == 'B':
                    # Cycle currents are not a factor in battery voltages.
                    if polars[i] == ['+','-']:# Came to positive side first.
                            newstr += ' + (-1)*'+str(lab)
                    elif polars[i]==['-','+']:# Came to neg side first.
                        newstr += ' + (+1)*'+str(lab)
                    else:# Component not in this loop.
                        pass
#                    for k in range(len(polars)):
#                        if polars[k] == ['+','-']:# Came to positive side first.
#                            newstr += ' + (-1)*'+str(lab)
#                        elif polars[k]==['-','+']:# Came to neg side first.
#                            newstr += ' + (+1)*'+str(lab)
#                        else:# Component not in this loop.
#                            pass
                        
                elif first == 'R':
                    for k in range(len(polars)):
                        if polars[k] == ['-','+']:# lead 0 is negative.
                            if leadNumStr == '0':# Came to 0 first.
                                newstr += ' + (+1)*I'+str(k)+'*'+str(lab)# pos dir
                            elif leadNumStr == '1':# Came to 1 first.
                                newstr += ' + (-1)*I'+str(k)+'*'+str(lab)
                            else:
                                pass
                        elif polars[k] == ['+','-']:
                            if leadNumStr == '0':
                                newstr += ' + (-1)*I'+str(k)+'*'+str(lab)
                            elif leadNumStr == '1':
                                newstr += ' + (+1)*I'+str(k)+'*'+str(lab)
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
            eqnstr += str(newstr)  
        eqnlist.append(str(eqnstr))
    return eqnlist

# Make a dictionary of component strings and sum current values.
    # Polarities must have been set.
    # compStrs excludes orientation designators.
def makeCompCurDict(compStrs,vStrs,vObjs,rrefMat,arrows):# Not quite right.
    # Get the cycle current values.
    refDir = [0,1]
    IList = []
    for i in range(len(rrefMat)):# i is both the index and the cycle cur id
        IList.append(rrefMat[i][-1])# Get the right most column of each row.
    arrowDict = {}
    # keys are [compStr,curId]
    # values are [0,1] or [1,0]
    # [0,1] means that the tail of the arrow is at lead 0 and the head is at lead 1.
    for i in range(len(arrows)):# Current loops
        for j in range(len(arrows[i])):# Each arrow list.
            arrowDict[(str(arrows[i][j][0]),int(arrows[i][j][2]))] = tuple(arrows[i][j][1])
#    for elem in arrows:# lists are unhashable, need tuples.
#        print('elem = '+str(elem))
#        arrowDict[(elem[0],elem[2])] = tuple(elem[1])
    compCurDict = {}
    for compStr in compStrs:
        compCurDict[compStr] = 0.0# Make an entry for each component.
        vObj = vObjs[vStrs.index(compStr)]# Get component vertex object.
        polarList = list(vObj.polarityList)
        for i in range(len(IList)):
            if polarList[i] != []:# Cur i goes through comp.
                curVal = IList[i]
                direction = list(arrowDict[(compStr,i)])# safe, because member
                if curVal >= 0:# current is nonnegative. Arrow direction correct.
                    pass
                elif curVal < 0:# Arrow direction is backwards.
                    direction.reverse()# Flip arrow direction
                    curVal = -curVal# and make current nonnegative.
                if direction == refDir:# forward relative to refDir
                    compCurDict[compStr] += curVal
                elif direction == [refDir[1],refDir[0]]:# Backward relative to refDir
                    compCurDict[compStr] -= curVal
    return  compCurDict

def makeCompVoltDict(compCurDict,compStrs,compVals):
    compVoltDict = {}
    for i in range(len(compStrs)):# V = I * R
        if compStrs[i][0] == 'R': # Skip batteries.
            compVoltDict[compStrs[i]] = compVals[i] * compCurDict[compStrs[i]]
    return compVoltDict
    

#[v,e] = makeGraph(e)
#we = addWeights(e)
#print(we)
#print(len(v))
#m = weightedEdgeList2distMatrix(v,we)
#M = np.matrix([[]])
#print(type(M))
#print(M)
#print(M.itemsize())
#print('v = '+str(v))
#displayMatrix(m,v)
#print(len(m))
#spanTree = Prims(v,m)
#print('spanTree = '+str(spanTree))
#print('spanTree = '+str(spanTree))
#print
#print('e = '+str(e))
#print(len(spanTree))
#print(len(e))
#print('dif = '+str(set.symmetric_difference(set())
#set(e)
#eset = [str(x) for x in e]
#treeset = [str(y) for y in spanTree]
#print(eset)
#print
#print(treeset)
#print
#print('dif_test = '+str(set.difference(set([1,2,3,4,5]),set([4]))))
#print('dif = '+str(set.difference(set(eset),set(treeset))))
#nontreeEdgeList = findDif(e,spanTree)
#print('findDif(e,spanTree) = '+str(nontreeEdgeList))
#print(list(set([1,2,3])))
#a = set([1,2,3])
#b = set([4,5,6])
#c = set([a,b])
#a = ['a','b','c']

#b = 'b'
#print(set([[1,2,3],[4,5,6],[7,8,9]]))
#print('0R0' < 'R0')
#set([set([]),set([])])
#print('setListDif(e,spantree) = '+str(setListDif(e,spanTree)))
#print(v)
#print(set([(1,2),(3,4)]))
#print(adjacencyLists(v,spanTree))
#l = ['a','b','c']
#print(l.index('b'))
#distlist,vObjs,eObjs = graphSearchDist(v,spanTree,v[0])
#print('distlist = '+str(distlist)+'\n\n vObjs = '+\
#      str([vert.toString() for vert in vObjs])+'\
#      \n\n eObjs = '+str([edg.toString() for edg in eObjs]))
#print
#print('v = '+str(v))
#print
#populateDecendants(vObjs[0])
#print('distlist = '+str(distlist)+'\n\n vObjs decendants = '+\
#      #str([[c.decendants for c in vert.children] for vert in vObjs])+'\
#      str([vert.decendants for vert in vObjs])+\
#      '\n\n eObjs = '+str([eOb.toString() for eOb in eObjs]))
#print(distlist)
#print(range(len(v)))
#print(v)
#print([(distlist[i],v[i]) for i in range(len(v))])

#vobs,eobs = list2graph(v,spanTree)

#manualTraverse(vobs[0])

#print
#a = [1,2,3]
#b = [4,5,6]
#a = a + b
#print(a)
#print(list(a))
#print(a+[])
#print
#print('spanTree = '+str(spanTree))
## self ancestors ?? 
#lca = lowestCommonAncestor(vObjs[v.index('R3')],vObjs[v.index('R5')])
#print
#print('lca.label = '+str(lca.label))
#print
#dist = lcaDist(lca)
#print('lca distance = '+str(dist))
#print
#print('lca rootDist = '+str(lca.rootDist))
#treeEdgeObj = eObjs[4]
#print('treeEdgeObj.endpointsStr = '+str(treeEdgeObj.endpointsStr)) 
#nteStr = nontreeEdgeList[1]
#print('nteStr = '+str(nteStr))
#pathEdges = findCycle(v,vObjs,treeEdgeObj,nteStr)
#print('pathEdges = '+str([edg.toString() for edg in pathEdges]))

#print(vObjs[1].label)
#print(vObjs[1].linked2)

#[masterEdges,cycleEdges] = findMasters(v,vObjs,eObjs,nontreeEdgeList)
#eCycles = findCycleList(v,vObjs,eObjs,nontreeEdgeList)
#print
#print('eCycles = ')
#print str([[edg.toString() for edg in eCycle] for eCycle in eCycles]))
#for i in range(len(eCycles)):
#    print('cycle '+str(i))
#    print([edg.toString() for edg in eCycles[i]])
#    print
#print
#cycle = cycles[0]
#print('cycle = '+str([edg.toString() for edg in cycle]))
#vCycleList = cycle2vObjsList(eCycles)
#print
#print('vCycleList = '+str(vert))
#print
#print('list of vertices in a cycle = '+str([vert.label for vert in vcycle]))
#print('vCycleList = '+str([[vert.label for vert in vcycle] for vcycle in vCycleList]))
#setPolarities(v,vObjs,vCycleList)
#print
#print('polarities are ')
#for vob in vObjs:
#    print(str(vob.label)+' '+str(vob.polarityList))
#print
#eqnList = eqStrWrite(vCycleList)
#for eqn in eqnList:
#    print(eqn)
#    print
#print
#print(' + (+1)*I0*R4 + (+1)*I0*R2 + (+1)*I2*R2 + (+1)*I0*R3 + (-1)*I1*R3 + (+1)*I2*R3'.find('I0'))
#print(eqnList)
#masterEdgeList