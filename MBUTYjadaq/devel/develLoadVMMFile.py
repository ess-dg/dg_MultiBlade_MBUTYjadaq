#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 13:59:56 2020

@author: francescopiscitelli
"""

import numpy as np
# import pandas as pd
import h5py
import os

###############################################################################

# datapathinput  = '/Users/francescopiscitelli/Desktop/temp/dataVMMutgard/'

datapathinput            = os.path.abspath('../')+'/data/' 

# filename = 'almostgdgem_readouts_20200402-154729_00000.h5'

filename = 'AmBeSource1526gdgem-readouts-20190819-152708_00000.h5'

# filename = 'Testinggdgem_readouts_20200402-133556_00000.h5'

Clockd = 1e-9  # clock is 1ns

###############################################################################


# DATA = np.array(pd.read_hdf((datapathinput+filename),'srs_hits'))

# TIME = (DATA[:,2]+DATA[:,8])*Clockd   # in s

# # check ch num has to start from 0 

# FEC = DATA[:,0]

# ChipID = DATA[:,1]

# CH  = DATA[:,3]
# ADC = DATA[:,6]



# # MyDict =	{
# #   "cassette": 33,
# #   "wires_fec": 2,
# #   "wires_chip": 3,
# #   "strips_fec": 2,
# #   "strips_chip": 5,
  
# #   "cassette": 33,
# #   "wires_fec": 2,
# #   "wires_chip": 3,
# #   "strips_fec": 2,
# #   "strips_chip": 5,
# # }

# fec2cass = np.zeros((6,5))

# fec2cass[0,0] = 33
# fec2cass[0,1] = 2
# fec2cass[0,2] = 3
# fec2cass[0,3] = 2
# fec2cass[0,4] = 5

# fec2cass[1,0] = 34
# fec2cass[1,1] = 2
# fec2cass[1,2] = 4
# fec2cass[1,3] = 2
# fec2cass[1,4] = 3

# digitID = [33]

# indexcass = np.argwhere(fec2cass[:,0] == digitID)

# selectionw = np.logical_and( DATA[:,0] == fec2cass[indexcass,1] , DATA[:,1] == fec2cass[indexcass,2] )

# data_w = DATA[selectionw[0,:],:]

# # TIME = (data_w[:,2]+data_w[:,8])*Clockd   # in s

# # etc....

# selections = np.logical_and( DATA[:,0] == fec2cass[indexcass,3] , DATA[:,1] == fec2cass[indexcass,4] )

# data_s = DATA[selections[0,:],:]


###############################################################################
###############################################################################


f  = h5py.File(datapathinput+filename, "r")

ff = f['srs_hits'][()]   

fec             = ff['fec']
chip_id         = ff['chip_id']
srs_timestamp   = ff['srs_timestamp']
channel         = ff['channel']
bcid            = ff['bcid']
tdc             = ff['tdc']
adc             = ff['adc']
over_threshold  = ff['over_threshold']
chiptime        = ff['chiptime']

f.close()

################################

Nrows = np.shape(fec)[0]

# FECs = np.zeros(None)

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
