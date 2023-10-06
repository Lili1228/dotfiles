#!/bin/sh
/usr/lib/geoclue-2.0/demos/agent &
nm-applet &
if [ "$XDG_SESSION_TYPE" = 'x11' ]; then
    setxkbmap pl
    wal -i Pictures/we0w4aea87f51.jpg
else
    swaybg -i Pictures/we0w4aea87f51.jpg &
    way-displays &
fi
# xfce4-power-manager --daemon
exec gammastep-indicator &
