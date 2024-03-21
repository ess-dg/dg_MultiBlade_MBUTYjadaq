#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 14:56:50 2019

@author: francescopiscitelli
"""

###############################################################################
###############################################################################
########    V8.22 2020/02/01      francescopiscitelli    ######################
########    (this version is equivalent of version MATLAB MBUTI v8.22)    #####
###############################################################################
###############################################################################

import numpy as np
import pandas as pd
import math as mt
import matplotlib.pyplot as plt
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
import h5py

# import the library with all specific functions that this code uses 
import MBUTYLIB as mb 

###############################################################################
print('----------------------------------------------------------------------')
###############################################################################
###############################################################################
########    here starts the section with all the settings you can choose  #####
###############################################################################
###############################################################################

sync = 0   #ON/OFF if you want to rsync the data 

###############################################################################

pathsource          = ''
desitnationpath     = '/Users/francescopiscitelli/Documents/DOC/DATA/2018_11/DATA_PSI/DATAraw/C_Masks/'
datapath            = desitnationpath 

filename = '13827-C-ESSmask-20181116-120805_00000.h5'

acqnum   = [0]    #do not need to be senquential

openWindowToSelectFiles = 0
     #  0 = filename and acqnum is loaded, no window opens
     #  1 = (does nothing for the moment)
     #  2 = filename and acqnum are both ignored, window opens and 
     #      serial is the only one selected 
     #  3 = filename is ignored, window opens and serial is acqnum  

SingleFileDuration       = 60   #s to check if h5 file has all the resets

###############################################################################
# variable POPH will be saved in a new h5 file
saveReducedData = 0 #ON/OFF

savereducedpath = '/Users/francescopiscitelli/Desktop/dest/'

nameMainFolder  = 'entry1'

compressionHDFT  = 'gzip'  
compressionHDFL  = 9     # gzip compression level 0 - 9

###############################################################################

# digitID = [34,33,31,142,143,137]
digitID = [34]

###############################################################################
# switch odd and even channels  
switchOddEven  = 1   # 0 = OFF, 1 = swaps both w and s,  2 = swaps only w, 3 = swaps only s

# reverse ch number 
flipOrderCh    = 2   # 0 = OFF, 1 = flips both w and s,  2 = flips only w, 3 = flips only s (Note: wire 1 must be at front!)
                      # 1 becomes 32 and 33 becomes 64
                    
overflowcorr      = 1   #ON/OFF (does not affect the MONITOR)
zerosuppression   = 1   #ON/OFF (does not affect the MONITOR)


Clockd            = 16e-9;  #s CAEN V1740D clock steps
Timewindow        = 2e-6;   #s to create clusters 

###############################################################################

plotChRaw         = 0;      #ON/OFF plot of raw ch in the file (not flipped, not swapped) no thresholds (only for 1st serial)

plottimestamp     = 0   #ON/OFF for debugging, plot the events VS time stamp (after thresholds)

plottimeTofs      = 0   #ON/OFF for debugging, plot the time duration of ToFs (after thresholds)

ToFduration       = 0.06;    #s
ToFbinning        = 100e-6   #s

plotMultiplicity  = 1   #ON/OFF

###############################################################################
# software thresholds
# NOTE: they are applied to the flipped or swpadded odd/even order of ch!
# th on ch number: 32 w and 32 s, one row per cassette 
softthreshold = 1   # 0 = OFF, 1 = File With Threhsolds Loaded, 2 = User defines the Thresholds in an array sth 

#####

if softthreshold == 0:
    print(' ---> Thresholds OFF ...')
elif softthreshold == 1:
    
    print(' ---> Thresholds ON ... Loading Threshold File ...')

    sthpath =  '/Users/francescopiscitelli/Documents/PYTHON/MBUTY/'
    sthfile =  'ThresholdsMB182.xlsx'

    [sth,softthreshold] = mb.softThresholds(sthpath,sthfile,digitID,softthreshold)

##### User defined thresholds 
elif softthreshold == 2:
        
    print(' ---> Thresholds ON ... Defined by User ...')

    sth = np.ones((np.size(digitID,axis=0),64))
        
    # sth[0:1,0:31] = 1
    sth[0,15] = 50000
    sth[1,0:31] = 6000
        
    sth[:,31]   = 10e3

    sth[1,42] = 9000
        
    sth[0,0:31] = 25000
    sth[0,4]  = 1000
    sth[0,0]  = 1000
    sth[0,28]  = 12
    sth[0,31]  = 2



###############################################################################
# ToF gate, remove events with ToF outside the indicated range 
# (it is applied globally to all images and PH and multiplicity)
ToFgate      = 0               # ON/OFF
ToFgaterange = [0.035, 0.04]   # s  

###############################################################################
# ToF per digitizer
plotToFhist  = 0    #ON/OFF
                                                   
###############################################################################
# PHS image of all wires and strips for all digitizers             
EnerHistIMG   = 0              # ON/OFF

energybins    = 128
maxenerg      = 65.6e3

###############################################################################
# Position reconstruction 

ChW = [0,31]  # wire channels NOTE: if ch from 1 many things do not work on indexes, keep ch num from 0
ChS = [0,31]  # strip channels

positionRecon = 2

if positionRecon == 0:
   posBins = [32,32]     # w x s max max
elif positionRecon == 1:
   posBins = [65,65]     # w x s CoG CoG
elif positionRecon == 2:
   posBins = [32,65]     # w x s max CoG
   
###############################################################################
   # not implemented yet
# # close the gaps, remove wires hidden; only works with posreconn 0 or 2, i.e. 32 bins on wires
# closeGaps = 1               # ON/OFF
# gaps      = [0, 3, 4, 4, 3, 2]   # (first must be always 0)
   
   
###############################################################################
# LAMBDA: calcualates lambda and plot hist 
calculateLambda  = 1              # ON/OFF  
   
inclination     = 5       #deg
wirepitch       = 4e-3    #m 
DistanceWindow1stWire = (36+2)*1e-3    #m distance between vessel window and first wire
DistanceAtWindow      = 9.288          #m
Distance        = DistanceWindow1stWire + DistanceAtWindow    #m  flight path at 1st wire
lambdaBins      = 191   
lambdaRange     = [1,18]    #A

#if chopper has two openings or more per reset of ToF
MultipleFramePerReset = 1  #ON/OFF (this only affects the lambda calculation)
NumOfBunchesPerPulse  = 2
lambdaMIN             = 2.5     #A

###############################################################################
# MONITOR (if present)
# NOTE: if the MON does not have any ToF, lambda and ToF spectra can be
# still calculated but perhaps meaningless

MONOnOff = 1       #ON/OFF

MONdigit = 137     #digitiser of the Monitor
MONch    = 63      #ch after reorganization of channels (from 0 to 63)

MONThreshold = 0   #threshold on MON, th is OFF if 0, any other value is ON
 
plotMONtofPH = 0   #ON/OFF plotting (MON ToF and Pulse Height) 

MONDistance  = 3   #m distance of MON from chopper if plotMONtofPH == 1 (needed for lambda calculation if ToF)

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
   mb.syncData(pathsource,desitnationpath)
###############################################################################
###############################################################################
#opening files 
   
     #  0 = filename and acqnum is loaded, no window opens
     #  1 = (does nothing for the moment)
     #  2 = filename and acqnum are both ignored, window opens and 
     #      serial is the only one selected 
     #  3 = filename is ignored, window opens and serial is acqnum  
   
if openWindowToSelectFiles == 0:
    fname = filename
elif openWindowToSelectFiles == 1:
    print('\n Option not supported yet! \n')
    print(' ---> Exiting ... \n')
    print('------------------------------------------------------------- \n')
    sys.exit()
elif openWindowToSelectFiles >= 2:
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

temp1 = fname.split('_')
fnamepart1 = temp1[0]+'_'      #file anme without serial and exstension .h5
temp2 = temp1[1].split('.')
fnamepart3 = '.'+temp2[1]      #.h5

if np.logical_or(openWindowToSelectFiles == 2, openWindowToSelectFiles == 1):
    acqnum = [int(temp2[0])]

print('with  serials: '+str(acqnum))
time.sleep(1)
   
###############################################################################
###############################################################################
# MONITOR

# check if monitor is in the data
if MONOnOff == 1: 
    if not(MONdigit in digitID):
        print('\n MONITOR absent in this cassette selection!')
        MONfound = 0
    elif (MONdigit in digitID):
        MONfound = 1
elif MONOnOff == 0:
      MONfound = 0
    
###############################################################################
###############################################################################

if saveReducedData == 1:
    
    outfile = savereducedpath+fnamepart1[:-1]+'-reduced-PY-From'+str(format(acqnum[0],'03d'))+'To'+str(format(acqnum[-1],'03d'))+fnamepart3
    
    # check if file already exist and in case yes delete it 
    if os.path.exists(outfile) == True:
       print('\n WARNING: Reduced DATA file exists, it will be overwritten!')
       os.system('rm '+outfile)
       
    # if you want to save reduced data, it must include lamda, so lambda calculation is turned ON if not yet 
    if calculateLambda == 0:
       calculateLambda = 1
       print('\n \t Lambda calculation turned ON to save reduced DATA')
     
    fid    = h5py.File(outfile, "w")
    
    # create groups in h5 file  
    gdet   = fid.create_group(nameMainFolder+'/detector')
    ginstr = fid.create_group(nameMainFolder+'/instrument')
    grun   = fid.create_group(nameMainFolder+'/run')
    
    if MONfound == 1:
       gmon = fid.create_group(nameMainFolder+'/monitor')
       gmon.attrs.create('columns:ToF,PH,lambda',1)
       gmon.attrs.create('units:seconds,a.u.,angstrom',1)
    ##### 

    grun.create_dataset('duration', data=(len(acqnum)*SingleFileDuration))
    grun.attrs.create('seconds',1)
    
    gdet.attrs.create('columns:X,Y,ToF,PHwires,PHstrips,multW,multS,Z,lambda',1)
    gdet.attrs.create('units:pix(0.350mm),pix(4mm),seconds,a.u.,a.u.,int,int,m,angstrom',1)
 
    gdet.create_dataset('arrangement', data=digitID ) #physical order of the digitizers
    
###############################################################################
###############################################################################
    
# PHS x-axis energy 
xener = np.linspace(0,maxenerg,energybins)

# ToF axis  
ToFmin    = 0
ToFmax    = ToFduration
ToFbins   = round((ToFmax-ToFmin)/ToFbinning)
ToFx      = np.linspace(ToFmin,ToFmax,ToFbins)

# lambda axis 
xlambda = np.linspace(lambdaRange[0],lambdaRange[1],lambdaBins)

# X (w) and Y (s) axis  
XX    = np.linspace(ChW[0],ChW[1],posBins[0])
YY    = np.linspace(ChS[0],ChS[1],posBins[1])

# global axis
# note that bins at edges are rounded, you need to use, check XXg_explained.py
XXg      = np.linspace(XX[0],(XX[-1]-XX[0]+1)*len(digitID)-(1-XX[0]),posBins[0]*len(digitID))         
YYg      = YY
ToFxg    = ToFx    
xlambdag = xlambda    

###############################################################################

XYglob     = np.zeros((len(YY),(len(digitID)*len(XX))))
XYprojGlob = np.zeros(len(digitID)*len(XX))
XToFglob   = np.zeros(((len(digitID)*len(XX)),len(ToFx)))

if plotMultiplicity == 1:
   # figmult = plt.figure(figsize=(9,6)) # alternative way
   figmult, axmult = plt.subplots(1, len(digitID), sharex='col', sharey='row')

if EnerHistIMG == 1:
   figphs, axphs = plt.subplots(4, len(digitID), sharex='col', sharey='row')  

if plotToFhist == 1:
   figtof, axtof = plt.subplots(1, len(digitID), sharex='col', sharey='row')
   
if calculateLambda == 1:
   figlam, axlam = plt.subplots(1, len(digitID), sharex='col', sharey='row')
   XLamGlob      = np.zeros(((len(digitID)*len(XX)),len(xlambda))) 
   
###############################################################################
###############################################################################
   
##################################### 
#START LOOP OVER DIGITIZERS        
##################################### 
for dd in range(len(digitID)):
    
    XYcum     = np.zeros((len(YY),len(XX))) 
    XYprojCum = np.zeros(len(XX)) 
    XToFcum   = np.zeros((len(XX),len(ToFx))) 
    
    if plotMultiplicity == 1:
       multx   = np.arange(0,33,1)
       multcum = np.zeros((len(multx)-1,3))
       multcumnorm = np.zeros((1,3))
       
    if EnerHistIMG == 1:
       PHSIwCum  = np.zeros((len(xener)-1,32))
       PHSIsCum  = np.zeros((len(xener)-1,32))
       PHSIwcCum = np.zeros((len(xener)-1,32))
      
    if calculateLambda == 1:
       XLamCum = np.zeros((len(XX),len(xlambda))) 
                   
##################################### 
#START LOOP OVER ACQNUM
#####################################      
    for ac in range(len(acqnum)):
        
        XY     = np.zeros((len(YY),len(XX))) 
        XYproj = np.zeros((1,len(XX))) 
        XToF   = np.zeros((len(XX),len(ToFx))) 
        
        if calculateLambda == 1:
           XLam = np.zeros((len(XX),len(xlambda))) 
   
        print('\n ---> Reading Digitizer '+str(digitID[dd])+', serial '+str(acqnum[ac]))
        
        filenamefull = fnamepart1+str(format(acqnum[ac],'05d'))+fnamepart3

        # check if file exists in folder
        if os.path.exists(datapath+filenamefull) == False:
           print('\n ---> File: '+filenamefull+' DOES NOT EXIST')
           print('\n ---> in folder: '+datapath+' \n')
           print(' ---> Exiting ... \n')
           print('------------------------------------------------------------- \n')
           sys.exit()
        #####################################
           
        ordertime = 1
        [data, Ntoffi, GTime, flag] = mb.readHDFefu(datapath,filenamefull,digitID[dd],Clockd,ordertime)
        # data here is 4 cols: time stamp in s, ch 0to63, ADC, global reset in ms
        # Ntoffi num of resets
        # GTime is time of the resets in ms, absolute time, make diff to see delta time betwen resets
        # flag is -1 if no digit is found otherwise 0    
        #####################################
        
        # check if the duration of the file is correct, expected number of resets and ToFs
        if flag == 0:
           tsec   = GTime*1e-3 #s
           tsecn  = tsec-tsec[0]
           SingleFileDurationFromFile = tsecn[-1] 
           if abs(SingleFileDurationFromFile-SingleFileDuration) > 1: #if they differ for more then 1s then warning
              print('\n     WARNING: check file duration ... found %.2f s, expected %.2f s \n' % (SingleFileDurationFromFile,SingleFileDuration))
              time.sleep(2)
           Ntoffiapriori = round(SingleFileDuration/ToFduration)   
           if abs(Ntoffiapriori-Ntoffi) >= 2: 
              print('\n     WARNING: check Num of ToFs ... found %d, expected %d \n' % (Ntoffiapriori,Ntoffi))
        elif flag == -1:
           SingleFileDurationFromFile = 0
           print('\n \t ---> No Data for Digitizer '+str(digitID[dd])+', serial '+str(acqnum[ac])+', to display ... skipped!')
           continue
        #####################################
        # histogram raw channels in the file 
        if np.logical_and(plotChRaw == 1, ac == 0):
            fig = plt.figure(figsize=(9,6))
            ax1 = fig.add_subplot(111)
            plt.hist(data[:,1],np.arange(0,64,1)) 
            plt.xlabel('raw ch no.')
            plt.ylabel('counts')
            plt.grid(axis='x', alpha=0.75)
            plt.grid(axis='y', alpha=0.75)
            
        #####################################
        data = mb.flipSwapChOrder(data,flipOrderCh,switchOddEven)
        
        #####################################
        # MONITOR
        if MONfound == 1 and MONdigit == digitID[dd]:
           selMON  = data[:,1] == MONch
           temp    = data[:,[0,2]] #selct only col with time stamp and charge
           MONdata = temp[selMON,:]
           MONdata[:,0] = np.around((MONdata[:,0]),decimals=6)     #  time stamp in s and round at 1us
           data    = data[np.logical_not(selMON),:] # remove MON data from data 
           
           print('\n \t Monitor found ... splitting MON data (%d ev.) from Data' % (len(MONdata)))
           
           if ac == 0:
             MONdataCum = MONdata
           else:
             MONdataCum = np.append(MONdataCum,MONdata,axis=0)
        
        #####################################  
        data = mb.cleaning(data,overflowcorr,zerosuppression)
           
        #####################################
        if softthreshold == 1: # ch from 0 to 63
            print(" \n \t ... software thresholds applied ... ")
            Nall = np.size(data,axis=0)
            for chj in np.arange(0,64,1):
                chbelowth = np.logical_and(data[:,1] == chj,data[:,2] < sth[dd,chj])
                data[chbelowth,2] = np.nan
            data = data[np.logical_not(np.isnan(data[:,2]))]
            Nallnew = np.size(data,axis=0)
            print(" \t file length: %d, below threshold %d, new file length %d " % (Nall,Nall-Nallnew,Nallnew));
        #####################################     
            
        # if np.logical_and(plottimeTofs == 1, flag == 0):
        if plottimeTofs == 1:
            deltat = np.diff(tsecn,1,axis=0)
            xax1   = np.arange(1,len(tsecn)+1,1)
            xax2   = np.arange(1,len(tsecn),1)
            xax3   = np.arange(0,0.1,0.0005) #in s
            
            fig = plt.figure(figsize=(9,6))
            ax1  = fig.add_subplot(131)
            plt.plot(xax1,tsecn,'r+')
            plt.xlabel('ToF no.')
            plt.ylabel('time (s)')
            plt.grid(axis='x', alpha=0.75)
            plt.grid(axis='y', alpha=0.75)
            ax2  = fig.add_subplot(132)
            plt.plot(xax2,deltat,'b+')
            plt.xlabel('ToF no.')
            plt.ylabel('time (s)')
            plt.grid(axis='x', alpha=0.75)
            plt.grid(axis='y', alpha=0.75)
            ax3  = fig.add_subplot(133)
            plt.hist(deltat, xax3) 
            plt.xlabel('delta time (s)')
            plt.ylabel('counts')
            plt.grid(axis='x', alpha=0.75)
            plt.grid(axis='y', alpha=0.75)
            
        ##################
            
        if plottimestamp == 1:
            fig = plt.figure(figsize=(9,6))
            ax1  = fig.add_subplot(111)
            plt.plot(data[:,0],'k+')
            plt.xlabel('trigger no.')
            plt.ylabel('time (s)')
            plt.grid(axis='x', alpha=0.75)
            plt.grid(axis='y', alpha=0.75)
            
        #####################################
        # clustering
        [POPH, Nevents] = mb.clusterPOPH(data,Timewindow)
        
        #####################################
        # gating ToF
        if ToFgate == 1:
           keep = np.logical_and((POPH[:,2] >= ToFgaterange[0]),(POPH[:,2] < ToFgaterange[1]))
           POPH = POPH[keep,:]
        
        #####################################         
        # lambda
        if calculateLambda == 1:
           
           #distance (in m) from first wire to the wire hit in depth       
           cosse = np.cos(np.deg2rad(inclination)) 
           Dist  = Distance + (POPH[:,0]*(wirepitch*cosse)) #m
           
           if MultipleFramePerReset == 1:
              #ToF shifted and corrected by number of bunches
              ToFstart = mb.lambda2ToF(Dist,lambdaMIN)
              temptof  = ( (POPH[:,2]-ToFstart) % (ToFduration/NumOfBunchesPerPulse) ) + ToFstart
           else:
              temptof  = POPH[:,2]
          
           lamb  = mb.ToF2lambda(Dist,temptof) #input m and s, output in A
            
           # append to POPH col 7 of POPH is depth in detecgtor - z (m) and col 8 is lambda   
           POPH = np.append(POPH,np.round(Dist[:,None],decimals=4),axis=1) 
           POPH = np.append(POPH,np.round(lamb[:,None],decimals=2),axis=1)
           
           
        #####################################           
        if plotMultiplicity == 1:

           myw, __  = np.histogram(POPH[:,5],multx) # wires all
           mys, __  = np.histogram(POPH[:,6],multx) # strips all
           mywc, __ = np.histogram(POPH[POPH[:,1]>=0,5],multx) # wires coinc
        
           multcum[:,0] = multcum[:,0]+myw         
           multcum[:,1] = multcum[:,1]+mys
           multcum[:,2] = multcum[:,2]+mywc
 
        #####################################         
        # energy hist
        if EnerHistIMG == 1:
            
           PHSIw  = np.zeros((len(xener)-1,32)) 
           PHSIs  = np.zeros((len(xener)-1,32))
           PHSIwc = np.zeros((len(xener)-1,32))
           
           chwRound  = np.round(POPH[:,0])
           chsRound  = np.round(POPH[:,1])
           TwoDim    = POPH[:,1] >= 0
           chwcRound = chwRound[TwoDim]
           POPHcoinc = POPH[TwoDim,:]
            
           for chi in range(0,32,1):    # wires
               PHSIw[:,chi], temp  = np.histogram(POPH[chwRound == chi,3],xener) # wires all
                          
           for chi in range(0,32,1):    # strips
               PHSIs[:,chi], temp  = np.histogram(POPH[chsRound == chi,4],xener) # strips all
               
           for chi in range(0,32,1):    # wires in coincidence 2D
               PHSIwc[:,chi], temp  = np.histogram(POPHcoinc[chwcRound == chi,3],xener) # wires coinc.

           PHSIwCum  = PHSIwCum  + PHSIw
           PHSIsCum  = PHSIsCum  + PHSIs
           PHSIwcCum = PHSIwcCum + PHSIwc
           
        #####################################         
        # X,Y,ToF hist         
        coincidence = 1    
        showStats   = 1
        XY, XYproj, XToF = mb.HISTXYToF(XX,POPH[:,0],YY,POPH[:,1],ToFx,POPH[:,2],coincidence,showStats)
        
        XYcum     = XYcum + XY
        XYprojCum = XYprojCum + XYproj
        XToFcum   = XToFcum + XToF

        ##################################### 
        # hist lambda
        if calculateLambda == 1:   
            
           coincidence = 1    
           showStats   = 0
           __ , __ , XLam = mb.HISTXYToF(XX,POPH[:,0],YY,POPH[:,1],xlambda,POPH[:,8],coincidence,showStats)  
                  
           XLamCum = XLamCum + XLam
        #####################################    
        if saveReducedData == 1:
            if ac == 0:
               POPHcum = POPH
            else:
               POPHcum = np.append(POPHcum,POPH,axis=0)
           
#####################################             
##################################### 
#END LOOP OVER ACQNUM
#####################################    
        
    # fill global hist  
    indexes = (dd*len(XX) + np.arange(len(XX)))

    XYglob[:,indexes]      = XYcum
    XYprojGlob[indexes]    = XYprojCum
    XToFglob[indexes,:]    = XToFcum
    
    if calculateLambda == 1: 
       XLamGlob[indexes,:] = XLamCum
                   
    #####################################           
    if plotMultiplicity == 1:     
        
       multcumnorm[0,:] = np.sum(multcum[1:,:],axis=0)
    
       multcum = multcum/multcumnorm
       # ax  = figmult.add_subplot(1,len(digitID),dd+1) # alternative way
       if len(digitID)>1:
          axmult[dd].step(multx[:6],multcum[:6,:],where='mid')
          axmult[dd].set_xlabel('multiplicity')
          axmult[dd].set_title('digit '+str(digitID[dd]))
          if dd == 0:
             axmult[dd].set_ylabel('probability')
       else:
          # axmult.step(multx[:6],multcum[:6,:], where='mid', label=( i for i in range(3)))
          #             # [['w'],['s'],['w coinc.']])
          axmult.step(multx[:6],multcum[:6,0],where='mid',label=['w'])
          axmult.step(multx[:6],multcum[:6,1],where='mid',label=['s'])
          axmult.step(multx[:6],multcum[:6,2],where='mid',label=['w coinc.'])
          # CHECK HOW TO MAKE LEGEND IT DOES NOT WORK 
          axmult.set_xlabel('multiplicity')
          axmult.set_ylabel('probability')
          legend = axmult.legend(loc='upper right', shadow=False, fontsize='large')
          
          
   ##################################### 
    if plotToFhist == 1:
       XToFcumSum = np.sum(XToFcum,axis=0)
       
       ToFxms = ToFx*1e3 # in ms 
       
       if len(digitID)>1:
          axtof[dd].plot(ToFxms,XToFcumSum)
          axtof[dd].set_xlabel('ToF (ms)')
          axtof[dd].set_title('digit '+str(digitID[dd]))
          if dd == 0:
             axtof[dd].set_ylabel('counts')
       else:
          axtof.plot(ToFxms,XToFcumSum)
          axtof.set_xlabel('ToF (ms)')
          axtof.set_ylabel('counts')
          
    #####################################         
    # energy hist
    if EnerHistIMG == 1:
        
       xeners = mb.shiftBinning(xener) # shifts bin by half bin and remove last bin
        
       if len(digitID)>1:
           axphs[0,dd].imshow(np.rot90(PHSIwCum),aspect='auto',interpolation='none',extent=[xeners[0],xeners[-1],-0.5,31.5], origin='upper')
           axphs[1,dd].imshow(np.rot90(PHSIsCum),aspect='auto',interpolation='none',extent=[xener[0],xener[-1],-0.5,31.5], origin='upper')
           axphs[2,dd].imshow(np.rot90(PHSIwcCum),aspect='auto',interpolation='none',extent=[xener[0],xener[-1],-0.5,31.5], origin='upper')
           if dd == 0:
              axphs[0,dd].set_ylabel('wires ch. no.')
              axphs[1,dd].set_ylabel('strips ch. no.')
              axphs[2,dd].set_ylabel('wires coinc. ch. no.')
           
       else:
           axphs[0].imshow(np.rot90(PHSIwCum),aspect='auto',interpolation='none',extent=[xeners[0],xeners[-1],-0.5,31.5], origin='upper')
           axphs[1].imshow(np.rot90(PHSIsCum),aspect='auto',interpolation='none',extent=[xener[0],xener[-1],-0.5,31.5], origin='upper')
           axphs[2].imshow(np.rot90(PHSIwcCum),aspect='auto',interpolation='none',extent=[xener[0],xener[-1],-0.5,31.5], origin='upper')
           if dd == 0:
              axphs[0].set_ylabel('wires ch. no.')
              axphs[1].set_ylabel('strips ch. no.')
              axphs[2].set_ylabel('wires coinc. ch. no.')
           
       #global PHS
       PHSGw  = np.sum(PHSIwCum,axis=1)
       PHSGs  = np.sum(PHSIsCum,axis=1)
       PHSGwc = np.sum(PHSIwcCum,axis=1)
       
       # global PHS plot
       if len(digitID)>1:
          axphs[3,dd].step(xeners,PHSGw,'r')
          axphs[3,dd].step(xeners,PHSGs,'b')
          axphs[3,dd].step(xeners,PHSGwc,'k')
          axphs[3,dd].set_xlabel('pulse height (a.u.)')
          if dd == 0:
             axphs[3,dd].set_ylabel('counts')
       else:
          axphs[3].step(xeners,PHSGw,'r')
          axphs[3].step(xeners,PHSGs,'b')
          axphs[3].step(xeners,PHSGwc,'k')
          axphs[3].set_xlabel('pulse height (a.u.)')
          axphs[3].set_ylabel('counts')

       
    #################################### 
    # hist lambda
    if calculateLambda == 1: 
       XLamCumProj = np.sum(XLamCum,axis=0) 
       
       # lambda hist per digit
       if len(digitID)>1:
          axlam[dd].step(xlambda,XLamCumProj,where='post')
          axlam[dd].set_xlabel('lambda (A)')
          axlam[dd].set_title('digit '+str(digitID[dd]))
          if dd == 0:
             axlam[dd].set_ylabel('counts')
       else:
          axlam.step(xlambda,XLamCumProj,where='post')
          axlam.set_xlabel('lambda (A)')
          axlam.set_ylabel('counts')
          
    ####################################    
    # saving data to h5 file      
    if saveReducedData == 1:
        
       gdetdigit = gdet.create_group('digit'+ str(digitID[dd]))
       gdetdigit.create_dataset('data', data=POPHcum, compression=compressionHDFT, compression_opts=compressionHDFL)
          
#####################################            
##################################### 
#END LOOP OVER DIGITIZERS        
##################################### 
       
###############################################################################
###############################################################################
# MONITOR
if MONfound == 1:
  
    if MONThreshold > 0:
       aboveTh = MONdataCum[:,1] >= MONThreshold
       MONdataCum = MONdataCum[aboveTh,:]

    if plotMONtofPH == 1:
         
        MONToFhistCum, __  = np.histogram(MONdataCum[:,0],ToFx) 
        MONPHShistCum, __  = np.histogram(MONdataCum[:,1],xener)
        
        ToFxs  = mb.shiftBinning(ToFx)
        xeners = mb.shiftBinning(xener)
        
        ToFxs  = ToFxs*1e3
        
        figmon, (axm1, axm2) = plt.subplots(figsize=(6,6), nrows=1, ncols=2)    
        pos2 = axm1.step(ToFxs,MONToFhistCum,'k',where='post')
        axm1.set_xlabel('ToF (ms)')
        axm1.set_ylabel('counts')
        axm1.set_title('MON ToF')
        pos3 = axm2.step(xeners,MONPHShistCum,'k',where='post')
        axm2.set_xlabel('pulse height (a.u.)')
        axm2.set_ylabel('counts')
        axm2.set_title('MON PHS')
 
    if calculateLambda == 1 and plotMONtofPH == 1:
        
           # if MultipleFramePerReset == 1:
           #    #ToF shifted and corrected by number of bunches
           #    ToFstart = mb.lambda2ToF(MONDistance,lambdaMIN)
           #    temptof  = ( (MONdataCum[:,0]-ToFstart) % (ToFduration/NumOfBunchesPerPulse) ) + ToFstart
           # else:
              # temptof  = MONdataCum[:,0]
         
        temptof  = MONdataCum[:,0]
          
        MONlamb  = mb.ToF2lambda(MONDistance,temptof) #input m and s, output in A
            
         # append to MONdataCum col 0 ToF, col 1 PH, col 2 lambda if present 
        MONdataCum = np.append(MONdataCum,np.round(MONlamb[:,None],decimals=2),axis=1) 
           
        MONLamHistCum, __  = np.histogram(MONdataCum[:,2],xlambda) 
        
        xlambdas = mb.shiftBinning(xlambda)
        
        figmonl, axml = plt.subplots(figsize=(6,6), nrows=1, ncols=1)
        axml.step(xlambdas,MONLamHistCum,'k',where='post')
        axml.set_xlabel('lambda (A)')
        axml.set_ylabel('counts')
        axml.set_title('MON lambda')
  
    if saveReducedData == 1:  
      gmon.create_dataset('data', data=MONdataCum, compression=compressionHDFT, compression_opts=compressionHDFL)
       
###############################################################################
###############################################################################

if saveReducedData == 1:
   # close h5 file
   fid.close()     
        
###############################################################################
###############################################################################
          
########   
# 2D image of detector X,Y
fig2D, (ax1, ax2) = plt.subplots(figsize=(6,12), nrows=2, ncols=1)    
# #fig.add_axes([0,0,1,1]) #if you want to position absolute coordinate
pos1  = ax1.imshow(XYglob,aspect='auto',interpolation='nearest',extent=[XXg[0],XXg[-1],YYg[-1],YYg[0]], origin='upper',cmap='jet')
# cbar1 =fig2D.colorbar(pos1,ax=ax1)
# cbar2.minorticks_on()
# ax1.set_aspect('tight')
ax1.set_xlabel('Wire ch.')
ax1.set_ylabel('Strip ch.')

########
# 1D image of detector, opnly wires, in coincidence with strips (2D) and not (1D)
XYprojGlobCoinc = np.sum(XYglob,axis=0) 

pos2 = ax2.step(XXg,XYprojGlob,'r',where='post',label='1D')
ax2.step(XXg,XYprojGlobCoinc,'b',where='post',label='2D')
ax2.set_xlabel('Wire ch.')
ax2.set_ylabel('counts')
ax2.set_xlim(XXg[0],XXg[-1])
legend = ax2.legend(loc='upper right', shadow=False, fontsize='large')

########
# 2D image of detector ToF vs Wires 
ToFxgms = ToFxg*1e3 # in ms 

fig2, ax2 = plt.subplots(figsize=(6,6), nrows=1, ncols=1) 
pos2  = ax2.imshow(XToFglob,aspect='auto',interpolation='none',extent=[ToFxgms[0],ToFxgms[-1],XXg[0],XXg[-1]], origin='upper',cmap='jet')
# cbar2 = fig2D.colorbar(pos2,ax=ax2)
# cbar2.minorticks_on()
ax2.set_ylabel('Wire ch.')
ax2.set_xlabel('ToF (ms)')

######## 
# 2D image of detector Lambda vs Wires
if calculateLambda == 1:
   figl, axl = plt.subplots(figsize=(6,6), nrows=1, ncols=1) 
   posl1  = axl.imshow(XLamGlob,aspect='auto',interpolation='none',extent=[xlambdag[0],xlambdag[-1],XXg[0],XXg[-1]], origin='upper',cmap='jet')
   # cbar2 = fig2D.colorbar(pos2,ax=ax2)
   # cbar2.minorticks_on()
   axl.set_ylabel('Wire ch.')
   axl.set_xlabel('lambda (A)')


###############################################################################
###############################################################################

        # fig = plt.figure(figsize=(9,6))
        # ax  = fig.add_subplot(111)
        # plt.step(binx[1:],by)

# # # data2 = np.copy(data)


# ############################
    
# mbins = np.arange(0,33,1)

# TwoDim = POPH[:,1] >= 0
# H, xedges1, yedges1 = np.histogram2d(POPH[TwoDim,0],POPH[TwoDim,1],bins=(mbins,mbins))


# ################################################################################


# #sc = np.histogram(POPH[:,0],bi)

# #temp = POPH[np.logical_and(POPH[:,0]>0,POPH[:,0]<2),0]


# fig = plt.figure(figsize=(15,10))
# #fig.add_axes([0,0,1,1]) #if you want to position absolute coordinate
# ax  = fig.add_subplot(121)
# n, bins, patches = plt.hist(POPH[:,0], mbins, facecolor='darkblue', alpha=0.5)
# #n, bins, patches = plt.hist(temp, bi, facecolor='darkblue', alpha=0.5)
# plt.grid(axis='y', alpha=0.75)
# plt.grid(axis='x', alpha=0.75)
# plt.show()

# # ax  = fig.add_subplot(122)
# # plt.plot(bi[0:-1],n)

# xedges = mbins
# yedges = xedges


# ax2  = fig.add_subplot(122)
# H, xedges, yedges = np.histogram2d(POPH[:,0], POPH[:,1], bins=(xedges, yedges))
# plt.imshow(H, interpolation='nearest', origin='low',   extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
# plt.show()

###############################################################################
###############################################################################
print('----------------------------------------------------------------------')
