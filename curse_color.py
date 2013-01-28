#!/usr/bin/env python2
# coding: utf-8

import curses
import time

def curse_main(screen):
    curses.curs_set(False)
    curses.init_pair(1,curses.COLOR_YELLOW,curses.COLOR_RED)
    curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_GREEN)
    screen.bkgd("*",curses.color_pair(1))
    screen.border()
    window = screen.subwin(15,20,10,10)
    window.bkgd(" ",curses.color_pair(2))
    window.move(1,0)
    colors = [color for color in curses.__dict__.keys() if "COLOR_" in color and "PAIRS" not in color]
    for kk,color in enumerate(colors):
        curses.init_pair(3+kk,curses.COLOR_BLACK,curses.__dict__[color])
        window.addstr("%s\n" % color,curses.color_pair(3+kk))
    screen.refresh()

    while True:
        char = screen.getch()
        screen.move(1,1)
        screen.addstr("%-10s" % curses.keyname(char),curses.A_BOLD)
        screen.refresh()
        window.move(0,0)
        window.addstr("%-3d" % char,curses.A_UNDERLINE)
        window.refresh()
        if char == ord('q') or char == 27:
            break

    curses.curs_set(True)

curses.wrapper(curse_main)

