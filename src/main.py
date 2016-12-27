#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

### import other class in src
from npc import NPC
from dialog import Dialog




class EnterPoint:
    def __init__(self):
        ### initial game's property value
        self.running = True
        self.screen = None

        ## window size
        self.size = self.width, self.height = 840, 600 

        ##background color 
        self.background = 255,255,255 

        ## dialog index
    	self.index = 0
    	
    def on_init(self):
        ## game initail process
        pygame.init()  
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        ## window title
        pygame.display.set_caption("WindowTitle")

        ## load minon NPC
        npcMinion = NPC("../pic/npc_minion.jpeg")
        self.npcMinion,self.npcMinion_rect=npcMinion.load()

        ## init dialog font 
        self.font = pygame.font.SysFont(None, 80)

    def on_event(self, event):
        dialog = Dialog()
        self.text = dialog.load(self.index)

        if event.type == pygame.QUIT:
            self.running = False
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
            ## restart dialog  
            elif event.key == pygame.K_ESCAPE:
            	##
            	self.index = 0

        self.text = dialog.load(self.index)
        self.dialog = self.font.render(self.text, False, (0,0,0))

    def on_loop(self):
    	## FaceDetect put it.
        
        pass

    def on_render(self):
        ## fill background color
        self.screen.fill(self.background)

        ## render npc
        self.screen.blit(self.npcMinion, self.npcMinion_rect)

        ##render dialog
        self.screen.blit(self.dialog, (20,300))
        pygame.display.flip()
        

    def on_cleanup(self):
        
        pygame.quit()

 
if __name__ == "__main__" :

    Enter = EnterPoint()
    
    if Enter.on_init() == False:
    	Enter.running = False

    while( Enter.running ):
        for event in pygame.event.get():
            Enter.on_event(event)
        Enter.on_loop()
        Enter.on_render()
    Enter.on_cleanup()

