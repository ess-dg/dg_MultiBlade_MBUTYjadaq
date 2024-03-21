#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 08:46:04 2020

@author: francescopiscitelli
"""

import numpy as np

# NOTE: this module already supports 32 wires and 64 strips 

# makes 1D or 2D histograms

#  Usage: mm1 = hsm.histog(), nn1 = mm1.hist1(xbins=XX, xvar=AA)
#or mm2 = hsm.histog(outBounds=False).hist2(xbins=XX[0:32], xvar=AA, yvar=BB, ybins=YY)

    
###############################################################################
############################################################################### 
 
def hist1(xbins,xvar,outBounds=True):

    binX   = len(xbins) 
        
    Xmin   = np.min(xbins) 
    Xmax   = np.max(xbins) 

    hist   = np.zeros(binX) 
    
    index = np.int_(np.around(((binX-1)*((xvar-Xmin)/(Xmax-Xmin)))))
    
    if outBounds == False:
        if not(np.all(index >= 0) and np.all(index <= binX-1)):
            print('\033[1;33mWARNING: hist out of bounds, change limits!\033[1;37m') 
    
    for k in range(binX):    
        hist[k] = np.sum(index == k) 
       
        if outBounds == True:
            # fill overflow last bin and first bin
            hist[0]  += np.sum(index<0)
            hist[-1] += np.sum(index>binX-1)
        
    return hist

###############################################################################
############################################################################### 
    
def hist2(xbins, xvar, ybins, yvar, outBounds=True):
    
    # if np.size(self.ybins) == 1 and np.size(self.yvar) == 1:
    #     hist = 0
    #     return hist
    
    binX   = len(xbins) 
    binY   = len(ybins) 
        
    Xmin   = np.min(xbins) 
    Xmax   = np.max(xbins) 
    
    Ymin   = np.min(ybins) 
    Ymax   = np.max(ybins) 

    cont = 0
    
    hist = np.zeros((binY,binX)) 
    
    if not( (len(xvar) == len(yvar))):
        print('\n \t \033[1;31m----> ABORTED: X and Y not same length! \033[1;37m\n')
        return hist
    
    xxtemp =  np.int_(np.around(((binX-1)*((xvar-Xmin)/(Xmax-Xmin)))))
    yytemp =  np.int_(np.around(((binY-1)*((yvar-Ymin)/(Ymax-Ymin)))))
         
    for k in range(len(xvar)):
     
        xx =  xxtemp[k]
        yy =  yytemp[k]
    
        if outBounds == True:
            
           if ( (xx >= 0) and (xx <= binX-1) and (yy >= 0) and (yy <= binY-1) ):
               hist[yy,xx] += 1
           elif ( (xx >= 0) and (xx > binX-1) and (yy >= 0) and (yy <= binY-1) ):
               hist[yy,-1] += 1
           elif ( (xx < 0) and (xx <= binX-1) and (yy >= 0) and (yy <= binY-1) ):
                hist[yy,0] += 1
           elif ( (xx >= 0) and (xx <= binX-1) and (yy < 0) and (yy <= binY-1) ):
               hist[0,xx] += 1
           elif ( (xx >= 0) and (xx <= binX-1) and (yy >= 0) and (yy > binY-1) ):
               hist[-1,xx] += 1
               
        elif outBounds == False:
             
           if ( (xx >= 0) and (xx <= binX-1) and (yy >= 0) and (yy <= binY-1) ):
              hist[yy,xx] += 1
           else:
               if cont == 0:
                   print('\033[1;33mWARNING: hist out of bounds.\033[1;37m') 
                   cont = 1  
                      
    return hist

###############################################################################
############################################################################### 