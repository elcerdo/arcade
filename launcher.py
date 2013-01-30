#!/usr/bin/env python2

import pygame
import sys
import time
import random
import optparse
import os

basedir = "~/git/arcade"
basedir = os.path.expanduser(basedir)

# Option parser
from optparse import OptionParser
parser = optparse.OptionParser()
parser.add_option("-f", "--fullscreen", action="store_true", help="launch interface in full screen", default=False)
(options, args) = parser.parse_args()

# Init 
pygame.init()
pygame.joystick.init()
print "found %d joystick" % pygame.joystick.get_count()
for i in range(pygame.joystick.get_count()):
    joy=pygame.joystick.Joystick(i)
    print "  %s" % joy.get_name()
    joy.init()
pygame.display.set_caption("ARCADE!!!!! MOZAFUCKA")

# Load conf
games = [line.replace("\n","").split(";") for line in open(os.path.join(basedir,"burne.config"),"r")]
print "found %d games" % len(games)

# Check games roms
for game_name,game_rom in games:
    if os.path.isfile(os.path.join(basedir,"roms",game_rom)):
        continue
    print "missing rom for game %s (%s)" % (game_name,game_rom)

# Colors
class Colors:
    white = (255,255,255)
    black = (0,0,0)
    debug = (255,0,255)
    background = black
    font = white

# Set screen
resolution = (1024,768)
screen_flags = pygame.DOUBLEBUF|pygame.HWSURFACE
if options.fullscreen: screen_flags |= pygame.FULLSCREEN
screen = pygame.display.set_mode(resolution, screen_flags)
spacing = 2
font_size = 50
font_size_progression = 8
left = 100
left_progression = 5

# Helpers
def blit_text_centered(text,height,left,baseline,color=Colors.debug,font_name=None):
    font = pygame.font.Font(font_name, int(height))
    font_surface = font.render(text, True, color)
    font_surface_rect = font_surface.get_bounding_rect()
    screen.blit(font_surface, (left,baseline-font_surface_rect.height/2.), font_surface_rect)

def visible_games(index,delta=4):
    for delta_index in range(-delta,delta+1):
        current_index = delta_index+index
        current_index %= len(games)
        yield delta_index, games[current_index]

# Main loop
index_target = 0
index_current = 0
index_direction = 0
index_frame = 0
frame = 0
colors = pygame.image.load(os.path.join(basedir,"colors.png"))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()

        if event.type == pygame.JOYHATMOTION:
            index_direction = event.value[1]+event.value[0]*3
        if event.type == pygame.JOYBUTTONDOWN and event.button==0:
            index_target = random.randint(0,len(games)-1)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            index_direction = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            index_direction = -1
        if event.type == pygame.KEYUP and event.key in (pygame.K_DOWN,pygame.K_UP):
            index_direction = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            index_target = random.randint(0,len(games)-1)

    if index_frame>0:
        index_frame -=1
    elif index_direction:
        index_frame = 5
        index_target += index_direction
    
    index_current += (index_target-index_current)*.05
    if abs(index_current-index_target)<.2: index_current=index_target
    index_residual = index_current-round(index_current)

    screen.fill(Colors.background)
    for delta_index, game  in visible_games(int(round(index_current))):
        delta_index_current = delta_index-index_residual
        title = game[0]
        this_font_size = font_size-abs(delta_index_current)*font_size_progression
        this_left      = left+left_progression*delta_index_current*delta_index_current
        this_baseline  = resolution[1]/2+(spacing+(font_size+this_font_size)/2)*delta_index_current
        this_color     = Colors.white
        if delta_index==0:
            this_color = colors.get_at(((frame*10)%colors.get_width(),0))
        blit_text_centered(title,this_font_size,this_left,this_baseline,this_color,os.path.join(basedir,"font.ttf"))
    blit_text_centered("%d %.2f %.2f %d %d" % (index_target,index_current,index_residual,round(index_current),index_frame),20,10,20)
    pygame.display.flip()

    frame += 1
    
    time.sleep(10e-3)
