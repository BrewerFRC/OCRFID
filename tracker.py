import time
import tag
import database

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

def riseEvent():
    if enabled:
        database.recordTime(tag.readUUID())

def fallEvent():
    pass
