#!/usr/bin/env python2

import pygame
import sys
import time
import random
import optparse
import os
import time

basedir = "~/git/arcade"
basedir = os.path.expanduser(basedir)

# Option parser
from optparse import OptionParser
parser = optparse.OptionParser()
parser.add_option("-f", "--fullscreen", action="store_true", help="launch interface in full screen", default=False)
parser.add_option("-d", "--debug", action="store_true", help="activate debug display", default=False)
parser.add_option("-c", "--config-file", dest="config", help="load config from FILE", metavar="FILE", default="good.config")
parser.add_option("-i", "--index", dest="index", help="start interface on game INDEX", metavar="INDEX", type="int", default=0)
(options, args) = parser.parse_args()

# Init 
pygame.init()
pygame.mixer.init()
pygame.joystick.init()
print "found %d joystick" % pygame.joystick.get_count()
for i in range(pygame.joystick.get_count()):
    joy=pygame.joystick.Joystick(i)
    print "  %s" % joy.get_name()
    joy.init()
pygame.display.set_caption("ARCADE!!!!! MOZAFUCKA")
pygame.mouse.set_visible(False)

# Load sounds
class SoundFX:
    channel = pygame.mixer.Channel(0)
    move = pygame.mixer.Sound(os.path.join(basedir,"Powerup.wav"))
    select = pygame.mixer.Sound(os.path.join(basedir,"Powerup2.wav"))

# Load conf
games = [line.replace("\n","").split(";") for line in open(os.path.join(basedir,options.config),"r")]
print "found %d games" % len(games)

# Check games roms
try:
    for game_name,game_rom in games:
        if os.path.isfile(os.path.join(basedir,"roms",game_rom)):
            continue
        print "missing rom for game %s (%s)" % (game_name,game_rom)
except ValueError:
    print "unable to check rom file"

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
left = 75
left_progression = 5

# Helpers
def blit_text_centered(text,height,left,baseline,color=Colors.debug,font_name=None):
    font = pygame.font.Font(font_name, int(height))
    font_surface = font.render(text, True, color)
    font_surface_rect = font_surface.get_bounding_rect()
    screen.blit(font_surface, (left,baseline-font_surface_rect.height/2.), font_surface_rect)

def blit_text_multiline(text,height,left,baseline,color=Colors.debug,font_name=None):
    font = pygame.font.Font(font_name, int(height))
    for kk,line in enumerate(text.split("\n")):
        font_surface = font.render(line, True, color)
        screen.blit(font_surface, (left,baseline+kk*height))

def visible_games(index,delta=4):
    for delta_index in range(-delta,delta+1):
        current_index = delta_index+index
        current_index %= len(games)
        yield delta_index, games[current_index]

def launch_game(index):
    SoundFX.channel.play(SoundFX.select)
    index_modulo = index % len(games)
    game = games[index_modulo]
    print "INDEX=%d" % index_modulo
    print "TITLE=%s" % game[0]
    if len(game)==3 and "sdlmame" in game[1]:
        print "COMMAND=sdlmame %s" % game[2]
    while SoundFX.channel.get_busy():
        time.sleep(1e-3)
    sys.exit()

# Main loop
index_target = options.index
index_target %= len(games)
index_current = index_target
index_current_last = index_target
index_direction = 0
index_frame = 0
frame = 0
time_start = time.time()
colors = pygame.image.load(os.path.join(basedir,"colors.png"))
joystick_last = -1
events = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(1)
        if event.type == pygame.KEYDOWN and event.scancode == 124:
            sys.exit(1)

        if event.type == pygame.JOYHATMOTION:
            index_direction = event.value[1]+event.value[0]*3
            joystick_last = event.joy
        if event.type == pygame.JOYBUTTONDOWN and event.button in [5]:
            index_target = random.randint(0,len(games)-1)
            joystick_last = event.joy
        if event.type == pygame.JOYBUTTONDOWN and event.button in [0,1,2,3,4]:
            launch_game(int(round(index_current)))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            index_direction = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            index_direction = -1
        if event.type == pygame.KEYUP and event.key in (pygame.K_DOWN,pygame.K_UP):
            index_direction = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            index_target = random.randint(0,len(games)-1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            launch_game(int(round(index_current)))

        if options.debug:
            events.append("%s" % event)
            while len(events)>5:
                events.pop(0)

    if index_frame>0:
        index_frame -=1
    elif index_direction:
        index_frame = 5
        index_target += index_direction
    
    index_current += (index_target-index_current)*.05
    if abs(index_current-index_target)<.2: index_current=index_target
    index_residual = index_current-round(index_current)

    if int(round(index_current))!=index_current_last:
        index_current_last = int(round(index_current))
        SoundFX.channel.play(SoundFX.move)

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

    frame += 1
    time_last = time.time()
    
    if options.debug:
        blit_text_multiline("INDEX\ntarget=%d\ncurrent=%.2f\nresidual=%.2f\ncurrent_round=%d\nframe=%d" % (index_target,index_current,index_residual,round(index_current),index_frame),20,10,10)
        blit_text_multiline("JOYSTICK\ncount=%d\nlast=%d\n\nframe=%d\nfps=%.1f" % (pygame.joystick.get_count(),joystick_last,frame,frame/(time_last-time_start)),20,140,10)
        blit_text_multiline("EVENT\n"+"\n".join(events),20,270,10)
    pygame.display.flip()

    time.sleep(10e-3)
