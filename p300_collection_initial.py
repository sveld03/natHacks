# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
import numpy as np
from matplotlib import pyplot as plt
from pylsl import StreamInlet, resolve_stream, resolve_byprop

print("looking for an EEG stream")
stream = resolve_byprop('source_id', 'Cyton_Data_Packager3333')
print("Got stream!")

# create new inlet to read from stream
inlet = StreamInlet(stream[0])

aux_received = False
saved_eeg_data = np.zeros((70000, 8))

header = ["channel1", "channel2", "channel3", "channel4", "channel5", "channel6", "channel7", "channel8"]

try:
    sample_ind = 0
    reg_ind = 0
    
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        if not aux_received:
            
            sample, _ = inlet.pull_sample()
                   
            print(sample[8])
            
            if sample[8] == 1:
                aux_received = True
            
        if aux_received:
                        
            chunk, _ = inlet.pull_chunk()
            
            if len(chunk) > 0:
                #print(chunk)
                #print(np.shape(chunk))
                
                saved_eeg_data[reg_ind:reg_ind+np.shape(chunk)[0]] = np.array(chunk)[:,0:8]
                reg_ind += np.shape(chunk)[0]
        
except KeyboardInterrupt:
    
    with open('sessiontest4.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the data
        writer.writerow(header)
        writer.writerows(saved_eeg_data[:reg_ind-1])
    print('Data collected and exported!')
    
    
