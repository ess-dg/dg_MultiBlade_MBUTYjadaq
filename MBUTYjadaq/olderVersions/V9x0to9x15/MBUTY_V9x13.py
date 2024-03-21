#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
###############################################################################
########    V9.12 2020/03/30      francescopiscitelli    ######################
########    (this version uses an excel file for mapping channels into geometry)
########    (and can load either EFU files or JADAQ files)
###############################################################################
###############################################################################

# argparse 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import time
import h5py
import os
import glob
import sys
from PyQt5.QtWidgets import QFileDialog


# import the library with all specific functions that this code uses 
from lib import libSyncUtil as syu 
from lib import libLoadFile as lof 
from lib import libHistog as hh
from lib import libToFconverter as tcl
from lib import libMBUTY_V9x13 as mbl 

###############################################################################
tProfilingStart = time.time()
print('----------------------------------------------------------------------')
plt.close("all")
###############################################################################
###############################################################################
########    here starts the section with all the settings you can choose  #####
###############################################################################
###############################################################################

sync = 0   #ON/OFF if you want to rsync the data 

###############################################################################

EFU_JADAQ_fileType = 1  # 0 = JADAQ, 1 = EFU file loading 

pathsourceEFU         = 'efu@192.168.0.58:/home/efu/data/temp/'
pathsourceJDQ         = ''

# desitnationpath     = '/Users/francescopiscitelli/Documents/DOC/DATA/2018_11/DATA_PSI/DATAraw/C_Masks/'
desitnationpath  = '/Users/francescopiscitelli/Desktop/try/'

# datapath            = desitnationpath 
datapath            = os.path.abspath('.')+'/data/' 

filename = '13827-C-ESSmask-20181116-120805_00000.h5'

acqnum   = [0]    #do not need to be sequential

openWindowToSelectFiles = 0
     #  0 = filename and acqnum is loaded, no window opens
     #  1 = latest file created in folder is loaded with its serial
     #  2 = filename and acqnum are both ignored, window opens and 
     #      serial is the only one selected 
     #  3 = filename is ignored, window opens and serial is acqnum  

SingleFileDuration       = 60   #s to check if h5 file has all the resets

###############################################################################
# variable POPH will be saved in a new h5 file
saveReducedData = 0 #ON/OFF

savereducedpath = '/Users/francescopiscitelli/Desktop/reducedFile/'

nameMainFolder  = 'entry1'

compressionHDFT  = 'gzip'  
compressionHDFL  = 9     # gzip compression level 0 - 9

###############################################################################

digitID = [34,33,31,142,143,137]

digitID = [34,33]

###############################################################################
# mapping channels into geometry 

MAPPING =    1     # ON/OFF, if OFF channels are used as in the file

# mappath = '/Users/francescopiscitelli/Documents/PYTHON/MBUTY/tables/'
mappath = os.path.abspath('.')+'/tables/'
mapfile = 'MB18_mapping.xlsx'

###############################################################################
                    
overflowcorr      = 1   #ON/OFF (does not affect the MONITOR)
zerosuppression   = 1   #ON/OFF (does not affect the MONITOR)

Clockd            = 16e-9   #s CAEN V1740D clock steps
Timewindow        = 2e-6    #s to create clusters 

###############################################################################

plotChRaw         = 0   #ON/OFF plot of raw ch in the file (not flipped, not swapped) no thresholds (only for 1st serial)

plottimestamp     = 0   #ON/OFF for debugging, plot the events VS time stamp (after thresholds)

plottimeTofs      = 0   #ON/OFF for debugging, plot the time duration of ToFs (after thresholds)

ToFduration       = 0.06     #s
ToFbinning        = 100e-6   #s

plotMultiplicity  = 0   #ON/OFF

###############################################################################
# software thresholds
# NOTE: they are applied to the flipped or swpadded odd/even order of ch!
# th on ch number: 32 w and 32 s, one row per cassette 
softthreshold = 1   # 0 = OFF, 1 = File With Threhsolds Loaded, 2 = User defines the Thresholds in an array sth 

#####
#  if 1 the file containing the threhsolds is loaded: 

# sthpath =  '/Users/francescopiscitelli/Documents/PYTHON/MBUTY/'
sthpath =  os.path.abspath('.')+'/tables/'
sthfile =  'MB18_thresholds.xlsx'
  
#####  
#  if 2 here you can define your thresholds  
    
sth = np.ones((np.size(digitID,axis=0),64))
        
#     # sth[0:1,0:31] = 1
# sth[0,10] = 30000

# sth[0,0] = 30000

# sth[0,63] = 30000

# sth[0,33] = 30000

# sth[1,0:31] = 6000
        
# sth[:,31]   = 10e3

# sth[1,42] = 9000
        
# sth[0,0:31] = 25000
# sth[0,4]  = 1000
# sth[0,0]  = 1000
# sth[0,28]  = 12
# sth[0,31]  = 2
    
    
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

plotEnerHistIMGinLogScale = 0   # ON/OFF

energybins    = 128
maxenerg      = 70e3

# correlation of PHS wires VS strips per digitiser (only calculated first serial acqnum)
CorrelationPHSws = 0              # ON/OFF

###############################################################################
# Position reconstruction (max is max amplitude ch in clsuter either on w or s,
# CoG is centre of gravity on ch)

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
# close the gaps, remove wires hidden; only works with posreconn 0 or 2, i.e. 32 bins on wires
closeGaps = 0               # 0 = OFF shows the raw image, 1 = ON shows only the closed gaps img, 2 shows both
gaps      = [0, 3, 4, 4, 3, 2]   # (first must be always 0)
   
###############################################################################
# plot the 2D imafge of the detector, lamda and ToF in linear =0 or log scale =1
plotIMGinLogScale = 0
   
###############################################################################
# LAMBDA: calcualates lambda and plot hist 
calculateLambda  = 0              # ON/OFF  
   
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

MONOnOff = 0       #ON/OFF

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

if EFU_JADAQ_fileType == 0:
    pathsource = pathsourceJDQ
elif EFU_JADAQ_fileType == 1: 
    pathsource = pathsourceEFU
    
if sync == 1:
   syu.syncData(pathsource,desitnationpath)
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
        
    # print('\n Option not supported yet! \n')
    # print(' ---> Exiting ... \n')
    # print('------------------------------------------------------------- \n') 
    # sys.exit()
    
elif openWindowToSelectFiles >= 2:
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
print('File selected: '+fname)

temp1 = fname.split('_')
fnamepart1 = temp1[0]+'_'      #file name without serial and exstension .h5
temp2 = temp1[1].split('.')
fnamepart3 = '.'+temp2[1]      #.h5

if openWindowToSelectFiles == 2 or openWindowToSelectFiles == 1:
    acqnum = [int(temp2[0])]

print('with serials: '+str(acqnum))
time.sleep(1)
   
###############################################################################
###############################################################################

if softthreshold == 0:
    print(' ---> Thresholds OFF ...')
elif softthreshold == 1:
    print(' ---> Thresholds ON ... Loading Threshold File ...')
    [sth,softthreshold] = mbl.softThresholds(sthpath,sthfile,digitID,softthreshold)
elif softthreshold == 2:   
    print(' ---> Thresholds ON ... Defined by User ...')
    
###############################################################################
###############################################################################

if MAPPING == 0:
   print(' ---> Mapping OFF ...') 
elif MAPPING == 1:
   mapfullpath = mappath+mapfile         
   if os.path.exists(mapfullpath) == False:
      print('\n ---> WARNING ... File: '+mapfullpath+' NOT FOUND')
      print("\t ... Mapping switched OFF ... ")
      MAPPING = 0
      time.sleep(2)
   else:
      print(' ---> Mapping ON ... Loading Mapping File ...')
      
###############################################################################
###############################################################################
      
if closeGaps == 1 or closeGaps == 2:
    
    print(' ---> Closing gaps ON ...')

    if positionRecon == 1: 
        closeGaps = 0
        print(' ---> closing gaps for pos. reconstr. 1 not allowed ... skipped! ')

    if len(digitID) == 1: 
        closeGaps = 0
        print(' ---> closing gaps OFF for only 1 cassette! \n')

    if len(gaps) != len(digitID):
        print(' ---> closing gaps: length(gaps) ~= length(cassette) ... check! -> Default 3 wires used ... ')
        gaps    = [3]*len(digitID)
        gaps[0] = 0

###############################################################################
###############################################################################
        
if plotIMGinLogScale == 1:
    normColors = LogNorm()
elif plotIMGinLogScale == 0:
    normColors = None
    
if plotEnerHistIMGinLogScale == 1:
    normColorsPH = LogNorm()
elif plotEnerHistIMGinLogScale == 0:
    normColorsPH = None

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
       
    # if you want to save reduced data, it must include lambda, so lambda calculation is turned ON if not yet 
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

if plotChRaw == 1:
   figchraw, axchraw = plt.subplots(1, len(digitID), sharex='col', sharey='row')

if plotMultiplicity == 1:
   # figmult = plt.figure(figsize=(9,6)) # alternative way
   figmult, axmult = plt.subplots(1, len(digitID), sharex='col', sharey='row')

if EnerHistIMG == 1:
   figphs, axphs = plt.subplots(4, len(digitID), sharex='col', sharey='row')  
   
if CorrelationPHSws == 1:
   figphscorr, axphscorr = plt.subplots(1, len(digitID), sharex='col', sharey='row') 

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
       multx   = np.arange(0,32,1)
       multcum = np.zeros((len(multx),3))
       multcumnorm = np.zeros((1,3))
       
    if EnerHistIMG == 1:
       PHSIwCum  = np.zeros((len(xener),32))
       PHSIsCum  = np.zeros((len(xener),32))
       PHSIwcCum = np.zeros((len(xener),32))
      
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
        
        if EFU_JADAQ_fileType == 0: 
            
            try:
                ordertime = 1
                [data, Ntoffi, GTime, _, flag] = lof.readHDFjadaq_3col(datapath,filenamefull,digitID[dd],Clockd,ordertime)
            except: 
                print('\n ---> this looks like a file created with the EFU file writer, change mode with EFU_JADAQ_fileType set to 1!')
                print(' ---> Exiting ... \n')
                print('------------------------------------------------------------- \n')
                sys.exit()
                
        
        elif EFU_JADAQ_fileType == 1:
            
            try:
               ordertime = 1
               [data, Ntoffi, GTime, _, flag] = lof.readHDFefu_3col(datapath,filenamefull,digitID[dd],Clockd,ordertime)
                    # data here is 3 cols: time stamp in s, ch 0to63, ADC, 
                    # Ntoffi num of resets
                    # GTime is time of the resets in ms, absolute time, make diff to see delta time betwen resets
                    # DGTtime global reset in ms
                    # flag is -1 if no digit is found otherwise 0    
                    #####################################
            except: 
                print('\n ---> this looks like a file created with the JADAQ file writer, change mode with EFU_JADAQ_fileType set to 0!')
                print(' ---> Exiting ... \n')
                print('------------------------------------------------------------- \n')
                sys.exit()

        # check if the duration of the file is correct, expected number of resets and ToFs
        if flag == 0:
           tsec   = GTime*1e-3 #s
           
           if tsec[0] != 0: 
               tsecn  = tsec-tsec[0]
           else:
               tsecn  = tsec-tsec[1]
               
           SingleFileDurationFromFile = tsecn[-1] 
           if abs(SingleFileDurationFromFile-SingleFileDuration) > 1: #if they differ for more then 1s then warning
              print('\n     WARNING: check file duration ... found %.2f s, expected %.2f s' % (SingleFileDurationFromFile,SingleFileDuration))
              time.sleep(2)
           Ntoffiapriori = round(SingleFileDuration/ToFduration)   
           if abs(Ntoffiapriori-Ntoffi) >= 2: 
              print('\n     WARNING: check Num of ToFs ... found %d, expected %d' % (Ntoffi, Ntoffiapriori))
        elif flag == -1:
           SingleFileDurationFromFile = 0
           print('\n \t ---> No Data for Digitizer '+str(digitID[dd])+', serial '+str(acqnum[ac])+', to display ... skipped!')
           continue
        #####################################
        # histogram raw channels in the file 
        if plotChRaw == 1 and ac == 0:
            
            # temp = data[data[:,1] <= 1 ,1]
            
            Xaxis  = np.arange(0,64,1)
            histxx = hh.hist1(Xaxis,data[:,1],1)     
            
            if len(digitID)>1:
               axchraw[dd].bar(Xaxis[:32],histxx[:32],0.8,color='r')
               axchraw[dd].bar(Xaxis[32:],histxx[32:],0.8,color='b')
               axchraw[dd].set_xlabel('raw ch no.')
               axchraw[dd].set_title('digit '+str(digitID[dd]))
               if dd == 0:
                  axchraw[dd].set_ylabel('counts')
            else:
               axchraw.bar(Xaxis[:32],histxx[:32],0.8,color='r')
               axchraw.bar(Xaxis[32:],histxx[32:],0.8,color='b')
               axchraw.set_xlabel('raw ch no.')
               axchraw.set_ylabel('counts')
            
        #####################################   
        data = mbl.mappingChToGeometry(data,MAPPING,mappath,mapfile)

        #####################################
        # MONITOR
        if MONfound == 1 and MONdigit == digitID[dd]:
           selMON  = data[:,1] == MONch
           temp    = data[:,[0,2]] #selct only col with time stamp and charge
           MONdata = temp[selMON,:]
           MONdata[:,0] = np.around((MONdata[:,0]),decimals=6)     #  time stamp in s and round at 1us
           data    = data[np.logical_not(selMON),:] # remove MON data from data 
           
           print('\n \t Monitor found ... splitting MONITOR data (%d ev.) from Data' % (len(MONdata)))
           
           if ac == 0:
             MONdataCum = MONdata
           else:
             MONdataCum = np.append(MONdataCum,MONdata,axis=0)
        
        #####################################  
        data = mbl.cleaning(data,overflowcorr,zerosuppression)
        
        #####################################
        if softthreshold > 0: # ch from 0 to 63
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
            ax1 = fig.add_subplot(111)
            plt.plot(data[:,0],'k+')
            plt.xlabel('trigger no.')
            plt.ylabel('time (s)')
            plt.grid(axis='x', alpha=0.75)
            plt.grid(axis='y', alpha=0.75)
            
        #####################################
        # clustering
            # old cluster function
        # [POPH, Nevents] = mb.clusterPOPH(data,Timewindow)
            # use _q for speed -> new cluster
            
        # np.save('data4cluster.npy',data)
            
        # data input here is 3 cols: time stamp in s, ch 0to63, ADC,
        [POPH, Nevents] = mbl.clusterPOPH_q(data,Timewindow)
        
        #  POPH has 7 cols:X,Y,ToF,PHwires,PHstrips,multW,multS
        #  units:pix(0.350mm),pix(4mm),seconds,a.u.,a.u.,int,int
        
        # aaaa = POPH
        
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
              ToFstart = tcl.lambda2ToF(Dist,lambdaMIN)
              temptof  = ( (POPH[:,2]-ToFstart) % (ToFduration/NumOfBunchesPerPulse) ) + ToFstart
           else:
              temptof  = POPH[:,2]
          
           lamb  = tcl.ToF2lambda(Dist,temptof) #input m and s, output in A
            
           # append to POPH col 7 of POPH is depth in detecgtor - z (m) and col 8 is lambda   
           POPH = np.append(POPH,np.round(Dist[:,None],decimals=4),axis=1) 
           POPH = np.append(POPH,np.round(lamb[:,None],decimals=2),axis=1)
           
           
        #####################################           
        if plotMultiplicity == 1:
            
           myw  = hh.hist1(multx,POPH[:,5],1) # wires all
           mys  = hh.hist1(multx,POPH[:,6],1) # strips all
           mywc = hh.hist1(multx,POPH[POPH[:,1]>=0,5],1) # wires coinc

           multcum[:,0] = multcum[:,0]+myw         
           multcum[:,1] = multcum[:,1]+mys
           multcum[:,2] = multcum[:,2]+mywc
 
        #####################################         
        # energy hist
        if EnerHistIMG == 1:
            
           PHSIw  = np.zeros((len(xener),32)) 
           PHSIs  = np.zeros((len(xener),32))
           PHSIwc = np.zeros((len(xener),32))
           
           chwRound  = np.round(POPH[:,0])
           chsRound  = np.round(POPH[:,1])
           TwoDim    = POPH[:,1] >= 0
           chwcRound = chwRound[TwoDim]
           POPHcoinc = POPH[TwoDim,:]
            
           # this can be replaced with a 2D hist done in a single shot!
           for chi in range(0,32,1):    # wires
               PHSIw[:,chi] = hh.hist1(xener,POPH[chwRound == chi,3],1) # wires all
                          
           for chi in range(0,32,1):    # strips
               PHSIs[:,chi] = hh.hist1(xener,POPH[chsRound == chi,4],1) # strips all
               
           for chi in range(0,32,1):    # wires in coincidence 2D
               PHSIwc[:,chi] = hh.hist1(xener,POPHcoinc[chwcRound == chi,3],1) # wires coinc.

           PHSIwCum  = PHSIwCum  + PHSIw
           PHSIsCum  = PHSIsCum  + PHSIs
           PHSIwcCum = PHSIwcCum + PHSIwc
           
        #####################################         
        # X,Y,ToF hist         
        coincidence = 1    
        showStats   = 1
        XY, XYproj, XToF = mbl.myHistXYZ(XX,POPH[:,0],YY,POPH[:,1],ToFx,POPH[:,2],coincidence,showStats)
        
        XYcum     = XYcum + XY
        XYprojCum = XYprojCum + XYproj
        XToFcum   = XToFcum + XToF

        ##################################### 
        # hist lambda
        if calculateLambda == 1:   
            
           coincidence = 1    
           showStats   = 0
           __ , __ , XLam = mbl.myHistXYZ(XX,POPH[:,0],YY,POPH[:,1],xlambda,POPH[:,8],coincidence,showStats)  
                  
           XLamCum = XLamCum + XLam
        #####################################    
        if saveReducedData == 1:
            if ac == 0:
               POPHcum = POPH
            else:
               POPHcum = np.append(POPHcum,POPH,axis=0)
               
        #####################################
        # correlation PH wires VS PH strips (only for the first serial acqnum)
        if CorrelationPHSws == 1 and ac == 0:
            
            # if you want to remove the 1D
            PH1 =  POPH[POPH[:,1]>=0,3]  
            PH2 =  POPH[POPH[:,1]>=0,4] 
            #  all events also 1D
            # PH1 = POPH[:,3]
            # PH2 = POPH[:,4]
            
            PHcorr = hh.hist2(xener,PH1,xener,PH2,0)
            
            if len(digitID)>1:
                axphscorr[dd].imshow(PHcorr,aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],xener[0],xener[-1]], origin='lower',cmap='jet')
                if dd == 0:
                    axphscorr[dd].set_ylabel('pulse height strips (a.u.)')
                axphscorr[dd].set_xlabel('pulse height wires (a.u.)')
                axphscorr[dd].set_title('digit '+str(digitID[dd]))            
            else:
                axphscorr.imshow(PHcorr,aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],xener[0],xener[-1]], origin='lower',cmap='jet')
                if dd == 0:
                    axphscorr.set_ylabel('pulse height strips (a.u.)')
                axphscorr.set_xlabel('pulse height wires (a.u.)')
                axphscorr.set_title('digit '+str(digitID[dd]))
           
    
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
      
       width = 0.2
    
       multcum = multcum/multcumnorm
       # ax  = figmult.add_subplot(1,len(digitID),dd+1) # alternative way
       if len(digitID)>1:
          axmult[dd].bar(multx[:6]- width,multcum[:6,0],width,label='w')
          axmult[dd].bar(multx[:6]+ width,multcum[:6,1],width,label='s')
          axmult[dd].bar(multx[:6],multcum[:6,2],width,label='w coinc. s')
          axmult[dd].set_xlabel('multiplicity')
          axmult[dd].set_title('digit '+str(digitID[dd]))
          legend = axmult[dd].legend(loc='upper right', shadow=False, fontsize='large')
          if dd == 0:
             axmult[dd].set_ylabel('probability')
       else:
          axmult.bar(multx[:6]- width,multcum[:6,0],width,label='w')
          axmult.bar(multx[:6]+ width,multcum[:6,1],width,label='s')
          axmult.bar(multx[:6],multcum[:6,2],width,label='w coinc. s')
          # CHECK HOW TO MAKE LEGEND IT DOES NOT WORK 
          axmult.set_xlabel('multiplicity')
          axmult.set_ylabel('probability')
          legend = axmult.legend(loc='upper right', shadow=False, fontsize='large')
          
   ##################################### 
    if plotToFhist == 1:
       XToFcumSum = np.sum(XToFcum,axis=0)
       
       ToFxms = ToFx*1e3 # in ms 
       
       if len(digitID)>1:
          axtof[dd].step(ToFxms,XToFcumSum,where='mid')
          axtof[dd].set_xlabel('ToF (ms)')
          axtof[dd].set_title('digit '+str(digitID[dd]))
          if dd == 0:
             axtof[dd].set_ylabel('counts')
       else:
          axtof.step(ToFxms,XToFcumSum,where='mid')
          axtof.set_xlabel('ToF (ms)')
          axtof.set_ylabel('counts')
          
    #####################################         
    # energy hist
    if EnerHistIMG == 1:
               
       if len(digitID)>1:
           axphs[0,dd].imshow(np.rot90(PHSIwCum),aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],-0.5,31.5], origin='upper',cmap='jet')
           axphs[1,dd].imshow(np.rot90(PHSIsCum),aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],-0.5,31.5], origin='upper',cmap='jet')
           axphs[2,dd].imshow(np.rot90(PHSIwcCum),aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],-0.5,31.5], origin='upper',cmap='jet')
           if dd == 0:
              axphs[0,dd].set_ylabel('wires ch. no.')
              axphs[1,dd].set_ylabel('strips ch. no.')
              axphs[2,dd].set_ylabel('wires coinc. ch. no.')
           
       else:
           axphs[0].imshow(np.rot90(PHSIwCum),aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],-0.5,31.5], origin='upper',cmap='jet')
           axphs[1].imshow(np.rot90(PHSIsCum),aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],-0.5,31.5], origin='upper',cmap='jet')
           axphs[2].imshow(np.rot90(PHSIwcCum),aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],-0.5,31.5], origin='upper',cmap='jet')
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
          axphs[3,dd].step(xener,PHSGw,'r',where='mid')
          axphs[3,dd].step(xener,PHSGs,'b',where='mid')
          axphs[3,dd].step(xener,PHSGwc,'k',where='mid')
          axphs[3,dd].set_xlabel('pulse height (a.u.)')
          if dd == 0:
             axphs[3,dd].set_ylabel('counts')
       else:
          axphs[3].step(xener,PHSGw,'r',where='mid')
          axphs[3].step(xener,PHSGs,'b',where='mid')
          axphs[3].step(xener,PHSGwc,'k',where='mid')
          axphs[3].set_xlabel('pulse height (a.u.)')
          axphs[3].set_ylabel('counts')

       
    #################################### 
    # hist lambda
    if calculateLambda == 1: 
       XLamCumProj = np.sum(XLamCum,axis=0) 
       
       # lambda hist per digit
       if len(digitID)>1:
          axlam[dd].step(xlambda,XLamCumProj,where='mid')
          axlam[dd].set_xlabel('lambda (A)')
          axlam[dd].set_title('digit '+str(digitID[dd]))
          if dd == 0:
             axlam[dd].set_ylabel('counts')
       else:
          axlam.step(xlambda,XLamCumProj,where='mid')
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
 
        MONToFhistCum = hh.hist1(ToFx,MONdataCum[:,0],1)
        MONPHShistCum = hh.hist1(xener,MONdataCum[:,1],1)
             
        figmon, (axm1, axm2) = plt.subplots(figsize=(6,6), nrows=1, ncols=2)    
        pos2 = axm1.step(ToFx*1e3,MONToFhistCum,'k',where='mid')
        axm1.set_xlabel('ToF (ms)')
        axm1.set_ylabel('counts')
        axm1.set_title('MON ToF')
        pos3 = axm2.step(xener,MONPHShistCum,'k',where='mid')
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
          
        MONlamb  = tcl.ToF2lambda(MONDistance,temptof) #input m and s, output in A
            
         # append to MONdataCum col 0 ToF, col 1 PH, col 2 lambda if present 
        MONdataCum = np.append(MONdataCum,np.round(MONlamb[:,None],decimals=2),axis=1) 
           
        MONLamHistCum = hh.hist1(xlambda,MONdataCum[:,2],1) 
        
        figmonl, axml = plt.subplots(figsize=(6,6), nrows=1, ncols=1)
        axml.step(xlambda,MONLamHistCum,'k',where='mid')
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

if closeGaps == 0 or closeGaps == 2:     
    
    ########   
    # 2D image of detector X,Y
    fig2D, (ax1, ax2) = plt.subplots(figsize=(6,12), nrows=2, ncols=1)    
    # #fig.add_axes([0,0,1,1]) #if you want to position absolute coordinate
    pos1  = ax1.imshow(XYglob,aspect='auto',norm=normColors,interpolation='nearest',extent=[XXg[0],XXg[-1],YYg[-1],YYg[0]], origin='upper',cmap='jet')
    fig2D.colorbar(pos1, ax=ax1)
    # cbar1 =fig2D.colorbar(pos1,ax=ax1)
    # cbar2.minorticks_on()
    # ax1.set_aspect('tight')
    ax1.set_xlabel('Wire ch.')
    ax1.set_ylabel('Strip ch.')
    
    
    ########
    # 1D image of detector, opnly wires, in coincidence with strips (2D) and not (1D)
    XYprojGlobCoinc = np.sum(XYglob,axis=0) 
    
    pos2 = ax2.step(XXg,XYprojGlob,'r',where='mid',label='1D')
    ax2.step(XXg,XYprojGlobCoinc,'b',where='mid',label='2D')
    ax2.set_xlabel('Wire ch.')
    ax2.set_ylabel('counts')
    ax2.set_xlim(XXg[0],XXg[-1])
    legend = ax2.legend(loc='upper right', shadow=False, fontsize='large')


    ########
    # 2D image of detector ToF vs Wires 
    ToFxgms = ToFxg*1e3 # in ms 
    
    fig2, ax2 = plt.subplots(figsize=(6,6), nrows=1, ncols=1) 
    pos2  = ax2.imshow(XToFglob,aspect='auto',norm=normColors,interpolation='none',extent=[ToFxgms[0],ToFxgms[-1],XXg[0],XXg[-1]], origin='lower',cmap='jet')
    fig2.colorbar(pos2, ax=ax2)
    ax2.set_ylabel('Wire ch.')
    ax2.set_xlabel('ToF (ms)')
    
    ######## 
    # 2D image of detector Lambda vs Wires
    if calculateLambda == 1:
       figl, axl = plt.subplots(figsize=(6,6), nrows=1, ncols=1) 
       posl1  = axl.imshow(XLamGlob,aspect='auto',norm=normColors,interpolation='none',extent=[xlambdag[0],xlambdag[-1],XXg[0],XXg[-1]], origin='lower',cmap='jet')
       figl.colorbar(posl1, ax=axl)
       axl.set_ylabel('Wire ch.')
       axl.set_xlabel('lambda (A)')
   
   
########  CLOSED GAPS PLOTS  
# 2D and 1D image of detector X,Y with removed shadowed channels
if closeGaps == 1 or closeGaps == 2:
    
    XYglobc, XXgc = mbl.closeTheGaps(XYglob,XXg,YYg,gaps,1)
  
    fig2Dc, (axc1, axc2) = plt.subplots(figsize=(6,12), nrows=2, ncols=1)    
    
    posc1  = axc1.imshow(XYglobc,aspect='auto',norm=normColors,interpolation='nearest',extent=[XXgc[0],XXgc[-1],YYg[-1],YYg[0]], origin='upper',cmap='jet')
    axc1.set_xlabel('Wire ch.')
    axc1.set_ylabel('Strip ch.')
    fig2Dc.colorbar(posc1, ax=axc1)
    
    XYprojGlobCoincC = np.sum(XYglobc,axis=0)
    
    posc2 = axc2.step(XXgc,XYprojGlobCoincC,'b',where='mid',label='2D')
    axc2.set_xlabel('Wire ch.')
    axc2.set_ylabel('counts')
    axc2.set_xlim(XXgc[0],XXgc[-1])
    
    XToFglobc, __ = mbl.closeTheGaps(XToFglob,XXg,ToFxg,gaps,0)
    
    if calculateLambda == 1:
        XLamGlobc, __ = mbl.closeTheGaps(XLamGlob,XXg,xlambdag,gaps,0)
    
    # 2D image of detector ToF vs Wires 
    ToFxgms = ToFxg*1e3 # in ms 
    
    ########
    # 2D image of detector ToF vs Wires 
    fig2C, ax2C = plt.subplots(figsize=(6,6), nrows=1, ncols=1) 
    pos2C  = ax2C.imshow(XToFglobc,aspect='auto',norm=normColors,interpolation='none',extent=[ToFxgms[0],ToFxgms[-1],XXgc[0],XXgc[-1]], origin='lower',cmap='jet')
    fig2C.colorbar(pos2C, ax=ax2C)
    ax2C.set_ylabel('Wire ch.')
    ax2C.set_xlabel('ToF (ms)')
    
    ######## 
    # 2D image of detector Lambda vs Wires
    if calculateLambda == 1:
       figlC, axlC = plt.subplots(figsize=(6,6), nrows=1, ncols=1) 
       posl1C  = axlC.imshow(XLamGlobc,aspect='auto',norm=normColors,interpolation='none',extent=[xlambdag[0],xlambdag[-1],XXgc[0],XXgc[-1]], origin='lower',cmap='jet')
       figlC.colorbar(posl1C, ax=axlC)
       axlC.set_ylabel('Wire ch.')
       axlC.set_xlabel('lambda (A)')

###############################################################################
###############################################################################

plt.show()

tElapsedProfiling = time.time() - tProfilingStart
print('\n Completed --> time elapsed: %.2f s' % tElapsedProfiling)

###############################################################################
###############################################################################
print('----------------------------------------------------------------------')
