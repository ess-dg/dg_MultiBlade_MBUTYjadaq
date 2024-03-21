#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 10:45:25 2020

@author: francescopiscitelli
"""

###############################################################################
###############################################################################
########    V1.0  2020/04/04      francescopiscitelli    ######################
###############################################################################
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import sys
from PyQt5.QtWidgets import QFileDialog

# import the library with all specific functions that this code uses 
from lib import VMMloadLIB as vl 

###############################################################################
# tProfilingStart = time.time()
print('----------------------------------------------------------------------')
plt.close("all")
###############################################################################
###############################################################################
########    here starts the section with all the settings you can choose  #####
###############################################################################
###############################################################################

sync = 0   #ON/OFF if you want to rsync the data 

###############################################################################

# pathsource         = 'mg@192.168.0.60:/home/mg/dataVMMutgard/'
pathsource         = 'mg@10.0.0.3:/home/mg/dataVMMutgard2/'

desitnationpath    = '/Users/francescopiscitelli/Desktop/temp/dataVMMutgard2/'

datapath            = desitnationpath 
# datapath            = os.path.abspath('.')+'/data/' \

# datapath = '/Users/francescopiscitelli/Documents/DOC/DATA/2020_04/VMM_SRS_testsFunctGenAtutgard/'

filename = 'AmBeSource1526gdgem-readouts-20190819-152708_00000.h5'

# filename = 'almostgdgem_readouts_20200402-154729_00000.h5'

openWindowToSelectFiles = 2
     #  0 = filename is loaded, no window opens 
     #  1 = filename is ignored, no window open, last created file in directory is loaded automatically 
     #  2 = filename is ignored, window opens to selct the file 
     
###############################################################################

Clockd             = 1e-9   #s clock steps

###############################################################################

PlotPHS     =   1

###############################################################################
###############################################################################
########    end of with all the settings you can choose   #####################
########        DO NOT EDIT BELOW THIS LINE!!!!           #####################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
#  syncing the data from remote computer where files are written
if sync == 1:
   vl.syncData(pathsource,desitnationpath)
###############################################################################
###############################################################################
#selecting files 

if openWindowToSelectFiles == 0:
    fname = filename

elif openWindowToSelectFiles == 1: 
    listOfFiles = glob.glob(datapath+'/*.h5') 
    if not len(listOfFiles):
        print('\n No file exists in directory \n')
        print(' ---> Exiting ... \n')
        print('------------------------------------------------------------- \n')
        sys.exit()   
    latestFile  = max(listOfFiles, key=os.path.getmtime)
    temp        = os.path.split(latestFile)
    datapath    = temp[0]+'/'
    fname       = temp[1]
    
elif openWindowToSelectFiles == 2:
    temp = QFileDialog.getOpenFileName(None, "Select Files", datapath, "hdf files (*.h5)")
    temp = os.path.split(temp[0])
    datapath = temp[0]+'/'
    fname = temp[1]
    if fname == "":
        print('\n Nothing selected! \n')
        print(' ---> Exiting ... \n')
        print('------------------------------------------------------------- \n')
        sys.exit()
        
else:
    print('\n Please select a correct open file mode! \n')
    print(' ---> Exiting ... \n')
    print('------------------------------------------------------------- \n')
    sys.exit()
    
# print('\n File selected: '+datapath)      
print('File selected: '+fname)

###############################################################################
###############################################################################
#loading file

data, Nrows, Nfec, FECs, Nhybrids, Nvmm, VMMs = vl.loadVMMdata(datapath,fname,Clockd)
   
# data[0] = time
# data[1] = fec
# data[2] = chip_id
# data[3] = channel
# data[4] = adc


###############################################################################
###############################################################################

fig, ax = plt.subplots(Nhybrids, 2, figsize=(11,6), sharex='col')
# , sharey='row')  

Xaxis  = np.arange(0,64,1)

for k in range(Nvmm):
    
    selection = data[:,2] == VMMs[(k)]
    hiscounts = vl.hist1(Xaxis,data[selection,3])   

    indexRow = np.int(np.floor(k/2))
    indexCol = np.int(np.mod(k,2))
    
    # print(str(indexRow) + ' - '+str(indexCol))
           
    if Nvmm > 2: 
        ax[indexRow][indexCol].bar(Xaxis[:32],hiscounts[:32],0.8,color='r')
        ax[indexRow][indexCol].bar(Xaxis[32:],hiscounts[32:],0.8,color='b')
        ax[indexRow][indexCol].set_xlabel('raw ch no.')
        ax[indexRow][indexCol].set_ylabel('counts')
        ax[indexRow][indexCol].set_title('VMM '+str(np.int(VMMs[k])))
    
    else:
        ax[indexCol].bar(Xaxis[:32],hiscounts[:32],0.8,color='r')
        ax[indexCol].bar(Xaxis[32:],hiscounts[32:],0.8,color='b')
        ax[indexCol].set_xlabel('raw ch no.')
        ax[indexCol].set_ylabel('counts')
        ax[indexCol].set_title('VMM '+str(np.int(VMMs[k])))
    
   
    # if PLotPHS == 1:
    #     histPHS = vl.hist2(Xaxis,data[selection,3])   

        







###############################################################################
###############################################################################
print('----------------------------------------------------------------------')