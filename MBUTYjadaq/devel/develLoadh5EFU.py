#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:56:48 2020

@author: francescopiscitelli

"""

import numpy as np
import os
import pandas as pd
import time
import h5py

# import MBUTYLIB_V9x11 as mb 

# from lib import libLoadFile as lof 

digitID = [34]

ordertime = 1

Clockd = 16e-9

datapathinput = os.path.abspath('../.')+'/data/' 

filename = '13827-C-ESSmask-20181116-120805_00000.h5'


###############################################################################
###############################################################################

# t1 = time.time()

# [data1, Ntoffi1, GTime1, DGTime1, flag1] = mb.readHDFefu_3col(datapathinput,filename,digitID,Clockd,ordertime) 

# elapsed1 = time.time() - t1
# print('--> time el.: ' + str(elapsed1) + ' s')  


t2 = time.time()

DATA = np.array(pd.read_hdf((datapathinput+filename),'mbcaen_readouts'))
   
if not(digitID in DATA[:,1]): #if the digitID does not exist in the file 
    
    Cdata  = np.ones([2,3], dtype='float64' )*np.inf
    Ntoffi = np.array([1], dtype='float64' )*np.inf
    GTime  = np.array([1], dtype='float64' )*np.inf
    DGTime = np.array([1], dtype='float64' )*np.inf
    flag   = -1
    presentdigit = np.unique(DATA[:,1])
    print('\n \t No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
    for digit in presentdigit:
        print(digit,end=' ')
           
else:
    
    flag   = 0
    
    selectdigi = DATA[:,1] == digitID

    Adata = DATA[selectdigi,:]
    
    ## CH NUMBER FROM 0 NOT FROM 1 AS MATLAB !!!!! OTHERVIWISE ADD A LINE HERE TO ADD +1
#        uncomment for ch from 1 to 64
    # Adata[:,3] = Adata[:,3]+np.float64(1) ## ch is from 1 to 64
    
    GTime  = np.unique(Adata[:,0]) 
    Ntoffi = len(GTime)
    
    #plt.plot(GTime)
    
    tofChange = np.diff(Adata[:,0])
    tofChange = np.append([np.float64(1)], tofChange)
    ###tofChange[tofChange != 0] = 1
    index = np.flatnonzero(tofChange)
    index = np.append(index,[np.int64(len(tofChange))])
    
    Bdata  = Adata[:,2:5] 
    Bdata  =  np.concatenate((Bdata,tofChange[:,None]),axis=1)
 
    # col 1 time stamp, col 2 channel, col 3 ADC, 
    # col 4 global time reset delta in ms moved to DGTime
    
    #Bdata[2:10,0] = range(444008,444000,-1)
    
    if ordertime == 1:
        for k in range(0,Ntoffi,1):
        #    print(index[k])
            temp = Bdata[index[k]:index[k+1],:]
            temp = temp[temp[:,0].argsort(),]
            Bdata[index[k]:index[k+1]] = temp
            
    Bdata[:,0] = Bdata[:,0]*Clockd       # time in s 
    
    DGTime = Bdata[:,3]
    
    Cdata  = Bdata[:,0:3]
    
    
elapsed2 = time.time() - t2
print('--> time el.: ' + str(elapsed2) + ' s')  
    
###############################################################################
###############################################################################

# t3 = time.time()

# temp = h5py.File(datapathinput+filename, "r")


# elapsed3 = time.time() - t3
# print('--> time el.: ' + str(elapsed3) + ' s')  

# t3 = time.time()

# temp = np.array(pd.read_hdf((datapathinput+filename),'mbcaen_readouts'))


# elapsed3 = time.time() - t3
# print('--> time el.: ' + str(elapsed3) + ' s')  

###############################################################################
###############################################################################

t3 = time.time()



# k = f.keys()

# print(k)

# for key in f.keys():
#       print(key)

# namemain = list(f.keys())

# if len(namemain) > 1:
#     print('WARNING more than one dataset in h5 file -> exiting.')
#     flag  = -1
#     # data = 0


# namemain = 'mbcaen_readouts'
    
# mr = f['/entry/mr_scan/mr']
# i00 = f['/entry/mr_scan/I00']
# print("%s\t%s\t%s" % ("#", "mr", "I00"))
# for i in range(len(mr)):
#     print("%d\t%g\t%d" % (i, mr[i], i00[i]))

# ff = f[namemain[0]][()]

# for k in ff.dtype():
#       print(k)
      
# data1 = ff

# ddaf = data1([()])

# names = list(ff.dtype.names)

# orderednames = ['global_time','digitizer','local_time','channel','adc']

# for name in names :
#     print(name)

######################
    
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

######################
                
if not(digitID in DATA[:,1]): #if the digitID does not exist in the file 
    
    Cdata  = np.ones([2,3], dtype='float64' )*np.inf
    Ntoffi = np.array([1], dtype='float64' )*np.inf
    GTime  = np.array([1], dtype='float64' )*np.inf
    DGTime = np.array([1], dtype='float64' )*np.inf
    flag   = -1
    presentdigit = np.unique(DATA[:,1])
    print('\n \t No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
    for digit in presentdigit:
        print(digit,end=' ')
           
else:
    
    flag   = 0
    
    selectdigi = DATA[:,1] == digitID

    Adata = DATA[selectdigi,:]
    
    ## CH NUMBER FROM 0 NOT FROM 1 AS MATLAB !!!!! OTHERVIWISE ADD A LINE HERE TO ADD +1
#        uncomment for ch from 1 to 64
    # Adata[:,3] = Adata[:,3]+np.float64(1) ## ch is from 1 to 64
    
    GTime  = np.unique(Adata[:,0]) 
    Ntoffi = len(GTime)
    
    #plt.plot(GTime)
    
    tofChange = np.diff(Adata[:,0])
    tofChange = np.append([np.float64(1)], tofChange)
    ###tofChange[tofChange != 0] = 1
    index = np.flatnonzero(tofChange)
    index = np.append(index,[np.int64(len(tofChange))])
    
    Bdata  = Adata[:,2:5] 
    Bdata  =  np.concatenate((Bdata,tofChange[:,None]),axis=1)
 
    # col 1 time stamp, col 2 channel, col 3 ADC, 
    # col 4 global time reset delta in ms moved to DGTime
    
    #Bdata[2:10,0] = range(444008,444000,-1)
    
    if ordertime == 1:
        for k in range(0,Ntoffi,1):
        #    print(index[k])
            temp = Bdata[index[k]:index[k+1],:]
            temp = temp[temp[:,0].argsort(),]
            Bdata[index[k]:index[k+1]] = temp
            
    Bdata[:,0] = Bdata[:,0]*Clockd       # time in s 
    
    DGTime = Bdata[:,3]
    
    Cdata  = Bdata[:,0:3]
    

    
    
    
    
# for j in len(orderednames):
#     print(j)
#     for k in len(names):
#         print(k)
#         if orderednames[j] in names[k]:
#             data[:,j] = ff[names[k]]

    
# indices = [i for i, orderednames[0] in enumerate(names) if orderednames[0] in names]

# items = list(ff.dtype())

# ad = ff['adc']
     
# dataset = f[namemain[0]]['adc']

# dataset2 = f['mbcaen_readouts'][()]

# # data2 = f.get('mbcaen_readouts')

# data2 = np.array(dataset)[()]

# # data = dataset[()]     







elapsed3 = time.time() - t3
print('--> time el.: ' + str(elapsed3) + ' s')  


