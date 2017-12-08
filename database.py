import sqlite3
import time

conn = sqlite3.connect('ocrfid.db')

def registerMember(name, uuid):
    c = conn.cursor()
    #Delete old entries from uuid to be registered
    c.execute('''DELETE FROM timesheet WHERE uuid=?''', (uuid,))

    #Migrate past user entries to new ID
    c.execute('''SELECT uuid FROM members where name=?''', (name,))
    lastUUID = c.fetchone()
    if len(lastUUID) > 0:
        c.execute('''SELECT (event, in_time, out_time) FROM timesheet WHERE uuid=?''', (lastUUID[0],))
        for entry in c.fetchall():
            c.execute('''INSERT INTO timesheet (uuid, event, in_time, out_time) VALUES(?, ?, ?, ?)''', (uuid, entry[0], entry[1], entry[2],))
        c.execute('''DELETE FROM timesheet WHERE uuid=?''', (lastUUID[0],))

    #If uuid has been registered, update name and register time, otherwise insert new entry
    c.execute('''SELECT uuid FROM members WHERE uuid=?''', (uuid,))
    if len(c.fetchone()) > 0:
        c.execute('''UPDATE members SET name=?, register_time=? WHERE uuid=?''', (name, time.time(), uuid,))
    else:
        c.execute('''INSERT INTO members (uuid, name, register_time) VALUES (?, ?, ?)''', (uuid, name, time.time()))

def close():
    conn.close()
