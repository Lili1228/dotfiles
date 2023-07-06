#!/bin/sh
if [ -x /bin/doas ]; then
	_SUDO=doas
else
	_SUDO=sudo
fi
. /etc/os-release
case "$ID" in
	alpine)
		$_SUDO apk add feh gammastep mpv neovim py3-psutil py3-xlib qtile
		;;
	arch|artix)
		#           wallpaper, night light, media player, editor,  notifications,    CPU usage, screen detection
    	$_SUDO pacman -Syu feh gammastep-indicator mpv neovim-qt python-dbus-next python-psutil python-xlib qtile
		;;
	debian|devuan|linuxmint|ubuntu)
		# tested on Devuan 4.0 (Debian 11) and Mint 21 Xfce (Ubuntu 22.04)
		$_SUDO apt update && $_SUDO apt install feh gammastep mpv neovim-qt python3-cairocffi python3-pip python3-psutil python3-xlib
		_DEBVER="$(cat /etc/debian_version)"
		if [ "$_DEBVER" != "${_DEBVER#11}" ]; then
			# python3-xcffib is too old for later versions
			$_SUDO pip3 install qtile==0.18.0
		elif [ "$VERSION_CODENAME" = jammy ] || [ "$UBUNTU_CODENAME" = jammy ]; then
			# doesn't have python3-dbus-next in repo
			$_SUDO pip3 install dbus-next qtile
		else
			$_SUDO apt install python3-dbus-next
			$_SUDO pip3 install qtile
		fi
		_DEBVER=
		;;
	fedora)
		$_SUDO dnf install feh gammastep-indicator mpv neovim-qt python3-cairocffi python3-dbus-next python3-pip python3-psutil python3-xlib
		$_SUDO pip3 install qtile
		;;
	*)
		echo Unsupported distro.
		;;
esac
_SUDO=
