# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
import tkinter as tk
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pylsl import StreamInlet, resolve_stream

print("looking for an EEG stream")
streams = resolve_stream('type', 'EEG')

# create new inlet to read from stream
inlet = StreamInlet(streams[0])

eeg_data = np.zeros((250, 8))
header = ["timestamp", "channel1", "channel2", "channel3", "channel4", "channel5", "channel6", "channel7", "channel8"]

# GUI for displaying EEG data
# gui = tk.Tk()
# gui.geometry('1200x700+200+100')
# gui.title('Plotting live data')
# gui.state('zoomed')
# gui.config(background='#fafafa')

xar = []
yar = []

# matplotlib plotting
style.use('ggplot')
fig = plt.figure(figsize=(14, 4.5), dpi=100)
ax1 = fig.add_subplot(1,1,1)

try:
    sample_ind = 0
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        eeg_data[sample_ind] = sample
        #print(timestamp, *sample)
        #print(np.shape(eeg_data))
        sample_ind = sample_ind + 1
        if sample_ind >= 250:
            sample_ind = 0
            
        if sample_ind % 50 == 0:
            plt.clf()
            plt.plot(eeg_data[:,0].T)
            plt.show()
except KeyboardInterrupt:
    with open('p300_check.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        
        # write the data
        writer.writerow(header)
        writer.writerows(eeg_data)
    print('Data collected and exported!')
    
# def animate(i):
#     sample, timestamp = inlet.pull_sample()
#     eeg_data.append([timestamp, *sample])
#     line.set_data(xar, yar)
        
# line, = ax1.plot(eeg_data, 'r', marker='o')


# plotcanvas = FigureCanvasTkAgg(fig, gui)
# plotcanvas.get_tk_widget().grid(column=1, row=1)
# ani = animation.FuncAnimation(fig, animate, interval=1, blit=False)



#gui.mainloop()