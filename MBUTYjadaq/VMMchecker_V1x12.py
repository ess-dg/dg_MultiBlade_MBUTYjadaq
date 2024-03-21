#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 10:45:25 2020

@author: francescopiscitelli
"""

###############################################################################
###############################################################################
########    V1.12  2021/04/16     francescopiscitelli    ######################
###############################################################################
###############################################################################

# NOTE: this code assumes only 1 FEC!

import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import sys
import time
from PyQt5.QtWidgets import QFileDialog
from matplotlib.colors import LogNorm

# import the library with all specific functions that this code uses 
from lib import libSyncUtil as syu 
from lib import libLoadVMMfile as lofv 
from lib import libHistog as hh
from lib import libMBUTY_V9x24 as mbl 

###############################################################################
# tProfilingStart = time.time()
print('----------------------------------------------------------------------')
plt.close("all")
###############################################################################
###############################################################################
########    here starts the section with all the settings you can choose  #####
###############################################################################
###############################################################################

sync = False   #ON/OFF if you want to rsync the data 

###############################################################################

# pathsource         = 'mg@192.168.0.60:/home/mg/dataVMMutgard/'
pathsource        = 'vmm3@172.30.244.205:/home/vmm3/data/efu_dump/'

desitnationpath   = '/Users/francescopiscitelli/Documents/DOC/DATA/2021_04/UtgardDataVMM/'

# datapath          = desitnationpath 
datapath          = os.path.abspath('.')+'/data/' 

# datapath = '/Users/francescopiscitelli/Documents/DOC/DATA/2020_04/04_VMM_2hybr_ClusteringTestFunctGen/'

filename = 'AmBeSource1526gdgem-readouts-20190819-152708_00000.h5'

# filename = 'almostgdgem_readouts_20200402-154729_00000.h5'

openWindowToSelectFiles = 0
     #  0 = filename is loaded, no window opens 
     #  1 = filename is ignored, no window open, last created file in directory is loaded automatically 
     #  2 = filename is ignored, window opens to selct the file 
     
###############################################################################

Clockd      = 1e-9   #s clock steps

###############################################################################

plotTimeStamps   =   True   # ON/OFF

plotChRaw        =   True    # ON/OFF

###############################################################################
# PHS image of all ch in each VMM
             
EnerHistIMG   = True            # ON/OFF

plotEnerHistIMGinLogScale = True   # ON/OFF

energybins    = 128
maxenerg      = 1050

###############################################################################
# CLUSTERING

#  wires FEC VMM channels, strips FEC VMM channels

Cassette2chipID = {0: ['w', 2, 0, np.arange(0,32), 's', 2, 3, np.arange(32,64),'r'],
                    1: ['w', 2, 0, np.arange(32,64), 's', 2, 3, np.arange(0,31),'g'],
                    2: ['w', 2, 1, np.arange(0,32), 's', 2, 2, np.arange(32,64),'b'],
                    3: ['w', 2, 1, np.arange(32,64), 's', 2, 2, np.arange(0,32),'k']}

# Cassette2chipID = {0: ['w', 2, 0, np.arange(32,64), 's', 2, 1, np.arange(0,32),'r']}

Timewindow  = 2e-6   #s time window for clustering 

clusterize           = True    # ON/OFF

cassetteToClusterize = [0] 

###############################################################################
# mapping channels into geometry 

MAPPING =    False     # ON/OFF, if OFF channels are used as in the file

# mappath = '/Users/francescopiscitelli/Documents/PYTHON/MBUTY/tables/'
mappath = os.path.abspath('.')+'/tables/'
mapfile = 'MB18_mapping.xlsx'

###############################################################################


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

if plotEnerHistIMGinLogScale is True:
    normColorsPH = LogNorm()
elif plotEnerHistIMGinLogScale is False:
    normColorsPH = None

###############################################################################
###############################################################################
###############################################################################
#  syncing the data from remote computer where files are written
if sync is True:
   syu.syncData(pathsource,desitnationpath)
###############################################################################
###############################################################################
#selecting files 

if openWindowToSelectFiles == 0:
    fname = filename
    
    # check if file exists in folder
    if os.path.exists(datapath+filename) == False:
           print('\n \033[1;31m---> File: '+filename+' DOES NOT EXIST \033[1;37m')
           print('\n ---> in folder: '+datapath+' \n')
           print(' ---> Exiting ... \n')
           print('------------------------------------------------------------- \n')
           sys.exit()

elif openWindowToSelectFiles == 1: 
    listOfFiles = glob.glob(datapath+'/*.h5') 
    if not len(listOfFiles):
        print('\n \033[1;31mNo file exists in directory \033[1;37m\n')
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
        print('\n \033[1;31mNothing selected! \033[1;37m\n')
        print(' ---> Exiting ... \n')
        print('------------------------------------------------------------- \n')
        sys.exit()
        
else:
    print('\n \033[1;31mPlease select a correct open file mode! \033[1;37m\n')
    print(' ---> Exiting ... \n')
    print('------------------------------------------------------------- \n')
    sys.exit()
    
# print('\n File selected: '+datapath)      
print('\033[1;36mFile selected: '+fname+' \033[1;37m\n')

###############################################################################
###############################################################################
#  load mapping fro specific detector 

if MAPPING is False:
   print(' ---> Mapping OFF ...') 
elif MAPPING is True:
   mapfullpath = mappath+mapfile         
   if os.path.exists(mapfullpath) == False:
      print('\n \033[1;33m---> WARNING ... File: '+mapfullpath+' NOT FOUND\033[1;37m')
      print("\t ... Mapping switched OFF ... ")
      MAPPING = 0
      time.sleep(2)
   else:
      print(' ---> Mapping ON ... Loading Mapping File ...')
      
###############################################################################
###############################################################################
#loading file

data, Nrows, Nfec, FECs, Nhybrids, Nvmm, VMMs = lofv.loadVMMdata(datapath,fname,Clockd)
   
# data[0] = time
# data[1] = fec
# data[2] = chip_id
# data[3] = channel
# data[4] = adc

# sort time stamps 
data = data[np.argsort(data[:,0]),:]

###############################################################################
###############################################################################

# PHS x-axis energy 
xener = np.linspace(0,maxenerg,energybins)

if EnerHistIMG is True:
   figphs, axphs = plt.subplots(num=601, figsize=(9,5), nrows=2, ncols=Nvmm, sharex='col', sharey='row')  
   axphs.shape   = (2,Nvmm)
   axphs         = np.atleast_2d(axphs)

###############################################################################
###############################################################################

if plotTimeStamps is True:
    
    X = np.arange(0,data.shape[0],1)
    
    fig2, ax2 = plt.subplots(1, 1, figsize=(9,5))
    ax2.plot(X,data[:,0],color='r',marker='+',linestyle='')
    ax2.set_xlabel('row num.')
    ax2.set_ylabel('time stamp (s)')
    
    
###############################################################################
###############################################################################

if plotChRaw is True:
    
    fig, ax = plt.subplots(Nhybrids, 2, figsize=(10,6), sharex='col')
    
    Xaxis  = np.arange(0,64,1)
 
    for k in range(Nvmm):
        
        # k=0
        
        indexRow = np.int(np.floor(k/2))
        indexCol = np.int(np.mod(k,2))
        # print(str(indexRow) + ' - '+str(indexCol))
    
        selection    = data[:,2] == VMMs[k]
        
        dataSelVMMCh = data[selection,3]
        
        hiscounts    = hh.hist1(Xaxis,dataSelVMMCh)   
    
        # Cassette2chipID = {5: ['w', 2, 4, np.arange(0,32), 's', 2, 3, np.arange(32,64),'k'],
        #            6: ['w', 2, 4, np.arange(32,64), 's', 2, 3, np.arange(0,31),'b'],
        #            7: ['w', 2, 5, np.arange(0,32), 's', 2, 2, np.arange(32,64),'r'],
        #            8: ['w', 2, 5, np.arange(32,64), 's', 2, 2, np.arange(0,32),'m']}
        
        # col1 = 'r'
        # col2 = 'b'
        
        # cassW = np.logical_and( data[:,2] == c2v[2] , np.in1d(data[:,3],c2v[3]) ) 
        # cassS = np.logical_and( data[:,2] == c2v[6] , np.in1d(data[:,3],c2v[7]) ) 
        
        for cc in Cassette2chipID:
        # cc = 7
            c2v  = Cassette2chipID.get(cc)
            
            col1 = 'y'
            col2 = 'y'
        
            alp1 = 0.1
            alp2 = 0.1
            
            if c2v[2] == VMMs[k]: # these are wires 
                
                if (c2v[3] <= 31).sum() > 0:
                    col1 = c2v[8]
                    alp1 = 1
                else:
                    col2 = c2v[8]
                    alp2 = 1
                
            if c2v[6] == VMMs[k]: # these are strips 
                
                if (c2v[7] <= 31).sum() > 0:
                    col1 = c2v[8]
                    alp1 = 0.5
                else:
                    col2 = c2v[8]
                    alp2 = 0.5
                   
            if Nvmm > 2: 
                ax[indexRow][indexCol].bar(Xaxis[0:32],hiscounts[0:32],0.8,color=col1,alpha=alp1)
                ax[indexRow][indexCol].bar(Xaxis[32:64],hiscounts[32:64],0.8,color=col2,alpha=alp2)
                ax[indexRow][indexCol].set_xlabel('raw ch no.')
                ax[indexRow][indexCol].set_ylabel('counts')
                ax[indexRow][indexCol].set_title('VMM '+str(np.int(VMMs[k])))
            
            else:
                ax[indexCol].bar(Xaxis[0:32],hiscounts[0:32],0.8,color=col1,alpha=alp1)
                ax[indexCol].bar(Xaxis[32:64],hiscounts[32:64],0.8,color=col2,alpha=alp2)
                ax[indexCol].set_xlabel('raw ch no.')
                ax[indexCol].set_ylabel('counts')
                ax[indexCol].set_title('VMM '+str(np.int(VMMs[k])))
            
               
            # if pLotPHS == 1:
            #     histPHS = vl.hist2(Xaxis,data[selection,3])   

###############################################################################
###############################################################################  

# data[0] = time
# data[1] = fec
# data[2] = chip_id
# data[3] = channel
# data[4] = adc

if EnerHistIMG is True:
    
    for vm in range(Nvmm):
        
       dataSelectVMM = data[data[:,2] == VMMs[vm],:]

       PHS  = np.zeros((len(xener),64)) 
           
       for chi in range(0,64,1):    # all ch
            PHS[:,chi] = hh.hist1(xener,dataSelectVMM[dataSelectVMM[:,3] == chi,4],1) 
                 

       pos1 = axphs[0][vm].imshow(np.rot90(PHS),aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],63+0.5,0-0.5], origin='lower',cmap='jet')
       figphs.colorbar(pos1, ax=axphs[0][vm], orientation="horizontal",fraction=0.07,anchor=(1.0,0.0))

       if vm == 0:
           axphs[0][vm].set_ylabel('ch. no.')
           
       axphs[0][vm].set_xlabel('pulse height (a.u.)')  
       axphs[0][vm].set_title('VMM '+str(np.int(VMMs[vm])))   
           
       #global PHS
       PHSG  = np.sum(PHS,axis=1)
       
       
       # global PHS plot
       axphs[1][vm].step(xener,PHSG,'r',where='mid')
       axphs[1][vm].set_xlabel('pulse height (a.u.)')
       if vm == 0:
            axphs[1][vm].set_ylabel('counts')                 
           

###############################################################################
###############################################################################  


if clusterize is True:
    
    Ncass = len(cassetteToClusterize)
    
      # X (w) and Y (s) axis  
    XX    = np.linspace(0,31,32)
    YY    = np.linspace(0,31,32)
    
    fig2D, ax2D = plt.subplots(1, Ncass, figsize=(9,5), sharey='col')
    
    for cc in range(len(cassetteToClusterize)):
    
        print('\n ---> Cassette '+str(cassetteToClusterize[cc]))
        
        c2v = Cassette2chipID.get(cassetteToClusterize[cc])
        
        ###### this piece of code will be a seprate function later 
        cassW = np.logical_and( data[:,2] == c2v[2] , np.in1d(data[:,3],c2v[3]) ) 
        cassS = np.logical_and( data[:,2] == c2v[6] , np.in1d(data[:,3],c2v[7]) ) 
        
        dataTemp = np.copy(data)
        
        # wires must be 0-31 and strips must be 32-64
        if (c2v[3] >= 32).sum() > 0:
            dataTemp[cassW,3] = dataTemp[cassW,3]-32
            
        if (c2v[7] <= 31).sum() > 0:
            dataTemp[cassS,3] = dataTemp[cassS,3]+32
        
        cassWS  = np.logical_or(cassW,cassS)
        
        dataCass = dataTemp[cassWS,:]
        
        dataSel  = dataCass[:,[0,3,4]]
        
        #################################################
        dataSel = mbl.mappingChToGeometry(dataSel,MAPPING,mappath,mapfile)
        #################################################
        
        # data input here is 3 cols: time stamp in s, ch 0to63, ADC,
        [POPH, Nevents, NumeventNoRej] = mbl.clusterPOPH(dataSel,Timewindow)
        
        #  POPH has 7 cols:X,Y,ToF,PHwires,PHstrips,multW,multS
        #  units:pix(0.350mm),pix(4mm),seconds,a.u.,a.u.,int,int
        #################################################      
        
        XY = hh.hist2(XX,POPH[:,0],YY,POPH[:,1],outBounds=0)
        
        if Ncass > 1:
            pos2D = ax2D[cc].imshow(XY,aspect='auto',interpolation='nearest',extent=[XX[0],XX[-1],YY[-1],YY[0]], origin='upper',cmap='jet')  
            ax2D[cc].set_xlabel('Wire ch.')
            ax2D[cc].set_ylabel('Strip ch.')
            ax2D[cc].set_title('cass '+str(cassetteToClusterize[cc]))
            fig2D.colorbar(pos2D, ax=ax2D[cc])
        else:
            pos2D = ax2D.imshow(XY,aspect='auto',interpolation='nearest',extent=[XX[0],XX[-1],YY[-1],YY[0]], origin='upper',cmap='jet')  
            ax2D.set_xlabel('Wire ch.')
            ax2D.set_ylabel('Strip ch.')
            ax2D.set_title('cass '+str(cassetteToClusterize[cc]))
            fig2D.colorbar(pos2D, ax=ax2D)
            
            
###############################################################################
###############################################################################


    # fig2D.colorbar(pos, ax=ax2D)






###############################################################################
###############################################################################
print('----------------------------------------------------------------------')