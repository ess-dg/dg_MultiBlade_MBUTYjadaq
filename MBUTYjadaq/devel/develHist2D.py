#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 08:40:18 2020

@author: francescopiscitelli
"""
import numpy as np
# import time
import matplotlib.pyplot as plt

data = np.load('datate.npy')

XX = np.linspace(0.5e4,4e4,128)
A  = data[:,2]
YY = np.linspace(0,31,32)
B  = data[:,1]

OutBound = 0 

###############################################################################
############################################################################### 

# # this 2D hist states a warning if there is an out of bounds events, buth these events are not shown in the hist 
# def myHist2D (XX,A,YY,B):
    
binX   = len(XX) 
binY   = len(YY)
    
Xmin   = min(XX) 
Xmax   = max(XX) 
Ymin   = min(YY) 
Ymax   = max(YY) 

cont = 0

histXY = np.zeros((binY,binX)) 

if not( (len(A) == len(B))):
    print('\n \t ----> ABORT: X and Y not same length! \n')
    # return histXY

xxtemp =  np.int_(np.around(((binX-1)*((A-Xmin)/(Xmax-Xmin)))))
yytemp =  np.int_(np.around(((binY-1)*((B-Ymin)/(Ymax-Ymin)))))
     
for k in range(len(A)):
 
    xx =  xxtemp[k]
    yy =  yytemp[k]

    if OutBound == 1:
        
       if ( (xx >= 0) and (xx <= binX-1) and (yy >= 0) and (yy <= binY-1) ):
           histXY[yy,xx] += 1
       elif ( (xx >= 0) and (xx > binX-1) and (yy >= 0) and (yy <= binY-1) ):
            histXY[yy,-1] += 1
       elif ( (xx < 0) and (xx <= binX-1) and (yy >= 0) and (yy <= binY-1) ):
            histXY[yy,0] += 1
       elif ( (xx >= 0) and (xx <= binX-1) and (yy < 0) and (yy <= binY-1) ):
           histXY[0,xx] += 1
       elif ( (xx >= 0) and (xx <= binX-1) and (yy >= 0) and (yy > binY-1) ):
           histXY[-1,xx] += 1
           
    elif OutBound == 0:
         
       if ( (xx >= 0) and (xx <= binX-1) and (yy >= 0) and (yy <= binY-1) ):
          histXY[yy,xx] += 1
       else:
           if cont == 0:
               print('warning: hist out of bounds') 
               cont = 1
       
       
fig, ax = plt.subplots(figsize=(6,6), nrows=1, ncols=1)    
pos  = ax.imshow(histXY,aspect='auto',interpolation='none',extent=[XX[0],XX[-1],YY[-1],YY[0]], origin='upper',cmap='jet')
                
    # return histXY