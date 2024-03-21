#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:31:11 2020

@author: francescopiscitelli
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

plotIMGinlogScale = 0

data = np.load('data2DimgESSmask.npy')

fig = plt.figure()
ax = fig.add_subplot(111)

if plotIMGinlogScale == 1:
    normColors = LogNorm()
elif plotIMGinlogScale == 0:
    normColors = None

ax.imshow(data,aspect='auto',norm=normColors,interpolation='nearest',origin='upper',cmap='jet')

plt.savefig('savedFigW.pdf', dpi=None, facecolor='w', edgecolor='w',
        orientation='landscape', format='pdf', transparent=False, pad_inches=0.1)

plt.savefig('savedFigT.pdf', dpi=None, orientation='landscape', format='pdf', transparent=True, pad_inches=0.1)