#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 12:53:17 2020

@author: francescopiscitelli
"""

import libLoadFile as lof 
import numpy as np
import os


digitID = [34]

ordertime = 1

Clockd = 16e-9

datapath = os.path.abspath('../.')+'/data/' 

filenamefull = '13827-C-ESSmask-20181116-120805_00000.h5'

###############################################################################
###############################################################################

# Cassette2Digit  = {1: ['w', 2, 4, np.arange(0,32), 's', 2, 3, np.arange(32,64),'r'],
#                    2: ['w', 2, 4, np.arange(32,64), 's', 2, 3, np.arange(0,31),'g'],
#                    6: ['w', 2, 5, np.arange(0,32), 's', 2, 2, np.arange(32,64),'b'],
#                    4: ['w', 2, 5, np.arange(32,64), 's', 2, 2, np.arange(0,32),'k']}

#wires must go to 0-31, strip1 32-63, strip2 64-95

Cassette2Digit  = {1: {'wires': {'digit': 34, 'ch': np.arange(0,32)}, 'strips1': {'digit': 34, 'ch': np.arange(32,64)}, 'strips2': {'digit': 31, 'ch': np.arange(32,64)} },
                   2: {'wires': {'digit': 33, 'ch': np.arange(0,32)}, 'strips1': {'digit': 33, 'ch': np.arange(32,64)}, 'strips2': {'digit': 31, 'ch': np.arange(0,32) } } }
 
###############################################################################
###############################################################################

wss = ['wires','strip1','strip2']

# for cc in Cassette2Digit:
    
cc = 1
print(cc)

# for ws in wss:
    
ws = 'wires'
print(ws)

digitID = Cassette2Digit[cc][ws]['digit']

ordertime = 1
[data, Ntoffi, GTime, DGtime, flag] = lof.readHDFefu(datapath,filenamefull,digitID,Clockd,ordertime)

ch = Cassette2Digit[cc][ws]['ch']

selection = np.isin(data[:,1],ch)

temp = np.append(data,DGtime[:,None],axis=1)

datatemp = temp[selection]

# you need to separate the tofs using DGTime and attach them after 
