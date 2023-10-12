# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from matplotlib import pyplot as plt
from pylsl import StreamInlet, resolve_stream

print("looking for an EEG stream")
streams = resolve_stream('type', 'EEG')
print("Got stream!")

# create new inlet to read from stream
inlet = StreamInlet(streams[0])

eeg_data = np.zeros((250, 8))
header = ["timestamp", "channel1", "channel2", "channel3", "channel4", "channel5", "channel6", "channel7", "channel8"]

try:
    sample_ind = 0
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        eeg_data[sample_ind] = sample
        
        sample_ind = sample_ind + 1
        if sample_ind >= 250:
            sample_ind = 0
            
        if sample_ind % 50 == 0:
            plt.clf()
            plt.plot(eeg_data[:,0].T)
            plt.show()
            
except KeyboardInterrupt:
    print('Done!')
    
    
