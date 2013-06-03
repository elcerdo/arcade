#!/usr/bin/env python2
# coding: utf-8

import pygame
import sys

pygame.init()
pygame.joystick.init()
print "found %d joystick" % pygame.joystick.get_count()
for i in range(pygame.joystick.get_count()):
    joy=pygame.joystick.Joystick(i)
    print "  %s" % joy.get_name()
    joy.init()

while True:
    for event in pygame.event.get():
        if event.type==pygame.JOYBUTTONDOWN and event.joy==0 and event.button==7:
            print "KILL"
            sys.exit()

