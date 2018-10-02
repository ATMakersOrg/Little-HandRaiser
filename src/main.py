# ATMakers HandUp
# Listens to the USB Serial port and responds to incoming strings
# Sets appropriate colors on the DotStar LED

# This program uses the board package to access the Trinket's pin names
# and uses adafruit_dotstar to talk to the LED
# other boards would use the neopixel library instead

import board
import adafruit_dotstar

# create an object for the dotstar pixel on the Trinket M0
# It's an array because it's a sequence of one pixel
pixels = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 
                                  1, brightness=.75)

# this function takes a standard "hex code" for a color and returns
# a tuple of (red, green, blue)
def hex2rgb(hexcode):
    red = int("0x"+hexcode[0:2], 16)
    green = int("0x"+hexcode[2:4], 16)
    blue = int("0x"+hexcode[4:6], 16)
    rgb = (red, green, blue)
    return rgb

# When we start up, make the LED black
pixels.fill((0, 0, 0))
# and show it
pixels.show()

# main loop
while True:
    # Read the input from the serial connection (over USB)
    # input() will block until a newline is sent
    # Note: in PowerShell you have to send that with backticks (`r`n) 
    # We use lower() the input in case someone sends Black instead of black
    inColor = input().lower()
    # Use startswith() instead of == to skip the newline & make Windows happier
    # Set the right color (don't show it yet)
    if (inColor.startswith("black")):
        pixels.fill((0, 0, 0))
    elif (inColor.startswith("red")):
        pixels.fill((255, 0, 0))
    elif (inColor.startswith("green")):
        pixels.fill((0, 255, 0))
    elif (inColor.startswith("yellow")):
        pixels.fill((255, 255, 0))
    elif (inColor.startswith("#")):
        # In this case, we need to parse the input
        # We remove the # here
        hexcode = inColor[1:]
        pixels.fill(hex2rgb(hexcode))
    else:
        # if we don't understand the message, just go gray
        pixels.fill((50, 50, 50))
    # No matter how we got here, show the color
    pixels.show()
    # That's it - continue the loop.. because of the blocking input()
    # there is no need for a delay