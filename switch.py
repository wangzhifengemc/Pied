#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

LedPin = 26    # pin26

def Switch_setup():
#	GPIO.setmode(GPIO.BCM)       # Numbers pins by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
	GPIO.output(LedPin, GPIO.HIGH) # Set pin to high(+3.3V) to off the led

def Switch(Ins):
    Switch_setup()
    if Ins==0:
        GPIO.output(LedPin, GPIO.LOW)  # led on
    if Ins==1:
        GPIO.output(LedPin, GPIO.HIGH) # led off

def Switch_destroy():
    GPIO.output(LedPin, GPIO.HIGH)     # led off

if __name__ == '__main__':     # Program start from here
    GPIO.setmode(GPIO.BCM)       # Numbers pins by physical location
    Switch_setup()
    try:
        while True:
            print '...led on'
            Switch(0)  # led on
            time.sleep(0.5)
            print 'led off...'
            Switch(1) # led off
            time.sleep(0.5)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        Switch_destroy()
        GPIO.cleanup()


