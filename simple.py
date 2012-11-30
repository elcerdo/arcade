#!/usr/bin/env python2
# coding: utf-8

import pygame
import sys
import numpy
import time
import copy

pygame.init()
pygame.joystick.init()

joystick = None
if pygame.joystick.get_count()>0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print "using joystick '%s'" % joystick.get_name()

font = pygame.font.Font(None,30)
resolution = (800,600)
background_color = (0,0,0)

#screen = pygame.display.set_mode(resolution,pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN)
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

def pairs(elements):
    if len(elements)<2:
        return
    last_element = None
    for element in elements:
        if last_element is None:
            last_element = element
            continue
        yield (last_element,element)
        last_element = element

class Title:
    def __init__(self,xx,yy):
        self.sprites = [pygame.image.load("title_%s.png" % letter) for letter in "arcade"]
        self.rects = [sprite.get_rect() for sprite in self.sprites]
        self.start_time = time.time()
        self.move_to(xx,yy)
    def move_to(self,xx,yy):
        self.rects[0].left = xx
        self.rects[0].top = yy
        for left_rect,right_rect in pairs(self.rects):
            right_rect.left = left_rect.right-39
            right_rect.top  = left_rect.top
        self.rects[-1].left += 8 # correct d upper cut
    def update(self,event):
        pass
    def draw(self):
        time_delta = time.time()-self.start_time
        positions = 5*numpy.cos(2*numpy.pi*(300*time_delta-numpy.array([rect.left for rect in self.rects],dtype=float))/400.)
        #positions = numpy.zeros(len(self.rects))
        for sprite,rect,position in zip(self.sprites,self.rects,positions):
            rect_position = copy.copy(rect)
            rect_position.top -= position
            rect_position.left -= position
            screen.blit(sprite,rect_position)

class Background:
    def __init__(self):
        self.sprites = [pygame.image.load("background_%d.png" % (number+1)) for number in xrange(2)]
        self.rects = [sprite.get_rect() for sprite in self.sprites]
        self.transforms = [numpy.array(((294,0),(-187,213)),dtype=float),numpy.array(((187,66),(40,186)),dtype=float)]
        self.inverses = [numpy.linalg.inv(transform) for transform in self.transforms]
        self.start_time = time.time()
        self.direction = numpy.random.rand()*numpy.pi*2
        self.direction = numpy.array((numpy.cos(self.direction),numpy.sin(self.direction)))
        self.joystick_position = None
    def update(self,event):
        if joystick is None:
            return
        self.joystick_position = numpy.array((joystick.get_axis(0),joystick.get_axis(1)))
    def draw(self):
        motion = 100.*self.direction*(time.time()-self.start_time)
        if self.joystick_position is not None:
            motion = 200.*self.joystick_position
        for sprite,rect,transform,inverse in reversed(zip(self.sprites,self.rects,self.transforms,self.inverses)):
            motion_discrete = numpy.dot(motion,inverse).astype(int)
            motion_real = motion-numpy.dot(motion_discrete,transform)
            motion *= 1.5
            for ii in xrange(-5,5):
                for jj in xrange(-5,5):
                    disp = numpy.dot((jj,ii),transform)+motion_real
                    rect_position = copy.copy(rect)
                    rect_position.left += disp[0]
                    rect_position.top += disp[1]
                    if not screen.get_rect().colliderect(rect_position):
                        continue
                    screen.blit(sprite,rect_position)
                    #pygame.draw.rect(screen,(255,0,0),rect_position,4)
                    #screen.blit(font.render(repr((jj,ii)),True,(0,255,0)),rect_position)

class Lighning:
    def __init__(self,key,tau=.3):
        self.key = key
        self.tau = tau
        self.start_time = time.time()
    def update(self,event):
        if event.type == pygame.KEYDOWN and event.key == self.key: self.start_time = time.time()
    def draw(self):
        value = 255*numpy.exp((self.start_time-time.time())/self.tau)
        screen.fill((value,value,value))

elements = [
    Lighning(pygame.K_a),
    Background(),
    Button("red",pygame.K_a,50,50),
    Button("yellow",pygame.K_q,100,100),
    Button("green",pygame.K_z,150,50),
    Button("blue",pygame.K_s,200,100),
    Button("white",pygame.K_e,250,50),
    Joystick(pygame.K_LEFT,pygame.K_RIGHT,100,150),
    Title(50,300)
    ]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        for element in elements:
            element.update(event)

    for element in elements:
        element.draw()
    pygame.display.flip()

    #time.sleep(10e-3)

