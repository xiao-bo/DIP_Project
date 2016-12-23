#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from pgu import gui
class NPC:
    def __init__(self):
        ### initial value
        self.running = True
        self.screen = None
        self.size = self.width, self.height = 840, 600
        self.background=255,255,255
        self.hello=None
        self.text="hello"

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True

        ## load npc
        self.npc_minion = pygame.image.load("../pic/npc_minion.jpeg")
        self.npc_minion_rect = self.npc_minion.get_rect()
        self.npc_minion_rect.x=500
        self.npc_minion_rect.y=200

        ##
        font = pygame.font.SysFont(None, 80)
        self.hello = font.render(self.text, False, (0,0,0))
        pygame.display.set_caption("WindowTitle")
    def on_event(self, event):

        if event.type == pygame.QUIT:
            self.running = False
        elif event.type==pygame.MOUSEBUTTONUP:
            self.text="goodbye"
        elif event.type==pygame.MOUSEBUTTONDOWN:
            self.text="hello"

    def on_loop(self):
        font = pygame.font.SysFont(None, 80)
        self.hello = font.render(self.text, False, (0,0,0))
        pass

    def on_render(self):
        self.screen.fill(self.background)
        self.screen.blit(self.npc_minion, self.npc_minion_rect)
        self.screen.blit(self.hello, (20,300))
        pygame.display.flip()
        

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self.running = False
 
        while( self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theNPC = NPC()
    theNPC.on_execute()