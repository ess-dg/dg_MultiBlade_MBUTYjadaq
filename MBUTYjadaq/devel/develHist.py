#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:25:03 2020

@author: francescopiscitelli
"""

import numpy as np
import time
import matplotlib.pyplot as plt

data = np.load('datate.npy')

XX = np.arange(0,64,1)

YY = data[:,1]

# 

binX   = len(XX) 
        
Xmin   = min(XX) 
Xmax   = max(XX) 

histXX = np.zeros(binX) 

histXX2 = np.zeros(binX) 

histXX3 = np.zeros(binX) 

####################################

# t = time.time()
    
# for k in range(len(YY)):
     
#    index =  np.int(round(((binX-1)*((YY[k]-Xmin)/(Xmax-Xmin)))))

#    if ( (index >= 0) and (index <= binX-1) ):
#       histXX[index] += 1
#    else:
#            print('warning: hist out of bounds')   
           
# elapsed = time.time() - t
# print(elapsed)   

# ####################################   

# t2 = time.time()
           
# aa =  np.int_(np.around(((binX-1)*((YY-Xmin)/(Xmax-Xmin)))))

# for k in range(len(aa)):
     
#    index = aa[k]
    
#    if ( (index >= 0) and (index <= binX-1) ):
#       histXX2[index] += 1
#    else:
#            print('warning: hist out of bounds')   


# elapsed2 = time.time() - t2
# print(elapsed2)  

####################################
#  much faster !!! !

t3 = time.time()

aa =  np.int_(np.around(((binX-1)*((YY-Xmin)/(Xmax-Xmin)))))

if not(np.all(aa >= 0) and np.all(aa <= binX-1)):
   print('warning: hist out of bounds') 

for k in range(len(XX)):

    histXX3[k] = np.sum(aa==k)
    
# fill overflow last bin and first bin
histXX3[0]  += np.sum(aa<0)
histXX3[-1] += np.sum(aa>binX-1)

fig, ax = plt.subplots(figsize=(6,6), nrows=1, ncols=1)    
pos = ax.step(XX,histXX3,'k',where='mid')


elapsed3 = time.time() - t3
print(elapsed3)  


####################################

# aa.astype(int)
           
# index1 = np.int(np.round(((binX-1)*((YY-Xmin)/(Xmax-Xmin)))))