#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 13:17:22 2020

@author: francescopiscitelli
"""

import numpy as np

inclination = 5
wirepitch   = 4
strippitch  = 4
Xoffset1stWires = 10.11
 
POPH1b = np.zeros((32,3))

POPH1b[:,0] = np.arange(0,32,1)
POPH1b[:,1] = np.arange(0,32,1)
# POPH1b[:,2] = np.arange(0,32,1)

digit = [12,34,565]

POPH = np.zeros((32*len(digit),3))


for dd in np.arange(len(digit)):
    
    index = np.arange(32*dd,32*(dd+1))
    
    sinne = np.sin(np.deg2rad(inclination)) 
    POPH[index,0] = np.round( (POPH1b[:,0]*(wirepitch*sinne) + Xoffset1stWires*dd), decimals=2 )  #mm
            
    POPH[index,1] = np.round((POPH1b[:,1]*strippitch), decimals=2 )  #mm
    
    cosse = np.cos(np.deg2rad(inclination)) 
    POPH[index,2] = (POPH1b[:,0]*(wirepitch*cosse))  #mm