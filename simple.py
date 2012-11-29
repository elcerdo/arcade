#!/usr/bin/env python2
# coding: utf-8

import pygame
import sys
import numpy

pygame.init()

resolution = (800,600)
background_color = (0,0,0)

screen = pygame.display.set_mode(resolution,pygame.DOUBLEBUF|pygame.HWSURFACE)

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
        self.down_rect.bottom = self.up_rect.bottom
    def update(self,event):
        if event.type == pygame.KEYDOWN and event.key == self.key: self.state = True
        if event.type == pygame.KEYUP and event.key == self.key: self.state = False
    def draw(self):
        if self.state:
            screen.blit(self.down_sprite,self.down_rect)
            return
        screen.blit(self.up_sprite,self.up_rect)

class Joystick:
    def __init__(self,key_left,key_right,xx,yy):
        self.key_right = key_right
        self.key_left = key_left
        self.state_right = False
        self.state_left = False
        self.middle_sprite = pygame.image.load("joystick_middle.png")
        self.right_sprite = pygame.image.load("joystick_right.png")
        self.left_sprite = pygame.image.load("joystick_left.png")
        self.middle_rect = self.middle_sprite.get_rect()
        self.right_rect = self.right_sprite.get_rect()
        self.left_rect = self.left_sprite.get_rect()
        self.move_to(xx,yy)
    def move_to(self,xx,yy):
        self.middle_rect.left = xx
        self.right_rect.left = xx
        self.left_rect.right = self.middle_rect.right
        self.middle_rect.top = yy
        self.right_rect.bottom = self.middle_rect.bottom
        self.left_rect.bottom = self.middle_rect.bottom
    def update(self,event):
        if event.type == pygame.KEYDOWN and event.key == self.key_right: self.state_right = True
        if event.type == pygame.KEYUP and event.key == self.key_right: self.state_right = False
        if event.type == pygame.KEYDOWN and event.key == self.key_left: self.state_left = True
        if event.type == pygame.KEYUP and event.key == self.key_left: self.state_left = False
    def draw(self):
        if self.state_right and not self.state_left:
            screen.blit(self.right_sprite,self.right_rect)
            return
        if self.state_left and not self.state_right:
            screen.blit(self.left_sprite,self.left_rect)
            return
        screen.blit(self.middle_sprite,self.middle_rect)

buttons = [
    Button("red",pygame.K_a,50,50),
    Button("yellow",pygame.K_q,100,100),
    Button("green",pygame.K_z,150,50),
    Button("blue",pygame.K_s,200,100),
    Button("white",pygame.K_e,250,50),
    Joystick(pygame.K_LEFT,pygame.K_RIGHT,100,150)
    ]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        for button in buttons:
            button.update(event)

    screen.fill((0,255,0))
    for button in buttons:
        button.draw()
    pygame.display.flip()

