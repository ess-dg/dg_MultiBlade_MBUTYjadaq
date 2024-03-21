#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 09:21:00 2022

@author: francescopiscitelli
"""

indexSt = 1

for kk in range(5):

        if kk < indexSt:
            
            print('kk= '+str(kk)+' from '+str(kk*32)+' to '+str((kk+1)*32)+' <- from '+str(kk*32)+' to '+str((kk+1)*32))
            # XYprojGlob2[kk*32:(kk+1)*32]  = XYprojGlob[kk*32:(kk+1)*32]
            # XXg2[kk*32:(kk+1)*32]  = XXg[kk*len(XX):(kk+1)*32] 
        
        elif kk >= indexSt:
            
            print('kk= '+str(kk)+' from '+str(kk*32)+' to '+str((kk+1)*32)+' <- from '+str((kk+1)*32)+' to '+str((kk+2)*32))
            
            # XYprojGlob2[kk*len(XX):(kk+1)*len(XX)]  = XYprojGlob[(kk+1)*len(XX):(kk+2)*len(XX)]
            # XXg2[kk*len(XX):(kk+1)*len(XX)]  = XXg[(kk+1)*len(XX):(kk+2)*len(XX)] 