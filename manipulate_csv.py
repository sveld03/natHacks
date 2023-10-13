# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 15:50:28 2023

@author: mauma
"""

import numpy as np
import csv
import matplotlib.pyplot as plt
import scipy.signal as sig

csvfile = np.loadtxt("Steven1b.csv", delimiter=',', skiprows=1)

# cum_signal = np.zeros((500, 8))
# for i in range(28500):
#     cum_signal[i % 500] += csvfile[i]
   
# cum_signal /= 57

# #plt.plot(range(0, 2000, 4), cum_signal[:,7])
# plt.plot(range(0, 2000, 4), cum_signal)

det_sig = np.zeros((500, 8))
cum_signal = np.zeros((500, 8))
for i in range(0, 30000, 500):
    for chan in range(8):
        det_sig[:,chan] = sig.detrend(csvfile[i:i+500, chan])
    cum_signal += det_sig
    
cum_signal /= 60

bpfilt = sig.butter(4, (0.1, 12.5), 'bandpass', output='sos', fs=250)
for ch in range(8):        
    cum_signal[:,ch] = sig.sosfilt(bpfilt, cum_signal[:,ch]);

plt.plot(range(0, 2000, 4), cum_signal[:,6:])
#plt.plot(range(0, 2000, 4), cum_signal)