#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:15:04 2020

@author: francescopiscitelli
"""
import numpy as np
# import pandas as pd
# import math as mt
import time
import sys

temp = np.load('datate.npy')

Timewindow = 2e-6

    #data is col 0: time stamp in 16ns precision, col 1: ch number (FROM 0 TOP 63), col2: ADC value, col3: global time reset delta in ms
    # if there is no strip it will be -1, with 0 PH and 0 multiplicity
    
    # # move ch starting from 1 beacuse for the weighting of calculation position would not work if starts at 0
    # data = np.copy(datain)
    # data[:,1] = data[:,1]+1;

# data1 = temp[1:100,:]
# data2 = temp[1:100,:]
# data3 = temp[1:100,:]

# temp[3,1] = 51 

# data1 = temp[12632:12640,:]
# data2 = temp[12632:12640,:]
# data3 = temp[:,:]

data1 = temp[:,:]
# data2 = temp[:,:]

###############################################################################
###############################################################################
    
# data = data1

# t2 = time.time()

# print('\n \t clustering ... ')
    
#     # this is a trick to accept also the clusters very close in time otherwise rejected
# Timewindowrec = mt.ceil(Timewindow*1e6/3)/1e6+0.01e-6;
# Timewindow    = Timewindow+0.01e-6;
#     ##########
    
# data = np.concatenate((np.zeros([1,4]),data),axis=0)  #add a line at top not to lose the 1st event
    
# tof     = data[:,0]                  #tof column in seconds
# tof1us  = np.around(tof, decimals=6) #tof rounded at 1us precision 
#     #data[:,0] = data[:,0]
    
# data[:,0] = tof1us
    
# dtof1us = np.diff(tof1us[:]) #1st derivative of tof 
# dtof1us = np.concatenate(([0],dtof1us),axis=0) #add a zero at top to restore length of vector
    
# clusterlogic = (np.absolute(dtof1us) <= Timewindowrec) #is zero when a new cluster starts 
    
#     # data1 = np.concatenate((data,clusterlogic[:,None]),axis=1) #this is for debugging 
    
# index = np.argwhere(clusterlogic == 0) #find the index where a new cluster may start 
    
# NumClusters = len(index)
    
#     #NumClusters = 6
    
#     #np.arange(0,NumClusters,1)
    
# rejCounter = np.zeros(5)
    
# POPH2 = np.zeros((NumClusters,7))  #output data with col0 position wires, col1 poisiton strips, col2 tof, col3 pulse height wires, col4 pulse height strips, col 5 multiplicity w, col 6 muiltiplicity strips
    
# for kk in np.arange(0,NumClusters,1):
        
#         if kk < (NumClusters-1): #any cluster in data but the last 
#             clusterq = data[index[kk,0]:index[kk+1,0] , 0:3]
#         elif kk == (NumClusters-1): #last cluster
#             clusterq = data[index[kk,0]: , 0:3]
            
#         acceptWindow = ((clusterq[-1,0] - clusterq[0,0]) <= Timewindow)  #max difference in time between first and last in cluster 
        
#     #    clusterq_old = clusterq
            
#         clusterq = clusterq[clusterq[:,1].argsort(kind='quicksort')]  #order cluster by ch number
        
#         # IF CH FORM 1 TO 64
#         # wws = clusterq[:,1] <= 32;    #wires 
#         # sss = clusterq[:,1] >= 33;    #strips
        
#         wws = clusterq[:,1] <= 31;    #wires 
#         sss = clusterq[:,1] >= 32;    #strips
       
#         # n wires n strips in cluster
#         ww = sum(wws)  #num of wires in cluster
#         ss = sum(sss)  #num of strips in cluster
    
#         if (ww != 0 and ss != 0 and ss <= 32 and ww <= 32 and acceptWindow): #if there is at least 1 wire and 1 strip and no ch number above 32
        
#             #check if they are neighbours 
#             dcw   = np.concatenate( (np.diff(clusterq[wws,1]),[1.0]),axis=0)
#             dcs   = np.concatenate( (np.diff(clusterq[sss,1]),[1.0]),axis=0)
#             neigw = sum(dcw)*(sum(dcw == 1) == sum(dcw))    #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
#             neigs = sum(dcs)*(sum(dcs == 1) == sum(dcs))
    
#             if (neigw == ww and neigs == ss):    #if they are neighbour then...
    
#                 rejCounter[0] = rejCounter[0]+1;                #counter 2D
    
#                 Wires  = clusterq[wws,:]
#                 Strips = clusterq[sss,:]
                
#                 POPH2[kk,5]   = neigw     #multiuplicity wires
#                 POPH2[kk,6]   = neigs     #multiuplicity strips
#                 POPH2[kk,2]   = clusterq[0,0]     #tof
#                 POPH2[kk,3]   = sum(Wires[:,2])   #PH wires
#                 POPH2[kk,4]   = sum(Strips[:,2])   #PH strips
#                 POPH2[kk,0]   = round((sum(Wires[:,1]*Wires[:,2]))/(POPH2[kk,3]),2)   #position wires
#                 POPH2[kk,1]   = round((((sum(Strips[:,1]*Strips[:,2]))/(POPH2[kk,4]))-32),2)  #position strips from 1 to 32 or from 0 to 31

#             else:
#                 rejCounter[1] = rejCounter[1]+1;                #counter if they are no neighbour 
                
#         elif (ww >= 1 and ss == 0 and ww <= 32 and acceptWindow): #put in 1D hist only for wires when there is no strip 
                
#             #check if they are neighbours 
#             dcw   = np.concatenate( (np.diff(clusterq[wws,1]),[1.0]),axis=0)
#             neigw = sum(dcw)*(sum(dcw == 1) == sum(dcw))    #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
           
#             if (neigw == ww):    #if they are neighbour then...
    
#                 rejCounter[2] = rejCounter[2]+1;                #counter 1D
    
#                 Wires  = clusterq[wws,:]
                
#                 POPH2[kk,5]   = neigw     #multiuplicity wires
#                 POPH2[kk,2]   = clusterq[0,0]     #tof
#                 POPH2[kk,3]   = sum(Wires[:,2])   #PH wires
#                 POPH2[kk,0]   = round((sum(Wires[:,1]*Wires[:,2]))/(POPH2[kk,3]),2)   #position wires
#                 POPH2[kk,1]   = -1 #position strips if absent
                
#     #            if POPH[kk,3] != 0 :
#     #                POPH[kk,0]   = (sum(Wires[:,1]*Wires[:,2]))/(POPH[kk,3])   #position wires
#     #            else:
#     #                POPH[kk,0]   =-3
      
                
#             else:
#                 rejCounter[1] = rejCounter[1]+1              #counter if they are no neighbour 
                
#         elif (ww >= 33 or ss >= 33):
#              rejCounter[3] = rejCounter[3]+1               #counter if cluster above possible limits          
#              print('\n cluster > 32 in either directions w or s -> probably rate too high \n')
             
#         else:
#             rejCounter[4] = rejCounter[4]+1               #any other case not taken into account previously
            
    
# rejected = np.logical_and((POPH2[:,5] == 0),(POPH2[:,6] == 0))    #remove rejected from data in rejCoiunter[4] it is when only strips and wire and sgtrip mult is 0, whole row in POPH is 0 actually 
    
# POPH2     = POPH2[np.logical_not(rejected),:];    #remove rejected from data
     
# NumeventNoRej = NumClusters - (rejCounter[1]+rejCounter[3]+rejCounter[4]);
# rej2 = 100*(rejCounter/NumClusters);
# rej3 = 100*(rejCounter/NumeventNoRej);
    
# print("\t N of events: %d -> not rejected (2D and 1D) %d " % (NumClusters,NumeventNoRej))
# print("\t not rej (2D) %.1f%%, only w (1D) %.1f%%, rejected (2D or 1D) %.1f%%, rejected >32 %.1f%%, rejected other reasons (only strips - noise)  %.1f%% " % (rej2[0],rej2[2],rej2[1],rej2[3],rej2[4]));
# print("\t not rej (2D) %.1f%%, only w (1D) %.1f%% \n " % (rej3[0],rej3[2]))
    
# mbins=np.arange(0,33,1)
    
# TwoDim = POPH2[:,1] >= 0
# multiwhistcoinc = np.histogram(POPH2[TwoDim,5],mbins)
# multishistcoinc = np.histogram(POPH2[:,6],mbins)
        
# wirefire  = multiwhistcoinc[0]/sum(multiwhistcoinc[0])
# stripfire = multishistcoinc[0]/sum(multishistcoinc[0][1:])
# print(' \t multiplicity:')      
# print(" \t 2D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*wirefire[1],100*wirefire[2],100*wirefire[3],100*wirefire[4],100*wirefire[5])); 
# print(" \t 2D: percentage of strips fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*stripfire[1],100*stripfire[2],100*stripfire[3],100*stripfire[4],100*stripfire[5])); 
                 
# OneDim = POPH2[:,1] == -1
# multiwhist = np.histogram(POPH2[OneDim,5],mbins)

# if         sum(multiwhist[0]) != 0:
#     wirefire1D  = multiwhist[0]/sum(multiwhist[0])
        
#     print(" \t 1D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5) \n" % (100*wirefire1D[1],100*wirefire1D[2],100*wirefire1D[3],100*wirefire1D[4],100*wirefire1D[5])); 

#     # return POPH, NumClusters

# elapsed2 = time.time() - t2
# print('--> time el.: ' + str(elapsed2) + ' s')  



###############################################################################
###############################################################################

# data = data2

# t3 = time.time()

# #################################

# print('\n \t clustering ... ')
    
# # this is a trick to accept also the clusters very close in time otherwise rejected
# Timewindowrec = mt.ceil(Timewindow*1e6/3)/1e6+0.01e-6;
# Timewindow    = Timewindow+0.01e-6;
# ##########
    
# data = np.concatenate((np.zeros([1,4]),data),axis=0)  #add a line at top not to lose the 1st event
    
# tof        = data[:,0]                        #tof column in seconds
# tof1us     = np.around(tof, decimals=6) #tof rounded at 1us precision 
    
# data[:,0] = tof1us
    
# dtof1us = np.diff(tof1us[:])                   #1st derivative of tof 
# dtof1us = np.concatenate(([0],dtof1us),axis=0) #add a zero at top to restore length of vector
    
# clusterlogic = (np.absolute(dtof1us) <= Timewindowrec) #is zero when a new cluster starts 
    
# # data1 = np.concatenate((data,clusterlogic[:,None]),axis=1) #this is for debugging 
    
# index = np.argwhere(clusterlogic == 0) #find the index where a new cluster may start 

# #################################

# ADCCH = np.zeros((np.shape(data)[0],13))

# ADCCH[:,0:4] = data         # first 4 columns as data
# ADCCH[:,4]   = clusterlogic # col 4 is 0 where a new cluster may start

# ADCCH[:,5]   = data[:,1] <= 31   # wire  (this is 31 if ch from 0)
# ADCCH[:,6]   = data[:,1] >= 32   # strip (this is 32 if ch from 0)

# ADCCH[:,7]   = data[:,1]*ADCCH[:,5]   # wire ch
# ADCCH[:,8]   = data[:,1]*ADCCH[:,6]   # strip ch

# ADCCH[:,9]   = data[:,2]*ADCCH[:,5]   # wire ADCs 
# ADCCH[:,10]  = data[:,2]*ADCCH[:,6]   # strip ADCs 

# ADCCH[:,11]  =  ADCCH[:,5]*ADCCH[:,7]*ADCCH[:,9]   # weighted position on wires
# ADCCH[:,12]  =  ADCCH[:,6]*ADCCH[:,8]*ADCCH[:,10]  # weighted position on strips

# #################################

# NumClusters = np.shape(index)[0]
        
# rejCounter = np.zeros(5)
    
# POPH = np.zeros((NumClusters,7))  #output data with col0 position wires, col1 poisiton strips, col2 tof, col3 pulse height wires, col4 pulse height strips, col 5 multiplicity w, col 6 muiltiplicity strips

# # filling ToF column
# tempTof   = data[index,0]
# POPH[:,2] = tempTof[:,0]     #tof
 
# #################################

# # add a fake last cluster to make loop up to the very last true cluster
# index = np.concatenate((index,[[np.shape(data)[0]]]),axis=0)
# ADCCH = np.concatenate((ADCCH,np.zeros((1,13))),axis=0) 

# for kk in np.arange(0,NumClusters,1):
        
#         clusterq = ADCCH[index[kk,0]:index[kk+1,0],:]
 
#         acceptWindow = ((clusterq[-1,0] - clusterq[0,0]) <= Timewindow)  #max difference in time between first and last in cluster 
        
#         is_wire  = clusterq[:,5] == 1
#         is_strip = clusterq[:,6] == 1
        
#         # n wires n strips in cluster
#         ww = len(clusterq[is_wire, 5])  #num of wires in cluster
#         ss = len(clusterq[is_strip, 6])  #num of strips in cluster
            
#         # clusterq = clusterq[clusterq[:,1].argsort(kind='quicksort')]  #order cluster by ch number
        
#         if (ww != 0 and ss != 0 and ss <= 32 and ww <= 32 and acceptWindow): #if there is at least 1 wire and 1 strip and no ch number above 32
                     
#             #check if they are neighbour
#             mmaxw = np.max(clusterq[is_wire, 7],axis=0)
#             mmaxs = np.max(clusterq[is_strip, 8],axis=0)
#             mminw = np.min(clusterq[is_wire, 7],axis=0)
#             mmins = np.min(clusterq[is_strip, 8],axis=0)

#             neigw = (mmaxw - mminw) == (ww-1) #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
#             neigs = (mmaxs - mmins) == (ss-1)
            
#             if (neigw == 1 and neigs == 1):    #if they are neighbour then...
                
#                 rejCounter[0] = rejCounter[0]+1;   #counter 2D
                
#                 POPH[kk,5]   = ww     #multiuplicity wires
#                 POPH[kk,6]   = ss     #multiuplicity strips
#                 POPH[kk,3]   = np.sum(clusterq[:,9],axis=0)   #PH wires
#                 POPH[kk,4]   = np.sum(clusterq[:,10],axis=0)  #PH strips
#                 POPH[kk,0]   = round((np.sum(clusterq[:,11],axis=0))/(POPH[kk,3]),2)         #position wires
#                 POPH[kk,1]   = round((((np.sum(clusterq[:,12],axis=0))/(POPH[kk,4]))-32),2)  #position strips from 1 to 32 or from 0 to 31

#             else:
#                 rejCounter[1] = rejCounter[1]+1;                #counter if they are no neighbour 
                
#         elif (ww >= 1 and ss == 0 and ww <= 32 and acceptWindow): #put in 1D hist only for wires when there is no strip 
                
#             #check if they are neighbours 
#             mmaxw  = np.max(clusterq[is_wire, 7],axis=0)
#             mminw  = np.min(clusterq[is_wire, 7],axis=0)

#             neigw = (mmaxw - mminw) == (ww-1)    #works even if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
           
#             if (neigw == 1):    #if they are neighbour then...
    
#                 rejCounter[2] = rejCounter[2]+1;                #counter 1D
    
#                 POPH[kk,5]   = ww     #multiuplicity wires
#                 POPH[kk,3]   = np.sum(clusterq[:,9],axis=0)   #PH wires
#                 POPH[kk,0]   = round((np.sum(clusterq[:,11],axis=0))/(POPH[kk,3]),2)         #position wires
#                 POPH[kk,1]   = -1 #position strips if absent
                   
#             else:
#                 rejCounter[1] = rejCounter[1]+1              #counter if they are no neighbour 
                
#         elif (ww >= 33 or ss >= 33):
#               rejCounter[3] = rejCounter[3]+1               #counter if cluster above possible limits          
#               print('\n cluster > 32 in either directions w or s -> probably rate too high \n')
             
#         else:
#             rejCounter[4] = rejCounter[4]+1               #any other case not taken into account previously
        
        
# rejected = np.logical_and((POPH[:,5] == 0),(POPH[:,6] == 0))    #remove rejected from data in rejCoiunter[4] it is when only strips and wire and sgtrip mult is 0, whole row in POPH is 0 actually 
    
# POPH     = POPH[np.logical_not(rejected),:]    #remove rejected from data

# ################################
# # some stats    
# NumeventNoRej = NumClusters - (rejCounter[1]+rejCounter[3]+rejCounter[4]);
# rej2 = 100*(rejCounter/NumClusters);
# rej3 = 100*(rejCounter/NumeventNoRej);
    
# print("\t N of events: %d -> not rejected (2D and 1D) %d " % (NumClusters,NumeventNoRej))
# print("\t not rej (2D) %.1f%%, only w (1D) %.1f%%, rejected (2D or 1D) %.1f%%, rejected >32 %.1f%%, rejected other reasons (only strips - noise)  %.1f%% " % (rej2[0],rej2[2],rej2[1],rej2[3],rej2[4]));
# print("\t not rej (2D) %.1f%%, only w (1D) %.1f%% \n " % (rej3[0],rej3[2]))
    
# mbins = np.arange(0,33,1)
    
# TwoDim = POPH[:,1] >= 0
# multiwhistcoinc = np.histogram(POPH[TwoDim,5],mbins)
# multishistcoinc = np.histogram(POPH[:,6],mbins)

# if  sum(multiwhistcoinc[0]) != 0:        
#     wirefire  = multiwhistcoinc[0]/sum(multiwhistcoinc[0])
#     stripfire = multishistcoinc[0]/sum(multishistcoinc[0][1:])
#     print(' \t multiplicity:')      
#     print(" \t 2D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*wirefire[1],100*wirefire[2],100*wirefire[3],100*wirefire[4],100*wirefire[5])); 
#     print(" \t 2D: percentage of strips fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*stripfire[1],100*stripfire[2],100*stripfire[3],100*stripfire[4],100*stripfire[5])); 
                 
# OneDim = POPH[:,1] == -1
# multiwhist = np.histogram(POPH[OneDim,5],mbins)
        
# if  sum(multiwhist[0]) != 0:
#     wirefire1D  = multiwhist[0]/sum(multiwhist[0])
            
#     print(" \t 1D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5) \n" % (100*wirefire1D[1],100*wirefire1D[2],100*wirefire1D[3],100*wirefire1D[4],100*wirefire1D[5])); 

#     # return POPH, NumClusters

# elapsed3 = time.time() - t3
# print('--> time el.: ' + str(elapsed3) + ' s')  


###############################################################################
###############################################################################

# data = data3

# t4 = time.time()

# #################################

# print('\n \t clustering ... ')
    
# # this is a trick to accept also the clusters very close in time otherwise rejected
# Timewindowrec = mt.ceil(Timewindow*1e6/3)/1e6+0.01e-6;
# Timewindow    = Timewindow+0.01e-6;
# ##########
    
# data = np.concatenate((np.zeros([1,4]),data),axis=0)  #add a line at top not to lose the 1st event
    
# tof        = data[:,0]                        #tof column in seconds
# tof1us  = np.around(tof, decimals=6) #tof rounded at 1us precision 
    
# data[:,0] = tof1us
    
# dtof1us = np.diff(tof1us[:])                   #1st derivative of tof 
# dtof1us = np.concatenate(([0],dtof1us),axis=0) #add a zero at top to restore length of vector
    
# clusterlogic = (np.absolute(dtof1us) <= Timewindowrec) #is zero when a new cluster starts 
    
# # data1 = np.concatenate((data,clusterlogic[:,None]),axis=1) #this is for debugging 
    
# index = np.argwhere(clusterlogic == 0) #find the index where a new cluster may start 

# #################################

# ADCCH = np.zeros((np.shape(data)[0],13))

# ADCCH[:,0:4] = data         # first 4 columns as data
# ADCCH[:,4]   = clusterlogic # col 4 is 0 where a new cluster may start

# ADCCH[:,5]   = data[:,1] <= 31   # wire  (this is 31 if ch from 0)
# ADCCH[:,6]   = data[:,1] >= 32   # strip (this is 32 if ch from 0)

# ADCCH[:,7]   = data[:,1]*ADCCH[:,5]   # wire ch
# ADCCH[:,8]   = data[:,1]*ADCCH[:,6]   # strip ch

# ADCCH[:,9]   = data[:,2]*ADCCH[:,5]   # wire ADCs 
# ADCCH[:,10]  = data[:,2]*ADCCH[:,6]   # strip ADCs 

# ADCCH[:,11]  =  ADCCH[:,5]*ADCCH[:,7]*ADCCH[:,9]   # weighted position on wires
# ADCCH[:,12]  =  ADCCH[:,6]*ADCCH[:,8]*ADCCH[:,10]  # weighted position on strips

# #################################

# NumClusters = np.shape(index)[0]
        
# # rejCounter = np.zeros(5)
    
# POPH = np.zeros((NumClusters,7))  #output data with col0 position wires, col1 poisiton strips, col2 tof, col3 pulse height wires, col4 pulse height strips, col 5 multiplicity w, col 6 muiltiplicity strips

# # filling ToF column
# tempTof   = data[index,0]
# POPH[:,2] = tempTof[:,0]     #tof

# conditions = np.zeros((NumClusters,5)) 
 
# #################################

# # add a fake last cluster to make loop up to the very last true cluster
# index = np.concatenate((index,[[np.shape(data)[0]]]),axis=0)
# ADCCH = np.concatenate((ADCCH,np.zeros((1,13))),axis=0) 

# for kk in np.arange(0,NumClusters,1):
        
#         clusterq = ADCCH[index[kk,0]:index[kk+1,0],:]
 
#         acceptWindow = ((clusterq[-1,0] - clusterq[0,0]) <= Timewindow)  #max difference in time between first and last in cluster 
        
#         # n wires n strips in cluster
#         ww = np.sum(clusterq[:,5],axis=0)  #num of wires in cluster
#         ss = np.sum(clusterq[:,6],axis=0)  #num of strips in cluster
            
#         # clusterq = clusterq[clusterq[:,1].argsort(kind='quicksort')]  #order cluster by ch number
        
#         #check if they are neighbour
#         try:
#             mmaxw = np.max(clusterq[ clusterq[:,5] == 1, 7],axis=0)
#         except ValueError:
#             mmaxw = 0
            
#         try:   
#             mmaxs = np.max(clusterq[ clusterq[:,6] == 1, 8],axis=0)
#         except ValueError:
#             mmaxs = 0
            
#         try:   
#             mminw = np.min(clusterq[ clusterq[:,5] == 1, 7],axis=0)
#         except ValueError:
#             mminw = 0
            
#         try:   
#             mmins = np.min(clusterq[ clusterq[:,6] == 1, 8],axis=0)
#         except ValueError:
#             mmins = 0
            
            
#         neigw = (mmaxw - mminw) == (ww-1) #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
#         neigs = (mmaxs - mmins) == (ss-1)
            
#         # conditions[kk,0] = ww
#         # conditions[kk,1] = ss
#         # conditions[kk,2] = neigw
#         # conditions[kk,3] = neigs
#         # conditions[kk,4] = acceptWindow
        
        
#         conditions[kk,1] = ww >= 1 and ss == 0 and ww <= 32 and acceptWindow and neigw == 1
#         conditions[kk,2] = ww != 0 and ss != 0 and ss <= 32 and ww <= 32 and acceptWindow and neigw == 1 and neigs == 1
     
#         POPH[kk,5]   = ww     #multiuplicity wires
#         POPH[kk,6]   = ss     #multiuplicity strips
#         POPH[kk,3]   = np.sum(clusterq[:,9],axis=0)   #PH wires
#         POPH[kk,4]   = np.sum(clusterq[:,10],axis=0)  #PH strips
#         if POPH[kk,3] != 0:
#             POPH[kk,0]   = round((np.sum(clusterq[:,11],axis=0))/(POPH[kk,3]),2)         #position wires
#         else:
#             POPH[kk,0]   = -1
#         if POPH[kk,4] != 0:
#             POPH[kk,1]   = round((((np.sum(clusterq[:,12],axis=0))/(POPH[kk,4]))-32),2)  #position strips from 1 to 32 or from 0 to 31
#         else:
#             POPH[kk,1]   = -1

 
# conditions[:,0] =  np.logical_and(np.logical_not(conditions[:,1]), np.logical_not(conditions[:,2]))

# temp = np.sum(conditions,axis=0)

# rejCounter    = np.zeros(5)
# rejCounter[0] = temp[2]
# rejCounter[2] = temp[1]
# rejCounter[1] = temp[0]

# #remove rejected from data in rejCoiunter[4] it is when only strips and wire and sgtrip mult is 0, whole row in POPH is 0 actually 
    
# POPH  = POPH[np.logical_not(conditions[:,0]),:]    #remove rejected from data

# # change from nan to -1
# temp = np.isnan(POPH[:,1])
# POPH[temp,1] = -1

# ################################
# # some stats    
# NumeventNoRej = NumClusters - rejCounter[1]
# rej2 = 100*(rejCounter/NumClusters);
# rej3 = 100*(rejCounter/NumeventNoRej);
    
# print("\t N of events: %d -> not rejected (2D and 1D) %d " % (NumClusters,NumeventNoRej))
# print("\t not rej (2D) %.1f%%, only w (1D) %.1f%%, rejected (2D or 1D) %.1f%%" % (rej2[0],rej2[2],rej2[1]));
# print("\t not rej (2D) %.1f%%, only w (1D) %.1f%% \n " % (rej3[0],rej3[2]))
    
# mbins = np.arange(0,33,1)
    
# TwoDim = POPH[:,1] >= 0
# multiwhistcoinc = np.histogram(POPH[TwoDim,5],mbins)
# multishistcoinc = np.histogram(POPH[:,6],mbins)
        
# wirefire  = multiwhistcoinc[0]/sum(multiwhistcoinc[0])
# stripfire = multishistcoinc[0]/sum(multishistcoinc[0][1:])
# print(' \t multiplicity:')      
# print(" \t 2D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*wirefire[1],100*wirefire[2],100*wirefire[3],100*wirefire[4],100*wirefire[5])); 
# print(" \t 2D: percentage of strips fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*stripfire[1],100*stripfire[2],100*stripfire[3],100*stripfire[4],100*stripfire[5])); 
                 
# OneDim = POPH[:,1] == -1
# multiwhist = np.histogram(POPH[OneDim,5],mbins)
        
# # try:
# wirefire1D  = multiwhist[0]/sum(multiwhist[0])
# print(" \t 1D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5) \n" % (100*wirefire1D[1],100*wirefire1D[2],100*wirefire1D[3],100*wirefire1D[4],100*wirefire1D[5])); 
# # except ValueError:
# #     print(1)
#     # return POPH, NumClusters

# elapsed4 = time.time() - t4
# print('--> time el.: ' + str(elapsed4) + ' s')


###############################################################################
###############################################################################

data = data1

t3 = time.time()

#################################

print('\n \t clustering ... ')
    
# this is a trick to accept also the clusters very close in time otherwise rejected
Timewindowrec = np.ceil(Timewindow*1e6/3)/1e6+0.01e-6
Timewindow    = Timewindow+0.01e-6
##########
    
data = np.concatenate((np.zeros([1,4]),data),axis=0)  #add a line at top not to lose the 1st event
    
tof        = data[:,0]                        #tof column in seconds
tof1us     = np.around(tof, decimals=6) #tof rounded at 1us precision 
    
data[:,0] = tof1us
    
dtof1us = np.diff(tof1us[:])                   #1st derivative of tof 
dtof1us = np.concatenate(([0],dtof1us),axis=0) #add a zero at top to restore length of vector
    
clusterlogic = (np.absolute(dtof1us) <= Timewindowrec) #is zero when a new cluster starts 
    
# data1 = np.concatenate((data,clusterlogic[:,None]),axis=1) #this is for debugging 
    
index = np.argwhere(clusterlogic == 0) #find the index where a new cluster may start 

#################################

ADCCH = np.zeros((np.shape(data)[0],13))

ADCCH[:,0:4] = data         # first 4 columns as data
ADCCH[:,4]   = clusterlogic # col 4 is 0 where a new cluster may start

ADCCH[:,5]   = data[:,1] <= 31   # wire  (this is 31 if ch from 0)
ADCCH[:,6]   = data[:,1] >= 32   # strip (this is 32 if ch from 0)

ADCCH[:,7]   = data[:,1]*ADCCH[:,5]   # wire ch
ADCCH[:,8]   = data[:,1]*ADCCH[:,6]   # strip ch

ADCCH[:,9]   = data[:,2]*ADCCH[:,5]   # wire ADCs 
ADCCH[:,10]  = data[:,2]*ADCCH[:,6]   # strip ADCs 

ADCCH[:,11]  =  ADCCH[:,5]*ADCCH[:,7]*ADCCH[:,9]   # weighted position on wires
ADCCH[:,12]  =  ADCCH[:,6]*ADCCH[:,8]*ADCCH[:,10]  # weighted position on strips

#################################

NumClusters = np.shape(index)[0]
        
rejCounter = np.zeros(5)
    
POPH4 = np.zeros((NumClusters,7))  #output data with col0 position wires, col1 poisiton strips, col2 tof, col3 pulse height wires, col4 pulse height strips, col 5 multiplicity w, col 6 muiltiplicity strips

# filling ToF column
tempTof   = data[index,0]
POPH4[:,2] = tempTof[:,0]     #tof
 
#################################

# add a fake last cluster to make loop up to the very last true cluster
index = np.concatenate((index,[[np.shape(data)[0]]]),axis=0)
ADCCH = np.concatenate((ADCCH,np.zeros((1,13))),axis=0) 





# NumClusters = 1000

for kk in np.arange(0,NumClusters,1):
    
        # if np.mod(kk,10000) == 0:
        # #     # symbols = ['-','\','|','/']
        # #     print('-', end = '')
    
        #     sys.stdout.write('\r')
        #     # the exact output you're looking for:
        #     sys.stdout.write("[%-20s] %d%%" % ('='*kk, 5*kk))
        #     sys.stdout.flush()
    
        # n_bar =10 #size of progress bar
        # postText = 'clustering ...'
        # j = kk/(NumClusters-1)
        # sys.stdout.write('\r')
        # sys.stdout.write(f"{postText} [{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%")
        # sys.stdout.flush()
            
        
        clusterq = ADCCH[index[kk,0]:index[kk+1,0],:]
        
        # temp = clusterq
        clusterq = clusterq[clusterq[:,1].argsort(kind='quicksort')]  #order cluster by ch number
 
        acceptWindow = ((clusterq[-1,0] - clusterq[0,0]) <= Timewindow)  #max difference in time between first and last in cluster 
        
        is_wire  = clusterq[:,5] == 1
        is_strip = clusterq[:,6] == 1
        
        # n wires n strips in cluster
        ww = len(clusterq[is_wire, 5])  #num of wires in cluster
        ss = len(clusterq[is_strip, 6])  #num of strips in cluster
            
        if (ww != 0 and ss != 0 and ss <= 32 and ww <= 32 and acceptWindow): #if there is at least 1 wire and 1 strip and no ch number above 32
                     
            # #check if they are neighbour
            # mmaxw = np.max(clusterq[is_wire, 7],axis=0)
            # mmaxs = np.max(clusterq[is_strip, 8],axis=0)
            # mminw = np.min(clusterq[is_wire, 7],axis=0)
            # mmins = np.min(clusterq[is_strip, 8],axis=0)
            
            mmaxw = clusterq[is_wire, 7][-1]
            mmaxs = clusterq[is_strip, 8][-1]
            mminw = clusterq[is_wire, 7][0]
            mmins = clusterq[is_strip, 8][0]

            neigw = (mmaxw - mminw) == (ww-1) #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
            neigs = (mmaxs - mmins) == (ss-1)
            
            if (neigw == 1 and neigs == 1):    #if they are neighbour then...
                
                rejCounter[0] = rejCounter[0]+1;   #counter 2D
                
                POPH4[kk,5]   = ww     #multiuplicity wires
                POPH4[kk,6]   = ss     #multiuplicity strips
                POPH4[kk,3]   = np.sum(clusterq[:,9],axis=0)   #PH wires
                POPH4[kk,4]   = np.sum(clusterq[:,10],axis=0)  #PH strips
                POPH4[kk,0]   = round((np.sum(clusterq[:,11],axis=0))/(POPH4[kk,3]),2)         #position wires
                POPH4[kk,1]   = round((((np.sum(clusterq[:,12],axis=0))/(POPH4[kk,4]))-32),2)  #position strips from 1 to 32 or from 0 to 31

            else:
                rejCounter[1] = rejCounter[1]+1;                #counter if they are no neighbour 
                
        elif (ww >= 1 and ss == 0 and ww <= 32 and acceptWindow): #put in 1D hist only for wires when there is no strip 
                
            #check if they are neighbours 
            mmaxw  = np.max(clusterq[is_wire, 7],axis=0)
            mminw  = np.min(clusterq[is_wire, 7],axis=0)

            neigw = (mmaxw - mminw) == (ww-1)    #works even if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
           
            if (neigw == 1):    #if they are neighbour then...
    
                rejCounter[2] = rejCounter[2]+1;                #counter 1D
    
                POPH4[kk,5]   = ww     #multiuplicity wires
                POPH4[kk,3]   = np.sum(clusterq[:,9],axis=0)   #PH wires
                POPH4[kk,0]   = round((np.sum(clusterq[:,11],axis=0))/(POPH4[kk,3]),2)         #position wires
                POPH4[kk,1]   = -1 #position strips if absent
                   
            else:
                rejCounter[1] = rejCounter[1]+1              #counter if they are no neighbour 
                
        elif (ww >= 33 or ss >= 33):
              rejCounter[3] = rejCounter[3]+1               #counter if cluster above possible limits          
              print('\n cluster > 32 in either directions w or s -> probably rate too high \n')
             
        else:
            rejCounter[4] = rejCounter[4]+1               #any other case not taken into account previously
        
        
rejected = np.logical_and((POPH4[:,5] == 0),(POPH4[:,6] == 0))    #remove rejected from data in rejCoiunter[4] it is when only strips and wire and sgtrip mult is 0, whole row in POPH is 0 actually 
    
POPH4     = POPH4[np.logical_not(rejected),:]    #remove rejected from data

################################
# some stats    
NumeventNoRej = NumClusters - (rejCounter[1]+rejCounter[3]+rejCounter[4]);
rej2 = 100*(rejCounter/NumClusters);
rej3 = 100*(rejCounter/NumeventNoRej);
    
print("\t N of events: %d -> not rejected (2D and 1D) %d " % (NumClusters,NumeventNoRej))
print("\t not rej (2D) %.1f%%, only w (1D) %.1f%%, rejected (2D or 1D) %.1f%%, rejected >32 %.1f%%, rejected other reasons (only strips - noise)  %.1f%% " % (rej2[0],rej2[2],rej2[1],rej2[3],rej2[4]));
print("\t not rej (2D) %.1f%%, only w (1D) %.1f%% \n " % (rej3[0],rej3[2]))
    
mbins = np.arange(0,33,1)
    
TwoDim = POPH4[:,1] >= 0
multiwhistcoinc = np.histogram(POPH4[TwoDim,5],mbins)
multishistcoinc = np.histogram(POPH4[:,6],mbins)

if  sum(multiwhistcoinc[0]) != 0:        
    wirefire  = multiwhistcoinc[0]/sum(multiwhistcoinc[0])
    stripfire = multishistcoinc[0]/sum(multishistcoinc[0][1:])
    print(' \t multiplicity:')      
    print(" \t 2D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*wirefire[1],100*wirefire[2],100*wirefire[3],100*wirefire[4],100*wirefire[5])); 
    print(" \t 2D: percentage of strips fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*stripfire[1],100*stripfire[2],100*stripfire[3],100*stripfire[4],100*stripfire[5])); 
                 
OneDim = POPH4[:,1] == -1
multiwhist = np.histogram(POPH4[OneDim,5],mbins)
        
if  sum(multiwhist[0]) != 0:
    wirefire1D  = multiwhist[0]/sum(multiwhist[0])
            
    print(" \t 1D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5) \n" % (100*wirefire1D[1],100*wirefire1D[2],100*wirefire1D[3],100*wirefire1D[4],100*wirefire1D[5])); 

    # return POPH, NumClusters

elapsed3 = time.time() - t3
print('--> time el.: ' + str(elapsed3) + ' s')  


###############################################################################
###############################################################################
