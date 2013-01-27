#!/usr/bin/env python2

import pygame
import sys

# Init 
pygame.init()
pygame.joystick.init()
for i in range(pygame.joystick.get_count()):
    joy=pygame.joystick.Joystick(i)
    print "initialize %s" % joy.get_name()
    joy.init()
pygame.display.set_caption("ARCADE!!!!! MOZAFUCKA")

# Load conf
games = [line.split(";") for line in open("burne.config","r")]
print "found %d games" % len(games)

# Colors
class Colors:
    white = (255,255,255)
    black = (0,0,0)
    debug = (255,0,255)
    background = black
    font = white

# Set screen
resolution = (800,600)
screen = pygame.display.set_mode(resolution, pygame.DOUBLEBUF|pygame.HWSURFACE)
spacing = 2
font_size = 50
font_size_progression = 8
left = 100
left_progression = 5
left_init = -50

# Helpers
def blit_text_centered(text,height,left,baseline):
    font = pygame.font.Font("font.ttf", height)
    font_surface = font.render(text, True, Colors.white)
    font_surface_rect = font_surface.get_rect()
    font_surface_rect.height -= 8/50.*height
    font_surface_rect.top += 8/50.*height
    screen.blit(font_surface, (left,baseline-font_surface_rect.height/2.), font_surface_rect)

def visible_games(index,delta=4):
    for delta_index in range(-delta,delta+1):
        current_index = delta_index+index
        current_index %= len(games)
        yield delta_index, games[current_index]

# Main loop
index = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.type == pygame.JOYHATMOTION:
            index -= event.value[1]+event.value[0]*10
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            index += 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            index -= 1

    screen.fill(Colors.background)
    for delta_index, game  in visible_games(index):
        title = game[0]
        this_font_size = font_size-abs(delta_index)*font_size_progression
        blit_text_centered(title,this_font_size,left+left_progression*delta_index*delta_index+left_init*(delta_index==0),resolution[1]/2+(spacing+(font_size+this_font_size)/2)*delta_index)
    pygame.display.flip()
