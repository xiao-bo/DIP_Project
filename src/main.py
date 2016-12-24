#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from pgu import gui

### other class in src
from npc import NPC



class EnterPoint:
    def __init__(self):
        ### initial game's property value
        self.running = True
        self.screen = None
        self.size = self.width, self.height = 840, 600 ## window size
        self.background=255,255,255 ##background color 


        
       
    def on_init(self):
        ## game initail process
        pygame.init()  
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        ## window title
        pygame.display.set_caption("WindowTitle")

        ## load minon NPC
        npcMinion=NPC("../pic/npc_minion.jpeg")
        self.npcMinion,self.npcMinion_rect=npcMinion.load()

        
    def on_event(self, event):

        if event.type == pygame.QUIT:
            self.running = False
        
    def on_loop(self):
       
        pass

    def on_render(self):
        self.screen.fill(self.background)
        self.screen.blit(self.npcMinion, self.npcMinion_rect)
        pygame.display.flip()
        

    def on_cleanup(self):
        pygame.quit()

 
if __name__ == "__main__" :

    Enter = EnterPoint()
    
    if Enter.on_init()==False:
    	Enter.running=False

    while( Enter.running ):
        for event in pygame.event.get():
            Enter.on_event(event)
        Enter.on_loop()
        Enter.on_render()
    Enter.on_cleanup()

    #theStart.on_execute()
