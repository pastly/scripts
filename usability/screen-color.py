#!/usr/bin/env python3
from datetime import datetime, time, timedelta
################################################################################
# This script is meant to be used with cron and sct as a way to smoothly change
# between a minimum color temperature and a maximum at various times of day.
#
# If the current time is within two transition ranges, then multiple lines will
# be printed and sct won't like that.
#
# In Gentoo, sct is x11-misc/sct.
#
# It should be used by adding a line like the following to cron
#
# * * * * * env DISPLAY=:0 XAUTHORITY=$HOME/.Xauthority /usr/bin/sct $(/path/to/script.py)
################################################################################

################################################################################
# Customizations here
################################################################################
min_temp = 2000
max_temp = 6500
# Can't transition across midnight, sorry
periods = [
    ('min',time(0,0),time(6,0)),
    ('up',time(6,0),time(9,0)),
    ('max',time(9,0),time(17,0)),
    ('down',time(17,0),time(20,0)),
    ('min',time(20,0),time(23,59)),
]
################################################################################

now = datetime.now().time()

for period in periods:
    direction, start, end = period
    if now >= start and now < end:
        if direction == 'min':
            new_temp = min_temp
        elif direction == 'max':
            new_temp = max_temp
        else:
            temp_diff = max_temp - min_temp
            seconds_since_start = \
                (now.hour - start.hour) * 3600 + \
                (now.minute - start.minute) * 60 + \
                (now.second - start.second)
            total_seconds = \
                (end.hour - start.hour) * 3600 + \
                (end.minute - start.minute) * 60 + \
                (end.second - start.second)
            factor = seconds_since_start / total_seconds
            amount = temp_diff * factor
            if direction == 'up':
                new_temp = min_temp + amount
            elif direction == 'down':
                new_temp = max_temp - amount
        new_temp = int(new_temp)
        print(new_temp)
