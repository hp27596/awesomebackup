#!/usr/bin/env bash

if [ $(awk -F"[][]" '/Left:/ { print $4 }' <(amixer sget Master)) == 'off' ];
then
    status=Muted
else
    status=Available
fi

notify-send -t 2000 "Audio Status: $status" "Volume: $(awk -F"[][]" '/Left:/ { print $2 }' <(amixer sget Master))"
