#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 13:46:23 2019

@author: ralph
"""

#m4 = [['R4+R2+R3','-R3','R2+R3','0'],
#      ['-R3','R8+R7+R3+R1+R0','-R8-R7-R3','B0'],
#      ['R2+R3','-R3-R7-R8','R2+R3+R7+R8+R6+R5','0']]
#
#strEqnList = ['+ (+1)*I0*R4 + (+1)*I0*R2 + (+1)*I2*R2 + (+1)*I0*R3 + (-1)*I1*R3 + (+1)*I2*R3',
#
# '+ (+1)*I1*R8 + (-1)*I2*R8 + (+1)*I1*R7 + (-1)*I2*R7 + (-1)*I0*R3 + (+1)*I1*R3'+
# '+ (-1)*I2*R3 + (+1)*I1*R1 + (+1)*I1*R0 + (-1)*B0',
#
# '+ (+1)*I0*R2 + (+1)*I2*R2 + (+1)*I0*R3 + (-1)*I1*R3 + (+1)*I2*R3 + (-1)*I1*R7'+ 
# '+ (+1)*I2*R7 + (-1)*I1*R8 + (+1)*I2*R8 + (+1)*I2*R6 + (+1)*I2*R5']
#
#strEqnList = [' + (+1)*I0*R3 + (-1)*I1*R3 + (-1)*B2 + (+1)*I0*R2', 
#              ' + (-1)*B1 + (-1)*I0*R3 + (+1)*I1*R3 + (+1)*I1*R1',
#              ' + (+1)*I2*R0 + (-1)*B0 + (-1)*B1 + (-1)*B2']
#
#R0 = 1.0
#R1 = 2.0
#R2 = 3.0
#R3 = 4.0
#R4 = 5.0
#R5 = 6.0
#R6 = 7.0
#R7 = 8.0
#R8 = 9.0
#B0 = 10.0
#
#compStrs = ['R0','R1','R2','R3','R4','R5','R6','R7','R8','B0']
#compVals = [ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0,10.0]
#
#R0 = 47
#R1 = 22
#R2 = 33
#R3 = 10
#B0 = 12
#B1 = 6
#B2 = 8
#
#compStrs = ['R0','R1','R2','R3','B0','B1','B2']
#compVals = [47,22,33,10,12,6,8]

def strEqns2strMatrix(strEqnList):
    iListList = []# a list of lists of values assocatied with each electrical current
    for i in range(len(strEqnList)):
        iList = ['' for j in range(len(strEqnList))]# a list of values assocatied with each electrical current
        terms = strEqnList[i].split(' + ')
        rightStr = '0'# The batteries or sources that go on the right side of the eqn.
        #print('terms = '+str(terms))
        while '' in terms:
            terms.remove('')
        for term in terms:
           # print(term.split('+ '))
            #print(term.lstrip('+ '))
            term.lstrip('+ ')# Get rid of the leading + .
           # print(term)
            factorList = term.split('*')
            while '' in factorList:
                factorList.remove('')
            polarity = ''
            curNum = -1
            component = ''
            for factor in factorList:
                if factor == '(+1)':
                    polarity = ''
                elif factor == '(-1)':
                    polarity = '-'
                elif len(factor.split('I')) == 2:
                    curNum = int(factor.split('I')[1])
                elif factor == '':
                    #print('--------factor in e = '+factor)
                    pass
                else:
                    component = str(factor)
            if component[0] == 'B':
                if rightStr == '0':# Zero by default. Replace.
                    if polarity == '':# + --> - on RHS
                        rightStr = str('-'+str(component))
                    elif polarity == '-':# - --> + on RHS
                        rightStr = str(''+str(component))
                else:# Add to.
                    if polarity == '':#+polarity, becomes - when sent to right side of eqn
                        rightStr = str(rightStr)+'-'+str(component)# + --> - on RHS
                    elif polarity == '-':
                        rightStr = str(rightStr)+'+'+str(component)# - --> + on RHS
            elif iList[curNum] == '' or polarity == '-':
                iList[curNum] = str(iList[curNum])+str(polarity+component)
            else:
                iList[curNum] = str(iList[curNum])+str('+'+polarity+component)
        iList.append(rightStr)    
        iListList.append(list(iList))
    print
    print('iListList')  
    print      
    for i in range(len(iListList)):
            print iListList[i]
            print
    return iListList

def strMat2numMat(compStrs,compVals,strMat):
    numMat = []
    for i in range(len(strMat)):
        numMat.append([])# numMat[i]
        for j in range(len(strMat[i])):
            numElem = 0# Numeric element of numMat.
            strVal = strMat[i][j]
            addedPluses = ''
            for k in range(len(strVal)):
                if strVal[k] == '-':
                    addedPluses = str(addedPluses)+str('+-')
                else:
                    addedPluses = str(addedPluses)+str(strVal[k])
            terms = addedPluses.split('+')                   
            while '' in terms:
                terms.remove('')
            for term in terms:
                #print('term = |'+str(term)+'|')
                sign = 2.0
                comp = ''
                if term[0] == '-':
                    sign = -1.0
                    comp = str(term)
                    comp = comp.lstrip('-')
                else:
                    sign = 1.0
                    comp = str(term)
                #print('sign = '+str(sign)+', comp = '+str(comp))
                for l in range(len(compStrs)):
                    if comp == compStrs[l]:# Batteries are already seperated out.
                        numElem += sign*compVals[l]
            numMat[i].append(float(numElem))#NumMat[i][j]
    return numMat

def reduceExp(exp):#Reduce an algebraic expression and systematize its form.
    
    return

# Compute the current through and voltage across each component.
#def makeCompCurDict(mat,compStrs,strEqnList,V,vObjs):
#    IList = []# If cur is negative, then the arrow direction was backwards.
#    for i in range(len(mat)):# for each row
#        IList.append(float(mat[i][-1]))# for each last column, store current
#    print
#    print('IList = '+str(IList))
#    print
#    compCurDict = {}
#    for comp in compStrs:
#        compCurDict[comp] = 0.0# The sum algebraic current through each component.
#    #IRcomboList = []
#    for i in range(len(strEqnList)):# i is both the index and the current.
#        eqnStr = strEqnList[i]
#        termList = eqnStr.split(' + ')
##        print
##        print('termList = '+str(termList))
##        print
#        while '' in termList:
#            termList.remove('')
#        for term in termList:
#            factorList = term.split('*')
##            print
##            print('factorList = '+str(factorList))
##            print
#            while '' in factorList:
#                factorList.remove('')
#            sign = ''
#            curNum = ''
#            comp = ''
#            for factor in factorList:
#                if factor == '(-1)':
#                    sign = '-'
#                elif factor == '(+1)':
#                    sign = '+'
#                elif factor[0] == 'I':# A current
#                    curStr = factor[1:]# Slice off the I and keep the rest
#                    curNum = int(curStr)
#                elif factor[0] == 'B':
#                    curNum = int(i)
#                    comp = str(factor)
#                elif factor[0] == 'R':
#                    comp = str(factor)
#                else:
#                    print('inIRc, else')
#            if curNum == i:# Update dict once for each IR combo where I cycle = i.
#                cur = 0.0
#                if sign == '-':# Can be - for batteries.
#                    cur = -IList[curNum]
#                elif sign == '+':# Should be plus for resistors
#                    cur = IList[curNum]
#                    
#                #curStr = sign+str(IList[curNum])
#                compCurDict[comp] += cur
#            else:
#                pass# through away.
#    return compCurDict

#print(strEqnList)
#print
#print('strMat = ')
#print
#strMat = strEqns2strMatrix(strEqnList)

#print(strMat)
#numMat = strMat2numMat(compStrs,compVals,strMat)
#print('numMat = ')
#print(numMat)
#a = '1+2+3+4-5-6-7+8-9'.split('+\|-')
#print(a)
#print '+ (+1)*I0*R4 + (+1)*I0*R2'.split('+ ')
#print(int('1000'))
#print('I123'.split('I')[0])
#print('R456'.split('I')[0])
#print(''.split('I'))
#[1,2,3].index(4)
#a = ['','ed','']
#if '' in a:
#    a.remove('')
#print([1,2,3].remove(''))
#aList = ['']
#print(aList[0] += 'abc'+'def')
#'abc' += 'def'

