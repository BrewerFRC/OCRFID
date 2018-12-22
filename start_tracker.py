import database, tag, time

try:
    database.removeOutdatedEntries()
    tag.start()
    while True:
        tag.update()
        time.sleep(0.1)
finally:
    tag.ENABLED = False
