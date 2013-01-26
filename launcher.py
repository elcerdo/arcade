#!/usr/bin/env python2

import pygame

pygame.init()
pygame.joystick.init()

for i in range(pygame.joystick.get_count()):
    joy=pygame.joystick.Joystick(i)
    joy.init()
    print joy.get_name()

# Set screen
size = (800,600)
background_color = (0,0,0)
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF|pygame.HWSURFACE)
white = (255,255,255)
spacing = 55
font_size = 50
left = 100

def blit_text_centered(text,height,left,baseline):
    font = pygame.font.Font("font.ttf", height)
    font_surface = font.render(text, True, white)
    screen.blit(font_surface, (left, baseline-height/2))

# Title
pygame.display.set_caption("ARCADE!!!!! MOZAFUCKA")

# Import conf
gameList=[]
for line in open("burne.config","r"):
    gameList.append(line.split(";"))
for i in range(100):
    gameList.append([str(i)])
index=0

# ---Main---

flag = True
while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            flag = False
        if event.type == pygame.JOYHATMOTION:
            index -= event.value[1]+event.value[0]*10
            index %= len(gameList)
    screen.fill(background_color)

    for delta_index in range(-3,4):
        title = gameList[(index+delta_index)%len(gameList)][0]
        this_font_size = font_size-abs(delta_index)*10
        blit_text_centered(title,this_font_size,left,size[1]/2+spacing*delta_index)

    pygame.display.flip()
