#!/bin/sh

#compton -b --config ~/.config/compton/compton.conf &
nitrogen --restore &
#xsettingsd &
# xfce4-power-manager &
# volumeicon &
nm-applet &
/usr/lib/geoclue-2.0/demos/agent &
gammastep-indicator -m drm &
setxkbmap pl
light-locker --lock-on-suspend &
wal -R
exec expressvpn connect &
