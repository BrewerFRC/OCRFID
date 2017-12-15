import sqlite3
import time

conn = sqlite3.connect('ocrfid.db')
currentEvent = "build"

def registerMember(name, uuid):
    c = conn.cursor()
    #Delete old entries from uuid to be registered
    c.execute('''DELETE FROM timesheet WHERE uuid=?''', (uuid,))

    #Migrate past user entries to new ID
    c.execute('''SELECT uuid FROM members where name=?''', (name,))
    lastUUID = c.fetchone()
    if lastUUID:
        c.execute('''SELECT (event, in_time, out_time) FROM timesheet WHERE uuid=?''', (lastUUID[0],))
        for entry in c.fetchall():
            c.execute('''INSERT INTO timesheet (uuid, event, in_time, out_time) VALUES(?, ?, ?, ?)''', (uuid, entry[0], entry[1], entry[2],))
        c.execute('''DELETE FROM timesheet WHERE uuid=?''', (lastUUID[0],))

    #If uuid has been registered, update name and register time, otherwise insert new entry
    c.execute('''SELECT uuid FROM members WHERE uuid=?''', (uuid,))
    if c.fetchone():
        c.execute('''UPDATE members SET name=?, register_time=? WHERE uuid=?''', (name, time.time(), uuid,))
    else:
        c.execute('''INSERT INTO members (uuid, name, register_time) VALUES (?, ?, ?)''', (uuid, name, time.time()))

def recordTime(uuid):
    c = conn.cursor()

    #Check for incomplete time slots
    c.execute('''SELECT in_time FROM timesheet WHERE uuid=? AND out_time=-1''', (uuid,))
    incompleteTime = c.fetchone()
    if incompleteTime:
        #Ignore incomplete entry if over 18 hours old.
        if incompleteTime[0] - time.time() > 3600*18:
            print "Removed time for ", uuid
            c.execute('''DELETE FROM timesheet WHERE uuid=? AND out_time=-1''', (uuid,))
        else:
            print "Closed time for ", uuid
            c.execute('''UPDATE timesheet SET out_time=? WHERE uuid=? AND out_time=-1''', (time.time(), uuid,))
            return
    #If no open time is found, create a login
    print "Opened time for ", uuid
    c.execute('''INSERT INTO timesheet (uuid, event, in_time, out_time) VALUES (?, ?, ?, -1)''', (uuid, currentEvent, time.time(),))

def removeOutdatedEntries():
    c = conn.cursor()
    #Delete incomplete slots
    c.execute('''DELETE FROM timesheet WHERE out_time=-1''')

def close():
    conn.close()
