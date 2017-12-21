import time
import datetime
import tag
import database
#import tracker
from flask import Flask, render_template, request, json
import threading
import os

app = Flask(__name__)

def buildTimeData():
    members = database.getMembers()
    data = []
    for m in members:
        date = datetime.datetime.fromtimestamp(m[2])
        lastClockTime = database.lastClock(m[0], ("build",))
        if lastClockTime:
            lastClock = datetime.datetime.fromtimestamp(lastClockTime).strftime('%b %d, %Y')
        else:
            lastClock = None
        data.append([str(m[0]), str(m[1]), str(database.sumTime(m[0], ("build",))), str(lastClock), str(date.strftime('%b %d, %Y'))])
    return data

class FlaskThread(threading.Thread):
    @app.route("/")
    def time():
        events = []
        for i in range(0, len(database.events)):
            events.append(str(database.events[i]))
        return render_template("time.html", members=buildTimeData(), events=events,)

    @app.route("/newEvent", methods=['POST'])
    def newEvent():
        event = request.form['event']
        database.createEvent(event)
        return json.dumps({'status':'OK'});

    @app.route("/register", methods=['POST'])
    def register():
        uuid = tag.readUUID()
        name = request.form['member']
        if uuid and name:
            database.registerMember(name, uuid)
            return json.dumps({'status':'OK'})
        else:
            return json.dumps({'status':'FAILED'})

    @app.route("/tagPresent")
    def tagPresent():
        if tag.readUUID():
            return "Present"
        else:
            return "Missing"

    @app.route("/timeData")
    def timeData():
        return buildTimeData()

    def run(self):
            app.secret_key = 'super secret key'
            app.config['SESSION_TYPE'] = 'filesystem'
            app.run(host= '0.0.0.0', port=int(os.environ.get("PORT", 80)), debug=True, use_reloader=False, threaded=True)

flaskThread = FlaskThread()
flaskThread.start()
"""
try:
    while True:
        tracker.update()
        print database.sumTime(tag.readUUID())
        time.sleep(0.1)
finally:
    tag.ENABLED = False
"""
