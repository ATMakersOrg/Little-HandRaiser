# ATMakers HandUp
# Listens to the USB Serial port and responds to incoming strings
# Sets appropriate colors on the DotStar LED

# This program uses the board package to access the Trinket's pin names
# and uses adafruit_dotstar to talk to the LED
# other boards would use the neopixel library instead

import board
import adafruit_dotstar
from time import sleep

import supervisor

# create an object for the dotstar pixel on the Trinket M0
# It's an array because it's a sequence of one pixel
pixels = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=.15)

# this function takes a standard "hex code" for a color and returns
# a tuple of (red, green, blue)
def hex2rgb(hexcode):
    red = int("0x"+hexcode[0:2], 16)
    green = int("0x"+hexcode[2:4], 16)
    blue = int("0x"+hexcode[4:6], 16)
    
    rgb = (red, green, blue)
    # print(rgb)
    return rgb

# When we start up, make the LED black
black = (0, 0, 0)
# the color that's passed in over the text input
targetColor = black

#pos is used for all modes that cycle or progress
#it loops from 0-255 and starts over
pos = 0

#curColor is the color that will be displayed at the end of the main loop
#it is mapped using pos according to the mode
curColor = black


#the mode can be one of 
# solid - just keep the current color
# blink - alternate between black and curColor
# ramp  - transition continuously between black and curColor
# beat* - pulse to a recorded heartbeat intensity
# wheel - change hue around the colorwheel (curColor is ignored)

mode='solid'

# standard function to rotate around the colorwheel
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 85:
        return (int(pos * 3), int(255 - (pos * 3)), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - (pos * 3)), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))


# Map the color to the current value of 'pos' 
# according to the current mode
def runMode():
    global curColor
    global black
    global targetColor
    global pos
    if (mode == 'blink'):
        if(curColor == black):
            curColor = targetColor
        else:
            curColor = black
        sleep(.4)
    #        print('.', end='')
        pixels.fill(curColor)
        pixels.show()   
    elif (mode == 'wheel'):
        pos = (pos + 1) % 255
        pixels.fill(wheel(pos))
        pixels.show()
    elif (mode == 'solid'):
        pixels.fill(targetColor)
        pixels.show()

#We start by turning off pixels
pixels.fill(black)
pixels.show()

#Main Loop
while True:
    #Check to see if there's input available (requires CP 3.3+)
    if (supervisor.runtime.serial_bytes_available):
        #read in text (mode, #RRGGBB, standard color)
        #input() will block until a newline is sent
        inText = input()
        #Sometimes Windows sends an extra (or missing) newline - ignore them
        if(inText == ""):
            continue
        #Process the input text - start with the presets (no #,@,etc)
        #We use startswith to not have to worry about CR vs CR+LF differences
        if (inText.lower().startswith("red")):
            #set the target color to red
            targetColor = (255, 0, 0)
            #and set the mode to solid if we're in a mode that ignores targetColor
            if (mode == "wheel"):
                mode="solid"
        #similar for green, yellow, and black
        elif (inText.lower().startswith("green")):
            targetColor = (0, 255, 0)
            if (mode == "wheel"):
                mode="solid"
        elif (inText.lower().startswith("yellow")):
            targetColor = (200, 200, 0)
            if (mode == "wheel"):
                mode="solid"
        elif (inText.lower().startswith("black")):
            targetColor = (0, 0, 0)
            if (mode == "wheel"):
                mode="solid"
        #Here we're going to change the mode - which starts w/@
        elif (inText.lower().startswith("@")):
            mode= inText[1:]
        #Here we'll change the target color just like above
        #but to any #RedGreenBlue color 
        elif (inText.startswith("#")):
            hexcode = inText[1:]
            targetColor = hex2rgb(hexcode)
            if (mode == "wheel"):
                mode="solid"
        #if we get a command we don't understand, set it to gray
        #we should probably just ignore it but this helps debug
        else:
            targetColor =(50, 50, 50)
            if (mode == "wheel"):
                mode="solid"
    else:
        #If no text availble, update the color according to the mode
        runMode()
        continue

