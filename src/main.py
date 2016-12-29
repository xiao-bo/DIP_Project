#!/usr/bin/env python
# -*- coding: utf-8 -*-

## pygame part 
import pygame

## opencv 2
import cognitive_face as CF
import cv2

## python build-in library
import numpy as np
from threading import Thread
## import our class in src
from npc import NPC
from dialog import Dialog
from ageDetection import getAge

cascPath = "../db/haarcascade_frontalface_default.xml"        
KEY = 'f36fd7a2c5a84e0ea61fa81a80aed7d8'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

#img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
img_url="../pic/self.jpg"


class EnterPoint:
    def __init__(self):
        ### initial game's property value
        self.running = True
        self.screen = None
        
        ## window size
        self.size = self.width, self.height = 840, 600 

        ## dialog index
        self.index = 0
        self.flag=False
        
    def on_init(self):
        ## game initail process
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

        ## window title
        pygame.display.set_caption("WindowTitle")

        ## load minon NPC
        ## 500,200 represent position x,y
        npcMinion = NPC("../pic/npc_minion.jpeg",500,400)
        self.npcMinion,self.npcMinion_rect=npcMinion.load()

        ## init dialog font 
        self.font = pygame.font.SysFont(None, 80)

        ##camera init
        self.video_capture = cv2.VideoCapture(0)

        ##camera position (x,y)
        self.video_capture.set(3,840)
        self.video_capture.set(4,480)
        

    def on_event(self, event):
        dialog = Dialog()
        text = dialog.load(self.index)

        if event.type == pygame.QUIT:
            self.running = False

        #### dialog part ####   
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
        text = dialog.load(self.index)
        ## change text font and color
        self.dialog = self.font.render(text, False, (255,255,255))

    def on_loop(self):

        #### camera part ####
        ## camera takes frame 
        ret, frame = self.video_capture.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ## load face model
        faceCascade = cv2.CascadeClassifier(cascPath)

        ## detect person face
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        ## draw rectangle
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        t=Thread(target=getAge(frame))
        t.start()
        #result=getAge(frame)
        #print result
        
        ## frame color into normal mode 
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)


        ## turn frame into right angle 
        frame=np.rot90(frame)

        ## turn frame(nd.array) into surface            
        self.frame = pygame.surfarray.make_surface(frame)
        


    
    def on_render(self):
        
       
        ## render frame on screen 
        self.screen.blit(self.frame,(0,0))


        if (self.flag):
            self.screen.blit(self.npcMinion, self.npcMinion_rect)
        else:
            pass
        self.screen.blit(self.dialog, (20,480))
        pygame.display.flip()
        

    def on_cleanup(self):
        pygame.quit()
        self.video_capture.release()
        cv2.destroyAllWindows()
        
 
if __name__ == "__main__" :

    Enter = EnterPoint()
    
    if Enter.on_init() == False:
        Enter.running = False

    ### game loop
    while( Enter.running ):
        ## event callback
        for event in pygame.event.get():
            Enter.on_event(event)

        Enter.on_loop()
        Enter.on_render()
    Enter.on_cleanup()

