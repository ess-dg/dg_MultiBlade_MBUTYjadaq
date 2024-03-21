#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 14:34:33 2020

@author: francescopiscitelli
"""

import os

# print("\033[1;32m Bright Green  \033[1;37m \n")

dd = 0

ac = 0

digitID = [33]
acqnum  = [0]
 
print('ciao')

print('\n \033[1;32m ---> Reading Digitizer '+str(digitID[dd])+', serial '+str(acqnum[ac])+'\033[1;37m')

print('ciao')

filenamefull = 'pippo'

print('\n \033[1;31m ---> File: '+filenamefull+' DOES NOT EXIST \033[1;37m')

print('ciao')

Ntoffi = 8
Ntoffiapriori = 9

print('\n \033[1;33m WARNING: check Num of ToFs ... found %d, expected %d \033[1;37m' % (Ntoffi, Ntoffiapriori))

print('ciao')