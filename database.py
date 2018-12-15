import db, queries, time

#Time in seconds to wait before allowing another time event for a user.
DEBOUNCE = 5

events = []

for event in db.fetchAll(queries.get_events):
    if len(event) > 0:
        events.append(event[0])

curr = db.fetchOne(queries.get_current_event)
if curr and len(curr) > 0:
    currentEvent = curr[0]
else:
    currentEvent = events[0]

def createEvent(eventName):
    db.execute(queries.create_event, (eventName,))
    events.append(eventName)

def registerMember(name, uuid):
    #Delete old entries from uuid to be registered
    db.execute(queries.clear_member_clocks, (uuid,))

    #Migrate past user entries to new ID
    lastUUID = db.fetchOne(queries.get_uuid_by_name, (name,))
    if lastUUID:
        for entry in db.fetchAll(queries.get_clocks, (lastUUID[0],)):
            db.execute(queries.clock_member, (uuid, entry[0], entry[1], entry[2],))
        db.execute(queries.clear_member_clocks, (lastUUID[0],))

    #If uuid has been registered, update name and register time, otherwise insert new entry
    if db.fetchOne(queries.check_member_exists, (uuid,)):
        db.execute(queries.update_name, (name, time.time(), uuid,))
    else:
        db.execute(queries.register_member, (uuid, name, time.time()))

def getMembers():
    members = db.fetchAll(queries.get_members)
    if members:
        return members
    return []

def recordTime(uuid, customTime=-1):
    if not uuid:
        return
    if customTime > 0:
        clockTime = customTime
    else:
        clockTime = time.time()

    #Check for incomplete time slots
    incompleteTime = db.fetchOne(queries.check_for_open, (uuid,))
    if incompleteTime:
        #Ignore incomplete entry if over 18 hours old.
        if time.time() - incompleteTime[0] > 3600*18:
            print "Removed time for ", uuid
            db.execute(queries.cancel_open_member_clock, (uuid,))
        #Ignore accidental triggers close to login
        elif time.time() - incompleteTime[0] < DEBOUNCE:
            print "Ignoring accidental trigger."
            return
        else:
            print "Closed time for ", uuid
            db.execute(queries.close_clock, (clockTime, uuid,))
            return
    #If no open time is found, create a login
    lastOutTime = db.fetchOne(queries.get_last_member_clock_out, (uuid,))
    if lastOutTime and lastOutTime[0]:
        if time.time() - lastOutTime[0] < DEBOUNCE:
            print "Ignoring accidental trigger."
            return
    print "Opened time for ", uuid
    db.execute(queries.clock_member, (uuid, currentEvent, clockTime,))

def removeOutdatedEntries():
    #Delete incomplete slots
    #db.execute(queries.clear_open_clocks)
    pass

def sumTime(uuid, events=[currentEvent]):
    if not uuid:
        return 0, False
    if not events or len(events) == 0:
        return 0, False

    eventString = "("
    for i in range(0, len(events)-1):
        eventString += "\"" + events[i] + "\", "
    eventString += "\"" + events[len(events)-1] + "\")"

    #sum = '''SELECT sum(out_time), sum(in_time) FROM timesheet WHERE uuid=? AND out_time!=-1 AND event IN ''' + eventString
    sum = queries.get_clocks_by_event + eventString
    timeList = db.fetchAll(sum, (uuid,))
    #if time and len(time) >= 2 and time[0] and time[1]:
    #    return time[0] - time[1]
    loggedIn = False
    runningSum = 0
    if timeList and len(timeList) > 0:
        for t in timeList:
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

    eventString = "("
    for i in range(0, len(events)-1):
        eventString += "\"" + events[i] + "\", "
    eventString += "\"" + events[len(events)-1] + "\")"

    clock = queries.get_last_member_clock_out_by_event + eventString
    last = db.fetchOne(clock, (uuid,))
    if last and len(last) > 0:
        return last[0]
