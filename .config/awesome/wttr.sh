#!/bin/sh

curl -s wttr.in/Hanoi\?format="%l+%c%t+%f" | awk -F ', |' '!($2="")' | tr -d , | tr -s " "
