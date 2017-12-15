import time
import tag
import database

rising = False
falling = False

def update():
    if tag.readUUID():
        if not rising:
            rising()
            rising = True
        falling = False
    else:
        if not falling:
            falling()
            falling = True
        rising = False

def rising():
    database.recordTime(tag.readUUID())

def falling():
    pass
