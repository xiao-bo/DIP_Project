#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Hello, world!")

# 文字格式
font = pygame.font.SysFont(None, 80)
# 列出文字（第1引数列出文字、第2引数寫True文字看的比較順、第3引数彩色、第4引数背景顔色） 
hello1 = font.render("Hello,    world!", False, (0,0,0))
hello2 = font.render("Hello, world!", True, (0,0,0))
hello3 = font.render("Hello, world!", True, (255,0,0), (255,255,0))

while True:
  screen.fill((0,0,255))

  # 顕示在印幕上
  screen.blit(hello1, (20,50))
  screen.blit(hello2, (20,150))
  screen.blit(hello3, (20,250))

  pygame.display.update()

  for event in pygame.event.get():
    if event.type == QUIT:
      sys.exit()