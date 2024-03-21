#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 09:01:27 2020

@author: francescopiscitelli
"""

import numpy as np
import pandas as pd
import h5py
import os

import time

digitIDtemp = [34,33,31,142,143,137]

digitID = digitIDtemp[3]

ordertime = 1

Clockd = 16e-9

datapathinput = '/Users/francescopiscitelli/Desktop/reducedFile/'

filename = '13827-C-ESSmask-20181116-120805-reduced-PY-From000To000.h5'

###############################################################################
###############################################################################

f = h5py.File(datapathinput+filename, "r")

for key in f.keys():
       # print(key)
       name = key
     
ff = f[name]

# for key in ff.keys():
#       print(key)

try:
    rtemp = ff['run']
    duration = rtemp['duration'][()]
except:
    print('--> no run info')
    duration = 0
    
try:
    mtemp   = ff['monitor']
    MONdata = mtemp['data'][()]  #
except:
    print('--> no monitor')
    MONdata = np.ones((1,2),dtype=float)*np.inf

try:
    dtemp = ff['detector']
    arrangement = np.float64(dtemp['arrangement'][()])
    
    items = list(dtemp.keys())
    
    stringToFind = 'digit'
    
    presentDigit = []
    
        # for k, dset in enumerate(dtemp.keys()) :
        
    #     print (k, dset)
    
    for k in range(len(items)):    
        if stringToFind in items[k]:
            # print(items[k],k)
            temp =  items[k].split(stringToFind)
            presentDigit = np.append(presentDigit,np.int64(temp[1]))
    
    if not(digitID in presentDigit):
        data = np.ones((1,9),dtype=float)*np.inf
        print('\n \t No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
        for digit in presentDigit:
            print(np.int(digit),end=' ')
    else:

        selDigit = stringToFind+str(digitID)
    
        for k in range(len(items)):    
            if selDigit in items[k]:
                # print(items[k])
                data = dtemp[selDigit]['data'][()]
               
except:
    print('--> no detector data')
    arrangement = 0
    data        = np.ones((1,9),dtype=float)*np.inf
   

# return data, MONdata, duration 