import datetime, tag, database, threading, os, tracker
from flask import Blueprint, render_template, request, json, jsonify

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

@app.route("/")
def time():
    events = []
    for i in range(0, len(database.events)):
        events.append(str(database.events[i]))
    return render_template("time.html", members=buildTimeData(), events=events, currentEvent=database.currentEvent,)

@app.route("/newEvent", methods=['POST'])
def newEvent():
    event = request.form['event']
    database.createEvent(event)
    return json.dumps({'status':'OK'})

@app.route("/selectEvent", methods=['POST'])
def selectEvent():
    return jsonify(buildTimeData(request.form.getlist('events[]')))

@app.route("/changeEvent", methods=['POST'])
def changeEvent():
    print request.form
    database.currentEvent = request.form['currentEvent']
    return json.dumps({'status':'OK'})

@app.route("/register", methods=['POST'])
def register():
    uuid = tag.readUUID()
    name = request.form['member']
    if uuid and name:
        database.registerMember(name, uuid)
        return json.dumps({'status':'OK'})
    else:
        return json.dumps({'status':'FAILED'})

@app.route("/toggleSignIn", methods=['POST'])
def toggleSignIn():
    tracker.enabled = not tracker.enabled
    return json.dumps({'enabled':str(tracker.enabled)})

@app.route("/tagPresent")
def tagPresent():
    if tag.readUUID():
        return "Present"
    else:
        return "Missing"

@app.route("/timeData")
def timeData():
    return buildTimeData()
