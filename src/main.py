#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame

import numpy as np
import threading 
## import our class in src
from npc import NPC
from dialog import Dialog
#from ageDetection import ageThread

import time
import sys
import cognitive_face as CF
import cv2

## faceAPI variable 
cascPath = "../db/haarcascade_frontalface_default.xml"        
KEY = 'f36fd7a2c5a84e0ea61fa81a80aed7d8'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)
resultFaceAPI = [None] 

class ageThread(object):
    def __init__(self,frame):
        self.interval=1
        t=threading.Thread(target=self.run,args=[frame])
        t.daemon=True
        t.start()
    def run(self,frame):
        cv2.imwrite("age.jpg",frame)
        resultFaceAPI[0] = CF.face.detect("age.jpg",False,False,'age,smile,gender')

        
class EnterPoint:
    def __init__(self):
        ### initial game's property value
        self.running = True
        self.screen = None
        
        ## window size
        self.size = self.width, self.height = 840, 600 

        ## dialog index
        self.index = 0

        #detect face by passing person
        self.count = 0
        self.result = None
        self.somebody = False
        
    def on_init(self):
        ## game initail process
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

        ## window title
        pygame.display.set_caption("WindowTitle")

        
        ## load minon NPC
        ## 500,200 represent position x,y
        npcMinion = NPC("../pic/npc_minion.jpeg",450,100)
        self.npcMinion,self.npcMinion_rect=npcMinion.load()
        

        ## init dialog font 
        self.font = pygame.font.SysFont(None, 50)

        #camera init
        self.video_capture = cv2.VideoCapture(0)
        #camera windows size
        
        self.video_capture.set(3,840)
        self.video_capture.set(4,480)
        
        

    def on_event(self, event):
        dialog = Dialog()
        self.text = dialog.load(self.index)

        if event.type == pygame.QUIT:
            self.running = False

        ## dialog part     
        ## detect keydown 
        elif event.type == pygame.KEYDOWN:
            ## if key is right
            if event.key == pygame.K_RIGHT: 
                ## change dialog
                self.index = (self.index+1)%5 
            elif event.key == pygame.K_LEFT:
                self.index = (self.index-1)%5

            ## simulate person is leaving state.    
            elif event.key == pygame.K_BACKSPACE: 
                ## text is "goodbye"
                self.index = 6  
            ## simulate person appears in another side  
            elif event.key == pygame.K_SPACE: 
                ## text is "bug hole will opening"
                self.index = 5
                self.flag=True
            ## restart dialog  
            elif event.key == pygame.K_ESCAPE:
                ##
                self.index = 0
                self.flag=False


        ##change text content
        self.text = dialog.load(self.index)
        ## change text font and color
        self.dialog = self.font.render(self.text, False, (255,0,0))

    def on_loop(self):

        ## camera part 
        ## camera takes frame 
        ret, self.frame = self.video_capture.read()
        
        ## load face model
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        ## detect person face
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
 
       	#determine person age by count
        
        if len(faces)>0:

            self.count = self.count + 1
            self.somebody = True
            if self.count == 1:
                ## create thread to get age
                ageThread(self.frame)
                print "result  "+str(resultFaceAPI)

        else:
            self.somebody = False
            self.count = 0	
        
        ## frame color into normal mode 
        self.frame=cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)

        ## turn frame into right angle 
        self.frame=np.rot90(self.frame)

        ## turn frame(nd.array) into surface            
        self.frame = pygame.surfarray.make_surface(self.frame)
       
    def on_render(self):
        
        ## render frame on screen 
        self.screen.blit(self.frame,(0,0))

        ## if have person, npc and dialog appear. 
        if self.somebody == True:
            self.screen.blit(self.npcMinion, self.npcMinion_rect)
            self.screen.blit(self.dialog, (20,50))

        pygame.display.update()
        
        
    def on_cleanup(self):
        pygame.quit()
        cv2.destroyAllWindows()
        


if __name__ == "__main__" :

    Enter = EnterPoint()
    
    ## game init variable
    if Enter.on_init() == False:
        Enter.running = False

    ## game loop 
    while( Enter.running ):
        for event in pygame.event.get():
            Enter.on_event(event)
        Enter.on_loop()
        Enter.on_render()
    Enter.on_cleanup()

