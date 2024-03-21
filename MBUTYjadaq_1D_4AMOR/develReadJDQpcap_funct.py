#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:36:45 2022

@author: francescopiscitelli
"""
# import argparse
import numpy as np
import pcapng as pg
import os
import time
import sys
# from lib import libPlotting as plo

###############################################################################
###############################################################################

filePathAndFileName = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYjadaq_1D/testJDQdata.pcapng'

NSperClockTick = 16

 # filePathAndFileName, NSperClockTick, timeResolutionType = 'fine', sortByTimeStampsONOFF = True
 
 
 
ff = open(filePathAndFileName, 'rb')
scanner = pg.FileScanner(ff)

counterPackets = 0
counterCandidatePackets = 0


packetsSizes = np.zeros((0),dtype='int64')

for block in scanner:
    
          if counterPackets <= 4:
        
    
               counterPackets += 1
               print("packet {}".format(counterPackets))
               
               if counterPackets == 5:
        
                   try:
                            packetSize = block.packet_len
                            print("packetSize {} bytes".format(packetSize))
                   except:
                            print('--> other packet found No. {}'.format(counterPackets-counterCandidatePackets))
                   else:
                            counterCandidatePackets += 1
                            packetsSizes = np.append(packetsSizes,packetSize)
                            
                            print('counterPackets {}, counterCandidatePackets {}'.format(counterPackets,counterCandidatePackets))    
               
               
               
                   try:
                       packetLength = block.packet_len
                       packetData   = block.packet_data
                    
                   except:
                        print('--> other packet found')
                    
                   else:
                       
                        offset = 42
                        uno  = int.from_bytes(packetData[0+offset:8+offset], byteorder='big') # bytes
                        due  = int.from_bytes(packetData[offset+8:offset+16], byteorder='big') # bytes
                        tre  = int.from_bytes(packetData[offset+16:offset+24], byteorder='big') # bytes
                        quat  = int.from_bytes(packetData[offset+24:offset+32], byteorder='big') # bytes
                        digi  = int.from_bytes(packetData[offset+32:offset+40], byteorder='big') # bytes
                        
                        h1  = int.from_bytes(packetData[offset+40:offset+44], byteorder='little') # bytes
                        h2  = int.from_bytes(packetData[offset+44:offset+48], byteorder='little') # bytes
                        h3  = int.from_bytes(packetData[offset+48:offset+52], byteorder='little') # bytes
                        h4  = int.from_bytes(packetData[offset+52:offset+56], byteorder='little') # bytes
                        h5  = int.from_bytes(packetData[offset+56:offset+60], byteorder='little') # bytes
                        h6  = int.from_bytes(packetData[offset+60:offset+64], byteorder='little') # bytes
                        
                        g1  = int.from_bytes(packetData[offset+32:offset+40], byteorder='little') # bytes
                        g2  = int.from_bytes(packetData[offset+40:offset+44], byteorder='little') # bytes
                        g3  = int.from_bytes(packetData[offset+44:offset+48], byteorder='little') # bytes
                        
                        # digi  = int.from_bytes(packetData[offset+128:offset+160], byteorder='big') # bytes
                        
                        
                        
                        