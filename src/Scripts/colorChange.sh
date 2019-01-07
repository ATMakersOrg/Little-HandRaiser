#!/bin/bash
# The line above has to be bash (not sh) because we're using the printf builtin

#First, get the name of the most recent Adafruit serial device connected
#Conveniently linux hels us by grouping them by manufacturer id


DEVNAME=`ls -1t /dev/serial/by-id/ | grep Adafruit | head -1`

if [[ -z "$DEVNAME" ]]; then
    echo "No Adafruit Device Found"
    exit
fi

FULLDEVPATH=/dev/serial/by-id/$DEVNAME

#Comment this to remove debug text
echo "Found recent Adafruit device at $FULLDEVPATH"

text=$@

if [[ -z "$text" ]]; then
    echo "Usage: colorChange.sh <Text To Send>"
    exit
fi

#Comment this to remove debug text
echo "Sending text '$text' to serial device"

printf "$text\r" > $FULLDEVPATH ; head -1 $FULLDEVPATH > /dev/null