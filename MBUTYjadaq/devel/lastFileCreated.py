#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 12:37:34 2020

@author: francescopiscitelli
"""

import os
import glob
import numpy as np

datapathinput    = '/Users/francescopiscitelli/Desktop/temp/dataVMMutgard2/'

# dirFile = []
# listOfFiles = os.listdir(datapathinput)
# for k, files in enumerate(listOfFiles):
#     dirFile = np.append(dirFile,os.path.join(datapathinput,files))
#     # print(dirFile)
    
# latestFile  = max(dirFile, key=os.path.getctime)
# print(latestFile)


list_of_files = glob.glob(datapathinput+'/*.h5') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getmtime)
print(latest_file)

parts = os.path.split(latest_file)