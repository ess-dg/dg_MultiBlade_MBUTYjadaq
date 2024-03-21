#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 11:34:58 2020

@author: francescopiscitelli
"""
import os
import math as mt
import pandas as pd
import numpy  as np
import h5py
 # input m and s, output in A


desitnationpath     = '/Users/francescopiscitelli/Documents/DOC/DATA/2018_11/DATA_PSI/DATAraw/C_Masks/'
datapath            = desitnationpath 

savereducedpath = '/Users/francescopiscitelli/Desktop/dest/'


filename = '13827-C-ESSmask-20181116-120805_00000.h5'

outfile = savereducedpath+'myfile.h5'

if os.path.exists(outfile) == True:
   print('\n WARNING: Reduced DATA file exists, it will be overwritten! \n')
   os.system('rm '+outfile)


# f = pd.read_hdf((datapath+filename),'mbcaen_readouts')

DATA = np.array(pd.read_hdf((datapath+filename),'mbcaen_readouts'))
    
  
# with h5py.File(outfile, "w") as fid:
# dset = fid.create_dataset("mydataset", (100,), dtype='i')


  
fid    = h5py.File(outfile, "w")    

dset = fid.create_dataset('gr/mydataset', data=DATA)

fid.close()