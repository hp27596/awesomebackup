#!/bin/bash

# Simple script to handle a DIY shutdown menu. When run you should see a bunch of options (shutdown, reboot etc.)
#
# Requirements:
# - dmenu
# - systemd

chosen=$(echo -e "0. Screen Off\n1. Logout\n2. Shutdown\n3. Reboot\n4. Suspend\n5. Lockscreen" | dmenu -i -l 10 -p "Choose Action:")
if [[ $chosen = "0. Screen Off" ]]; then
	xset dpms force off
elif [[ $chosen = "4. Suspend" ]]; then
	systemctl suspend
elif [[ $chosen = "1. Logout" ]]; then
	echo 'shutdown()' | qtile shell
elif [[ $chosen = "2. Shutdown" ]]; then
	systemctl poweroff
elif [[ $chosen = "3. Reboot" ]]; then
	systemctl reboot
elif [[ $chosen = "5. Lockscreen" ]]; then
	systemctl reboot
fi
