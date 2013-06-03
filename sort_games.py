#!/usr/bin/env python2
# coding: utf-8

import datetime

months = [ "janvier", "février", "mars", "avril", "mai", "juin" ]
months = dict(zip(months,map(repr,range(1,len(months)+1))))
print months

date_start = None
name_start = None
database = {}

for line in open("arcade_log",'r'):
    line = line.rstrip("\n")
    splitted = line.split(" ")
    datestr = " ".join([splitted[1],months[splitted[2]]]+splitted[3:5])
    name = " ".join(splitted[6:])
    date = datetime.datetime.strptime(datestr,"%d %m %Y, %H:%M:%S")
    if "QUIT" in name:
        delta = date - date_start
        if name_start not in database:
            database[name_start] = datetime.timedelta()
        database[name_start] += delta
    else:
        date_start = date
        name_start = name

database = database.items()
database.sort(key=lambda x: x[1],reverse=True)
database = database[:20]
print "\n".join("%s %s" % data for data in database)
