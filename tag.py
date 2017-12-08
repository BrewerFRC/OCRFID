import RPi.GPIO as GPIO
import MFRC522
import time

ENABLED = True
TIMEOUT = 0.1

reader = MFRC522.MFRC552()

uuid = None
rising = False

def readUUID():
    return uuid

def isRising():
    if rising:
        rising = False
        return True
    return rising

class Reader(threading.Thread):
    def run(self):
        while ENABLED:
            (status, tagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
            if status == reader.MI_OK:
                (status, uid) = reader.MFRC522_Anticoll()
                if status == reader.MI_OK:
                    if uuid == None:
                        rising = True
                    uuid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                else:
                    uuid = None
                    rising = False
            else:
                uuid = None
                rising = False
        GPIO.cleanup()

readerThread = Reader()
readerThread.start()
