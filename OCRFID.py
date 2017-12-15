import time
import tag
import database
import tracker
import Flask

class FlaskThread(threading.Thread):
    @app.route("/register")
    def register():
        uuid = tag.readUUID()
        if uuid:
            database.registerMember("Evan", uuid)
            return "Tag registered."
        else:
            return "Tag not found."
    def run(self):
            app.secret_key = 'super secret key'
            app.config['SESSION_TYPE'] = 'filesystem'
            app.run(host= '0.0.0.0', port=int(os.environ.get("PORT", 80)), debug=True, use_reloader=False, threaded=True)

flaskThread = FlaskThread()
flaskThread.start()

try:
    while True:
        tracker.update()
        time.sleep(0.1)
finally:
    tag.ENABLED = False
