#TODO: AVERAGE OVER SEVERAL TRIALS THEN FEED INTO LDA



from P3TE_Static_Variables import sampling_frequency;
import numpy as np;
import matplotlib.pyplot as plt;
import scipy.signal as sig;

# Get the target image id
#target_image_id = int(input("What was the target image id?\n"));
#TODO: switch this back
target_image_id = 0;

# Length of P300 response to evaluate (2s)
response_length = sampling_frequency * 2;

X = np.zeros((710,2000));
x_ind = 0;
y = np.zeros(710);
y2 = np.zeros(710);

label_files = ["trial_data\Steven_0_labels_faces_(31_trials)(10_images)(1300_downTime)(700_flashTime)_label0.csv",
               "trial_data\Steven_0_labels_faces_(30_trials)(10_images)(1300_downTime)(700_flashTime)_label0.csv",
               "trial_data\Steven_0_labels_faces_(10_trials)(10_images)(1300_downTime)(700_flashTime)label0.csv"];

data_files = ["trial_data\Steven_0_data_faces_(31_trials)(10_images)(1300_downTime)(700_flashTime)_label0.csv",
              "trial_data\Steven_0_data_faces_(30_trials)(10_images)(1300_downTime)(700_flashTime)_label0.csv",
              "trial_data\Steven_0_data_faces_(10_trials)(10_images)(1300_downTime)(700_flashTime)_label0.csv"];

for fileN in range(3):

    # Pull label data
    label_file = label_files[fileN];
    labels = (np.loadtxt(label_file, delimiter=',')).astype(int);
    
    # Extract trial parameters
    n_images = int(max(labels)+1);
    n_flashes = int(len(labels));
    n_trials = int(n_flashes/n_images);
    
    # Pull sample data
    data_file = data_files[fileN];
    samples = np.loadtxt(data_file, delimiter=',', skiprows=1);
    
    # Init filter
    bpfilt = sig.butter(4, (1, 12.5), 'bandpass', output='sos', fs=250)
    # Apply filter to each electrode
    for channel in range(8): 
        # Detrend channel
        samples[:,channel] = sig.detrend(samples[:,channel]);
        # Filter channel
        samples[:,channel] = sig.sosfilt(bpfilt, samples[:,channel]); 
            
    # Find end-of-countdown index and trim off countdown samples
    eoc_index = np.where(samples[:,8] == 0)[0][0];
    print("Countdown samples appeared to take up " + str(eoc_index/sampling_frequency) + " seconds.");
    samples = samples[eoc_index:,:];
    
    # Check if a shutdown signal was found
    if(np.sum(samples[:,9]) == 0):
        print("Warning! No shutdown signal was detected.");
    
    # Init response signals
    target_signals = np.zeros((n_trials,response_length,8));
    target_flash_index = 0;
    non_target_signals = np.zeros((n_trials*(n_images-1),response_length,8));
    non_target_flash_index = 0;
        
    # Loop through the data and find the data for each flash
    last_flash_index = 0;
    for flash in range(n_flashes):
        
        if(flash == n_flashes-1):
            continue;
            
        # Find start index of this flash
        start_index = np.where(samples[last_flash_index:,8] == 1)[0][0]+last_flash_index;
            
        # Check if this was a target flash or not & append accordingly
        if(labels[flash] == target_image_id):
            target_signals[target_flash_index,:,:] = samples[start_index:start_index+response_length,:8]
            target_flash_index += 1;
        else:
            non_target_signals[non_target_flash_index,:,:] = samples[start_index:start_index+response_length,:8]
            non_target_flash_index += 1;
            
            
        #for classifier
        X[x_ind,:] = np.reshape(samples[start_index:start_index+250,:8], (2000,));
        x_ind += 1;
        y[x_ind] = int(labels[flash]==target_image_id);
        y2[x_ind] = labels[flash];
        
        # Reset for next flash seek
        last_flash_index = np.where(samples[start_index:,8] == 0)[0][0]+start_index;
    
    
    # Calc avg responses
    avg_target_response = np.mean(target_signals, axis=0);
    avg_target_response = np.mean(avg_target_response, axis=1);
    avg_non_target_response = np.mean(non_target_signals, axis=0);
    avg_non_target_response = np.mean(avg_non_target_response, axis=1);


#X = np.mean(X, axis=2);

shuffled_indices = np.arange(710);
np.random.shuffle(shuffled_indices)

train_indices = shuffled_indices[:int(710*0.80)]
test_indices = shuffled_indices[int(710*0.80):]

y2 = y2[test_indices];

X_train, y_train = X[train_indices,:], y[train_indices]
X_test, y_test = X[test_indices,:], y[test_indices]

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
clf = LDA()
clf.fit(X_train, y_train)

probs = np.ones(10);
c_probs = np.zeros(10);
c_count = np.zeros(10);

for i in range(len(y2)):
    
    prob = clf.predict_proba([X_test[i,:]])[0,1];
    
    if(prob <.001):
        prob = .001;
    elif(prob >.999):
        prob = .999
        
    q_prob = (1-prob)/9;
    
    probs[int(y2[i])] *= prob;
    for j in range(len(y2)):
        if(i==j):
            continue;
        probs[int(y2[j])] *= q_prob;
    
    probs /= np.sum(probs);
    
    c_probs[int(y2[i])] += prob;
    c_count[int(y2[i])] += 1;

for i in range(10):
    c_probs[int(y2[i])] /= c_count[int(y2[i])];
    
print(probs);
print(c_probs);


"""
t = np.arange(0, 1000, 4);
plt.figure(1);
plt.clf();
plt.plot(avg_target_response);
plt.plot(avg_non_target_response);
"""


"""
# Visualize responses
plt.figure(1);
plt.subplot(231);
plt.plot(t,avg_target_response[:250,0:3]);
plt.subplot(232);
plt.plot(t,avg_target_response[:250,3:6]);
plt.subplot(233);
plt.plot(t,avg_target_response[:250,6:8]);
plt.subplot(234);
plt.plot(t,avg_non_target_response[:250,0:3]);
plt.subplot(235);
plt.plot(t,avg_non_target_response[:250,3:6]);
plt.subplot(236);
plt.plot(t,avg_non_target_response[:250,6:8]);
"""

























