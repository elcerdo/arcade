#!/usr/bin/env python2

import pygame
import sys
import time

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
def blit_text_centered(text,height,left,baseline,color):
    font = pygame.font.Font("font.ttf", height)
    font_surface = font.render(text, True, color)
    font_surface_rect = font_surface.get_bounding_rect()
    screen.blit(font_surface, (left,baseline-font_surface_rect.height/2.), font_surface_rect)

def visible_games(index,delta=4):
    for delta_index in range(-delta,delta+1):
        current_index = delta_index+index
        current_index %= len(games)
        yield delta_index, games[current_index]

# Main loop
index = 0
frame = 0
colors = pygame.image.load("colors.png")
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
        this_left      = left+left_progression*delta_index*delta_index+left_init*(delta_index==0)
        this_baseline  = resolution[1]/2+(spacing+(font_size+this_font_size)/2)*delta_index
        this_color     = Colors.white
        if delta_index==0:
            this_color = colors.get_at(((frame*10)%colors.get_width(),0))
        blit_text_centered(title,this_font_size,this_left,this_baseline,this_color)
    pygame.display.flip()

    frame += 1
    
    time.sleep(10e-3)
