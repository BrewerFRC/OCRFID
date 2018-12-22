import RPi.GPIO as GPIO, MFRC522, time, threading, database
from threading import Timer

ENABLED = True      #Setting false will kill the tag update thread.

readerThread = None #The tag reader update thread.
uuid = None         #The uuid of the current tag.

tracking = True     #Whether or not hardware changes will execute database updates.
rising = False      #Whether or not the last update was a rising edge.
falling = False     #Whether or not the last update was a falling edge.

def update():
    """Updates meta and status light to align with current hardware state.
    """
    global rising, falling
    if uuid:
        if not rising:
            riseEvent()
            rising = True
        falling = False
    else:
        if not falling:
            fallEvent()
            falling = True
        rising = False

def readUUID():
    """The currently present tag uuid.  None if no tag is present.
    """
    return uuid

def resetSignIn():
    """Turns off the sign-in status light.
    """
    GPIO.output(8, GPIO.LOW)

def riseEvent():
    """Handler function called when a tag becomes present after no tag was available.
    """
    if tracking:
        GPIO.output(8, GPIO.HIGH)
        database.recordTime(uuid)
        Timer(1, resetSignIn, ()).start()

def fallEvent():
    """Handler function called when a tag is removed.
    """
    pass

class Reader(threading.Thread):
    def run(self):
        global uuid, ENABLED
        reader = MFRC522.MFRC522()
        while ENABLED:
            (status, tagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
            if status == reader.MI_OK:
                (status, uid) = reader.MFRC522_Anticoll()
                if status == reader.MI_OK:
                    uuid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                else:
                    uuid = None
            else:
                uuid = None
        GPIO.cleanup()

def start():
    """Sets up the necessary hardware and processes for reading tag UUIDs.
    Only call this once.
    """
    global readerThread

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT)
    GPIO.output(8, GPIO.LOW)
    readerThread = Reader()
    readerThread.start()
