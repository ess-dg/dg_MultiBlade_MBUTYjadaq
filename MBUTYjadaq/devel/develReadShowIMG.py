#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 13:32:00 2020

@author: francescopiscitelli
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img=mpimg.imread('finIMG.jpg')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
imgplot = plt.imshow(img)