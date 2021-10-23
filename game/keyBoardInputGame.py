import RPi.GPIO as GPIO
import time
import sys
print(str(__file__))
sys.path.append(str(__file__).replace("/tests/keyBoardInputGame.py", "/"))
print(sys.path)
from keyBoardInput import keyBoardInput
from random import choice

"""
Randem LED (general output) is lit up on rasberrypi randemly from the list of valid GPIO numbers.
User must click the correct button which corresponds to the lit LED using a keypad.
Once the correct key is pressed, a new randem LED is lit.
"""

GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

LEDs =       [ 25, 26, 12, 16, 24, 20, 23, 21, 18]
characters = ["1","2","3","4","5","6","7","8","9"]
LEDmap = {}
for i in range(len(LEDs)):
    char = characters[i]
    led = LEDs[i]
    LEDmap[char]=led

for led in LEDs:
    GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)

light_port = LEDs[0]

def randem_led():
    global light_port
    global LEDs
    GPIO.output(light_port, GPIO.LOW)
    light_port = choice(LEDs)
    GPIO.output(light_port, GPIO.HIGH)
    print("led port: " + str(light_port))

def main():
    global light_port
    global LEDmap

    c0 = 19
    c1 = 13
    c2 = 6
    c3 = 5
    r3 = 4
    r2 = 17
    r1 = 27
    r0 = 22
    keyBoard = keyBoardInput(r0, r1, r2, r3, c0, c1, c2, c3)

    input = ""
    randem_led()
    while(input[-2:] != "DD"):
        if(keyBoard.wasKeyPressed()):
            char = keyBoard.getInput()
            print("map: " + str(LEDmap))
            input += char
            if (char in LEDmap and LEDmap[char] == light_port):
                randem_led()
            print(input + "\n")
    
    GPIO.output(light_port, GPIO.LOW)
    print("Exited test")


main()