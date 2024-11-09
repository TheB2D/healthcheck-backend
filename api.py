import os
import eventlet
import db_connector
import threading
from flask_socketio import SocketIO, emit
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import LLMsimplifier

# Load environment variables
load_dotenv()

app_name = os.getenv("APP_NAME")
app = Flask(app_name)
socketio = SocketIO(app, debug=True)


@app.route("/info", methods=['POST', 'GET'])
def info():
    # Check if the incoming request is JSON
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify({"error": "Request must be JSON"}), 400

    db = db_connector.get_db()
    collection = db['procedures_collection']  # Specify your collection name

    if request.method == 'POST':
        # Extracting data from the incoming JSON
        data_to_insert = {
            "client_username": data.get("client_username"),
            "procedures": {
                "doctor_username": data["procedures"].get("doctor_username"),
                "procedure_name": data["procedures"].get("procedure_name"),
                "procedure_steps": data["procedures"].get("procedure_steps")
            },
        }

        # Insert data into the MongoDB collection
        collection.insert_one(data_to_insert)

        return jsonify({"data": "Successfully inserted"}), 200

    elif request.method == 'GET':
        client_username = data.get("client_username")
        if not client_username:
            return jsonify({"error": "client_username is required"}), 400

        result = collection.find_one({"client_username": client_username})

        if result:
            return jsonify(result["procedures"]), 200
        else:
            return jsonify({"error": "Client not found"}), 404


@app.route("/simplify", methods=["POST"])
def simplify():

    return_data = []

    if request.is_json:
        data = request.get_json()

    for i in data["procedure_steps"].keys():
        return_data.append(LLMsimplifier.askme(i, data["language"]))

    return return_data

def stream():
    with db_connector.get_db().watch() as stream:
        for change in stream:
            print(f"[!] DB change {change}")
            socketio.emit('db_update', change)


stream_thread = threading.Thread(target=stream)
stream_thread.start()


@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(target=stream)


if __name__ == '__main__':
    socketio.run(app, debug=True)
