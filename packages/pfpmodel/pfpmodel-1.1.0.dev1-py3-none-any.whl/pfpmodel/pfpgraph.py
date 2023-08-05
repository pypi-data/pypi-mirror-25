import networkx as nx
import pandas as pd
from networkx.algorithms.assortativity.mixing import mixing_dict
from networkx.utils import dict_to_numpy_array
from networkx.utils import accumulate
import scipy.stats as stats
import numpy as np  
import matplotlib.pyplot as plt 
import math
import random


__all__ = ['pfp']

#m_Growth_Step =  9194
MAX_NUM_NODE = 101000
MAX_NUM_LINK = 303000
VERYBIG = 1000000
#m_Initial_L = 15
#m_Initial_N = 10
m_Para_P = 0.3
m_Para_Q = 0.1
m_Para_M = 3
m_Para_U = 0.0
m_Para_W = 0.6
m_delta = 0.048
MAX_TRY = 10000
#m_NumNode = [m_Initial_N]
#m_NumLink = [0]
m_If_InteractiveGrowth = True 


def Do_AddNewNode(thisNodeID): 
    m_Node_num_nghb[thisNodeID] = 0

def Do_GetRandom(theBase):
    return random.uniform(0, theBase)  

def Do_GetRandom_int(theBase):
    return random.randint(0,theBase)

def Do_IfHasNode(Start, End , NumNode):
    if Start == End or Start > NumNode or End > NumNode or Start < 0 or End < 0:
        return True
    else:
        return False

def Do_IfHasLink (thisStart, thisEnd):
    for iii in range(len(m_Link)):
        if m_Link[iii][1][0] == thisStart:
            if m_Link[iii][1][1] == thisEnd:
                return True 
        if m_Link[iii][1][0] == thisEnd:
            if m_Link[iii][1][1] == thisStart:
                return True
    return False       

def update_tempDoubleX(Node_ID):
    K = m_Node_num_nghb[Node_ID]
    Exponent = 1 + m_delta * np.log10(K)
    tempDoubleX[Node_ID] = K ** Exponent


def Do_GenerateInitialStatus(m_Initial_N , m_Initial_L):
    
    for iii in range(m_NumNode[0]):
        Do_AddNewNode(iii)
    
    for iii in range(m_Initial_N):
        temp = 0
        tempStart = iii
        
        
        while True: 
            tempEnd = Do_GetRandom_int(m_NumNode[0]-1)
            temp = temp + 1
            if Do_IfHasNode(tempStart, tempEnd, m_NumNode[0]) == False and Do_IfHasLink (tempStart, tempEnd) == False:
                break           
            if temp > MAX_TRY:
                return False

        m_Link.append([iii,[tempStart, tempEnd]])
        m_NumLink[0] = m_NumLink[0] + 1
        m_Node_num_nghb[tempStart] = m_Node_num_nghb[tempStart] + 1
        if tempEnd not in m_Node_num_nghb: 
            Do_AddNewNode(tempEnd)
        m_Node_num_nghb[tempEnd] = m_Node_num_nghb[tempEnd] + 1 
    
    for iii in range(m_Initial_N , m_Initial_L):
        temp = 0
        
        while True:
            tempStart = Do_GetRandom_int(m_NumNode[0]-1)
            tempEnd = Do_GetRandom_int(m_NumNode[0]-1)
            temp = temp + 1
           
            if Do_IfHasNode(tempStart, tempEnd, m_NumNode[0]) == False and Do_IfHasLink (tempStart, tempEnd) == False:
                break
            if temp > MAX_TRY:
                return False
            
        m_Link.append([iii,[tempStart, tempEnd]]) 
        m_NumLink[0] = m_NumLink[0] + 1
        if tempStart not in m_Node_num_nghb: 
            Do_AddNewNode(tempStart)
        m_Node_num_nghb[tempStart] = m_Node_num_nghb[tempStart] + 1
        if tempEnd not in m_Node_num_nghb: 
            Do_AddNewNode(tempEnd)
        m_Node_num_nghb[tempEnd] = m_Node_num_nghb[tempEnd] + 1 
        
        
    for iii in range(m_NumNode[0]):
        update_tempDoubleX(iii)

def Do_Get_Node_PFP(thisExecption):
    total = 0
    for iii in range(m_NumNode[0]):
        #K = m_Node_num_nghb[iii]
        #Exponent = 1 + m_delta * np.log10(K)
        #tempDoubleX[iii] = K ** Exponent
        total = total + tempDoubleX[iii]
    
    while True :
        tempA = 0 
        tempDouble  = Do_GetRandom(total)
        for iii in range(m_NumNode[0]):
            tempB = tempA + tempDoubleX[iii]
            if tempB >= tempDouble and tempDouble >= tempA:
                if iii == thisExecption:
                    break
                return iii
            tempA = tempB


def Do_Grow_Link_Interactive(thisStartNode):
    temp = 0
    
    while True:
        tempEndNode = Do_Get_Node_PFP(thisStartNode)
        temp = temp + 1
        if Do_IfHasNode(thisStartNode, tempEndNode, m_NumNode[0]) == False and Do_IfHasLink (thisStartNode, tempEndNode) == False:
            break
        if temp > MAX_TRY:
            return -1;

    m_Link.append([m_NumLink[0],[thisStartNode, tempEndNode]])
    m_NumLink[0] = m_NumLink[0] + 1
    
    
    m_Node_num_nghb[thisStartNode] = m_Node_num_nghb[thisStartNode] + 1
    m_Node_num_nghb[tempEndNode] = m_Node_num_nghb[tempEndNode] + 1 
    
    update_tempDoubleX(thisStartNode)
    update_tempDoubleX(tempEndNode)
    
    
    return tempEndNode

def Do_GeneratePFPNetwork(m_Growth_Step):
    for iii in range(m_Growth_Step):
        Do_AddNewNode(m_NumNode[0])
        temp = Do_GetRandom(1)
        
        if temp < m_Para_P + m_Para_Q:
            theEndNode = Do_Grow_Link_Interactive(m_NumNode[0])
            if m_If_InteractiveGrowth == True:
                Do_Grow_Link_Interactive(theEndNode)
                Do_Grow_Link_Interactive(theEndNode)
            
                
        elif temp < m_Para_P + m_Para_Q + m_Para_W:
            Do_Grow_Link_Interactive(m_NumNode[0])
            theEndNode = Do_Grow_Link_Interactive(m_NumNode[0])
            
            if m_If_InteractiveGrowth == True:
                #Do_test( theEndNode, tempNode)
                Do_Grow_Link_Interactive(theEndNode)
            
     
        else:  
            for ttt in range(m_Para_M):
                Do_Grow_Link_Interactive(m_NumNode[0])
        
        m_NumNode[0] = m_NumNode[0] + 1
        
def pfp(m_Initial_N, m_Initial_N, m_Growth_Step):
    m_NumNode = [m_Initial_N]
    m_NumLink = [0]
    m_Node_num_nghb = {}
    tempDoubleX = {}
    m_Link = []
    Do_GenerateInitialStatus(m_Initial_N , m_Initial_L)
    Do_GeneratePFPNetwork(m_Growth_Step)
    a = []
    for i in range(len(m_Link)):
        a.append( [m_Link[i][1][0],m_Link[i][1][1]])
    
    return nx.Graph(a)
