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
import time
from PyQt5.QtWidgets import QFileDialog

# import the library with all specific functions that this code uses 
from lib import libSyncUtil as syu 
from lib import libLoadVMMfile as lofv 
from lib import libHistog as hh
from lib import libMBUTY_V9x15 as mbl 

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
pathsource        = 'mg@10.0.0.3:/home/mg/dataVMMutgard2/'

desitnationpath   = '/Users/francescopiscitelli/Desktop/temp/dataVMMutgard2/'

datapath = '/Users/francescopiscitelli/Desktop/reducedFile/'

# datapath          = desitnationpath 
datapath          = os.path.abspath('.')+'/data/' 

# datapath = '/Users/francescopiscitelli/Documents/DOC/DATA/2020_04/04_VMM_2hybr_ClusteringTestFunctGen/'

filename = 'AmBeSource1526gdgem-readouts-20190819-152708_00000.h5'

# filename = 'almostgdgem_readouts_20200402-154729_00000.h5'

openWindowToSelectFiles = 2
     #  0 = filename is loaded, no window opens 
     #  1 = filename is ignored, no window open, last created file in directory is loaded automatically 
     #  2 = filename is ignored, window opens to selct the file 
     
###############################################################################

Clockd      = 1e-9   #s clock steps

Timewindow  = 2e-6   #s time window for clustering 

plotTimeStamps   =   1

plotChRaw        =   1

plotPHS          =   0


###############################################################################

#  wires FEC VMM channels, strips FEC VMM channels

Cassette2chipID = {5: ['w', 2, 4, np.arange(0,32), 's', 2, 3, np.arange(32,64),'r'],
                   6: ['w', 2, 4, np.arange(32,64), 's', 2, 3, np.arange(0,31),'g'],
                   7: ['w', 2, 5, np.arange(0,32), 's', 2, 2, np.arange(32,64),'b'],
                   8: ['w', 2, 5, np.arange(32,64), 's', 2, 2, np.arange(0,32),'k']}

clusterize           = 1    # ON/OFF

cassetteToClusterize = [5,6] 

# cassetteToClusterize = [5]

###############################################################################
# mapping channels into geometry 

MAPPING =    1     # ON/OFF, if OFF channels are used as in the file

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
###############################################################################
###############################################################################
###############################################################################
#  syncing the data from remote computer where files are written
if sync == 1:
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

if MAPPING == 0:
   print(' ---> Mapping OFF ...') 
elif MAPPING == 1:
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

if plotTimeStamps == 1:
    
    X = np.arange(0,data.shape[0],1)
    
    fig2, ax2 = plt.subplots(1, 1, figsize=(9,5))
    ax2.plot(X,data[:,0],color='r',marker='+',linestyle='')
    ax2.set_xlabel('row num.')
    ax2.set_ylabel('time stamp (s)')
    
    
###############################################################################
###############################################################################

if plotChRaw == 1:
    
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

if clusterize == 1:
    
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