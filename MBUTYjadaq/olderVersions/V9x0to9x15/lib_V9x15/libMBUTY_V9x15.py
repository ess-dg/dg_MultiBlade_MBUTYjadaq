#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 12:02:23 2020

@author: francescopiscitelli
"""

import os
import pandas as pd
import numpy  as np
import time
# import h5py

# NOTE: this module already supports 32 wires and 64 strips 

###############################################################################
###############################################################################
#cluster with improved speed perfomance 
    
def clusterPOPH (data,Timewindow):

        # data is col 0: time stamp in s, col 1: ch number (FROM 0 TO 63 or 95), col2: ADC value
        # IT MUST BE 3 columns 
        # it works either if strips are 32 or 64
        # INPUT always wires ch from 0 to 31 and strips from 32 to 63 or 95 
        # OUTPUT if there is no strip in coincidence it will be -1 in position, with 0 PH and 0 multiplicity
        # wires in output are always from 0 to 31 and strips either from 0 to 31 or 0 to 63
        # NOTE: in both cases of clusters with more than 32 wires or 32 strips are anyhow rejected
        
    print('\n \t clustering ... ',end='')
        
    # this is a trick to accept also the clusters very close in time otherwise rejected
    Timewindowrec = np.ceil(Timewindow*1e6/3)/1e6+0.01e-6;
    Timewindow    = Timewindow+0.01e-6;
    ##########
        
    data = np.concatenate((np.zeros([1,np.shape(data)[1]]),data),axis=0)  #add a line at top not to lose the 1st event
        
    tof        = data[:,0]                        #tof column in seconds
    tof1us     = np.around(tof, decimals=6) #tof rounded at 1us precision 
        
    data[:,0]  = tof1us
        
    dtof1us = np.diff(tof1us[:])                   #1st derivative of tof 
    dtof1us = np.concatenate(([0],dtof1us),axis=0) #add a zero at top to restore length of vector
        
    clusterlogic = (np.absolute(dtof1us) <= Timewindowrec) #is zero when a new cluster starts 
        
    # data1 = np.concatenate((data,clusterlogic[:,None]),axis=1) #this is for debugging 
        
    index = np.argwhere(clusterlogic == 0) #find the index where a new cluster may start 
    
    #################################
    
    ADCCH = np.zeros((np.shape(data)[0],12))
    
    ADCCH[:,0:3] = data         # first 3 columns as data
    ADCCH[:,3]   = clusterlogic # col 3 is 0 where a new cluster may start
    
    ADCCH[:,4]   = data[:,1] <= 31   # wire  (this is 31 if ch from 0)
    ADCCH[:,5]   = data[:,1] >= 32   # strip (this is 32 if ch from 0)
    
    ADCCH[:,6]   = data[:,1]*ADCCH[:,4]   # wire ch
    ADCCH[:,7]   = data[:,1]*ADCCH[:,5]   # strip ch
    
    ADCCH[:,8]   = data[:,2]*ADCCH[:,4]   # wire ADCs 
    ADCCH[:,9]  = data[:,2]*ADCCH[:,5]   # strip ADCs 
    
    ADCCH[:,10]  =  ADCCH[:,4]*ADCCH[:,6]*ADCCH[:,8]    # weighted position on wires
    ADCCH[:,11]  =  ADCCH[:,5]*ADCCH[:,7]*ADCCH[:,9]    # weighted position on strips
    
    #################################
    
    NumClusters = np.shape(index)[0]
            
    rejCounter = np.zeros(5)
        
    POPH = np.zeros((NumClusters,7))  #output data with col0 position wires, col1 poisiton strips, col2 tof, col3 pulse height wires, col4 pulse height strips, col 5 multiplicity w, col 6 muiltiplicity strips
    
    # filling ToF column
    tempTof   = data[index,0]
    POPH[:,2] = tempTof[:,0]     #tof
     
    #################################
    
    # add a fake last cluster to make loop up to the very last true cluster
    index = np.concatenate((index,[[np.shape(data)[0]]]),axis=0)
    ADCCH = np.concatenate((ADCCH,np.zeros((1,12))),axis=0) 
    
    intervals = 4
    
    for kk in range(0,NumClusters,1):
        
            steps = round(NumClusters/intervals)
            if np.mod(kk,steps) == 0 or kk == (NumClusters-1):
                percents = int(round(100.0 * kk / float(NumClusters), 1))
                print('['+format(percents,'01d') + '%]',end=' ')
            
            clusterq = ADCCH[index[kk,0]:index[kk+1,0],:]
            
            acceptWindow = ((clusterq[-1,0] - clusterq[0,0]) <= Timewindow)  #max difference in time between first and last in cluster 
            
            clusterq = clusterq[clusterq[:,1].argsort(kind='quicksort'),:]  #order cluster by ch number
       
            is_wire  = clusterq[:,4] == 1
            is_strip = clusterq[:,5] == 1
            
            # n wires n strips in cluster
            ww = len(clusterq[is_wire, 4])  #num of wires in cluster
            ss = len(clusterq[is_strip, 5])  #num of strips in cluster

            
            if (ww != 0 and ss != 0 and ss <= 32 and ww <= 32 and acceptWindow): #if there is at least 1 wire and 1 strip and no ch number above 32

                mmaxw = clusterq[is_wire, 6][-1]
                mmaxs = clusterq[is_strip, 7][-1]
                mminw = clusterq[is_wire, 6][0]
                mmins = clusterq[is_strip, 7][0]
    
                neigw = (mmaxw - mminw) == (ww-1) #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
                neigs = (mmaxs - mmins) == (ss-1)
                
                if (neigw == 1 and neigs == 1):    #if they are neighbour then...
                    
                    rejCounter[0] = rejCounter[0]+1;   #counter 2D
                    
                    POPH[kk,5]   = ww     #multiuplicity wires
                    POPH[kk,6]   = ss     #multiuplicity strips
                    POPH[kk,3]   = np.sum(clusterq[:,8],axis=0)   #PH wires
                    POPH[kk,4]   = np.sum(clusterq[:,9],axis=0)  #PH strips
                    POPH[kk,0]   = round((np.sum(clusterq[:,10],axis=0))/(POPH[kk,3]),2)         #position wires 0 to 31
                    POPH[kk,1]   = round((((np.sum(clusterq[:,11],axis=0))/(POPH[kk,4]))-32),2)  #position strips from 0 to 31 or up to 63
    
                else:
                    rejCounter[1] = rejCounter[1]+1;                #counter if they are no neighbour 
                    
            elif (ww >= 1 and ss == 0 and ww <= 32 and acceptWindow): #put in 1D hist only for wires when there is no strip 
                    
                mmaxw = clusterq[is_wire, 6][-1]
                mminw = clusterq[is_wire, 6][0] 
    
                neigw = (mmaxw - mminw) == (ww-1)    #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
               
                if (neigw == 1):    #if they are neighbour then...
        
                    rejCounter[2] = rejCounter[2]+1;                #counter 1D
        
                    POPH[kk,5]   = ww     #multiuplicity wires
                    POPH[kk,3]   = np.sum(clusterq[:,8],axis=0)   #PH wires
                    POPH[kk,0]   = round((np.sum(clusterq[:,10],axis=0))/(POPH[kk,3]),2)         #position wires
                    POPH[kk,1]   = -1 #position strips if absent
                       
                else:
                    rejCounter[1] = rejCounter[1]+1              #counter if they are no neighbour 
                    
            elif (ww >= 33 or ss >= 33):
                  rejCounter[3] = rejCounter[3]+1               #counter if cluster above possible limits          
                  print('\n cluster > 32 in either directions w or s -> probably rate too high \n')
                 
            else:
                rejCounter[4] = rejCounter[4]+1               #any other case not taken into account previously
                
    
    print('\n')        
       
    rejected = np.logical_and((POPH[:,5] == 0),(POPH[:,6] == 0))    #remove rejected from data in rejCoiunter[4] it is when only strips and wire and sgtrip mult is 0, whole row in POPH is 0 actually 
        
    POPH     = POPH[np.logical_not(rejected),:]    #remove rejected from data
    
    ################################
    # some stats    
    NumeventNoRej = NumClusters - (rejCounter[1]+rejCounter[3]+rejCounter[4]);
    rej2 = 100*(rejCounter/NumClusters);
    rej3 = 100*(rejCounter/NumeventNoRej);
        
    print("\t N of events: %d -> not rejected (2D and 1D) %d " % (NumClusters,NumeventNoRej))
    print("\t not rej (2D) %.1f%%, only w (1D) %.1f%%, rejected (2D or 1D) %.1f%%, rejected >32 %.1f%%, rejected other reasons (only strips - noise)  %.1f%% " % (rej2[0],rej2[2],rej2[1],rej2[3],rej2[4]));
    print("\t not rej (2D) %.1f%%, only w (1D) %.1f%% \n " % (rej3[0],rej3[2]))
        
    mbins = np.arange(0,33,1)
        
    TwoDim = POPH[:,1] >= 0
    multiwhistcoinc = np.histogram(POPH[TwoDim,5],mbins)
    multishistcoinc = np.histogram(POPH[:,6],mbins)
    
    if  sum(multiwhistcoinc[0]) != 0:        
        wirefire  = multiwhistcoinc[0]/sum(multiwhistcoinc[0])
        stripfire = multishistcoinc[0]/sum(multishistcoinc[0][1:])
        print(' \t multiplicity:')      
        print(" \t 2D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*wirefire[1],100*wirefire[2],100*wirefire[3],100*wirefire[4],100*wirefire[5])); 
        print(" \t 2D: percentage of strips fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*stripfire[1],100*stripfire[2],100*stripfire[3],100*stripfire[4],100*stripfire[5])); 
                     
    OneDim = POPH[:,1] == -1
    multiwhist = np.histogram(POPH[OneDim,5],mbins)
            
    if  sum(multiwhist[0]) != 0:
        wirefire1D  = multiwhist[0]/sum(multiwhist[0])
                
        print(" \t 1D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5) \n" % (100*wirefire1D[1],100*wirefire1D[2],100*wirefire1D[3],100*wirefire1D[4],100*wirefire1D[5])); 

    return POPH, NumClusters, NumeventNoRej


#HERE ENDS CLUSTERPOPH improved speed

###############################################################################
###############################################################################

def myHistXYZ (XX,A,YY,B,ZZ,C,coincidence=1,showStats=1):
 
    #  you pass the vectors XX, YY, ToFx, POPH
               
    # A = POPH[:,0]
    # B = POPH[:,1]
    # C = POPH[:,2]
           
    if coincidence == 1:
       print('\t building histograms ... coincidence ON ...')
    else:
       print('\t building histograms ... coincidence OFF ...')
       
    binX   = len(XX) 
    binY   = len(YY)
    binZ   = len(ZZ)
        
    Xmin   = min(XX) 
    Xmax   = max(XX) 
    Ymin   = min(YY) 
    Ymax   = max(YY) 
    Zmin   = min(ZZ)
    Zmax   = max(ZZ) 
           
    XY     = np.zeros((binY,binX)) 
    XYproj = np.zeros(binX) 
    XZ     = np.zeros((binX,binZ)) 
         
    count   = np.zeros((3,2)) #counter for rejected and good evetns
           
    if (not( (len(A) == len(B)) and (len(A) == len(C)))):
        print('\n \t \033[1;31m----> ABORT: X and/or Y and/or T not same length! \033[1;37m\n')
        return XY, XYproj, XZ

    xxtemp  =  np.int_(np.around(((binX-1)*((A-Xmin)/(Xmax-Xmin)))))
    yytemp  =  np.int_(np.around(((binY-1)*((B-Ymin)/(Ymax-Ymin)))))
    zztemp  =  np.int_(np.around(((binZ-1)*((C-Zmin)/(Zmax-Zmin)))))
         
    Nev = len(A)
        
    for k in range(0,Nev,1):
            
            xx =  xxtemp[k]
            yy =  yytemp[k]
            zz =  zztemp[k]
            
            #####################################
            if ( (xx >= 0) and (xx <= binX-1) ):
                
                # 2D hist X-Y
                if ( (yy >= 0) and (yy <= binY-1) ):
                    XY[yy,xx]  += 1
                    count[0,0] += 1  # if 2D
                else:
                    count[0,1] += 1  # if 1D
               
                # 1D hist X
                XYproj[xx]  += 1
                count[1,0]  += 1   # if at least 1D

                # 2D hist X-ToF or X-Lambda
                if coincidence == 1:
                     if ( (yy >= 0) and (yy <= binY-1) and (zz >= 0) and (zz <= binZ-1) ):
                         XZ[xx,zz]  += 1
                         count[2,0] += 1
                     else:
                         count[2,1] += 1
                elif coincidence == 0:
                     if ( (zz >= 0) and (zz <= binZ-1) ):
                         XZ[xx,zz]  += 1
                         count[2,0] += 1
                     else:
                         count[2,1] += 1
                         
            else:
                 count[1,1] += 1
            #####################################
                 
    countn = 100*(count/Nev)
       
    if count[1,1] != 0 :
       print('\n \t \033[1;33mWARNING: %.1f%% out of 1D boundaries \033[1;37m\n' % count[1,1])

    if showStats == 1:
       print(' \t percentage in 2D hist: %.1f%%, out of boundaries or only w %.1f%%' % (countn[0,0],countn[0,1]))
       print(' \t percentage in proj hist: %.1f%% (only w), out of boundaries %.1f%%' % (countn[1,0],countn[1,1]))
       print(' \t percentage in ToF/Lambda hist: %.1f%%, out of boundaries or only w %.1f%%' % (countn[2,0],countn[2,1]))
    
    return XY, XYproj, XZ
    
###############################################################################
###############################################################################
    
def softThresholds (sthpath,sthfile,digitID,softthreshold,numChannels=64):    
    
# digitID = [33,142,143,137]

# sthpath =  '/Users/francescopiscitelli/Documents/PYTHON/MBUTY/'
# sthfile = 'ThresholdsMB182.xlsx'

# softthreshold = 1

# 
        sthfullpath = sthpath+sthfile
        
        sth = np.zeros((np.size(digitID,axis=0),numChannels))
        
        if os.path.exists(sthfullpath) == False:
            print('\n \033[1;33m---> WARNING ... File: '+sthfullpath+' NOT FOUND\033[1;37m')
            print("\t ... software thresholds switched OFF ... ")
            softthreshold = 0
            time.sleep(2)
            return sth, softthreshold
        else:
            digit = pd.read_excel(sthfullpath).columns
            temp  = pd.read_excel(sthfullpath).values
            temp  = np.matrix.transpose(temp)
                 
        for k in range(len(digitID)):
           
             if not(digitID[k] in digit):
                print('\n \033[1;33m---> WARNING ... Threshold File does NOT contain all the digitser IDs\033[1;37m')
                print("\t ... software thresholds switched OFF for digitiser ",+(digitID[k]))
                sth[k,:] = 0  
             else:
                index = np.where(digitID[k] == digit)
                sth[k,:] = temp[index,:]
                
        return sth, softthreshold

###############################################################################
###############################################################################
#MAPPING according to excel file 
    
def mappingChToGeometry (data,MAPPING,mappath,mapfile):
       
    if MAPPING == 1:
        
       mapfullpath = mappath+mapfile
    
       mappe = pd.read_excel(mapfullpath).values
           
       dataorig = np.copy(data) 
           
       for k in range(np.shape(mappe)[0]):
           position = dataorig[:,1] == mappe[k,1] 
           data[position,1] = mappe[k,0]
              
    return data
               
###############################################################################
###############################################################################
    
#this is the equivalent of the MATALB function 
#data = cleaning(data,cleaningfromrepet,overflowcorr,zerosuppression)

#cleaning, works for 1 cassette
def cleaning (data,overflowcorr,zerosuppression):

    Noriginal = data.shape[0]
    print('\n \t file length: ',str(Noriginal),' rows',);
    
    if overflowcorr  == 1:
        over = data[:,2] >= 65535
        data = data[~over,:]
        Noverflow = sum(over)
        Nnew      = data.shape[0]
        if Noverflow != 0:
            print('\t    ... Overflow (65535) events!!! -> file cleaned! ', end=' ')
            print('overflow rows: ',str(Noverflow),', new file length: ',str(Nnew),' rows')
            
    if zerosuppression  == 1:
        zer  = data[:,2] == 0
        data = data[~zer,:]
        Nzer = sum(zer)
        Nnew = data.shape[0]
        if Nzer != 0:
            print('\t    ... zero ADC events!!! -> file cleaned! ', end=' ')
            print('zero ADC rows: ',str(Nzer),', new file length: ',str(Nnew),' rows')
            
    return data

###############################################################################
###############################################################################
# Close the gaps, shadowed channels

def closeTheGaps (XYglob,XXg,YYg,gaps,axis):
# gaps      = [0, 3, 4, 4, 3, 2]   # (first must be always 0)

    newlen = len(XXg)-sum(gaps)
    XXgc   = np.linspace(0,(newlen-1),newlen)
    
    if axis == 1:
        XYglobc = np.zeros((len(YYg),len(XXgc)))
    elif axis == 0:
        XYglobc = np.zeros((len(XXgc),len(YYg)))
    
    cumul = 0
    
    for k in range(len(gaps)):
        
        cumul = cumul + gaps[k]
        
        indexes1 = np.int_(k*32 + np.linspace(0,31,32))
        indexes2 = np.int_((k*32-cumul) + np.linspace(0,31,32))
        
        # print(cumul,indexes1,indexes2)
        
        if axis == 1:
    
            XYglobc[:,indexes2] = XYglobc[:,indexes2] + XYglob[:,indexes1]
            
        elif axis == 0:
            
            XYglobc[indexes2,:] = XYglobc[indexes2,:] + XYglob[indexes1,:]
    
    return XYglobc, XXgc

###############################################################################
###############################################################################
