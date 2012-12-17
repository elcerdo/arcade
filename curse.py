#!/usr/bin/env python2
# coding: utf-8

import curses
import time

def curse_main(screen):
    curses.curs_set(False)

    for color in xrange(curses.COLORS):
        curses.init_pair(color+1,curses.COLOR_BLACK,color)

    pad = curses.newpad(48,24)
    pad.bkgd("/")
    height,width = pad.getmaxyx()
    for yy in xrange(height):
        for xx in xrange(width):
            color = abs(xx)+abs(yy)
            color /= 3
            color %= 8
            pad.chgat(yy,xx,1,curses.color_pair(color+1)+curses.A_REVERSE)

    main = curses.newwin(20,20,2,2)
    main.border()
    main.bkgd("*",curses.color_pair(0))

    kk = -1
    while True:
        pad.refresh(kk,0,0,0,23,23)
        kk += 1
        kk %= 24
        main.redrawwin()
        main.refresh()

        char = screen.getch()
        if char == ord('q') or char == 27:
            break

    curses.curs_set(True)

curses.wrapper(curse_main)

