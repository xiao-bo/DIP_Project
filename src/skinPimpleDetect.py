import cv2
import sys
from pyimagesearch import imutils
import numpy as np
import argparse

cascPath = '../db/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

def remove(frame):
    cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,15,5)
    kernel = np.ones((5,5),np.uint8)
    dst=cv2.dilate(frame,kernel,anchor=(-1,-1),iterations=1)
    return dst

    
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame = imutils.resize(frame, width = 400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)

    ## frame call bitwise_and with other frame in skinMask range
    skin = cv2.bitwise_and(frame, frame, mask = skinMask)
    dst=remove(skin)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),

    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #print(converted.shape)
        for b in range(x, x+w):
            #print("b", b)
            for a in range(y, y+h):
                #print("a",a)
                roi = converted[y:(y+10), x:(x+10)]
                color0 = np.mean(roi[0])
                color1 = np.mean(roi[1])
                color2 = np.mean(roi[2])
                #print("color shape", color0)
                if color0<10 and color1>70 and color2>50: #converted[a,b,0]< 10 and converted[a,b,1] > 70 and converted[a,b,2] > 50:
                    cv2.rectangle(frame, (b, a), (b+10, a+10), (0, 255, 255), 2)
            
    # Display the resulting frame
    
<<<<<<< HEAD
    cv2.imshow('Video', np.hstack([frame, skin]))
    
=======
    cv2.imshow('Video',np.hstack([dst, skin]))
>>>>>>> origin/master

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
