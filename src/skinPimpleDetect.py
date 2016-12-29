import cv2
import sys
from pyimagesearch import imutils
import numpy as np
import argparse
import math

cascPath = '/Users/chenyu/Downloads/Webcam-Face-Detect-master/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
lower = np.array([0,30,60], dtype = "uint8")
upper = np.array([30,150,255], dtype = "uint8")

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame = imutils.resize(frame, width = 500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    #skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(frame, frame, mask = skinMask)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(80, 80),
    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        skin2=cv2.GaussianBlur(skin, (5,5),0)
        frame2 = frame-skin+skin2
    #print(converted.shape)
        '''for b in range(x, x+w):
            #print("b", b)
            for a in range(y, y+h):
                #print("a",a)
                roi = converted[y:(y+10), x:(x+10)]
                color0 = np.mean(roi[0])
                color1 = np.mean(roi[1])
                color2 = np.mean(roi[2])
                #print("color shape", color0)
                if color0<10 and color1>70 and color2>50: #converted[a,b,0]< 10 and converted[a,b,1] > 70 and converted[a,b,2] > 50:
                    cv2.rectangle(frame, (b, a), (b+10, a+10), (0, 255, 255), 2)'''
    # Display the resulting frame
    
    cv2.imshow('Video', np.hstack([frame, frame2, skin]))
    #cv2.imshow('image', skinMask)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()