#!/usr/bin/env python2.7

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
font = pygame.font.Font(None, 30)
font2 = pygame.font.Font(None, 20)
font3 = pygame.font.Font(None, 10)

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
        if event.type == pygame.JOYHATMOTION:
            index+=event.value[1]+event.value[0]*10
    screen.fill(background_color)
    screen.blit(font.render(gameList[index%len(gameList)][0], True, white), (100, 300))
    screen.blit(font2.render(gameList[(index-1)%len(gameList)][0], True, white), (100, 200))
    screen.blit(font2.render(gameList[(index+1)%len(gameList)][0], True, white), (100, 400))
    screen.blit(font3.render(gameList[(index-2)%len(gameList)][0], True, white), (100, 100))
    screen.blit(font3.render(gameList[(index+2)%len(gameList)][0], True, white), (100, 500))
#    for i,game in enumerate(gameList):
#        screen.blit(font.render(game[0], True, white), (100, i*100+200))

    pygame.display.flip()
