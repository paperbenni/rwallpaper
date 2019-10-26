#!/bin/bash
if (echo "$1" | egrep -o 'imgur.com/a/[a-z,A-Z]*'); then
    URL=$(curl $1 | grep '"hash"' |
        egrep -o '"hash":"[a-z,A-Z]{,10}"' |
        egrep -o ':".*"' | egrep -o '[^:"]*' |
        sort -u | shuf | head -1)
    echo "url $URL"
    wget -o wallpaper.png "https://i.imgur.com/$URL.png"
fi
