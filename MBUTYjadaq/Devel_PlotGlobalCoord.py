#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 08:56:38 2020

@author: francescopiscitelli
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import time
from matplotlib.colors import LogNorm

# import the library with all specific functions that this code uses 
from lib import libLoadFile as lof 
from lib import libHistog as hh
from lib import libMBUTY_V9x15 as mbl 

print('----------------------------------------------------------------------')
plt.close("all")

savereducedpath = '/Users/francescopiscitelli/Desktop/reducedFile/'

fname = '13827-C-ESSmask-20181116-120805-reduced-PY-From000To001.h5'

digitID = [34,33,31,142,143,137]

inclination = 5

sinne = np.sin(np.deg2rad(inclination)) 

wirepitch = 4

projWirePitch = sinne*wirepitch

XX    = np.arange(0,68,projWirePitch)
YY    = np.arange(0,126,2)

ToFduration       = 0.06     #s
ToFbinning        = 100e-6   #s

lambdaBins      = 127   
lambdaRange     = [2.8,9.2]    #A

OffsetOf1stWires = 10.11   #mm

# OffsetOf1stWires = 5

ToFmin    = 0
ToFmax    = ToFduration
ToFbins   = round((ToFmax-ToFmin)/ToFbinning)
ToFx      = np.linspace(ToFmin,ToFmax,ToFbins)

# lambda axis 
xlambda = np.linspace(lambdaRange[0],lambdaRange[1],lambdaBins)

POPH = []


for dd in np.arange(len(digitID)):

    POPHtemp, MONdata, MONcounts, duration, durationAll = lof.readHDFreducedFile(savereducedpath,fname,digitID[dd])
    
    POPHtemp[:,0] = POPHtemp[:,0]+OffsetOf1stWires*dd
    
    if dd == 0:
        POPH = POPHtemp
    else:
        POPH = np.append(POPH,POPHtemp, axis=0)
    
POPHc = POPH[POPH[:,1] >= 0,:]     
# POPHc = POPH

XY, XYproj, XToF = mbl.myHistXYZ(XX,POPHc[:,0],YY,POPHc[:,1],ToFx,POPHc[:,2],coincidence=1,showStats=1)
    
__ , __ , XLam = mbl.myHistXYZ(XX,POPHc[:,0],YY,POPHc[:,1],xlambda,POPHc[:,8],coincidence=1,showStats=0)  


# binY   = len(YY) 
# Ymin   = min(YY) 
# Ymax   = max(YY) 

# aa = np.int_(np.around(((binY-1)*((POPH[:,1]-Ymin)/(Ymax-Ymin)))))
# # print(aa)


normColors = None

fig2D, (ax1, ax2) = plt.subplots(num=101,figsize=(6,12), nrows=2, ncols=1)    
pos1  = ax1.imshow(XY,aspect='auto',norm=normColors,interpolation='none',extent=[XX[0],XX[-1],YY[-1],YY[0]], origin='upper',cmap='viridis')
fig2D.colorbar(pos1, ax=ax1)
ax1.set_xlabel('Wire (mm)')
ax1.set_ylabel('Strip (mm)')


########
# 1D image of detector, opnly wires, in coincidence with strips (2D) and not (1D)
XYprojCoinc = np.sum(XY,axis=0) 

pos2 = ax2.step(XX,XYproj,'r',where='mid',label='1D')
ax2.step(XX,XYprojCoinc,'b',where='mid',label='2D')
ax2.set_xlabel('Wire ch.')
ax2.set_ylabel('counts')
ax2.set_xlim(XX[0],XX[-1])
legend = ax2.legend(loc='upper right', shadow=False, fontsize='large')


# ########
# # 2D image of detector ToF vs Wires 
# ToFxgms = ToFx*1e3 # in ms 

# fig2, ax2 = plt.subplots(num=102,figsize=(6,6), nrows=1, ncols=1) 
# pos2  = ax2.imshow(XToF,aspect='auto',norm=normColors,interpolation='nearest',extent=[ToFxgms[0],ToFxgms[-1],XX[0],XX[-1]], origin='lower',cmap='viridis')
# fig2.colorbar(pos2, ax=ax2)
# ax2.set_ylabel('Wire ch.')
# ax2.set_xlabel('ToF (ms)')


# figl, axl = plt.subplots(num=103,figsize=(6,6), nrows=1, ncols=1) 
# posl1  = axl.imshow(XLam,aspect='auto',norm=normColors,interpolation='nearest',extent=[xlambda[0],xlambda[-1],XX[0],XX[-1]], origin='lower',cmap='viridis')
# figl.colorbar(posl1, ax=axl)
# axl.set_ylabel('Wire ch.')
# axl.set_xlabel('lambda (A)')
