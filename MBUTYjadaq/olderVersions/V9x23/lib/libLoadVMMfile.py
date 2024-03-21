#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 08:43:26 2020

@author: francescopiscitelli
"""
import numpy as np
# import pandas as pd
import h5py

# NOTE: this module already supports 32 wires and 64 strips 

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
    
    print(' ---> ',str(Nrows),' rows found with ',str(Nfec),' FEC and with ',str(Nvmm),' VMMs (',str(Nhybrids),' hybrids)')
    
    ################################
    
    time = (srs_timestamp+chiptime)*Clockd
    
    DATA = np.concatenate((time[:,None],fec[:,None],chip_id[:,None],channel[:,None],adc[:,None]),axis = 1)

    return DATA, Nrows, Nfec, FECs, Nhybrids, Nvmm, VMMs


###############################################################################
###############################################################################