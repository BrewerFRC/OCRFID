import time
import tag

try:
    while True:
        print tag.readUUID()
        time.sleep(1)
finally:
    tag.ENABLED = False
