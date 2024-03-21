#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 10:08:39 2020

@author: francescopiscitelli
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

# def readHDFefu (datapathinput,filename,digitID,Clockd,ordertime=1):
    
########################################

#  use pandas 
# DATA = np.array(pd.read_hdf((datapathinput+filename),'mbcaen_readouts'))

########################################

datapathinput = '/Users/francescopiscitelli/Documents/DOC/DATA/2020_09/DATA_PSI/RawData/I-MB300L-Rabbit/'
filename = 'ContScan2-20200909-155650_00000.h5'
ordertime = 1
digitID  = 34
digitID2 = 137
Clockd = 16e-9

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

########################################
    
    DATA = DATA[0:5000,:]
    
    flag   = 0
    
    selectdigi  = DATA[:,1] == digitID
    
    Adata = DATA[selectdigi,:]
    
    GTime, index  = np.unique(Adata[:,0], return_index=True) 
    Ntoffi = len(GTime)
    
    tofChange = np.zeros((len(Adata))) 
    tempt      = np.diff(Adata[:,0])
    tempt      = np.append([np.float64(1)], tempt)
    tofChange[index] = tempt[index]
    
    index = np.append(index,[np.int64(len(tofChange))])
    
    Bdata  = np.float64(Adata[:,2:5]) 
    
    if ordertime == 1:
        for k in range(0,Ntoffi,1):
            # print(k,index2[k],index2[k+1])
            temp = Bdata[index[k]:index[k+1],:]
            temp2 = temp[:,0].argsort()
            temp3 = temp[temp2,:]
            Bdata[index[k]:index[k+1],:] = temp3
            
    Bdata[:,0] = Bdata[:,0]*Clockd       # time in s 
    
    # DGTime = Bdata[:,3]
    
    DGTime = tofChange
    
    Gt = Adata[:,0]-Adata[0,0]
    
    
    
    ########################################
    
    selectdigi2  = DATA[:,1] == digitID2
    
    selectc1     = np.isin(DATA[:,3],np.arange(0,32))
    
    # ttetete = np.logical_and(selectdigi2,selectc1)
    
    Adata2 = DATA[ np.logical_and(selectdigi2,selectc1) ,:]
    
    GTime2, index2  = np.unique(Adata2[:,0], return_index=True) 
    Ntoffi2 = len(GTime2)
    
    tofChange2 = np.zeros((len(Adata2))) 
    tempt2      = np.diff(Adata2[:,0])
    tempt2      = np.append([np.float64(1)], tempt2)
    tofChange2[index2] = tempt2[index2]
    
    index2 = np.append(index2,[np.int64(len(tofChange2))])
    
    Bdata2  = np.float64(Adata2[:,2:5]) 
    
    if ordertime == 1:
        for k in range(0,Ntoffi2,1):
            # print(k,index2[k],index2[k+1])
            temp = Bdata2[index2[k]:index2[k+1],:]
            temp2 = temp[:,0].argsort()
            temp3 = temp[temp2,:]
            Bdata2[index2[k]:index2[k+1],:] = temp3
            
    Bdata2[:,0] = Bdata2[:,0]*Clockd       # time in s 
    
    # initof = np.argwhere(Bdata2[:,0] >= Bdata[100,0])[0]

    # Bdata2[:,0] = Bdata2[:,0] - Bdata[0,0] 
    # DGTime = Bdata[:,3]
    
    DGTime2 = tofChange2
    
    Gt2 = Adata2[:,0]-Adata[0,0]
    
    ########################################
    
    nrows = np.arange(0,len(Bdata),1)
    nrows2 = np.arange(0,len(Bdata2),1)
    
    fig1, ax2 = plt.subplots(num=1,figsize=(12,6), nrows=1, ncols=1) 
    ax2.plot(nrows,Bdata[:,0],color='k',marker='+',label=str(digitID))
    ax2.plot(nrows2,Bdata2[:,0],color='r',marker='+',label=str(digitID2))
# ax2.plot(D1,M4,color='m',linestyle=':',label='lin compensation')
    # ax2.set_xlabel('wire no.')
    # ax2.set_ylabel('gas gain')
    ax2.legend()
    ax2.grid()
    # ax2.set_xlim([0,8])
    
    fig2, [ax3, ax4] = plt.subplots(num=2,figsize=(12,6), nrows=1, ncols=2) 
    ax3.plot(nrows,DGTime,color='k',marker='+',label='1')
    ax3.plot(nrows2,DGTime2,color='r',marker='+',label='1')
    
    
    ax4.plot(nrows,Gt,color='k',marker='+',label='1')
    ax4.plot(nrows2,Gt2,color='r',marker='+',label='1')
            
# return Bdata, Ntoffi, GTime, DGTime, flag