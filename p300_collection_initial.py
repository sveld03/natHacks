# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
import numpy as np
from matplotlib import pyplot as plt
from pylsl import StreamInlet, resolve_stream

print("looking for an EEG stream")
streams = resolve_stream('type', 'EEG')
streamAUX = resolve_stream('type', 'AUX')
print("Got stream!")

# create new inlet to read from stream
inlet = StreamInlet(streams[0])
inletAUX = StreamInlet(streamAUX[0])

aux_data = np.zeros(8)
aux_received = False
eeg_data = np.zeros((1250, 8))
saved_eeg_data = np.zeros((70000, 8))
aux_data = np.zeros((70000,1))

header = ["channel1", "channel2", "channel3", "channel4", "channel5", "channel6", "channel7", "channel8"]

try:
    sample_ind = 0
    reg_ind = 0
    
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        auxsamp, auxts = inletAUX.pull_sample()
               
        if auxsamp[3] == 1.0:
            aux_received = True
            
        if aux_received:
            
            chunk, _ = inlet.pull_chunk()
            
            saved_eeg_data[reg_ind:reg_ind+np.shape(chunk)[0]] = chunk
            reg_ind += np.shape(chunk)[0]
        
except KeyboardInterrupt:
    
    print(reg_ind)
    
    with open('sessiontest3.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the data
        writer.writerow(header)
        writer.writerows(saved_eeg_data[:reg_ind-1])
    print('Data collected and exported!')
    
    
