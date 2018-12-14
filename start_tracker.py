import database, tracker, tag, time

try:
    database.removeOutdatedEntries()
    while True:
        tracker.update()
        time.sleep(0.1)
finally:
    tag.ENABLED = False
