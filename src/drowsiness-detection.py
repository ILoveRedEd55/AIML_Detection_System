import cv2
import os
from tensorflow.keras.models import load_model
import numpy as np
from pygame import mixer
import time


mixer.init()
sound = mixer.Sound('./src/index/alarm.wav')

face = cv2.CascadeClassifier('./lib/haar-cascade-files/haarcascade_frontalface_alt.xml')
leye = cv2.CascadeClassifier('./lib/haar-cascade-files/haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('./lib/haar-cascade-files/haarcascade_righteye_2splits.xml')



lbl=['Close','Open']

model = load_model('./lib/model/cnnCat2.h5')
path = os.getcwd()
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
count=0
score=0
thicc=2
rpred=[99]
lpred=[99]

while(True):
    ret, frame = cap.read()
    height,width = frame.shape[:2] 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
    left_eye = leye.detectMultiScale(gray)
    right_eye =  reye.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y) , (x+w,y+h) , (100,100,100) , 1 )

    for (x,y,w,h) in right_eye:
        r_eye=frame[y:y+h,x:x+w]
        count=count+1
        r_eye = cv2.cvtColor(r_eye,cv2.COLOR_BGR2GRAY)
        r_eye = cv2.resize(r_eye,(24,24))
        r_eye= r_eye/255
        r_eye=  r_eye.reshape(24,24,-1)
        r_eye = np.expand_dims(r_eye,axis=0)
        rpred = model.predict_classes(r_eye)
        if(rpred[0]==1):
            lbl='Open' 
        if(rpred[0]==0):
            lbl='Closed'
        break

    for (x,y,w,h) in left_eye:
        l_eye=frame[y:y+h,x:x+w]
        count=count+1
        l_eye = cv2.cvtColor(l_eye,cv2.COLOR_BGR2GRAY)  
        l_eye = cv2.resize(l_eye,(24,24))
        l_eye= l_eye/255
        l_eye=l_eye.reshape(24,24,-1)
        l_eye = np.expand_dims(l_eye,axis=0)
        lpred = model.predict_classes(l_eye)
        if(lpred[0]==1):
            lbl='Open'   
        if(lpred[0]==0):
            lbl='Closed'
        break

    if(rpred[0]==0 and lpred[0]==0):
        score=score+1
    else:
        score=score-1
    
        
    if(score<0):
        score=0 
    if(score>10):
        try:
            sound.play()
            
        except:  # isplaying = False
            pass
        if(thicc<16):
            thicc= thicc+2
        else:
            thicc=thicc-2
            if(thicc<2):
                thicc=2
        frame = cv2.copyMakeBorder(src=frame,
                        top= 10,
                        bottom= 10,
                        left= 10,
                        right= 10,
                        borderType=cv2.BORDER_CONSTANT,
                        dst=None,
                        value=[0, 0, 255]) 
    else:
        frame = cv2.copyMakeBorder(src=frame,
                        top= 10,
                        bottom= 10,
                        left= 10,
                        right= 10,
                        borderType=cv2.BORDER_CONSTANT,
                        dst=None,
                        value=[0, 255, 0])
    cv2.namedWindow('frame', flags=cv2.WINDOW_GUI_NORMAL)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty('frame', cv2.WND_PROP_TOPMOST, 1)
    cv2.resizeWindow('frame', 800, 600)
    cv2.moveWindow('frame', 370, 75)       
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
