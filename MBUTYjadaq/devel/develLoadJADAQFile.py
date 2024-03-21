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

digitID = digitIDtemp[0]

ordertime = 1

Clockd = 16e-9

datapathinput = os.path.abspath('../.')+'/data/' 

filename = 'JADAQ-QDC-file_00000.h5'

###############################################################################
###############################################################################

f = h5py.File(datapathinput+filename, "r")

# for key in f.keys():
#       print(key)

presentdigit = np.array(list(f.keys()),dtype=int)

if not(digitID in presentdigit):
    
        Cdata  = np.ones([2,3], dtype='float64' )*np.inf
        Ntoffi = np.array([1], dtype='float64' )*np.inf
        GTime  = np.array([1], dtype='float64' )*np.inf
        DGTime = np.array([1], dtype='float64' )*np.inf
        flag   = -1
        print('\n \t No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
        for digit in presentdigit:
            print(digit,end=' ')

else:
    
        flag = 0 
  
        digitgroup = f[str(digitID)]
        
        Notffi = len(digitgroup.items())
        
        GTime  = np.zeros([Notffi],dtype = 'uint64')
        
        # for k in digitgroup.visit():
        #    print(k)
    
        # group = ()
        
        # for i in range(len(f.keys())):
        #     group = np.append(group, list(f.keys())[i])


        for k, dset in enumerate(digitgroup.keys()) :
            
            # print(dset, k )
            
            GTime[k] = np.int64(dset)
            
            dsetsel = digitgroup[dset][()]
            
            temp = dsetsel['time']
            
            dataTemp = np.zeros((len(temp),3))
            
            # # col 1 time stamp, col 2 channel, col 3 ADC, 
            dataTemp[:,0] = temp
            dataTemp[:,1] = dsetsel['channel']
            dataTemp[:,2] = dsetsel['charge']
            
            if ordertime == 1:
                dataTemp = dataTemp[dataTemp[:,0].argsort(),]
            
            if k == 0:
                Cdata  =  dataTemp
            else:
                Cdata  =  np.concatenate((Cdata,dataTemp),axis=0)
     
         
        
        DGTime = np.zeros([len(Cdata)], dtype='float64' )
              
        
        Cdata[:,0] = Cdata[:,0]*Clockd       # time in s 
        
f.close()           
    # return Cdata, Ntoffi, GTime, DGTime, flag
            
            # cont += 1
            # print(dset)
            # temp = np.uint64(dset)
            # print(temp)
            
            # ds_data = h5py.h5f['\34'][dset]
            
            # ds_data = h5f[group][dset] # returns HDF5 dataset object
            # print (ds_data)
            # print (ds_data.shape, ds_data.dtype)
            # arr = h5f[group][dset][:] # adding [:] returns a numpy array
            # print (arr.shape, arr.dtype)
            # print (arr)
            
        
        # cont = 0 
        
    
        # for tf in digitgroup.items():
        #     print(tf)
        #     GTime[cont] = np.uint64(tf.index)
        #     cont = cont+1
            
        # for tp in digitgroup.values():
        #     print(tp)
        
        # for kk, tf in zip( range(Notffi), digitgroup.items()):
        #     print(kk)
        #     print(tf)
            # GTime[kk] = np.uint64(tf)
            
            # digitgroup['0'][()]
            
            
            
            
            # g1 = digitgroup['0'][()]


            
            # temp = g1['time']
            
            # DATAtemp = np.zeros((len(temp),3), dtype = 'uint64')
            
            # # col 1 time stamp, col 2 channel, col 3 ADC, 
            
            # DATAtemp[:,0] = temp
            # DATAtemp[:,1] = g1['channel']
            # DATAtemp[:,2] = g1['charge']
            
            
            
            
# ff = f['mbcaen_readouts'][()]    

# temp = ff['global_time']

# DATA = np.zeros((len(temp),5), dtype = 'uint64')

# DATA[:,0] = temp 
# DATA[:,1] = ff['digitizer']
# DATA[:,2] = ff['local_time']
# DATA[:,3] = ff['channel']
# DATA[:,4] = ff['adc']

# f.close() 
        
        
#         GTime  = np.array(list(temp[str(digitID[0])]), dtype = 'uint64')
        
#         Ntoffi = len(GTime)
        
#         for k in range(Ntoffi):
            
#             # aa = list(temp[str(digitID[0])+ ' ' + str(GTime[k])])
        




# # return Cdata, Ntoffi, GTime, DGTime, flag
      

# def print_attrs(name, obj):
#     print(name)
#     for key, val in obj.attrs.iteritems():
#         print("    %s: %s" % (key, val)) 
        