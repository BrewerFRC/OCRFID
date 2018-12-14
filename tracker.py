import time, tag, database, RPi.GPIO as GPIO
from threading import Timer

GPIO.setup(8, GPIO.OUT)
GPIO.output(8, GPIO.LOW)

enabled = True
rising = False
falling = False

def update():
    global rising
    global falling
    if tag.readUUID():
        if not rising:
            riseEvent()
            rising = True
        falling = False
    else:
        if not falling:
            fallEvent()
            falling = True
        rising = False

def resetSignIn():
    GPIO.output(8, GPIO.LOW)

def riseEvent():
    if enabled:
        GPIO.output(8, GPIO.HIGH)
        database.recordTime(tag.readUUID())
        Timer(1, resetSignIn, ()).start()

def fallEvent():
    pass
