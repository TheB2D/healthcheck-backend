import os
import eventlet

eventlet.monkey_patch()

import db_connector
import threading
from flask_socketio import SocketIO, emit

from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app_name = os.getenv("APP_NAME")

app = Flask(app_name)
socketio = SocketIO(app, debug=True)

@app.route("/info", methods=['POST', 'GET'])
def post_info():

    if request.is_json:
        data = request.get_json()

    if request.method == 'POST':

        data_to_insert = {
                "client_username": data["client_username"],
                "doctor_username": data["doctor_username"],
                "procedures": data["procedures"],
                "procedure_name": data["procedure_name"]
        }

        db_connector.get_db().insert_one(data_to_insert)

        return {"data": True}, 200

    elif request.method == 'GET': # for translation
        """
        get method:
        {
            "client_username": str
            "procedure_name": str
        }
        """
        pass

def stream():
    with db_connector.get_db().watch() as stream:
        for change in stream:
            print(f"[!] DB change {change}")
            socketio.emit('db_update', change)

stream_thread = threading.Thread(target=stream)
stream_thread.start()

@socketio.on('connect')
def handle_connect():
    print("Client Connected")

if __name__ == '__main__':
    socketio.run(app, debug=True)


