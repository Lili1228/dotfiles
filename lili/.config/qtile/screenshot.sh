#!/bin/sh
_path="/tmp/$(date +%xT%X).png"
case $1 in
	ctrl)
		# Take a screenshot of the selected region
		grim -g "$(slurp)" - | wl-copy
		;;
	alt)
		# Take a screenshot of the focused window
		pos=$(qtile cmd-obj -o window -f get_position | awk '{ print $1" "$2}' | tr -dc '0-9 ')
		xpos=$(echo "$pos" | awk '{ print $1 }')
		ypos=$(echo "$pos" | awk '{ print $2 }')
		size=$(qtile cmd-obj -o window -f get_size | awk '{ print $1" "$2}' | tr -dc '0-9 ')
		xsize=$(echo "$size" | awk '{ print $1 }')
		ysize=$(echo "$size" | awk '{ print $2 }')
		grim -g "$xpos"",""$ypos $xsize""x""$ysize" - | wl-copy
		;;
	*)
		# Take a screenshot of the currently focused output and save it into screenshots
		grim -o "$(qtile cmd-obj -o core -f eval -a "self._current_output.wlr_output.name" | awk -F"['']" '/,/{print $2}')" - | wl-copy
		;;
esac
