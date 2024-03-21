#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:36:41 2020

@author: francescopiscitelli
"""

# from PyPl import progressbar
from time import sleep

# bar = progressbar.ProgressBar(maxval=20, \
#     widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
# bar.start()
# for i in range(20):
#     bar.update(i+1)
#     sleep(0.1)
    
# bar.finish()

import sys
import numpy as np
import time
import os

# for i in range(21):
#     sys.stdout.write('\r')
#     # the exact output you're looking for:
#     sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
#     sys.stdout.flush()
#     sleep(0.25)

NumClusters = 2000
n_bar = 10 #size of progress bar
text = 'clustering ...'

# for kk in np.arange(NumClusters):
#     j = kk/(NumClusters-1)
#     # sys.stdout.write('\r')
#     sys.stdout.write(f"{text} [{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%")
#     sys.stdout.flush()

# def progress(count, total, status=''):

total = NumClusters
bar_len = 10

for kk in np.arange(NumClusters):
    

    
    # filled_len = int(round(bar_len * count / float(total)))
    
    intervals = 7
    total = NumClusters
    current = kk 
    
    steps = round(total/intervals)
    
    if np.mod(current,steps) == 0 or kk == (total-1):
      
        percents = int(round(100.0 * kk / float(total), 1))
        # print(percents)
        # bar = '=' * filled_len + ' ' * (bar_len - filled_len)
        
        # print('%s [%s] %s%s \r' % (text, bar, percents, '%'),end='')
        time.sleep(0.2)
        # print('%s [ {:.2f}% ] \r' % (text,percents),end=' ')
        print('['+format(percents,'01d') + '%]',end=' ')
        # print('\r',end=' ')
        # 
    
    # sys.stdout.flush() 
    # time.sleep(0.02)
    # os.system('cls')


# print(format(3,'03d'))


from time import sleep
from tqdm import tqdm


pbar = tqdm(total=100)


for i in range(100):
    sleep(0.5)
    pbar.update(10)
pbar.close()
        
        