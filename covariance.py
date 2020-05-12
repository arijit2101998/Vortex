import os
import pickle as cPickle
import numpy as np
from featureextraction import extract_features
#from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")

def covar(audio, sr, name):
   #source   = "./mic/storage.wav"
    #path where training speakers will be saved
   modelpathes =["Speakers_models_spherical/", "Speakers_models_diag/", "Speakers_models_full/"]
   user_valid = 0
   for modelpath in modelpathes:
       
       gmm_files = [os.path.join(modelpath,fname) for fname in 
                  os.listdir(modelpath) if fname.endswith('.gmm')]
    
        #Load the Gaussian gender Models
       models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
       speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
                  in gmm_files]
       
       #sr,audio = read(source)
       vector   = extract_features(audio,sr)
                #print("vector=",vector)
       log_likelihood = np.zeros(len(models))
       for i in range(len(models)):
           gmm    = models[i]  #checking with each model one by one
           scores = np.array(gmm.score(vector))
           #print(scores)
           log_likelihood[i] = scores.sum()
       speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
                  in gmm_files]
       speakers = sort_list(speakers,log_likelihood)
       print(speakers)
       if speakers[0]==name or speakers[1]==name:
           user_valid+=1
   return(user_valid)

def sort_list(list1, list2): 

	zipped_pairs = zip(list2, list1) 
	z = [x for _, x in sorted(zipped_pairs,reverse=True)] 
	return z 