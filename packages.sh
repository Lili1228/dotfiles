#!/bin/sh
if [ -x /bin/pacman ]; then
    sudo pacman -Syu feh gammastep-indicator mpv python-dbus-next python-psutil qtile
fi
