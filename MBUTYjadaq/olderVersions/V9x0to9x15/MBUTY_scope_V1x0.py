#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 13:51:09 2020

@author: francescopiscitelli
"""

###############################################################################
###############################################################################
########    V1.0  2020/03/30      francescopiscitelli    ######################
###############################################################################
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import sys
from PyQt5.QtWidgets import QFileDialog

# import the library with all specific functions that this code uses 
from lib import MBUTYLIB_scope_V1x0 as mbs 

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

pathsource         = 'efu@192.168.0.58:/home/efu/data/eszter/'

desitnationpath  = '/Users/francescopiscitelli/Desktop/try/'

# datapath            = desitnationpath 
datapath            = os.path.abspath('.')+'/data/' 

filename = 'JADAQ-traces-file_00000.h5'

openWindowToSelectFiles = 0
     #  0 = filename is loaded, no window opens 
     #  1 = filename is ignored, no window open, last created file in directory is loaded automatically 
     #  2 = filename is ignored, window opens to selct the file 
     
###############################################################################

digitID = 34

###############################################################################

gateWidth          = 320   # in samples, 16ns

###############################################################################

Clockd             = 16e-9   #s CAEN V1740D clock steps

VoltADCconversion  = 2/4096;  #V/ADC CAEN V1740D

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
   mbs.syncData(pathsource,desitnationpath)
###############################################################################
###############################################################################
#selecting files 
   
     #  0 = filename and acqnum is loaded, no window opens
     #  1 = (does nothing for the moment)
     #  2 = filename and acqnum are both ignored, window opens and 
     #      serial is the only one selected 
     #  3 = filename is ignored, window opens and serial is acqnum  
   
if openWindowToSelectFiles == 0:
    fname = filename
        
elif openWindowToSelectFiles ==1:
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
    fname    = temp[1]
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
print('File selected: '+fname+' \n')


###############################################################################
###############################################################################
#loading file

ordertime = 1

Cdata, Ntoffi, GTime, DGTime, flag, \
    numSamples, preTrigger, gate, holdOff, overTh, \
    traceData = mbs.readHDFjadaqTraces(datapath,fname,digitID,Clockd,ordertime)
   
# print('preTrigger '+str(preTrigger)) 
# print('preGate '+str(preTrigger-gate[))  
# print('gateWidth '+str(gateWidth))  

# print('\n')
###############################################################################
###############################################################################

Nevents = np.shape(Cdata)[0]

# initialize fig 
# plt.ion()
fig = plt.figure(figsize=(10,5)) 
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax3 = ax1.twiny()

for k in range(Nevents):
# for k in range(7):
    
    # k = 5
    
    Tn = np.arange(0,numSamples[k],1)

    Ts = (Clockd*(Tn-preTrigger[k]))*1e6 #in us
    
    trace  = traceData[k,:]
    
    traceV = VoltADCconversion*trace - 1
    
    threshold = trace[preTrigger[k]]
    
    gateStart = gate[k][0]
    
    ########################
    
    text = 'Event ' + str(k) + ' - channel '+ str(np.int(Cdata[k,1]))+' - PH '+str(np.int(Cdata[k,2]))
    
    print(text+' - ToF '+  '{:8.2f}'.format( Cdata[k,0]*1e3 ) +' ms')

    ########################
    # 
    ax1.set_xlabel('samples', fontsize=11)
    ax1.set_ylabel('ADC', fontsize=11)
    
    pos = ax1.get_position()
    pos.y1 = 0.85       
    ax1.set_position(pos)
    
    fig.suptitle(text, y=0.98, fontsize=14)
    
    ax2.set_ylabel('Amplitude (Volt)', fontsize=11)
    ax3.set_xlabel('time (us)', fontsize=11)
    
    ax1.xaxis.grid()
    ax1.yaxis.grid()
    
    ax1.set_xlim(0,numSamples[k])
    ax1.set_ylim(0,4096)
    
    # ax2.set_xlim(0,numSamples)
    ax2.set_ylim(-1,1)
    
    ax3.set_xlim(Ts[0],Ts[-1])
    # ax3.set_ylim(0,4096)

    ax1.plot(Tn, trace, color='red', linestyle='-', linewidth=2)
    # ax2.plot(Tn, traceV, color='tab:blue', linestyle=':', linewidth=2, marker='o')
    # ax3.plot(Ts, trace, color='tab:green', linestyle='-.', linewidth=2)

    ax1.plot([gateStart, gateStart], [0, 4096],color='green', linestyle='--', linewidth=1)
    # ax1.plot([gateStop, gateStop], [0, 4096],color='green', linestyle='-', linewidth=2)
    ax1.plot([gateStart+gateWidth, gateStart+gateWidth], [0, 4096],color='green', linestyle='--', linewidth=1)
    
    ax1.plot([preTrigger[k], preTrigger[k]], [0, 4096],color='magenta', linestyle=':', linewidth=2)
    
    ax1.plot([0, numSamples[k]], [threshold, threshold], color='magenta', linestyle=':', linewidth=2)
    
    # ax1.plot([overThStart, overThStart], [0, 4096],color='black', linestyle='-', linewidth=2)
    # ax1.plot([overThStop, overThStop], [0, 4096],color='magenta', linestyle='-', linewidth=2)


    plt.show()
    
    ########################
    
    plt.pause(0.5)
    
    inp = input('press (enter) to continue or (q + enter) to quit ')
    
    if inp == 'q':
        plt.close()
        print('----------------------------------------------------------------------')
        sys.exit()
       
    ########################
    
    ax1.clear()
    # ax2.clear()
    # ax3.clear()
    


plt.close()

    
###############################################################################
###############################################################################



# tElapsedProfiling = time.time() - tProfilingStart
# print('\n Completed --> time elapsed: %.2f s' % tElapsedProfiling)

###############################################################################
###############################################################################
print('----------------------------------------------------------------------')