import numpy as np
import sklearn
import csv
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

ntrials=100

csvfile6 = np.loadtxt("StevenEEG6-Yellow.csv", delimiter=',', skiprows=1)
csvfile7 = np.loadtxt("StevenEEG7-Yellow.csv", delimiter=',', skiprows=1)

labels6 = np.loadtxt("StevenColor6-Yellow.csv", delimiter=',')
labels7 = np.loadtxt("StevenColor7-Yellow.csv", delimiter=',')

labels6 = labels6.astype(int)
labels7 = labels7.astype(int)

csvfile = np.concatenate((csvfile6, csvfile7))
labels = np.concatenate((labels6, labels7))

det_sig = np.zeros((500, 8))

red_cum_signals = np.zeros((ntrials, 500, 8))
yel_cum_signals = np.zeros((ntrials, 500, 8))
blu_cum_signals = np.zeros((ntrials, 500, 8))

counter = 0
red_counter = 0
yel_counter = 0
blu_counter = 0

for i in range(0, 500*ntrials*3, 500):
    label = labels[counter]
    for chan in range(8):
        det_sig[:,chan] = sig.detrend(csvfile[i:i+500, chan])

    if (label == 1):
        red_cum_signals[red_counter] = det_sig
        red_counter += 1
    if (label == 2):
        yel_cum_signals[yel_counter] = det_sig
        yel_counter += 1
    if (label == 3):
        blu_cum_signals[blu_counter] = det_sig
        blu_counter += 1
    counter += 1    


bpfilt = sig.butter(4, (0.1, 12.5), 'bandpass', output='sos', fs=250)

for ch in range(8):        
    red_cum_signals[:, :, ch] = sig.sosfilt(bpfilt, red_cum_signals[:, :, ch]);
    yel_cum_signals[:, :, ch] = sig.sosfilt(bpfilt, yel_cum_signals[:, :, ch]);
    blu_cum_signals[:, :, ch] = sig.sosfilt(bpfilt, blu_cum_signals[:, :, ch]);

red_cum_signals = np.mean(red_cum_signals, axis=2)
blu_cum_signals = np.mean(blu_cum_signals, axis=2)
yel_cum_signals = np.mean(yel_cum_signals, axis=2)

labels = np.array([labels == 2], dtype=int)[0]

X = np.vstack((red_cum_signals, yel_cum_signals, blu_cum_signals))
y = labels

shuffled_indices = np.arange(3*ntrials)
np.random.shuffle(shuffled_indices)

train_indices = shuffled_indices[:240]
test_indices = shuffled_indices[240:]

X_train, y_train = X[train_indices], y[train_indices]
X_test, y_test = X[test_indices], y[test_indices]

clf = LDA()
clf.fit(X_train, y_train)
print(f'Score: {clf.score(X_test, y_test)}')