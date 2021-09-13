#!/bin/sh
if [ -x /bin/pacman ]; then
    pacman -Syu feh gammastep-indicator mpv python-psutil qtile xfce4-clipman
fi
