import datetime, tag, database, threading, os, tracker
from flask import Blueprint, render_template, request, json, jsonify
from app import socketio

blueprint = Blueprint('main', __name__)

def buildTimeData(events=[database.currentEvent]):
    members = database.getMembers()
    data = []
    for m in members:
        date = datetime.datetime.fromtimestamp(m[2])
        lastClockTime = database.lastClock(m[0], events)
        if lastClockTime:
            lastClock = datetime.datetime.fromtimestamp(lastClockTime).strftime('%b %d, %Y')
        else:
            lastClock = None
        hours, loggedIn = database.sumTime(m[0], events)
        data.append([str(m[0]), str(m[1]), str(hours), str(lastClock), str(date.strftime('%b %d, %Y')), str(loggedIn)])
    return sorted(data, key=lambda x: x[2], reverse=True)


"""
HTTP Endpoints
"""
@app.route("/")
def time():
    events = []
    for i in range(0, len(database.events)):
        events.append(str(database.events[i]))
    return render_template("time.html", members=buildTimeData(), events=events, currentEvent=database.currentEvent,)

@app.route("/status")
def status():
    events = []
    for i in range(0, len(database.events)):
        events.append(str(database.events[i]))
    return render_template("status.html", members=buildTimeData(), events=events, currentEvent=database.currentEvent,)

"""
SocketIO Handlers
"""
@socketio.on("new-event")
def newEvent(data):
    database.createEvent(data["event"])

@socketio.on("select-event")
def selectEvent(data):
    socketio.emit('select-event', buildTimeData(data['events']), namespace=request.sid)

@socketio.on('change-event')
def changeEvent(data):
    database.currentEvent = data['currentEvent']

@socketio.on('register')
def register(data):
    uuid = tag.readUUID()
    name = data['member']
    if uuid and name:
        database.registerMember(name, uuid)
        out = {"success": True}
    else:
        out = {"success": False}

    socket.emit('register', out, namespace=request.sid)

@app.route("/clock", methods=['POST'])
def clock():
    uuid = request.form['uuid']
    time = request.form['time']
    events = request.form['events']
    if not request.form['events']:
        events=None
    if uuid and time:
        database.recordTime(uuid=uuid, customTime=time)
    if not request.form['events']:
        return buildTimeData()
    return buildTimeData(events=events)

@socketio.on('toggle-sign-in')
def toggleSignIn(data):
    tracker.enabled = not tracker.enabled
    socketio.emit('toggle-sign-in', {'enabled': str(tracker.endabled)}, namespace=request.sid)

@socketio.on('tag-present')
def tagPresent(data):
    if tag.readUUID():
        socketio.emit('tag-present', {'tag': True}, namespace=request.sid)
    else:
        socketio.emit('tag-present', {'tag': False}, namespace=request.sid)

@app.route("/timeData")
def timeData():
    return buildTimeData()
