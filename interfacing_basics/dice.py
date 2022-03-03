#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import random

# Define a class to handle displaying a number on the LED array.
class led_display:
    # Define LED pins. There are a number of ways to do this
    # I am doing it this way because I want it to be readable, and meaningful.
    lp1 = 13 # pin for LED 1
    lp2 = 16
    lp3 = 19
    lp4 = 20
    lp5 = 26
    lp6 = 21
    lp = [lp1, lp2, lp3, lp4, lp5, lp6] # An array of all LED pins in LED order.

    # Class constructor function.
    # Initialize essential settings.
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for l in self.lp:
            GPIO.setup(l, GPIO.OUT)

    # Class Destructor function.
    # Do things that should be done with stopping.
    def __del__(self):
        sleep(2)
        GPIO.cleanup()
        return

    # Display function: Illuminate n LEDs based upon a number provided.
    def display(self, number):
        if number < 0:
            return False
        
        for i in range(0, len(self.lp)):
            n = i + 1
            if n <= number:
                GPIO.output(self.lp[i], 1)
            else:
                GPIO.output(self.lp[i], 0)

    # An animation to indicate something is happening.
    def interlude(self):
        # Clear all of the LEDs quickly.
        for l in self.lp:
            GPIO.output(l, 0)
        sleep(0.100)
        # Turn on each LED with a small pause between each.
        for l in self.lp:
            GPIO.output(l, 1)
            sleep(0.020)
        # Turn off each LED with a small pause between each.
        for l in self.lp:
            GPIO.output(l, 0)
            sleep(0.020)

button_pin = 22
press_count = 0

def roll_dice():
    led_display.interlude()
    press_count = press_count + 1
    roll = random.randint(1, 6)
    led_display.display(roll)
    print("Button Pressed {} times. New roll of: {}.".format(press_count, roll))

# Start monitoring for, and responding to, a button press.
def start(button_pin, led_display):
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=roll_dice, bouncetime=100)

led_display = led_display()
start(button_pin, led_display)
