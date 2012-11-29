#!/usr/bin/env python2
# coding: utf-8

import Image, ImageDraw, ImageColor

tile = Image.new("RGBA",(512,512),(0,0,0,0))
painter = ImageDraw.Draw(tile)

def draw_rectangle(level,xx,yy,line_width=6):
    size = (tile.size[0]/2**level,tile.size[1]/2**level)
    point0 = (size[0]*xx,size[1]*yy)
    point1 = (size[0]*(xx+1)-1,size[1]*(yy+1)-1)
    painter.rectangle((point0,point1),fill=(70,0,0))
    for kk in xrange(line_width):
        painter.line((point0[0]+kk,point0[1]+kk,point1[0]-kk,point0[1]+kk),fill=(60,0,0))
        painter.line((point0[0]+kk,point0[1]+kk,point0[0]+kk,point1[1]-kk),fill=(50,0,0))
        painter.line((point0[0]+kk,point1[1]-kk,point1[0]-kk,point1[1]-kk),fill=(40,0,0))
        painter.line((point1[0]-kk,point0[1]+kk+1,point1[0]-kk,point1[1]-kk),fill=(30,0,0))

draw_rectangle(1,0,0)
draw_rectangle(1,1,1)
draw_rectangle(2,2,1)
draw_rectangle(3,4,1)
draw_rectangle(3,2,4)
draw_rectangle(3,3,4)
draw_rectangle(4,7,10)

tile.save("tile.png")
