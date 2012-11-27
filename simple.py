#!/usr/bin/env python2
# coding: utf-8

import pygame
import sys
import numpy

pygame.init()

resolution = (800,600)
background_color = (0,0,0)

screen = pygame.display.set_mode(resolution)

class Button:
    def __init__(self,color,key,xx,yy):
        self.key = key
        self.state = False
        self.up_sprite = pygame.image.load("%s_up.png" % color)
        self.down_sprite = pygame.image.load("%s_down.png" % color)
        self.up_rect = self.up_sprite.get_rect()
        self.down_rect = self.down_sprite.get_rect()
        self.move_to(xx,yy)
    def move_to(self,xx,yy):
        self.up_rect.left = xx
        self.down_rect.left = xx
        self.up_rect.top = yy
        self.down_rect.top = yy+self.up_rect.height-self.down_rect.height
    def update(self,event):
        if event.type == pygame.KEYDOWN and event.key == self.key: self.state = True
        if event.type == pygame.KEYUP and event.key == self.key: self.state = False
    def draw(self):
        if self.state: screen.blit(self.down_sprite,self.down_rect)
        else: screen.blit(self.up_sprite,self.up_rect)

buttons = [
    Button("red",pygame.K_a,50,50),
    Button("yellow",pygame.K_q,100,100),
    Button("green",pygame.K_z,150,50),
    Button("blue",pygame.K_s,200,100),
    Button("white",pygame.K_e,250,50)
    ]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        for button in buttons:
            button.update(event)

    screen.fill((0,0,0))
    for button in buttons:
        button.draw()
    pygame.display.flip()

