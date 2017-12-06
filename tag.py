import RPi.GPIO as GPIO
import MFRC522
import time
import threading

ENABLED = True
TIMEOUT = 0.1

reader = MFRC522.MFRC522()

uuid = None

def readUUID():
    return uuid

class Reader(threading.Thread):
    def run(self):
        global uuid
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

readerThread = Reader()
readerThread.start()
