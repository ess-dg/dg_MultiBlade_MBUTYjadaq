#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 08:25:09 2020

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

filename = 'JADAQ-traces-file_00000.h5'



#  NOTE it works on CAEN V1740D config that has the same settings for all signals, 
#  common pretrigger, pregate etc....


###############################################################################
###############################################################################

# def readHDFjadaqTraces (datapathinput,filename,digitID,Clockd,ordertime=1):

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
        
        Ntoffi = len(digitgroup.items())
        
        GTime  = np.zeros([Ntoffi],dtype = 'uint64')
        
        # for k in digitgroup.visit():
        #    print(k)
    
        # group = ()
        
        # for i in range(len(f.keys())):
        #     group = np.append(group, list(f.keys())[i])
        
        cont = 0 

        for k, dset in enumerate(digitgroup.keys()) :
        # for k in range(1):
            
        #     dset = '0'
            
            # print(dset, k )
            
            GTime[k] = np.int64(dset)
            
            dsetsel = digitgroup[dset][()]
            
            temp = dsetsel['time']
            
            dataTemp = np.zeros((len(temp),3))
            
            # # col 1 time stamp, col 2 channel, col 3 ADC, 
            dataTemp[:,0] = temp
            dataTemp[:,1] = dsetsel['channel']
            dataTemp[:,2] = dsetsel['charge']
            
            try: 
                
                traceTemp = dsetsel['samples']
                samplesFound = 1
                
            except:
                
                samplesFound = 0
                 
                if cont == 0:
                    
                    print('\n \t WARNING: Digit ',str(digitID),' has no samples! Only QDC data loaded.')
                    cont += 1
                    
                    # numSamples   = 0
                    # preTrigger   = 0
                    # gateStart    = 0 
                    # gateStop     = 0
                    # holdOffStart = 0 
                    # holdOffStop  = 0
                    # overThStart  = 0
                    # overThStop   = 0
                    # traceData    = 0
                    
                    numSamples   = 0
                    preTrigger   = 0
                    gate         = 0
                    holdOff      = 0 
                    overThStart  = 0
                    traceData    = 0
                
                if ordertime == 1:
                    dataTemp  = dataTemp[dataTemp[:,0].argsort(),]
                    
                if k == 0:
                    Cdata     =  dataTemp
                   
                else:
                    Cdata     =  np.concatenate((Cdata,dataTemp),axis=0)
                    
            if samplesFound == 1:
                
                # if k == 0:
                # numSamples   = dsetsel['num_samples'][0]
                # preTrigger   = dsetsel['trigger'][0]
                # gateStart, gateStop        = dsetsel['gate'][0]
                # holdOffStart, holdOffStop  = dsetsel['holdoff'][0]
                # overThStart,  overThStop   = dsetsel['overthreshold'][0]
                
                numSamplesTemp   = dsetsel['num_samples']
                preTriggerTemp   = dsetsel['trigger']
                gateTemp         = dsetsel['gate']
                holdOffTemp      = dsetsel['holdoff']
                overThTemp       = dsetsel['overthreshold']
               
                # traceTemp = dsetsel['samples']
            
                if ordertime == 1:
                    
                    reoder         = dataTemp[:,0].argsort()
                    
                    dataTemp       = dataTemp[reoder,]
                    traceTemp      = traceTemp[reoder,]
                    numSamplesTemp = numSamplesTemp[reoder,]
                    preTriggerTemp = preTriggerTemp[reoder,]
                    gateTemp       = gateTemp[reoder,]
                    holdOffTemp    = holdOffTemp[reoder,]
                    overThTemp     = overThTemp[reoder,]
                    
                if k == 0:
                    Cdata      = dataTemp
                    traceData  = traceTemp
                    numSamples = numSamplesTemp
                    preTrigger = preTriggerTemp
                    gate       = gateTemp
                    holdOff    = holdOffTemp
                    overTh     = overThTemp
                    
                else:
                    Cdata      =  np.concatenate((Cdata,dataTemp),axis=0)
                    traceData  =  np.concatenate((traceData,traceTemp),axis=0)
                    numSamples =  np.concatenate((numSamples,numSamplesTemp),axis=0)
                    preTrigger =  np.concatenate((preTrigger,preTriggerTemp),axis=0)
                    gate       =  np.concatenate((gate,gateTemp),axis=0)
                    holdOff    =  np.concatenate((holdOff,holdOffTemp),axis=0)
                    overTh     =  np.concatenate((overTh,overThTemp),axis=0)
  
                       
        
        DGTime = np.zeros([len(Cdata)], dtype='float64' )
               
        Cdata[:,0] = Cdata[:,0]*Clockd       # time in s 
    
# f.close()    
                    
    # return Cdata, Ntoffi, GTime, DGTime, flag, numSamples, preTrigger, gateStart, gateStop, holdOffStart, holdOffStop, overThStart, overThStop, traceData

     
        