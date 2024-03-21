#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:08:57 2020

@author: francescopiscitelli
"""
import numpy as np

dd = [34,35,33]

ChW = [0,31]  # wire channels

posBins = 32
   
XX    = np.linspace(ChW[0],ChW[1],posBins)

XXg   = np.linspace(ChW[0],(XX[-1]-XX[0]+1)*len(dd)-(1-XX[0]),posBins*len(dd))        
         
#####################################  


XXa   =  np.zeros(len(dd)*len(XX))

for k in range(len(dd)):
    
    # print(dd[k])
    
    indexes = (k*len(XX) + np.arange(len(XX)))
    
    XXa[indexes] = k*(XX[-1]-XX[0]+1) + XX
    
    print(k*len(XX))
    


 