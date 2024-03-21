#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:25:09 2020

@author: francescopiscitelli
"""

import numpy as np
import time
import matplotlib.pyplot as plt

XYglob = np.load('XYimg.npy')

XX    = np.linspace(0,31,32)
YY    = np.linspace(0,31,65)

XXg   = np.linspace(XX[0],(XX[-1]-XX[0]+1)*6-(1-XX[0]),32*6)         
YYg   = YY

fig2D, ax = plt.subplots(figsize=(6,12), nrows=1, ncols=1)    
pos1 = ax.imshow(XYglob,aspect='auto',interpolation='nearest',extent=[XXg[0],XXg[-1],YYg[-1],YYg[0]], origin='upper',cmap='jet')



gaps      = [0, 3, 4, 4, 3, 2]   # (first must be always 0)

remove = sum(gaps)

llen = len(XXg)-remove

XXgc = np.linspace(0,(llen-1),llen)

XYglobc = np.zeros((len(YY),len(XXgc)))

cumul = 0

for k in range(len(gaps)):
    
    cumul = cumul + gaps[k]
    
    indexes1 = np.int_(k*32 + np.linspace(0,31,32))
    indexes2 = np.int_((k*32-cumul) + np.linspace(0,31,32))
    
    print(cumul,indexes1,indexes2)

    XYglobc[:,indexes2] = XYglobc[:,indexes2] + XYglob[:,indexes1]
    
    
    
fig, ax = plt.subplots(figsize=(6,12), nrows=1, ncols=1)    
ax.imshow(XYglobc,aspect='auto',interpolation='nearest',extent=[XXgc[0],XXgc[-1],YYg[-1],YYg[0]], origin='upper',cmap='jet')