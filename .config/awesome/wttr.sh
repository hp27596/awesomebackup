#!/bin/sh

curl -s wttr.in/\?format="%l+%c%t+%f" | awk -F ', | ' '!($2="")' | tr -d , | tr -s " "

