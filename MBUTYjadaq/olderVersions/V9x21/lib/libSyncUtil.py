#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 08:33:38 2020

@author: francescopiscitelli
"""

import os 

# NOTE: this module already supports 32 wires and 64 strips 

###############################################################################
############################################################################### 

def syncData (pathsource,desitnationpath):

    command = 'rsync -av --progress'

    # command = 'cp'
    
    comm = command + ' ' + pathsource + ' ' + desitnationpath
    
    # print(comm)
    
    print('\n ... syncing data ...');
    
    status = os.system(comm);
    
    # NOTE: it will ask for password 
    
    # disp(cmdout)
    
    if status == 0: 
          print('\n data sync completed')
    else:
          print('\n \033[1;31mERROR ... \n\033[1;37m')
    
    # print(status)      
          
    print('\n-----')
    
    return status 

###############################################################################
############################################################################### 