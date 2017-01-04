#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame

import numpy as np
import threading 
import time
import sys
import cognitive_face as CF
import cv2
import json

## import our class in src
from npc import NPC
from dialog import Dialog
from font import textHollow,textOutline
from skinPimpleDetect import removePimple

## faceAPI variable 
cascPath = "../db/haarcascade_frontalface_default.xml"        
KEY = 'f36fd7a2c5a84e0ea61fa81a80aed7d8'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

## result of FaceAPI , reason of using array is single value 
## can't pass by thread
## gender is same reason
resultFaceAPI = [None] 
## detect person gender
gender = [None]
age = [None]

def parseFaceAPI(data,gender,age):
    ## function will return key:value
    ## avoid no detection person 
    if None in data or not data[0]:
        return 'no'
    ##turn string into json fromat 
    jsonFormat=json.dumps(data[0][0])
    
    ## turn json into python dicitionary 
    dic=json.loads(jsonFormat)
    return dic['faceAttributes'][gender],dic['faceAttributes'][age]


class ageThread(object):
    def __init__(self,frame,gender_v,age_v):
        self.interval=1
        t=threading.Thread(target=self.run,args=[frame,gender_v,age_v])
        t.daemon=True
        t.start()
    def run(self,frame,gender_v,age_v):
        cv2.imwrite("age.jpg",frame)
        resultFaceAPI[0] = CF.face.detect("age.jpg",False,False,'age,gender')
        
        a,b=parseFaceAPI(resultFaceAPI,gender_v,age_v)
        print "a:"+str(a)+" b:"+str(b)
        gender[0]=a
        age[0]=b
        print "thread: "+str(resultFaceAPI)       
   
        
class EnterPoint:
    def __init__(self):
        ### initial game's property value
        self.running = True
        self.screen = None
        
        ## window size
        self.size = self.width, self.height = 840, 600 

        ## dialog index
        self.index = 0
        self.index2 = 0
        self.order = True
        self.flag = False
        self.bye = True
        self.yn = False

        #detect face by passing person
        self.count = 0
        self.result = None
        self.somebody = False

        #map and partner
        self.tour = False
        self.hole = False
        
        
    def on_init(self):
        ## game initail process
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

        ## window title
        pygame.display.set_caption("WindowTitle")

        
        ## load male ,female and old NPC
        ## 500,200 represent position x,y
        ## male NPC
        npcFire = NPC("../pic/fire.png",650,30)
        self.npcFire,self.npcFire_rect=npcFire.load()

        ## female NPC
        npcCat = NPC("../pic/jani.png",600,30)
        self.npcCat,self.npcCat_rect=npcCat.load()

        ## old NPC

        npcOld = NPC("../pic/old.png",600,30)
        self.npcOld,self.npcOld_rect=npcOld.load()


        ## load map and partner
        self.partner =pygame.image.load("../pic/partner.png")
        self.map =pygame.image.load("../pic/map.png")
        ## init dialog font 
        self.font = pygame.font.SysFont(None, 50)

        #camera init
        self.video_capture = cv2.VideoCapture(0)
        #camera windows size
        
        self.video_capture.set(3,840)
        self.video_capture.set(4,600)
        
        

    def on_event(self, event):

        ## dialog part     
        ## detect keydown 
        if event.type == pygame.QUIT:
            self.running = False

        ## dialog part     
        ## detect keydown 
        elif event.type == pygame.KEYDOWN:
            ## if key is right
            if event.key == pygame.K_RIGHT and self.order == True: 
                ## change dialog
                self.index = (self.index+1)%3
                if self.index == 2:
                    self.yn=True
            
            #open the ntu tour     
            elif event.key == pygame.K_UP and self.yn == True:
                self.index = 3
                self.order = False
                self.tour = True
                self.yn = False
            elif event.key == pygame.K_DOWN and self.yn == True:
                self.index = 7
                self.order = False
                self.yn = False
            #close the ntu tour         
            elif event.key == pygame.K_BACKSPACE and self.order == False:
                self.index = 7
                print self.index
                self.tour = False
                  
            ## simulate person appears in another side  
            elif event.key == pygame.K_SPACE: 
                ## text is "your partner is coming.keep smiling,then bug hole will open"
                self.index = 4
                self.index2 = 8
                self.flag=True
                self.order = False
                self.hole = False
                self.tour = False
            elif event.key == pygame.K_RSHIFT and self.flag == True:
                #text is "bug hole will open"
                self.index = 5   
                self.flag = False
                self.order = False
                self.hole = True
            ## esc the experience  
            elif event.key == pygame.K_ESCAPE:              
                #text is "goodbye"
                self.index = 6
                self.hole = False
                self.order = False  
                self.bye = False
            ## restart dialog   
            elif event.key == pygame.K_LSHIFT:
                self.index = 0
                self.order = True
                self.flag = False
                self.hole = False
                self.bye = True

   
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
            if self.hole==False:## hole is not open
                if self.count == 1:
                    ## create thread to get age
                    ageThread(self.frame,"gender","age")
    
            else:
                self.frame,skin=removePimple(self.frame)
                print "hole is open"
        else:
            ### initial variable
            self.somebody = False
            self.count = 0  
            self.index = 0
            self.order = True
            self.flag = False
            self.hole = False
            self.tour = False

        ## debug
        #print "count:"+str(self.count)
        ## frame color into normal mode 
        self.frame=cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)

        ## turn frame into right angle 
        self.frame=np.rot90(self.frame)

        ## turn frame(nd.array) into surface            
        self.frame = pygame.surfarray.make_surface(self.frame)
       
    def on_render(self):
        white = 255,255,255
        red = 255,0,0

        dialog = Dialog()
        ##change text content
        self.text = dialog.load(self.index)
        self.text2 = dialog.load(self.index2)

        ## change text font 
        self.dialog = self.font.render(self.text, False, (255,0,0))
        self.dialog2 = self.font.render(self.text2, False, (255,0,0))

        ## change text color
        self.dialog = textOutline(self.font, self.text, white, red)
        self.dialog2 = textOutline(self.font, self.text2, white, red)
        
        ## render frame on screen 
        self.screen.blit(self.frame,(0,0))

        ## if have person, npc and dialog appear. 
        print age[0]
        if self.somebody == True and age[0]!='o':

            if age[0] < 30.0:
                if gender[0]=="male":
                    self.screen.blit(self.npcFire, self.npcFire_rect)          
                    self.screen.blit(self.dialog, (20,40))
                elif gender[0] =='female':
                    self.screen.blit(self.npcCat, self.npcCat_rect)
                    self.screen.blit(self.dialog, (20,40))
               
            elif age[0] > 30.0:
                self.screen.blit(self.npcOld, self.npcOld_rect)
                self.screen.blit(self.dialog, (20,40))

            if self.flag == True and self.bye == True:
                self.screen.blit(self.dialog2, (20,85))
            if self.hole == True:
                self.screen.blit(self.partner,(600,370))
            if self.tour == True:
                self.screen.blit(self.map,(20,150))

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