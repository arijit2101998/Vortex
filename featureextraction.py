import numpy as np
#from sklearn import preprocessing
import python_speech_features as mfcc

def extract_features(audio,rate):
    """extract 20 dim mfcc features from an audio, performs CMS and combines 
    delta to make it 40 dim feature vector"""    
    
    mfcc_feature = mfcc.mfcc(audio,rate, 0.025, 0.01,26,nfft = 1200,preemph=0.97, appendEnergy = True)    
   # mfcc_feature = preprocessing.scale(mfcc_feature)
    mfcc_feature1= mfcc.logfbank(audio,rate,0.025,0.01,26,nfft = 1200)
    mfcc_feature2= mfcc.ssc(audio,rate,0.025,0.01,26,nfft = 1200)
    delta = mfcc.delta(mfcc_feature,26)
    combined = np.hstack((mfcc_feature,delta,mfcc_feature1,mfcc_feature2)) 
    return combined





















'''def calculate_delta(array):
    """Calculate and returns the delta of given feature vector matrix"""

    rows,cols = array.shape
    deltas = np.zeros((rows,26))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
              first =0
            else:
              first = i-j
            if i+j > rows-1:
                second = rows-1
            else:
                second = i+j 
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas
'''