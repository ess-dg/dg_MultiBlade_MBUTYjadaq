#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
###############################################################################
########    V9.25 2021/06/09      francescopiscitelli    ######################
########    (this version uses an excel file for mapping channels into geometry)
########    (and can load either EFU files or JADAQ files)
########    After AMOR beam time, bug fixed on load file h5 and X,Y,Z in mm option
###############################################################################
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import time
import h5py
import os
import glob
import sys

# import matplotlib
# # matplotlib.use(‘Qt5Agg’)
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QGridLayout, QLabel, QLineEdit
app = QApplication(sys.argv)

# import the library with all specific functions that this code uses 
from lib import libSyncUtil as syu 
from lib import libLoadFile as lof 
from lib import libHistog as hh
from lib import libToFconverter as tcl
from lib import libMBUTY_V9x25 as mbl

###############################################################################
###############################################################################
# check version
if sys.version_info < (3,5):
   print('\n \033[1;31mPython version too old, use at least Python 3.5! \033[1;37m\n')
   print(' ---> Exiting ... \n')
   print('------------------------------------------------------------- \n')
   sys.exit()

currentLoc = os.path.abspath(os.path.dirname(__file__))

###############################################################################
###############################################################################
tProfilingStart = time.time()
print('----------------------------------------------------------------------')
plt.close("all")
###############################################################################
###############################################################################
########    here starts the section with all the settings you can choose  #####
###############################################################################
###############################################################################

sync = False   #ON/OFF if you want to rsync the data 

###############################################################################

EFU_JADAQ_fileType = False  # False = JADAQ, True = EFU file loading 

# EFU_JADAQ_fileType = True

# pathsourceEFU      = 'efu@192.168.0.58:/home/efu/data/MB18-setup/'
pathsourceJDQ      = 'jadaq@192.168.0.57:/home/jadaq/data/amor/'
pathsourceEFU      = pathsourceJDQ

# pathsourceJDQ      = 'efu@172.30.244.44:/home/efu/data/JADAQdata/farnaz/'

desitnationpath    = '/Users/francescopiscitelli/Desktop/dataA/'



datapath         = desitnationpath 
# datapath         = os.path.abspath('.')+'/data/' 
# datapath         = os.path.join('/home/efu/data', sys.argv[1], '')

# datapath         = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYjadaq_1D/'

filename = '13827-C-ESSmask-20181116-120805_00000.h5'

acqnum = [0]

# filename = 'test10-220310-092742_00000.h5'

openWindowToSelectFiles = 2
     #  0 = filename and acqnum is loaded, no window opens
     #  1 = latest file created in folder is loaded with its serial
     #  2 = filename and acqnum are both ignored, window opens and 
     #      serial is the only one selected 
     #  3 = filename is ignored, window opens and serial is acqnum  

SingleFileDuration       = 60     #s to check if h5 file has all the resets

###############################################################################
# variable POPH will be saved in a new h5 file
# saveReducedData = False #ON/OFF

# # savereducedpath = os.path.join('/home/efu/data/reduced', sys.argv[1], '')

    
# savereducedpath = '/Users/francescopiscitelli/Desktop/reducedFile/'

# reducedDataInAbsUnit = False   #ON/OFF if ON data reduced X and Y is in mm, otherwise in ch number 

# nameMainFolder  = 'entry1'

# compressionHDFT  = 'gzip'  
# compressionHDFL  = 9     # gzip compression level 0 - 9

###############################################################################

# digitID = [34,33,31,142,143,137]

digitID = [34,33,31,142,143,137]

digitID = [142]

digitID_2D = [34]
digitID_2D = None

###############################################################################
# mapping channels into geometry 

MAPPING = False     # ON/OFF, if OFF channels are used as in the file

mappath = os.path.join(currentLoc,'tables/')
mapfile = 'MB18_mapping.xlsx'

###############################################################################
                    
overflowcorr      = True   #ON/OFF (does not affect the MONITOR)
zerosuppression   = True   #ON/OFF (does not affect the MONITOR)

Clockd            = 16e-9   #s CAEN V1740D clock steps
Timewindow        = 3e-6    #s to create clusters 

###############################################################################

plotChRaw         = False   #ON/OFF plot of raw ch in the file (not flipped, not swapped) no thresholds (only for 1st serial)

plottimestamp     = True   #ON/OFF for debugging, plot the events VS time stamp (after thresholds)

plottimeTofs      = False   #ON/OFF for debugging, plot the time duration of ToFs (after thresholds)

plotInstRate      = True    #ON/OFF hist the time diff between two susequent neutrons (after clustering) to evaluate inst. rate
instRateBin       = 1e-6    #s

ToFduration       = 0.12    #s
ToFbinning        = 500e-6   #s

plotMultiplicity  = False   #ON/OFF

###############################################################################
# software thresholds
# NOTE: they are applied to the flipped or swpadded odd/even order of ch!
# th on ch number: 32 w and 32 s, one row per cassette 
softthreshold = 0   # 0 = OFF, 1 = File With Threhsolds Loaded, 2 = User defines the Thresholds in an array sth 

#####
#  if 1 the file containing the threhsolds is loaded: 

sthpath =   os.path.join(currentLoc,'tables/')
sthfile =  'MB18_thresholds.xlsx'
  
#####  
#  if 2 here you can define your thresholds, ch from 0-31 wires, ch 32 to 63 strips  
    
sth = np.ones((np.size(digitID,axis=0),64))
        
###############################################################################
# ToF gate, remove events with ToF outside the indicated range 
# (it is applied globally to all images and PH and multiplicity)
ToFgate      = False           # ON/OFF
ToFgaterange = [0.035, 0.04]   # s  

###############################################################################
# ToF per digitizer (all ch summed togheter)
plotToFhist  = False    #ON/OFF
                                                   
###############################################################################
# PHS image of all wires and strips for all digitizers             
EnerHistIMG   = True            # ON/OFF

plotEnerHistIMGinLogScale = False   # ON/OFF

energybins    = 128
maxenerg      = 30e3


###############################################################################
# Position reconstruction (max is max amplitude ch in clsuter either on w or s,
# CoG is centre of gravity on ch)

numWires  = 32    # num of wire channels always from 0 to 31
numStrips = 32    # num of strip channels, either 0 to 31 or 0 to 63
  
positionRecon = 0

# binning position 
if positionRecon == 0:
   posBins = [32,32]     # w x s max max
# elif positionRecon == 1:
#    posBins = [64,64]     # w x s CoG CoG
# elif positionRecon == 2:
#     posBins = [32,64]     # w x s max CoG
   
###############################################################################
# close the gaps, remove wires hidden; only works with posreconn 0 or 2, i.e. 32 bins on wires
closeGaps = 0     # 0 = OFF shows the raw image, 1 = ON shows only the closed gaps img, 2 shows both
# gaps      = [0, 3, 4, 4, 3, 2]   # (first must be always 0)

###############################################################################
#detector geometry

# declare distnaces with .0 to force them to be float not int 
   
inclination             = 5.0       #deg
wirepitch               = 4.0       #mm 
strippitch              = 4.0       #mm 
OffsetOf1stWires        = 11.0      #mm

DistanceWindow1stWire = 38.0        #mm distance between vessel window and first wire
DistanceAtWindow      = 18750.0     #mm from chopper to detector window
Distance              = DistanceWindow1stWire + DistanceAtWindow    #mm  flight path at 1st wire
DistanceSampleWindow  = 4000.0      #mm
DistanceSample1stWire = DistanceWindow1stWire + DistanceSampleWindow #mm
BladeAngularOffset    = 0.15      #deg


###############################################################################
# plot the 2D image of the detector, lambda and ToF in linear =0 or log scale =1
plotIMGinLogScale = True
   
###############################################################################
# LAMBDA: calcualates lambda and plot hist 
calculateLambda  = False    # ON/OFF  

plotLambdaHist   = False    # ON/OFF hist per digitiser (all ch summed togheter)
                        # (calculateLambda has to be ON to plot this)
   
lambdaBins      = 127   
lambdaRange     = [2.0, 15]    #A

#if chopper has two openings or more per reset of ToF
MultipleFramePerReset = True  #ON/OFF (this only affects the lambda calculation)
NumOfBunchesPerPulse  = 2
lambdaMIN             = 3.0     #A

# PickUpTimeShift = -0.002 #s on chopper, time shift betweeen pickup and chopper edge 
# PickUpTimeShift =  13.5/(2.*180.) * ToFduration/NumOfBunchesPerPulse  #s
PickUpTimeShift = 3e-4 
###############################################################################
# MONITOR (if present)
# NOTE: if the MON does not have any ToF, lambda and ToF spectra can be
# still calculated but perhaps meaningless

MONOnOff = True       #ON/OFF

MONdigit = 34     #digitiser of the Monitor
MONch    = 63      #ch after reorganization of channels (from 0 to 63)

MONThreshold = 0   #threshold on MON, th is OFF if 0, any other value is ON
 
plotMONtofPH = False   #ON/OFF plotting (MON ToF and Pulse Height) 

MONDistance  = 0   #m distance of MON from chopper if plotMONtofPH == 1 (needed for lambda calculation if ToF)

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

colorrp = ['r','g','b','k','m','c']

###############################################################################
#  syncing the data from remote computer where files are written

if EFU_JADAQ_fileType is False:
    pathsource = pathsourceJDQ
elif EFU_JADAQ_fileType is True: 
    pathsource = pathsourceEFU
    
if sync is True:
    syu.syncData(pathsource,desitnationpath)
###############################################################################
###############################################################################
#opening files 
   
     #  0 = filename and acqnum is loaded, no window opens
     #  1 = latest file created in folder is loaded with its serial
     #  2 = filename and acqnum are both ignored, window opens and 
     #      serial is the only one selected 
     #  3 = filename is ignored, window opens and serial is acqnum  
   
if openWindowToSelectFiles == 0:
    fname = filename
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

elif openWindowToSelectFiles >= 2:
    temp = QFileDialog.getOpenFileName(None, "Select Files", datapath, "hdf files (*.h5)")
    temp = os.path.split(temp[0])
    datapath = temp[0]+'/'
    fname    = temp[1]
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
print('\033[1;36mFile selected: '+fname+' \033[1;37m')

temp1 = fname.rsplit('_',1)
fnamepart1 = temp1[0]+'_'      #file name without serial and exstension .h5
temp2 = temp1[1].rsplit('.',1)
fnamepart3 = '.'+temp2[1]      #.h5

if openWindowToSelectFiles == 2 or openWindowToSelectFiles == 1:
    acqnum = [int(temp2[0])]

print('\033[1;36mwith serials: '+str(acqnum)+'\033[1;37m')
print('\033[1;36mand Digitizers in this order: '+str(digitID)+'\033[1;37m\n')
time.sleep(0.5)
   
###############################################################################
###############################################################################

if softthreshold == 0:
    print(' ---> Thresholds OFF ...')
elif softthreshold == 1:
    print(' ---> Thresholds ON ... Loading Threshold File ...')
    [sth,softthreshold] = mbl.softThresholds(sthpath,sthfile,digitID,softthreshold,(numWires+numStrips))
elif softthreshold == 2:   
    print(' ---> Thresholds ON ... Defined by User ...')
    
###############################################################################
###############################################################################

if MAPPING is False:
   print(' ---> Mapping OFF ...') 
elif MAPPING is True:
   mapfullpath = mappath+mapfile         
   if os.path.exists(mapfullpath) == False:
      print('\n \033[1;33m---> WARNING ... File: '+mapfullpath+' NOT FOUND\033[1;37m')
      print("\t ... Mapping switched OFF ... ")
      MAPPING = False
      time.sleep(2)
   else:
      print(' ---> Mapping ON ... Loading Mapping File ...')
      
###############################################################################
###############################################################################
      
# if closeGaps == 1 or closeGaps == 2:
    
#     print(' ---> Closing gaps ON ...')

#     if positionRecon == 1: 
#         closeGaps = 0
#         print(' \033[1;33m---> closing gaps for pos. reconstr. 1 not allowed ... skipped! \033[1;37m')

#     if len(digitID) == 1: 
#         closeGaps = 0
#         print(' \033[1;33m---> closing gaps OFF for only 1 cassette! \033[1;37m\n')
#     else:
#         if len(gaps) != len(digitID):
#             print(' \033[1;33m---> closing gaps: length(gaps) ~= length(cassette) ... check! -> Default 3 wires used ... \033[1;37m')
#             gaps    = [3]*len(digitID)
#             gaps[0] = 0

###############################################################################
###############################################################################
        
if plotIMGinLogScale is True:
    normColors = LogNorm()
elif plotIMGinLogScale is False:
    normColors = None
    
if plotEnerHistIMGinLogScale is True:
    normColorsPH = LogNorm()
elif plotEnerHistIMGinLogScale is False:
    normColorsPH = None

###############################################################################
###############################################################################
# MONITOR

# check if monitor is in the data
if MONOnOff is True: 
    if not(MONdigit in digitID):
        print(' MONITOR absent in this cassette selection!')
        MONfound = False
    elif (MONdigit in digitID):
        MONfound = True
elif MONOnOff is False:
    MONfound = False
    
###############################################################################
###############################################################################
   
# if saveReducedData is True:
    
#     if not os.path.exists(savereducedpath):
#         os.makedirs(savereducedpath)
    
#     outfile = savereducedpath+fnamepart1[:-1]+'-reduced-PY-From'+str(format(acqnum[0],'03d'))+'To'+str(format(acqnum[-1],'03d'))+fnamepart3
    
#     # check if file already exist and in case yes delete it 
#     if os.path.exists(outfile):
#        print('\n \033[1;33mWARNING: Reduced DATA file exists, it will be overwritten!\033[1;37m')
#        os.system('rm '+outfile)
       
#     # if you want to save reduced data, it must include lambda, so lambda calculation is turned ON if not yet 
#     if calculateLambda is False:
#        calculateLambda = True
#        print('\n \t Lambda calculation turned ON to save reduced DATA')
     
#     fid    = h5py.File(outfile, "w")
    
#     # create groups in h5 file  
#     gdet   = fid.create_group(nameMainFolder+'/detector')
#     ginstr = fid.create_group(nameMainFolder+'/instrument')
    
#     for key, value in {
#                 'ToF-duration (s)': ToFduration,
#                 'DistanceAtWindow (mm)': DistanceAtWindow,
#                 'Distance (mm)': Distance,
#                 'DistanceSampleWindow (mm)': DistanceSampleWindow,
#                 'DistanceSample1stWire mm)' : DistanceSample1stWire,
#                 'PickUpTimeShift (s)': PickUpTimeShift,
#                 'BladeAngularOffset (deg)': BladeAngularOffset,
#                 'OffsetOf1stWires (mm)': OffsetOf1stWires,
#                 }.items():
#         ginstr.attrs.create(key, value)
    
#     grun   = fid.create_group(nameMainFolder+'/run')
    
#     if MONfound is True:
#        gmon = fid.create_group(nameMainFolder+'/monitor')
#        gmon.attrs.create('columns:ToF,PH,lambda',1)
#        gmon.attrs.create('units:seconds,a.u.,angstrom',1)
#     ##### 

#     #grun.create_dataset('duration', data=(len(acqnum)*(SingleFileDuration or 0)))
#     #grun.attrs.create('seconds',1)
    
#     gdet.attrs.create('columns:X,Y,ToF,PHwires,PHstrips,multW,multS,Z,lambda',1)
#     if reducedDataInAbsUnit is True:
#         gdet.attrs.create('units:mm,mm,seconds,a.u.,a.u.,int,int,mm,angstrom',1)
#     elif reducedDataInAbsUnit is False:
#         gdet.attrs.create('units:chNum,chNum,seconds,a.u.,a.u.,int,int,mm,angstrom',1)
 
#     gdet.create_dataset('arrangement', data=digitID ) #physical order of the digitizers
    
###############################################################################
###############################################################################

ChWires  = [0,numWires-1]     # wire channels NOTE: if ch from 1 many things do not work on indexes, keep ch num from 0
ChStrips = [0,numStrips-1]    # strip channels

# X (w) and Y (s) axis  
XX    = np.linspace(ChWires[0],ChWires[1],posBins[0])
YY    = np.linspace(ChStrips[0],ChStrips[1],posBins[1])

# PHS x-axis energy 
xener = np.linspace(0,maxenerg,energybins)

# ToF axis  
ToFmin    = 0
ToFmax    = ToFduration
ToFbins   = round((ToFmax-ToFmin)/ToFbinning)
ToFx      = np.linspace(ToFmin,ToFmax,ToFbins)

# InstRate axis 
if plotInstRate is True:
    DRmin    = -ToFduration
    DRmax    = ToFduration
    DRbins   = round((DRmax-DRmin)/instRateBin)
    DRx      = np.linspace(DRmin,DRmax,DRbins)

# lambda axis 
if lambdaRange[1] is None:
    lambdaRange[1]=lambdaRange[0]+tcl.ToF2lambda(DistanceAtWindow/1e3, ToFduration/NumOfBunchesPerPulse)
    print("    Wavelength Range:", lambdaRange[0], '-', lambdaRange[1])
xlambda = np.linspace(lambdaRange[0],lambdaRange[1],lambdaBins)


    
# global axis
# note that bins at edges are rounded, you need to use, check XXg_explained.py
XXg      = np.linspace(XX[0],(XX[-1]-XX[0]+1)*len(digitID)*2-(1-XX[0]),posBins[0]*len(digitID)*2)         
YYg      = YY
ToFxg    = ToFx    
xlambdag = xlambda    

###############################################################################

if digitID_2D is not None:
    XYglob     = np.zeros((len(YY),(len(digitID_2D)*len(XX))))
else:
    XYglob     = np.zeros((len(YY),(1*len(XX))))
    
XYprojGlob = np.zeros(len(digitID)*2*len(XX))
XToFglob   = np.zeros(((len(digitID)*2*len(XX)),len(ToFx)))

ratePerDigit      = np.zeros((4,len(digitID)*2))
ratePerDigit[3,:] = SingleFileDuration
rateMON      = np.zeros((4,1))
rateMON[3,0] = SingleFileDuration

Durations = np.zeros((len(acqnum),len(digitID)*2))

if plotChRaw is True:
   figchraw, axchraw = plt.subplots(num=901, nrows=1, ncols=len(digitID), sharex='col', sharey='row')
   axchraw.shape     =  (1,len(digitID))
   axchraw           = np.atleast_2d(axchraw)
   
if plotInstRate is True:
    figinstrat, axinstrat = plt.subplots(num=908, nrows=1, ncols=len(digitID), sharex='col', sharey='row')
    axinstrat.shape     =  (1,len(digitID))
    axinstrat           = np.atleast_2d(axinstrat)
   
if plotMultiplicity is True:
    # figmult = plt.figure(figsize=(9,6)) # alternative way
    figmult, axmult = plt.subplots(num=401, nrows=1, ncols=len(digitID)*2, sharey='row')
    axmult.shape    = (1,len(digitID)*2)
    axmult          = np.atleast_2d(axmult)

if EnerHistIMG is True:
   figphs, axphs = plt.subplots(num=601, nrows=2, ncols=len(digitID)*2, sharex='col', sharey='row')  
   axphs.shape   = (2,len(digitID)*2)
   axphs         = np.atleast_2d(axphs)
   
if plotToFhist is True:
   figtof, axtof = plt.subplots(num=301, nrows=1, ncols=len(digitID)*2, sharex='col', sharey='row')
   axtof.shape   = (1,len(digitID)*2)
   axtof         = np.atleast_2d(axtof)
   
if calculateLambda is True:
   XLamGlob      = np.zeros(((len(digitID)*2*len(XX)),len(xlambda))) 
   if plotLambdaHist == 1:
       figlam, axlam = plt.subplots(num=302, nrows=1, ncols=len(digitID)*2, sharex='col', sharey='row')
       axlam.shape   = (1,len(digitID)*2)
       axlam         = np.atleast_2d(axlam)
  
   
###############################################################################
###############################################################################
   
##################################### 
#START LOOP OVER DIGITIZERS        
##################################### 
for dd in range(len(digitID)):
    
    XYcum     = np.zeros((len(YY),len(XX))) 
    XYprojCum = np.zeros(len(XX)*2) 
    XToFcum   = np.zeros((len(XX)*2,len(ToFx))) 
    
    if plotMultiplicity is True:
       multx   = np.arange(0,32,1)
       multcum = np.zeros((len(multx),2))
       # mult2Dcum   = np.zeros((len(multx),len(multx)))

       
    if EnerHistIMG is True:
       PHSIwCum  = np.zeros((len(xener),numWires*2))

    if calculateLambda is True:
       XLamCum = np.zeros((len(XX)*2,len(xlambda))) 
                   
    if plotInstRate is True:
        instRateCum = np.zeros(len(DRx))
        
##################################### 
#START LOOP OVER ACQNUM
#####################################      
    for ac in range(len(acqnum)):
        
        # XY     = np.zeros((len(YY),len(XX))) 
        # XYproj = np.zeros((1,len(XX)*2)) 
        # XToF   = np.zeros((len(XX)*2,len(ToFx))) 
        
        # if calculateLambda is True:
        #    XLam = np.zeros((len(XX)*2,len(xlambda))) 
   
        # print('\n ---> Reading Digitizer '+str(digitID[dd])+', serial '+str(acqnum[ac]))
        print('\n \033[1;32m---> Reading Digitizer '+str(digitID[dd])+', serial '+str(acqnum[ac])+'\033[1;37m')
       
        filenamefull = fnamepart1+str(format(acqnum[ac],'05d'))+fnamepart3

        # check if file exists in folder
        if os.path.exists(datapath+filenamefull) is False:
           print('\n \033[1;31m---> File: '+filenamefull+' DOES NOT EXIST \033[1;37m')
           print('\n ---> in folder: '+datapath+' \n')
           print(' ---> Exiting ... \n')
           print('------------------------------------------------------------- \n')
           sys.exit()
        #####################################
        
        if EFU_JADAQ_fileType is False: 
            
            try:
                [data, Ntoffi, GTime, _, flag] = lof.readHDFjadaq(datapath,filenamefull,digitID[dd],Clockd,ordertime=True)
            except: 
                print('\n \033[1;31m---> this looks like either a file created with the EFU file writer, change mode with EFU_JADAQ_fileType set to 1! Or JADAQ file maybe empty! \033[1;37m')
                flag = 2
                continue
                # print(' ---> Exiting ... \n')
                # print('------------------------------------------------------------- \n')
                # sys.exit()
                
        
        elif EFU_JADAQ_fileType is True:
            
            try:
               [data, Ntoffi, GTime, _, flag] = lof.readHDFefu(datapath,filenamefull,digitID[dd],Clockd,ordertime=True)
                    # data here is 3 cols: time stamp in s, ch 0to63, ADC, 
                    # Ntoffi num of resets
                    # GTime is time of the resets in ms, absolute time, make diff to see delta time betwen resets
                    # DGTtime global reset in ms
                    # flag is -1 if no digit is found otherwise 0    
                    #####################################
                    # IN THE FUTURE THIS HAS TO LOAD THE CASSETTE (96 CH) AND NOT THE DIGIT ONLY
            except: 
                print('\n \033[1;31m---> this looks like a file created with the JADAQ file writer, change mode with EFU_JADAQ_fileType set to 0!\033[1;37m')
                print(' ---> Exiting ... \n')
                print('------------------------------------------------------------- \n')
                sys.exit()
                
        # check if the duration of the file is correct, expected number of resets and ToFs
        if flag == 0:
           tsec   = GTime*1e-3 #s
           
           if np.shape(tsec)[0] > 1:
               if tsec[0] != 0: 
                   tsecn  = tsec-tsec[0]
               else:
                   tsecn  = tsec-tsec[1]
               
               SingleFileDurationFromFile = tsecn[-1] 
               ratePerDigit[1,2*dd] =  ratePerDigit[1,2*dd] + SingleFileDurationFromFile
               
               Durations[ac,dd] = SingleFileDurationFromFile
          
               if abs(SingleFileDurationFromFile-SingleFileDuration) > 1: #if they differ for more then 1s then warning
                   print('\n     \033[1;33mWARNING: check file duration ... found %.2f s, expected %.2f s \033[1;37m' % (SingleFileDurationFromFile,SingleFileDuration))
                   time.sleep(2)
               Ntoffiapriori = round(SingleFileDuration/ToFduration)   
               if abs(Ntoffiapriori-Ntoffi) >= 2: 
                   print('\n     \033[1;33mWARNING: check Num of ToFs ... found %d, expected %d \033[1;37m' % (Ntoffi, Ntoffiapriori))
                   
           else:
               SingleFileDurationFromFile = 0
               tsecn = np.zeros((2,1))
               
        elif flag == -1:
           SingleFileDurationFromFile = 0
           print('\n \t \033[1;33m---> No Data for Digitizer '+str(digitID[dd])+', serial '+str(acqnum[ac])+', to display ... skipped!\033[1;37m')
           continue
        #####################################
        # histogram raw channels in the file 
        if plotChRaw is True and ac == 0:
            
            # temp = data[data[:,1] <= 1 ,1]
            
            Xaxis  = np.arange(0,numWires+numStrips,1)
            histxx = hh.hist1(Xaxis,data[:,1],1)     
            
            # if len(digitID)>1:
            axchraw[0][dd].bar(Xaxis[:32],histxx[:32],0.8,color='r') 
            axchraw[0][dd].bar(Xaxis[32:],histxx[32:],0.8,color='b')
            axchraw[0][dd].set_xlabel('raw ch no.')
            axchraw[0][dd].set_title('digit '+str(digitID[dd]))
            if dd == 0:
               axchraw[0][dd].set_ylabel('counts')
            
        #####################################  
        
        # this has to be modified to have always ch wires 0 to 31 and ch strips either 32 to 63 or up to 95
        # to map MB300L with 64 strips in multiple digitisers togheter with the readder of the file that has to load the 
        # cassette and not the digit 
        
        data = mbl.mappingChToGeometry(data,MAPPING,mappath,mapfile)

        #####################################
        # MONITOR
        if MONfound is True and MONdigit == digitID[dd]:
           selMON  = data[:,1] == MONch
           temp    = data[:,[0,2]] #select only col with time stamp and charge
           MONdata = temp[selMON,:]
           MONdata[:,0] = np.around((MONdata[:,0]),decimals=6)     #  time stamp in s and round at 1us
           data    = data[np.logical_not(selMON),:] # remove MON data from data 
           rateMON[0,0] = rateMON[0,0]+len(MONdata)
           rateMON[1,0] = rateMON[1,0]+SingleFileDurationFromFile

                      
           print('\n \t \033[1;35mMonitor found ... splitting MONITOR data (%d ev.) from Data \033[1;37m' % (len(MONdata)))
           
           if ac == 0:
             MONdataCum = MONdata
           else:
             MONdataCum = np.append(MONdataCum,MONdata,axis=0)
        
        #####################################  
        data = mbl.cleaning(data,overflowcorr,zerosuppression)
        
        #####################################
        if softthreshold > 0: # ch from 0 to 63 or 95
            print(" \n \t ... software thresholds applied ... ")
            Nall = np.size(data,axis=0)
            for chj in np.arange(0,numWires+numStrips,1):
                chbelowth = np.logical_and(data[:,1] == chj,data[:,2] < sth[dd,chj])
                data[chbelowth,2] = np.nan
            data = data[np.logical_not(np.isnan(data[:,2]))]
            Nallnew = np.size(data,axis=0)
            print(" \t file length: %d, below threshold %d, new file length %d " % (Nall,Nall-Nallnew,Nallnew));
        #####################################     
            
        # if np.logical_and(plottimeTofs == 1, flag == 0):
        if plottimeTofs is True:
            deltat = np.diff(tsecn,1,axis=0)
            xax1   = np.arange(1,len(tsecn)+1,1)
            xax2   = np.arange(1,len(tsecn),1)
            xax3   = np.arange(0,0.2,0.0005) #in s
            
            fig = plt.figure(num=902, figsize=(9,6))
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
            
        if plottimestamp is True:
            fig = plt.figure(num=903, figsize=(9,6))
            ax1 = fig.add_subplot(111)
            plt.plot(np.arange(len(data[:,0])),data[:,0],marker='+',color=str(colorrp[dd]))
            plt.xlabel('trigger no.')
            plt.ylabel('time (s)')
            plt.grid(axis='x', alpha=0.75)
            plt.grid(axis='y', alpha=0.75)
            
        #####################################
        # splitting first and second block of of 32 ch for only wires 1D detector
        
        
        for bbl in range(2):
            
            if digitID_2D is not None:
            
                if digitID[dd] != digitID_2D[0]:
                    
                    print('\n \033[1;32m    ---> Splitting ch block '+str(bbl+1)+' of 2 \033[1;37m')
                
                    blockSelection = np.logical_and( data[:,1] >= bbl*32 , data[:,1] < ((bbl+1)*32) ) 
                    
                    datasSelBlock = data[blockSelection,:] 
                    
                    datasSelBlock[:,1] = datasSelBlock[:,1] - bbl*32
                      
                elif  digitID[dd] == digitID_2D[0]: 
                    
                    print('\n \033[1;32m    ---> 2D cassette -> not Splitting ch block \033[1;37m')
                        
                    if bbl == 0:
                        datasSelBlock = data
                    elif bbl==1:
                        datasSelBlock = np.zeros((1,3),dtype=float)
                    
            else:
                
                    print('\n \033[1;32m    ---> Splitting ch block '+str(bbl+1)+' of 2 \033[1;37m')
                
                    blockSelection = np.logical_and( data[:,1] >= bbl*32 , data[:,1] < ((bbl+1)*32) ) 
                    
                    datasSelBlock = data[blockSelection,:] 
                    
                    datasSelBlock[:,1] = datasSelBlock[:,1] - bbl*32
                
                
            [POPHselblk, Nevents, NumeventNoRej] = mbl.clusterPOPH(datasSelBlock,Timewindow)    
            
            # if bbl == 1 and dd == 0:
            #     POPHselblk[:,0] = POPHselblk[:,0]-5
            #     POPHselblk[:,3] = 5000
            # elif bbl == 0 and dd == 0:
            #     POPHselblk[:,0] = POPHselblk[:,0]+12
            #     POPHselblk[:,3] = 12000
            # elif bbl == 0 and dd == 1:
            #     POPHselblk[:,0] = 2
            #     POPHselblk[:,3] = 20000
            # elif bbl == 1 and dd == 1:
            #     POPHselblk[:,0] = 16
            #     POPHselblk[:,3] = 60000
                # POPHselblk[:,2] = POPHselblk[:,2]
                
            # POPH output has 7 cols:X,Y,ToF,PHwires,PHstrips,multW,multS   
 
    
            ratePerDigit[0,2*dd+bbl] = ratePerDigit[0,2*dd+bbl]+NumeventNoRej
        
        
       #  #####################################
       #  # time of arrival
            if plotInstRate is True:
              diffeTime    = np.diff(POPHselblk[:,2],n=1,axis=0)
              instRateHist = hh.hist1(DRx,diffeTime,True) 
              instRateCum  = instRateCum + instRateHist
     
         #####################################
         # gating ToF
            if ToFgate is True:
                keep = np.logical_and((POPHselblk[:,2] >= ToFgaterange[0]),(POPHselblk[:,2] < ToFgaterange[1]))
                POPHselblk = POPHselblk[keep,:]
        
             #####################################         
             # lambda
            if calculateLambda is True:
               
                #distance (in m) from first wire to the wire hit in depth       
                cosse = np.cos(np.deg2rad(inclination)) 
                ZFirstWire = (POPHselblk[:,0]*(wirepitch*cosse))  #mm
               
                Dist  = Distance + ZFirstWire #mm
               
                if MultipleFramePerReset is True:
                   #ToF shifted and corrected by number of bunches
                   ToFstart = tcl.lambda2ToF((Dist*1e-3),lambdaMIN)
                   temptof  = ( (POPHselblk[:,2]-ToFstart-PickUpTimeShift) % (ToFduration/NumOfBunchesPerPulse) ) + ToFstart
                else:
                   temptof  = POPHselblk[:,2]
              
                lamb  = tcl.ToF2lambda((Dist*1e-3),temptof) #input m and s, output in A
                
                # append to POPH col 7 of POPH is depth in detector - z (mm) and col 8 is lambda
                POPHselblk = np.append(POPHselblk,np.round(ZFirstWire[:,None],decimals=2),axis=1) 
                POPHselblk = np.append(POPHselblk,np.round(lamb[:,None],decimals=2),axis=1)
           
           
         #####################################           
            if plotMultiplicity is True:
                
                myw  = hh.hist1(multx,POPHselblk[:,5],1) # wires all
               
                multcum[:,bbl] = multcum[:,bbl]+myw         

                # mult2Dcum    = mult2Dcum+my2Dwc
 
            #####################################         
            # energy hist
            if EnerHistIMG is True:
                
                PHSIw  = np.zeros((len(xener),numWires*2)) 
   
                chwRound  = np.round(POPHselblk[:,0])

                for chi in range(0,numWires,1):    # wires
                      PHSIw[:,bbl*32+chi] = hh.hist1(xener,POPHselblk[chwRound == chi,3],1) # wires all
    
                PHSIwCum  = PHSIwCum  + PHSIw
               
               
            #####################################         
            # X,Y,ToF hist         
            XY, XYproj, XToF = mbl.myHistXYZ(XX,POPHselblk[:,0],YY,POPHselblk[:,1],ToFx,POPHselblk[:,2],coincidence=False,showStats=True)
            
            XYcum     = XYcum + XY
            XYprojCum[bbl*32:(bbl+1)*32]   = XYprojCum[bbl*32:(bbl+1)*32] + XYproj
            XToFcum[bbl*32:(bbl+1)*32,:]   = XToFcum[bbl*32:(bbl+1)*32,:] + XToF

            ##################################### 
            # hist lambda
            if calculateLambda == 1:   
                __ , __ , XLam = mbl.myHistXYZ(XX,POPHselblk[:,0],YY,POPHselblk[:,1],xlambda,POPHselblk[:,8],coincidence=False,showStats=False)  
                      
                XLamCum[bbl*32:(bbl+1)*32,:] = XLamCum[bbl*32:(bbl+1)*32,:] + XLam
                
       #  #####################################    
       #  if saveReducedData is True:
       #      if ac == 0:
       #         POPHcum = POPH
       #      else:
       #         POPHcum = np.append(POPHcum,POPH,axis=0)
               
       #  #####################################
       #  # correlation PH wires VS PH strips (only for the first serial acqnum)
       #  if CorrelationPHSws is True and ac == 0:
            
       #      # if you want to remove the 1D
       #      PH1 =  POPH[POPH[:,1]>=0,3]  
       #      PH2 =  POPH[POPH[:,1]>=0,4] 
       #      #  all events also 1D
       #      # PH1 = POPH[:,3]
       #      # PH2 = POPH[:,4]
            
       #      PHcorr = hh.hist2(xener,PH1,xener,PH2,0)
        
       #      axphscorr[0][dd].imshow(PHcorr,aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],xener[0],xener[-1]], origin='lower',cmap='jet')
       #      if dd == 0:
       #         axphscorr[0][dd].set_ylabel('pulse height strips (a.u.)')
       #         axphscorr[0][dd].set_xlabel('pulse height wires (a.u.)')
       #         axphscorr[0][dd].set_title('digit '+str(digitID[dd]))            
    
#####################################             
##################################### 
#END LOOP OVER ACQNUM
#####################################    
      

    # fill global hist  
    indexes = ((2*dd*len(XX) + np.arange(2*len(XX))))
    
    if digitID_2D is not None:
        if  digitID[dd] == digitID_2D[0]:
            XYglob = XYcum
        
    XYprojGlob[indexes] = XYprojCum
    XToFglob[indexes,:] = XToFcum
        
    if calculateLambda is True: 
       XLamGlob[indexes,:] = XLamCum
                       
    #####################################           
    if plotMultiplicity is True:     
        
        for bblk in range(2):
        
            multcumnorm   = multcum[:,bblk]/np.sum(multcum[:,bblk],axis=0)
            
            width = 0.2
           
            extentplot = 7
        
            # ax  = figmult.add_subplot(1,len(digitID),dd+1) # alternative way
            axmult[0][2*dd+bblk].bar(multx[:extentplot],multcumnorm[:extentplot],width,label='w')
            # axmult[0][dd].bar(multx[:extentplot]+ width,multcumnorm[:extentplot,1],width,label='s')
            # axmult[0][dd].bar(multx[:extentplot],multcumnorm[:extentplot,2],width,label='w coinc. s')
            axmult[0][2*dd+bblk].set_xlabel('multiplicity')
            axmult[0][2*dd+bblk].set_title('digit '+str(digitID[dd])+' block '+str(bblk+1))
            # legend = axmult[0][dd].legend(loc='upper right', shadow=False, fontsize='large')
            if dd == 0:
              axmult[0][2*dd+bblk].set_ylabel('probability')
    
               # # CHECK HOW TO MAKE LEGEND IT DOES NOT WORK 
               # axmult.set_xlabel('multiplicity')
               # axmult.set_ylabel('probability')
               # legend = axmult.legend(loc='upper right', shadow=False, fontsize='large')
           
            # pos1 = axmult[1][dd].imshow(mult2Dcumnorm[:extentplot,:extentplot],aspect='auto',norm=None,interpolation='none',extent=[multx[0]-0.5,multx[extentplot]-0.5,multx[0]-0.5,multx[extentplot]-0.5], origin='lower',cmap='jet')
            # axmult[1][dd].set_xlabel('multiplicity wires')
            # if dd == 0:
            #     axmult[1][dd].set_ylabel('multiplicity strips')
               
            # plt.colorbar(pos1,ax=axmult[1][dd])
       
       
       
   ##################################### 
    if plotToFhist is True:
        
        for bblk in range(2):
            
            XToFcumSum = np.sum(XToFcum[bblk*32:(bblk+1)*32,:],axis=0)
           
            ToFxms = ToFx*1e3 # in ms 
           
            # if len(digitID)>1:
            axtof[0][2*dd+bblk].step(ToFxms,XToFcumSum,where='mid')
            axtof[0][2*dd+bblk].set_xlabel('ToF (ms)')
            axtof[0][2*dd+bblk].set_title('digit '+str(digitID[dd])+' block '+str(bblk+1))
            if dd == 0:
              axtof[0][2*dd+bblk].set_ylabel('counts')
          
    #####################################         
    # energy hist
    if EnerHistIMG is True:

       for bblk in range(2):
           
           temp = PHSIwCum[:, bblk*32:(bblk+1)*32 ]
           
           axphs[0][2*dd+bblk].imshow(np.rot90(temp),aspect='auto',norm=normColorsPH,interpolation='none',extent=[xener[0],xener[-1],ChWires[1]+0.5,ChWires[0]-0.5], origin='lower',cmap='jet')
           if dd == 0:
               axphs[0][2*dd+bblk].set_ylabel('wires ch. no.')
           axphs[0][2*dd+bblk].set_title('digit '+str(digitID[dd])+' block '+str(bblk+1))
               
           #global PHS
           PHSGw  = np.sum(temp,axis=1)
           
           # global PHS plot
           axphs[1][2*dd+bblk].step(xener,PHSGw,'r',where='mid')
    
           axphs[1][2*dd+bblk].set_xlabel('pulse height (a.u.)')
           if dd == 0:
               axphs[1][2*dd+bblk].set_ylabel('counts')
               
    # #####################################         
    # # inst rate hist
    if plotInstRate is True:
        axinstrat[0][dd].step(DRx*1e6,instRateCum,'k',where='mid')
        axinstrat[0][dd].set_xlabel('delta time between events (us)')
        if dd == 0:
            axinstrat[0][dd].set_ylabel('num of events')

    #################################### 
    # hist lambda
    if calculateLambda is True and plotLambdaHist is True:
    
        for bblk in range(2):
            
           XLamCumProj = np.sum(XLamCum[bblk*32:(bblk+1)*32,:],axis=0) 
           
           # lambda hist per digit
           axlam[0][2*dd+bblk].step(xlambda,XLamCumProj,where='mid')
           axlam[0][2*dd+bblk].set_xlabel('lambda (A)')
           axlam[0][2*dd+bblk].set_title('digit '+str(digitID[dd])+' block '+str(bblk+1))
           if dd == 0:
              axlam[0][2*dd+bblk].set_ylabel('counts')
  
    ####################################    
    # saving data to h5 file      
    # if saveReducedData is True:

    #    if reducedDataInAbsUnit is True:
    #            sinne = np.sin(np.deg2rad(inclination)) 
               
    #            # ucomment this line if you want to include the offset of blades at 1st wire in the reduced data 
    #            # POPHcum[:,0] = np.round( (POPHcum[:,0]*(wirepitch*sinne) + OffsetOf1stWires*dd), decimals=2 )  #mm
               
    #            POPHcum[:,0] = np.round( (POPHcum[:,0]*(wirepitch*sinne)), decimals=2 )  #mm
                    
    #            POPHcum[:,1] = np.round((POPHcum[:,1]*strippitch), decimals=2 )  #mm
    #            POPHcum[POPHcum[:,1]<0,1] = -1
               
        
    #    gdetdigit = gdet.create_group('digit'+ str(digitID[dd]))
    #    gdetdigit.create_dataset('data', data=POPHcum, compression=compressionHDFT, compression_opts=compressionHDFL)
          
#####################################            
##################################### 
#END LOOP OVER DIGITIZERS        
##################################### 

###############################################################################
###############################################################################

#   # saving data to h5 file      
# if saveReducedData is True:
   
#    if MONdigit in digitID:
#        Tduration = Durations[:, digitID.index(MONdigit)].sum()
#    else:
#        Tduration = Durations[:, 0].sum()
   
#    grun.create_dataset('TotalDuration', data=Tduration)
#    grun.attrs.create('seconds',1)
   
#    grun.create_dataset('Durations', data=Durations)
#    #run.attrs.create('seconds',1)
     
###############################################################################
###############################################################################
# #  rates 
# try:
#     ratePerDigit[2,:] = ratePerDigit[0,:]/ratePerDigit[1,:] 
    
#     rateGlobal   = np.sum(ratePerDigit[0,:])
#     rateGlobal   = round(rateGlobal/ratePerDigit[1,0],2)
     
#     print('\n \033[1;36mGlobal (time averaged - duration %d s from file) rate on detector (selected Digit.): %d Hz \033[1;37m' % (SingleFileDurationFromFile, rateGlobal))
    
#     if MONfound == 1:
#         rateMON[2,0] = round(rateMON[0,0]/rateMON[1,0],2)
#         print(' \033[1;35mMonitor rate: %d Hz \033[1;37m' % (rateMON[2,0]))
# except:
#     ratePerDigit[2,:] = ratePerDigit[0,:]/ratePerDigit[3,:] 
    
#     rateGlobal   = np.sum(ratePerDigit[0,:])
#     rateGlobal   = round(rateGlobal/ratePerDigit[3,0],2)
    
    
#     print('\n \033[1;36mGlobal (time averaged - duration %d s a priori) rate on detector (selected Digit.): %d Hz \033[1;37m' % (SingleFileDuration, rateGlobal))
    
#     if MONfound == 1:
#         rateMON[2,0] = round(rateMON[0,0]/rateMON[3,0],2)
#         print(' \033[1;35mMonitor rate: %d Hz \033[1;37m' % (rateMON[2,0]))
  
###############################################################################
###############################################################################
# MONITOR
if MONfound is True:
  
    if MONThreshold > 0:
       aboveTh = MONdataCum[:,1] >= MONThreshold
       MONdataCum = MONdataCum[aboveTh,:]

    if plotMONtofPH is True:
 
        MONToFhistCum = hh.hist1(ToFx,MONdataCum[:,0],1)
        MONPHShistCum = hh.hist1(xener,MONdataCum[:,1],1)
             
        figmon, (axm1, axm2) = plt.subplots(num=801, figsize=(6,6), nrows=1, ncols=2)    
        pos2 = axm1.step(ToFx*1e3,MONToFhistCum,'k',where='mid')
        axm1.set_xlabel('ToF (ms)')
        axm1.set_ylabel('counts')
        axm1.set_title('MON ToF')
        pos3 = axm2.step(xener,MONPHShistCum,'k',where='mid')
        axm2.set_xlabel('pulse height (a.u.)')
        axm2.set_ylabel('counts')
        axm2.set_title('MON PHS')
 
    if calculateLambda is True and plotMONtofPH is True:
        
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
        
        figmonl, axml = plt.subplots(num=802, figsize=(6,6), nrows=1, ncols=1)
        axml.step(xlambda,MONLamHistCum,'k',where='mid')
        axml.set_xlabel('lambda (A)')
        axml.set_ylabel('counts')
        axml.set_title('MON lambda')
       
    MONtotCounts = len(MONdataCum[:,0])   
         
    # if saveReducedData is True:  
    #   gmon.create_dataset('counts', data=[MONtotCounts], compression=compressionHDFT, compression_opts=compressionHDFL)
    #   gmon.create_dataset('data', data=MONdataCum, compression=compressionHDFT, compression_opts=compressionHDFL)
       
###############################################################################
###############################################################################

# if saveReducedData is True:
#    # close h5 file
#    fid.close(

###############################################################################
###############################################################################


if digitID_2D is not None:
    
    index = digitID.index(digitID_2D[0])
    
    indexSt = 2*index+1

    Axis1Dlength = 2*len(digitID) - len(digitID_2D)
    
    XYprojGlob2  = np.zeros(Axis1Dlength*len(XX))
    XToFglob2    = np.zeros((Axis1Dlength*len(XX),len(ToFx)))
    XXg2         = np.linspace(XX[0],(XX[-1]-XX[0]+1)*Axis1Dlength-(1-XX[0]),posBins[0]*Axis1Dlength)  
    XLamGlob2    = np.zeros((Axis1Dlength*len(XX),len(xlambda))) 
  

    for kk in range(Axis1Dlength):
        
        # XXg2[kk*len(XX):(kk+1)*len(XX)]  = XXg[kk*len(XX):(kk+1)*len(XX)] 

        if kk < indexSt:
            
            XYprojGlob2[kk*len(XX):(kk+1)*len(XX)]  = XYprojGlob[kk*len(XX):(kk+1)*len(XX)]
            XToFglob2[kk*len(XX):(kk+1)*len(XX),:]  = XToFglob[kk*len(XX):(kk+1)*len(XX),:]
            
            if calculateLambda is True:
                XLamGlob2[kk*len(XX):(kk+1)*len(XX),:]  = XLamGlob[kk*len(XX):(kk+1)*len(XX),:]
        
        elif kk >= indexSt:
            
            XYprojGlob2[kk*len(XX):(kk+1)*len(XX)]  = XYprojGlob[(kk+1)*len(XX):(kk+2)*len(XX)]
            XToFglob2[kk*len(XX):(kk+1)*len(XX),:]  = XToFglob[(kk+1)*len(XX):(kk+2)*len(XX),:]
            
            if calculateLambda is True:
                XLamGlob2[kk*len(XX):(kk+1)*len(XX),:]  = XLamGlob[(kk+1)*len(XX):(kk+2)*len(XX),:]
            
else:

    Axis1Dlength = 2*len(digitID) 

    XYprojGlob2   = XYprojGlob  
    XToFglob2     = XToFglob
    XXg2 = XXg 
    if calculateLambda is True:
        XLamGlob2 = XLamGlob
    
    
###############################################################################
###############################################################################

if closeGaps == 0 or closeGaps == 2:     
    
     ########
    
    mmaxxi = np.max(XYprojGlob2)*1.05
    
    ########   
    fig2, (ax1, ax2) = plt.subplots(num=101,figsize=(10,10), nrows=1, ncols=2)    
    
    pos1 = ax1.step(XXg2,XYprojGlob2,'k',where='mid',label='1D')
    ax1.set_ylabel('Wire ch.')
    ax1.set_ylabel('counts')
    ax1.set_xlim(XXg2[0],XXg2[-1])
    
    for kk in range(len(digitID)*2):
        ax1.plot([kk*32, kk*32],[0, mmaxxi],'r:', lw=1)
    
    ToFxgms = ToFxg*1e3 # in ms 
    
    pos2  = ax2.imshow(XToFglob2,aspect='auto',norm=normColors,interpolation='nearest',extent=[ToFxgms[0],ToFxgms[-1],XXg2[0],XXg2[-1]], origin='lower',cmap='viridis')
    fig2.colorbar(pos2, ax=ax2)
    ax2.set_ylabel('Wire ch.')
    ax2.set_xlabel('ToF (ms)')
    
    
    if digitID_2D is not None:
        fig2D, ax1 = plt.subplots(num=102,figsize=(10,10), nrows=1, ncols=1)  
        pos1  = ax1.imshow(XYglob,aspect='auto',norm=normColors,interpolation='none',extent=[XX[0],XX[-1],YYg[-1],YYg[0]], origin='upper',cmap='viridis')
        fig2D.colorbar(pos1, ax=ax1, orientation="horizontal",fraction=0.07,anchor=(1.0,0.0))
        ax1.set_xlabel('Wire ch.')
        ax1.set_ylabel('Strip ch.')
        ax1.set_title('2D cassette '+str(digitID_2D[0]))

    
    ######## 
    # 2D image of detector Lambda vs Wires
    if calculateLambda is True:
       figl, axl = plt.subplots(num=103,figsize=(6,6), nrows=1, ncols=1) 
       posl1  = axl.imshow(XLamGlob2,aspect='auto',norm=normColors,interpolation='nearest',extent=[xlambdag[0],xlambdag[-1],XXg[0],XXg[-1]], origin='lower',cmap='viridis')
       figl.colorbar(posl1, ax=axl)
       axl.set_ylabel('Wire ch.')
       axl.set_xlabel('lambda (A)')
   
   
# ########  CLOSED GAPS PLOTS  
# # 2D and 1D image of detector X,Y with removed shadowed channels
# if closeGaps == 1 or closeGaps == 2:
    
#     XYglobc, XXgc = mbl.closeTheGaps(XYglob,XXg,YYg,gaps,1)
  
#     fig2Dc, (axc1, axc2) = plt.subplots(num=201,figsize=(6,12), nrows=2, ncols=1)    
    
#     posc1  = axc1.imshow(XYglobc,aspect='auto',norm=normColors,interpolation='nearest',extent=[XXgc[0],XXgc[-1],YYg[-1],YYg[0]], origin='upper',cmap='jet')
#     axc1.set_xlabel('Wire ch.')
#     axc1.set_ylabel('Strip ch.')
#     fig2Dc.colorbar(posc1, ax=axc1,orientation="horizontal",fraction=0.07,anchor=(1.0,0.0))
    
#     XYprojGlobCoincC = np.sum(XYglobc,axis=0)
    
#     posc2 = axc2.step(XXgc,XYprojGlobCoincC,'b',where='mid',label='2D')
#     axc2.set_xlabel('Wire ch.')
#     axc2.set_ylabel('counts')
#     axc2.set_xlim(XXgc[0],XXgc[-1])
    
#     XToFglobc, __ = mbl.closeTheGaps(XToFglob,XXg,ToFxg,gaps,0)
    
#     if calculateLambda is True:
#         XLamGlobc, __ = mbl.closeTheGaps(XLamGlob,XXg,xlambdag,gaps,0)
    
#     # 2D image of detector ToF vs Wires 
#     ToFxgms = ToFxg*1e3 # in ms 
    
#     ########
#     # 2D image of detector ToF vs Wires 
#     fig2C, ax2C = plt.subplots(num=202,figsize=(6,6), nrows=1, ncols=1) 
#     pos2C  = ax2C.imshow(XToFglobc,aspect='auto',norm=normColors,interpolation='nearest',extent=[ToFxgms[0],ToFxgms[-1],XXgc[0],XXgc[-1]], origin='lower',cmap='jet')
#     fig2C.colorbar(pos2C, ax=ax2C)
#     ax2C.set_ylabel('Wire ch.')
#     ax2C.set_xlabel('ToF (ms)')
    
#     ######## 
#     # 2D image of detector Lambda vs Wires
#     if calculateLambda is True:
#        figlC, axlC = plt.subplots(num=203,figsize=(6,6), nrows=1, ncols=1) 
#        posl1C  = axlC.imshow(XLamGlobc,aspect='auto',norm=normColors,interpolation='nearest',extent=[xlambdag[0],xlambdag[-1],XXgc[0],XXgc[-1]], origin='lower',cmap='jet')
#        figlC.colorbar(posl1C, ax=axlC)
#        axlC.set_ylabel('Wire ch.')
#        axlC.set_xlabel('lambda (A)')

###############################################################################
###############################################################################

plt.show()

tElapsedProfiling = time.time() - tProfilingStart
print('\n Completed --> elapsed time: %.2f s' % tElapsedProfiling)

# img=mpimg.imread('finIMG.jpg')
# figf = plt.figure(num=1000)
# figf.add_subplot(111)
# imgplot = plt.imshow(img)
# plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis

###############################################################################
###############################################################################
print('----------------------------------------------------------------------')
