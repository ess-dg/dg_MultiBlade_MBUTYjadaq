#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 10:43:28 2020

@author: francescopiscitelli

"""

import numpy as np
# import pandas as pd
import h5py
import os
# import sys

###############################################################################
############################################################################### 

def loadVMMdata (datapathinput,filename,Clockd):

    f  = h5py.File(datapathinput+filename, "r")
    
    ff = f['srs_hits'][()]   
    
    fec             = ff['fec']
    chip_id         = ff['chip_id']
    srs_timestamp   = ff['srs_timestamp']
    channel         = ff['channel']
    # bcid            = ff['bcid']
    # tdc             = ff['tdc']
    adc             = ff['adc']
    # over_threshold  = ff['over_threshold']
    chiptime        = ff['chiptime']
    
    f.close()
    
    ################################
    
    # Nrows = np.shape(fec)[0]
    
    # FECs = np.float64(np.unique(fec))
    # Nfec = np.shape(FECs)[0]
    
    # VMMs = np.float64(np.unique(chip_id))
    # Nvmm = np.shape(VMMs)[0]
    
    Nrows = np.shape(fec)[0]
    
    # if Nrows == 0:
    #     print(' ---> Exiting ... \n')
    #     print('------------------------------------------------------------- \n')
    #     sys.exit()
    
    FECs = np.array(np.float64(np.unique(fec)))
    Nfec = np.size(FECs)
    FECs.shape = (Nfec)
    
    VMMs = np.array(np.float64(np.unique(chip_id)))
    Nvmm = np.size(VMMs)
    VMMs.shape = (Nvmm)
    
    Nhybrids  = np.int(np.ceil(Nvmm/2))
    
    print('--> ',str(Nrows),' rows found with ',str(Nfec),' FEC and with ',str(Nvmm),' VMMs (',str(Nhybrids),' hybrids)')
    
    ################################
    
    time = (srs_timestamp+chiptime)*Clockd
    
    DATA = np.concatenate((time[:,None],fec[:,None],chip_id[:,None],channel[:,None],adc[:,None]),axis = 1)

    return DATA, Nrows, Nfec, FECs, Nhybrids, Nvmm, VMMs

###############################################################################
###############################################################################  

def syncData (pathsource,desitnationpath):

# pathsource = '/Users/francescopiscitelli/Desktop/aa/*'
# desitnationpath = '/Users/francescopiscitelli/Desktop/bb'


    command = 'rsync -av --progress'

    # command = 'cp'
    
    comm = command + ' ' + pathsource + ' ' + desitnationpath
    
    # print(comm)
    
    print('\n ... syncing data ...');
    
    status = os.system(comm);
    
    # NOTE: it will ask for password 
    
     # disp(cmdout)
    
    if status == 0: 
          print('\n data sync completed')
    else:
          print('\n ERROR ... \n')
    
    # print(status)      
          
    print('\n-----')
    
    return status 
    
###############################################################################
###############################################################################
    
def hist1(xbins,xvar,outBounds=True):

    binX   = len(xbins) 
        
    Xmin   = np.min(xbins) 
    Xmax   = np.max(xbins) 

    hist   = np.zeros(binX) 
    
    index = np.int_(np.around(((binX-1)*((xvar-Xmin)/(Xmax-Xmin)))))
    
    if outBounds == False:
        if not(np.all(index >= 0) and np.all(index <= binX-1)):
            print('warning: hist out of bounds, change limits!') 
    
    for k in range(binX):    
        hist[k] = np.sum(index == k) 
       
        if outBounds == True:
            # fill overflow last bin and first bin
            hist[0]  += np.sum(index<0)
            hist[-1] += np.sum(index>binX-1)
        
    return hist