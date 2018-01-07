import sqlite3
import time

#Time in seconds to wait before allowing another time event for a user.
DEBOUNCE = 5

events = []

tempConn = sqlite3.connect('ocrfid.db')
tempC = tempConn.cursor()
tempC.execute('''SELECT DISTINCT value FROM settings WHERE attribute="event"''');
for event in tempC.fetchall():
    if len(event) > 0:
        events.append(event[0])

tempC.execute('''SELECT value FROM settings WHERE attribute="currentEvent"''');
curr = tempC.fetchone()
if curr and len(curr) > 0:
    currentEvent = curr[0]
else:
    currentEvent = events[0]
tempConn.close()

def createEvent(eventName):
    conn = sqlite3.connect('ocrfid.db')
    c = conn.cursor()
    c.execute('''INSERT INTO settings (attribute, value) VALUES("event", ?)''', (eventName,))
    conn.commit()
    conn.close()

    events.append(eventName)

def registerMember(name, uuid):
    conn = sqlite3.connect('ocrfid.db')
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

    conn.commit()
    conn.close()

def getMembers():
    conn = sqlite3.connect('ocrfid.db')
    c = conn.cursor()

    c.execute('''SELECT DISTINCT uuid, name, register_time FROM members''')
    members = c.fetchall()
    conn.close()
    if members:
        return members
    return []

def recordTime(uuid):
    if not uuid:
        return
    conn = sqlite3.connect('ocrfid.db')
    c = conn.cursor()

    #Check for incomplete time slots
    c.execute('''SELECT in_time FROM timesheet WHERE uuid=? AND out_time=-1''', (uuid,))
    incompleteTime = c.fetchone()
    if incompleteTime:
        #Ignore incomplete entry if over 18 hours old.
        if time.time() - incompleteTime[0] > 3600*18:
            print "Removed time for ", uuid
            c.execute('''DELETE FROM timesheet WHERE uuid=? AND out_time=-1''', (uuid,))
        #Ignore accidental triggers close to login
        elif time.time() - incompleteTime[0] < DEBOUNCE:
            print "Ignoring accidental trigger."
            return
        else:
            print "Closed time for ", uuid
            c.execute('''UPDATE timesheet SET out_time=? WHERE uuid=? AND out_time=-1''', (time.time(), uuid,))
            conn.commit()
            conn.close()
            return
    #If no open time is found, create a login
    c.execute('''SELECT uuid, in_time, out_time FROM timesheet WHERE uuid=?''', (uuid,))

    c.execute('''SELECT max(out_time) FROM timesheet WHERE uuid=?''', (uuid,))
    lastOutTime = c.fetchone()
    if lastOutTime and lastOutTime[0]:
        if time.time() - lastOutTime[0] < DEBOUNCE:
            print "Ignoring accidental trigger."
            return
    print "Opened time for ", uuid
    c.execute('''INSERT INTO timesheet (uuid, event, in_time, out_time) VALUES (?, ?, ?, -1)''', (uuid, currentEvent, time.time(),))

    conn.commit()
    conn.close()

def removeOutdatedEntries():
    conn = sqlite3.connect('ocrfid.db')
    c = conn.cursor()
    #Delete incomplete slots
    #c.execute('''DELETE FROM timesheet WHERE out_time=-1''')

    #conn.commit()
    conn.close()

def sumTime(uuid, events=[currentEvent]):
    if not uuid:
        return 0, False
    if not events or len(events) == 0:
        return 0, False
    conn = sqlite3.connect('ocrfid.db')
    c = conn.cursor()

    eventString = "("
    for i in range(0, len(events)-1):
        eventString += "\"" + events[i] + "\", "
    eventString += "\"" + events[len(events)-1] + "\")"

    #sum = '''SELECT sum(out_time), sum(in_time) FROM timesheet WHERE uuid=? AND out_time!=-1 AND event IN ''' + eventString
    sum = '''SELECT out_time, in_time FROM timesheet WHERE uuid=? AND event IN ''' + eventString
    c.execute(sum, (uuid,))
    time = c.fetchall()
    conn.close()
    #if time and len(time) >= 2 and time[0] and time[1]:
    #    return time[0] - time[1]
    loggedIn = False
    runningSum = 0
    if time and len(time) > 0:
        for t in time:
            if t[0] == -1:
                loggedIn = True
                runningSum += time.time() - t[1]
            else:
                runningSum += t[0] - t[1]
        return runningSum, loggedIn
    return 0, False

def lastClock(uuid, events=[currentEvent]):
    if not uuid:
        return 0
    if not events or len(events) == 0:
        return 0
    conn = sqlite3.connect('ocrfid.db')
    c = conn.cursor()

    eventString = "("
    for i in range(0, len(events)-1):
        eventString += "\"" + events[i] + "\", "
    eventString += "\"" + events[len(events)-1] + "\")"

    clock = '''SELECT max(out_time) FROM timesheet WHERE uuid=? AND out_time!=-1 AND event IN ''' + eventString
    c.execute(clock, (uuid,))
    last = c.fetchone()
    conn.close()
    if last and len(last) > 0:
        return last[0]
