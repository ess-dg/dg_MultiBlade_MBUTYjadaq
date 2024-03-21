#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 08:48:41 2020

@author: francescopiscitelli
"""

# NOTE: this module already supports 32 wires and 64 strips 

import numpy as np

### constants ###
ht        = 1.054e-34  #J*s
mneutr    = 1.67e-27   #Kg
constant  = ( ( (ht**2)*4*(3.14159**2) )/(2*mneutr) )*1e20*(6.24e18)   #A^2 * eV
##############################

def ToF2lambda (distance, ToF):
    
    velocity = distance/ToF               #m/s
    energy   = (1/2)*(mneutr/1.6e-19)*(velocity**2)     #eV
    lamb     = np.sqrt(constant/energy)                  #A
    # lamb   = np.round(lamb,decimals=2)
    
    return lamb

def lambda2ToF (distance, lamb):
    
    energy   = constant/(lamb**2)
    velocity = np.sqrt(2*energy/((mneutr/1.6e-19)))
    ToF      = distance/velocity
    
    return ToF