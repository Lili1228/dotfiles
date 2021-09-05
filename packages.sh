#!/bin/sh
if [ -x /bin/pacman ]; then
    pacman -Syu feh gammastep-indicator mpv python-psutil qtile
fi
