from flask import Flask
from flask_socketio import SocketIO
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
session = Session(app)
socketio = SocketIO(app, manage_session=False)
if "secret.txt" in os.listdir(os.getcwd()):
    with open("secret.txt") as file:
        app.secret_key = str(file.read())
        file.close()
else:
    app.secret_key = "super secret"

#Only use for development server.
def createApp():
    socketio.run(app, host='0.0.0.0', port=80)
