#!/bin/sh
/usr/lib/geoclue-2.0/demos/agent &
nm-applet &
setxkbmap pl
wal -i we0w4aea87f51.jpg
xfce4-power-manager --daemon
gammastep-indicator &
exec gnome-keyring-daemon --start
