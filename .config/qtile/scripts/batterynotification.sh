#!/usr/bin/env bash

kill $(pgrep -f batterynotification.sh | grep -v ^$$$)

full_notified=false
low_notified=false
empty_notified=false
last_state='Discharging'

while true
do
    battery_state=`acpi -b | awk '{print $3}' | cut -d ',' -f 1`
    battery_level=`acpi -b | awk '{print $4}' | rev | cut -c 3- | rev`

    if [ $full_notified = false ] && [ $battery_level -ge 90 ] && [ $battery_state = 'Charging' ]; then
        notify-send -t 2000 "Battery Full"
        full_notified=true
    elif [ $low_notified = false ] && [ $battery_level -le 20 ] && [ $battery_state = 'Discharging' ]; then
        notify-send -t 2000 "Battery Low"
        low_notified=true
    elif [ $empty_notified = false ] && [ $battery_level -le 10 ] && [ $battery_state = 'Discharging' ]; then
        notify-send -t 2000 --urgency=CRITICAL "Battery less than 10%"
        empty_notified=true
    fi

    if [ $battery_level -lt 89 ]; then
        full_notified=false
    elif [ $battery_level -gt 21 ]; then
        low_notified=false
    elif [ $battery_level -gt 11 ]; then
        empty_notified=false
    fi

    if [[ $last_state != $battery_state ]]; then
        if [[ $battery_state = 'Discharging' ]]; then
            last_state=$battery_state
            notify-send -t 2000 "Battery discharging"
        elif [[ $battery_state = 'Not' ]]; then
            last_state=$battery_state
            notify-send -t 2000 "Battery plugged in, not charging"
        elif [[ $battery_state = 'Charging' ]]; then
            last_state=$battery_state
            notify-send -t 2000 "Battery charging"
        fi
    fi
    sleep 5
done
