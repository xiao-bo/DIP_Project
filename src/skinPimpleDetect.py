import cv2
import sys
from pyimagesearch import imutils
import numpy as np
import argparse
import math




cascPath = '../db/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
lower = np.array([0,30,60], dtype = "uint8")
upper = np.array([30,150,255], dtype = "uint8")


def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


def removePimple(frame):
    
    
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(frame, frame, mask = skinMask)

    #prepare mask smaller than origin mask
    #smaller mask will eat edge of blur.
    skinMask2 = cv2.erode(skinMask, kernel, iterations = 1) ## new
    #print(skinMask.shape)
    skin2 = cv2.blur(skin, (3, 3))
    skin2 = cv2.bitwise_and(skin2, skin2, mask = skinMask2) ## new

    frame2 = np.maximum(frame, skin2)
    
    gamma = 1.5
    frame4 = adjust_gamma(frame2, gamma=gamma)
    
    return frame4,skin


if __name__=="__main__":

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        frame = imutils.resize(frame, width = 500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame2,skin=removePimple(frame)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(80, 80),
        )
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Display the resulting frame
        
        print skin.shape
        print frame.shape
        cv2.imshow('Video', np.hstack([frame, frame2, skin]))
        #cv2.imshow('image', skinMask)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
