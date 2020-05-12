import os
import pickle as cPickle
import numpy as np
from faces import face_check
from scipy.io.wavfile import read
from featureextraction import extract_features
from covariance import covar
#from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time
from tkinter import *
import speech_recognition as src

"""
#path to training data
source   = "development_set/"   
modelpath = "speaker_models/"
test_file = "development_set_test.txt"        
file_paths = open(test_file,'r')

"""
def lock():
    # Change Dir Path where you have Locker Folder
    os.chdir('C:\\Users\\USER\\Desktop')
    # If Locker folder or Recycle bin does not exist then we will be create Locker Folder 
    if not os.path.exists("Locker"):
        if not os.path.exists("Locker.{645ff040-5081-101b-9f08-00aa002f954e}"):
            os.mkdir("Locker")
            print("made")
        else:
            os.system("attrib -h Locker.{645ff040-5081-101b-9f08-00aa002f954e}")
            os.rename("Locker.{645ff040-5081-101b-9f08-00aa002f954e}","Locker")
            print("opened lock")
    else:
        os.rename("Locker","Locker.{645ff040-5081-101b-9f08-00aa002f954e}")
        os.system("attrib +h Locker.{645ff040-5081-101b-9f08-00aa002f954e}")
        print("locked again")
    os.chdir('C:\\Users\\USER\\.spyder-py3\\Speaker-Identification-Python-master')
    return
def clicked():
    #path to training data
   source   = "SampleData/"   

    #path where training speakers will be saved
   modelpath = "Speakers_models_tied/"
   
   gmm_files = [os.path.join(modelpath,fname) for fname in 
              os.listdir(modelpath) if fname.endswith('.gmm')]

    #Load the Gaussian gender Models
   models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
   
   take = selected.get()
   if take == 0:
        win2=Tk()
        win2.geometry('400x150')
        win2.title("Deveopers' Analytics")
        lbl = Label(win2, text="Username :", anchor=E, width=42).grid(column=0, row=1)
        txt = Entry(win2,width=10)
        txt.grid(column=1, row=1)
        lbl2 = Label(win2, text="Enter the File name from Test Audio Sample Collection :").grid(column=0, row=2)
        txt2 = Entry(win2,width=10)
        txt2.grid(column=1, row=2)
        def click():
            username=txt.get()
            path=txt2.get()
            sr,audio = read(source + path)
            vector   = extract_features(audio,sr)
            #print("vector=",vector)
            log_likelihood = np.zeros(len(models)) 
            lbl3 = Label(win2, text=" ")
            lbl3.grid(column=0, row=4)
            for i in range(len(models)):
                gmm    = models[i]  #checking with each model one by one
                scores = np.array(gmm.score(vector))
                #print(scores)
                log_likelihood[i] = scores.sum()
            speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
              in gmm_files]
            speakers = sort_list(speakers,log_likelihood)
            log_likelihood = sort_list(log_likelihood,speakers)
            print(speakers)
            print(log_likelihood)
            #winner = np.argmax(log_likelihood)
            if covar(audio,sr,username)>=2 and (username == speakers[0] or username==speakers[1]):
                lbl3['text']="Authorised user detected as - "+ username
                lock()
            else :
                lbl3['text']="User's voice mismatch"
        btn1 = Button(win2, text="Test Run", command=click)
        btn1.grid(column=0, row=5)
        btn2 = Button(win2, text="Quit", command=win2.destroy)
        btn2.grid(column =1,row=6)
        def cls():
            txt.delete(0,20)
            txt2.delete(0,20)
        btn3 = Button(win2, text="Clear", command=cls).grid(column=0, row=6)
        win2.mainloop()
        time.sleep(1.0)
   
   elif take == 1:
       win3=Tk()
       win3.geometry('400x150')
       win3.title("Speaker Identification")
       
       lbl2=Label(win3, text=" ")
       def Click():
           lbl=Label(win3, text="Please say something:", anchor=W)
           lbl.grid(column=0, row=1)
           recording = src.Recognizer()
           recording.energy_threshold=500
           recording.dynamic_energy_threshold = False
           with src.Microphone() as source: 
               recording.adjust_for_ambient_noise(source)
               audio = recording.listen(source,timeout=10)
           filename="storage.wav"
           name='./mic/'+str(filename)
           #file_obj=open(name,"w+")
           lbl2 = Label(win3, text="recorded")
           lbl2.grid(column=1, row=1)
           with open(name, "wb") as f:
               f.write(audio.get_wav_data())
           sr,audio = read(name)
           vector   = extract_features(audio,sr)
           print(sr)
           log_likelihood = np.zeros(len(models)) 
           lbl3 = Label(win3, text=" ")
           lbl3.grid(column=0, row=1)
           for i in range(len(models)):
                	gmm    = models[i]  #checking with each model one by one
                	scores = np.array(gmm.score(vector))
                	log_likelihood[i] = scores.sum()
           #print(log_likelihood)
           speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
              in gmm_files]
           speakers = sort_list(speakers,log_likelihood)
           print(speakers)
           #winner = np.argmax(log_likelihood)
           #print ("\tdetected as - ", speakers[winner])
           nam=face_check()
           #print(nam)
           if (speakers[0]==nam or speakers[1]==nam) and covar(audio,sr,nam)>=2:
               lbl3['text']="User detected and identified as - "+ nam
               lock()
           else:
               lbl3['text']="User's voice and face mismatch"
       btn1 = Button(win3, text="Authenticate", command=Click)
       btn1.grid(column=0, row=0)
       win3.mainloop()
       time.sleep(1.0)
       
window=Tk()
window.title("VORTEX")
selected = IntVar()
rad1 = Radiobutton(window,text='Real time testing for normal user', value=1, variable=selected)
rad2 = Radiobutton(window,text='Analytics for developers', value=0, variable=selected, anchor=W, width=25)
btn = Button(window, text="Click Me", command=clicked)
rad1.grid(column=0, row=0)
rad2.grid(column=0, row=1)
btn.grid(column=5, row=5)

def sort_list(list1, list2): 

	zipped_pairs = zip(list2, list1) 
	z = [x for _, x in sorted(zipped_pairs,reverse=True)] 
	return z 

window.mainloop()



