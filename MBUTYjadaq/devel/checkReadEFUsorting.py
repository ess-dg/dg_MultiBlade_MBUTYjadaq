#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:25:10 2020

@author: francescopiscitelli
"""

import numpy as np
import matplotlib.pyplot as plt
import h5py

datapathinput = '/Users/francescopiscitelli/Documents/PYTHON/MBUTY/devel/'
filename = 'day2-chp-on-20200908-094828_00000.h5'

digitID = 137

Clockd = 16e-9

ordertime=1

#this is the equivalent of the MATALB function 
#[DATA,Ntoffi,GTime] = readHDFEFUfile(datapathinput,filename,digitID,ordertime)
# output data 4 columns, col 0 time stamp, col 1 ch num from 0 to 63, col 2 ADC value, col 3 reset of ToF in ms

# def readHDFefu (datapathinput,filename,digitID,Clockd,ordertime=1):
    
########################################

#  use pandas 
# DATA = np.array(pd.read_hdf((datapathinput+filename),'mbcaen_readouts'))

########################################

#  or use h5py a bit faster 
f  = h5py.File(datapathinput+filename, "r")

ff = f['mbcaen_readouts'][()]    

temp = ff['global_time']

DATA = np.zeros((len(temp),5), dtype = 'uint64')

DATA[:,0] = temp 
DATA[:,1] = ff['digitizer']
DATA[:,2] = ff['local_time']
DATA[:,3] = ff['channel']
DATA[:,4] = ff['adc']
  
f.close() 

########################################

if not(digitID in DATA[:,1]): #if the digitID does not exist in the file 
    
    Bdata  = np.ones([2,3], dtype='float64' )*np.inf
    Ntoffi = np.array([1], dtype='float64' )*np.inf
    GTime  = np.array([1], dtype='float64' )*np.inf
    DGTime = np.array([1], dtype='float64' )*np.inf
    flag   = -1
    presentdigit = np.unique(DATA[:,1])
    print('\n \t \033[1;33mWARNING: No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
    for digit in presentdigit:
        print(digit,end=' ')
    print('\033[1;37m')
           
else:
    
    flag   = 0
    
    selectdigi = DATA[:,1] == digitID

    Adata = DATA[selectdigi,:]
    
    ## CH NUMBER FROM 0 NOT FROM 1 AS MATLAB !!!!! OTHERVIWISE ADD A LINE HERE TO ADD +1
#        uncomment for ch from 1 to 64
    # Adata[:,3] = Adata[:,3]+np.float64(1) ## ch is from 1 to 64
    
    GTime, index2  = np.unique(Adata[:,0], return_index=True) 
    Ntoffi = len(GTime)
    
    tofChange2 = np.zeros((len(Adata))) 
    tempt      = np.diff(Adata[:,0])
    tempt      = np.append([np.float64(1)], tempt)
    tofChange2[index2] = tempt[index2]
    
    index2 = np.append(index2,[np.int64(len(tofChange2))])
    
    #plt.plot(GTime)
    
    # tofChange = np.diff(Adata[:,0])
    # tofChange = np.append([np.float64(1)], tofChange)
    # ### tofChange[tofChange != 0] = 1
    # index = np.flatnonzero(tofChange)
    # # index = np.argwhere(np.abs(tofChange) > 1e3)
    
    # index = np.append(index,[np.int64(len(tofChange))])
    
    Bdata  = np.float64(Adata[:,2:5]) 
    # Bdata  =  np.concatenate((Bdata,tofChange[:,None]),axis=1)
 
    # col 1 time stamp, col 2 channel, col 3 ADC, 
    # col 4 global time reset delta in ms moved to DGTime
    
    #Bdata[2:10,0] = range(444008,444000,-1)
    
    if ordertime == 1:
        for k in range(0,Ntoffi,1):
            print(k,index2[k],index2[k+1])
            temp = Bdata[index2[k]:index2[k+1],:]
            temp2 = temp[:,0].argsort()
            temp3 = temp[temp2,:]
            Bdata[index2[k]:index2[k+1],:] = temp3
            
    Bdata[:,0] = Bdata[:,0]*Clockd       # time in s 
    
    # DGTime = Bdata[:,3]
    
    DGTime = tofChange2
            
# return Bdata, Ntoffi, GTime, DGTime, flag

fig = plt.figure(num=903, figsize=(9,6))
ax1 = fig.add_subplot(111)
plt.plot(np.arange(len(Bdata[:,0])),Bdata[:,0],marker='+',color='r',linestyle=None)
# plt.scatter(index,np.zeros((len(index))),marker='o',color='b')
plt.scatter(index2,np.zeros((len(index2))),marker='d',color='k')
plt.xlabel('trigger no.')
plt.ylabel('time (s)')
plt.grid(axis='x', alpha=0.75)
plt.grid(axis='y', alpha=0.75)