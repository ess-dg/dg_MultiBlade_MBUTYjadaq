#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 11:18:17 2019

@author: francescopiscitelli
"""

#this is the equivalent of the MATALB function 
#data = cleaning(data,cleaningfromrepet,overflowcorr,zerosuppression)

#cleaning, works for 1 cassette
def cleaning (data,overflowcorr,zerosuppression):

    Noriginal = data.shape[0]
    print('\n \t file length: ',str(Noriginal),' rows',);
    
    if overflowcorr  == 1:
        over = data[:,2] >= 65535
        data = data[~over,:]
        Noverflow = sum(over)
        Nnew      = data.shape[0]
        if Noverflow != 0:
            print('\n ... Overflow (65535) events!!! -> file cleaned! ', end=' ')
            print('overflow rows: ',str(Noverflow),', new file length: ',str(Nnew),' rows')
            
    if zerosuppression  == 1:
        zer  = data[:,2] == 0
        data = data[~zer,:]
        Nzer = sum(zer)
        Nnew = data.shape[0]
        if Nzer != 0:
            print('\n ... zero ADC events!!! -> file cleaned! ', end=' ')
            print('zero ADC rows: ',str(Nzer),', new file length: ',str(Nnew),' rows')
            
    return data