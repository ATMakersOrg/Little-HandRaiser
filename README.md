# Little-HandRaiser
Software to turn the Adafruit Trinket M0 into a notification tool to notify a teacher when a students wants their attention

The approach used on this device is to have the Trinket listen for messages over it's USB Serial port and have the computer it is attached to 
send short messages to change it's behavior.  This version accepts four words ("black", "red", "yellow", "green") as well as a color prefixed by a 
hash symbol "#FF00FF" identifying a color via Red/Green/Blue values.

This is under active development and is limited due to the lack of a non-blocking (or at least polling) input mechanism for the USB port.

Please join us on the ATMakers Facebook Group to help with this and other projects
https://www.facebook.com/groups/ATMakers/
