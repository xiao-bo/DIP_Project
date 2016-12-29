#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from pgu import gui



class NPC:
    def __init__(self,filename,x,y):
        ### initial value
        self.filename=filename
        self.positionX=x
        self.positionY=y
        
    def load(self):
        npc = pygame.image.load(self.filename)
        npc_rect = npc.get_rect()
        npc_rect.x=self.positionX
        npc_rect.y=self.positionY
        return npc,npc_rect
