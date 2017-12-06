import tag

try:
    while True:
        print tag.readUUID()
finally:
    tag.ENABLED = False
