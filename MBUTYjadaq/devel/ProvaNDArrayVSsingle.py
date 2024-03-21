#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:46:45 2020

@author: francescopiscitelli
"""

import numpy as np
import time



N = int(1e7)

a = np.ones(N)*1.6 
b = np.ones(N)*3.445
c = np.ones(N)*7.445
d = np.ones(N)*5
e = np.ones(N)*1.65 
f = np.ones(N)*3.5
g = np.ones(N)*9.445
h = np.ones(N)*34
i = np.ones(N)*1.65 
l = np.ones(N)*3.5
m = np.ones(N)*9.445
n = np.ones(N)*34
z = np.zeros(N)

AA = np.zeros((N,12))
AA[:,0] = a
AA[:,1] = b
AA[:,2] = c
AA[:,3] = d
AA[:,4] = e
AA[:,5] = f
AA[:,6] = g
AA[:,7] = h
AA[:,8] = i
AA[:,9] = l
AA[:,10] = m
AA[:,11] = n

x = np.zeros(N)



tProfilingStart2 = time.time()

for k in np.arange(0,N,1):
    
    x[k] = AA[k,0]+AA[k,1]+AA[k,2]+AA[k,3]+AA[k,4]+AA[k,5]+AA[k,6]+AA[k,7]+AA[k,8]+AA[k,9]+AA[k,10]+AA[k,11]


tElapsedProfiling2 = time.time() - tProfilingStart2
print('\n Completed --> elapsed time: %.2f s' % tElapsedProfiling2)



tProfilingStart1 = time.time()

for k in range(0,N,1):
    
    z[k] = a[k]+b[k]+c[k]+d[k]+e[k]+f[k]+g[k]+h[k]+i[k]+l[k]+m[k]+n[k]
    
tElapsedProfiling1 = time.time() - tProfilingStart1
print('\n Completed --> elapsed time: %.2f s' % tElapsedProfiling1)




