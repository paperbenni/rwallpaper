#!/usr/bin/env bash

#############################################################
## change wallpaper only once and on wednesdays (my dudes) ##
#############################################################

if date | grep -i 'We' &>/dev/null ||
    date | grep -i 'Mi' &>/dev/null; then
    echo "it is wednesday my dudes"
    if [ -e ~/paperbenni/wallpaper.conf ]; then
        CURRENTDATE=$(date +%F)
        OLDDATE=$(cat ~/paperbenni/wallpaper.conf)
        echo "old $OLDDATE"
        echo "current $CURRENTDATE"
        if [ "$OLDDATE" == "$CURRENTDATE" ]; then
            echo "wallpaper already set"
            exit 0
        else
            date +%F >~/paperbenni/wallpaper.conf
            python3 ~/paperbenni/rwallpaper.py
        fi
    else
        date >~/paperbenni/wallpaper.conf
        python3 ~/paperbenni/rwallpaper.py
    fi
else
    echo "its not wednesday, no new wallpaper for you"
fi

feh --bg-scale ~/paperbenni/wallpaper.jpg
