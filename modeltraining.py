import _pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture as GMM
#from sklearn.mixture import GMM 
from featureextraction import extract_features
#import pandas as pd
#from pandas import DataFrame 
#import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

#path to training data
# source   = "development_set/"
source   = "trainingData/"   

#path where training speakers will be saved

# dest = "speaker_models/"
# train_file = "development_set_enroll.txt"

dest = "Speakers_models_tied/"
train_file = "trainingDataPath.txt"        
file_paths = open(train_file,'r')

count = 1
# Extracting features for each speaker (5 files per speakers)
features = np.asarray(())
for path in file_paths:    
    path = path.strip()   
    print (path)
    
    # read the audio
    sr,audio = read(source + path)
    print(sr)
    # extract 40 dimensional MFCC & delta MFCC features
    vector   = extract_features(audio,sr)
    if features.size == 0:
        features = vector
    else:
        features = np.vstack((features, vector))
    # when features of 5 files of speaker are concatenated, then do model training
	# -> if count == 5: --> edited below
    if count == 15:    
        gmm = GMM(n_components = 16,max_iter=200,covariance_type='tied',n_init=3)
        gmm.fit(features)
        #d=pd.DataFrame(features)
        #plt.scatter(d[0],d[1])
        #plt.show
        # dumping the trained gaussian model
        picklefile = path.split("-")[0]+".gmm"
        cPickle.dump(gmm,open(dest + picklefile,'wb'))
        print ('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)    
        features = np.asarray(())
        count = 0
    count = count + 1
