#!/usr/bin/env python2
# coding: utf-8

import os
import struct

class State:
    def __init__(self):
        self.initialized = False
        self.buttons = {}
        self.axis = {}
        self.controls = {0x01:self.buttons, 0x02:self.axis}
    def __repr__(self):
        lines = []
        lines.append("initialized=%d" % self.initialized)
        if self.buttons: lines.append("buttons %s" % " ".join("%d=%d" % item for item in self.buttons.items()))
        if self.axis:    lines.append("axis    %s" % " ".join("%d=%d" % item for item in self.axis.items()))
        return "\n".join(lines)
    def parse_event(self,(event_timestamp,event_value,event_type,event_number)):
        event_init = (event_type & 0x80 != 0)
        self.initialized |= not event_init
        assert((event_init and not self.initialized) or (not event_init and self.initialized))
        event_type &= ~0x80
        assert(event_type == 0x01 or event_type == 0x02)
        self.controls[event_type][event_number] = event_value


joystick_device = "/dev/input/js0"
joystick_handle = open(joystick_device,"r")

joystick_struct = struct.Struct("IhBB")
# unsigned int  -> timestamp
# signed short  -> value (axis position)
# unsigned byte -> type (0x01 -> button, 0x02 -> axis, 0x80 -> init)
# unsigend byre -> button/axis number

state = State()
while True:
    event = joystick_struct.unpack_from(joystick_handle.read(joystick_struct.size))
    state.parse_event(event)
    if not state.initialized:
        continue
    print state

