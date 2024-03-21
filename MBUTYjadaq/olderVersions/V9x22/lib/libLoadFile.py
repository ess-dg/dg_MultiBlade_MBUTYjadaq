#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 08:32:38 2020

@author: francescopiscitelli
"""

import numpy as np
import h5py
# import os

# NOTE: this module already supports 32 wires and 64 strips 

###############################################################################
###############################################################################

#this is the equivalent of the MATALB function 
#[DATA,Ntoffi,GTime] = readHDFEFUfile(datapathinput,filename,digitID,ordertime)
# output data 4 columns, col 0 time stamp, col 1 ch num from 0 to 63, col 2 ADC value, col 3 reset of ToF in ms

def readHDFefu (datapathinput,filename,digitID,Clockd,ordertime=1):
    
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
        
        # GTime  = np.unique(Adata[:,0]) 
        # Ntoffi = len(GTime)
        
        # #plt.plot(GTime)
        
        # tofChange = np.diff(Adata[:,0])
        # tofChange = np.append([np.float64(1)], tofChange)
        # ###tofChange[tofChange != 0] = 1
        # # index = np.flatnonzero(tofChange)
        # index = np.argwhere(tofChange > 0.1)
        # index = np.append(index,[np.int64(len(tofChange))])
        
        GTime, index  = np.unique(Adata[:,0], return_index=True) 
        Ntoffi = len(GTime)
        
        tofChange = np.zeros((len(Adata))) 
        tempt      = np.diff(Adata[:,0])
        tempt      = np.append([np.float64(1)], tempt)
        tofChange[index] = tempt[index]
        
        index = np.append(index,[np.int64(len(tofChange))])
        
        Bdata  = np.float64(Adata[:,2:5]) 
        # Bdata  =  np.concatenate((Bdata,tofChange[:,None]),axis=1)
     
        # col 1 time stamp, col 2 channel, col 3 ADC, 
        # col 4 global time reset delta in ms moved to DGTime
        
        #Bdata[2:10,0] = range(444008,444000,-1)
        
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
                
    return Bdata, Ntoffi, GTime, DGTime, flag

###############################################################################
###############################################################################
    
def readHDFjadaq (datapathinput,filename,digitID,Clockd,ordertime=1):

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
            print('\n \t \033[1;33mWARNING: No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
            for digit in presentdigit:
                print(digit,end=' ')
            print('\033[1;37m')
    
    else:
        
            flag = 0 
      
            digitgroup = f[str(digitID)]
            
            Ntoffi = len(digitgroup.items())
            
            GTime  = np.zeros([Ntoffi],dtype = 'uint64')
            
    
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
                      
    return Cdata, Ntoffi, GTime, DGTime, flag

###############################################################################
###############################################################################

def readHDFjadaqTraces (datapathinput,filename,digitID,Clockd,ordertime=1):

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
            print('\n \t \033[1;33mWARNING: No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
            for digit in presentdigit:
                print(digit,end=' ')
            print('\033[1;37m')
    
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
                        
                        print('\n \t \033[1;33mWARNING: Digit ',str(digitID),' has no samples! Only QDC data loaded.\033[1;37m')
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
                        overTh       = 0
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
        
    f.close()    
                    
    return Cdata, Ntoffi, GTime, DGTime, flag, numSamples, preTrigger, gate, holdOff, overTh, traceData

###############################################################################
###############################################################################
    
def readHDFreducedFile (datapathinput,filename,digitID):

    f = h5py.File(datapathinput+filename, "r")
    
    for key in f.keys():
           # print(key)
           name = key
         
    ff = f[name]
    
    # for key in ff.keys():
    #       print(key)
    
    try:
        rtemp = ff['run']
        duration = rtemp['TotalDuration'][()]
        durationAll = rtemp['Durations'][()]
    except:
        print('--> no run info')
        duration = 0
        durationAll = 0
  
    try:
        mtemp   = ff['monitor']
        MONdata = mtemp['data'][()]  #
        MONcounts = mtemp['counts'][()]  #
    except:
        print('--> no monitor')
        MONdata = np.ones((1,2),dtype=float)*np.inf
        MONcounts = 0
    
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
            print('\n \t \033[1;33mWARNING: No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
            for digit in presentDigit:
                print(np.int(digit),end=' ')
            print('\033[1;37m')
            
        else:
    
            selDigit = stringToFind+str(digitID)
        
            for k in range(len(items)):    
                if selDigit in items[k]:
                    # print(items[k])
                    data = dtemp[selDigit]['data'][()]
                   
    except:
        print('\033[1;33m-->WARNING: no detector data\033[1;37m')
        # arrangement = 0
        data        = np.ones((1,9),dtype=float)*np.inf
        
    f.close() 
       
    return data, MONdata, MONcounts, duration, durationAll