import time
import tag
import database

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
    database.recordTime(tag.readUUID())

def fallEvent():
    pass
