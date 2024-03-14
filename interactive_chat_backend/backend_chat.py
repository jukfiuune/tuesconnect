from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import time
import hashlib

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load users and clubs from JSON files
try:
    with open("data.json", "r") as file:
        data = json.load(file)
except (FileNotFoundError, ValueError):
    data = {"users": {}, "clubs": []}

@app.route("/register", methods=["POST"])
@cross_origin()
def register():
    req_data = request.get_json()
    username = req_data["username"]
    email = req_data["email"]
    password = req_data["password"]
    hobbies = req_data["hobbies"]

    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()

    data["users"][username] = {
        "email": email,
        "password": hash_password,
        "hobbies": hobbies,
    }

    with open("data.json", "w") as file:
        json.dump(data, file)

    return jsonify(list(data["users"].keys()))

@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    req_data = request.get_json()
    username = req_data["username"]
    password = req_data["password"]

    if username not in data["users"]:
        return "Username not found", 401

    user = data["users"][username]
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()

    if hash_password != user["password"]:
        return "Incorrect password", 401

    return str(list(data["users"].keys()).index(username))

@app.route("/send_message", methods=["POST"])
@cross_origin()
def send_message():
    req_data = request.get_json()
    id = int(req_data["id"])
    clubname = req_data["clubname"]
    message = req_data["message"]

    if clubname not in data["clubs"]:
        return "Club not found", 404

    clubdata = {}
    try:
        with open(clubname + ".json", "r") as file:
            clubdata = json.load(file)
    except FileNotFoundError:
        pass

    timestamp = time.time()
    clubdata["messages"].append({"id": id, "message": message, "timestamp": timestamp})

    with open(clubname + ".json", "w") as file:
        json.dump(clubdata, file)

    return jsonify({"id": id, "message": message, "timestamp": timestamp})

@app.route("/get_message", methods=["GET"])
@cross_origin()
def get_message():
    req_data = request.get_json()
    clubname = req_data["clubname"]
    last_msg_ts = float(req_data["last_msg_ts"])
    if clubname not in data["clubs"]:
        return "Club not found", 404
    clubdata = {}
    try:
        with open(clubname + ".json", "r") as file:
            clubdata = json.load(file)
    except FileNotFoundError:
        pass
    msgs = []
    for message in clubdata["messages"]:
        if float(message["timestamp"]) > last_msg_ts:
            msgs.append(message)
    return jsonify(msgs)

@app.route("/get_clubs", methods=["GET"])
@cross_origin()
def get_clubs():
    return jsonify(data["clubs"])

@app.route("/create_club", methods=["POST"])
@cross_origin()
def create_club():
    req_data = request.get_json()
    clubname = req_data["clubname"]
    data["clubs"].append(clubname)
    with open(clubname + ".json", "w") as file:
        json.dump({"messages": []}, file)
    with open("data.json", "w") as file:
        json.dump(data, file)
    data["users"][list(data["users"].keys())[id]]["hobbies"].append(clubname)
    return jsonify(data["clubs"])

@app.route("/add_user_to_club", methods=["POST"])
@cross_origin()
def add_user_to_club():
    req_data = request.get_json()
    clubname = req_data["clubname"]
    id = req_data["id"]
    if clubname not in data["clubs"]:
        return "Club not found", 404
    usr_dict = data["users"][list(data["users"].keys())[id]]
    usr_dict["username"] = list(data["users"].keys())[id]
    return jsonify(usr_dict)

@app.route("/get_user", methods=["GET"])
@cross_origin()
def get_user():
    req_data = request.get_json()
    id = int(req_data["id"])
    usr_dict = data["users"][list(data["users"].keys())[id]]
    usr_dict["username"] = list(data["users"].keys())[id]
    return jsonify(usr_dict)

if __name__ == "__main__":
    app.run(host='0.0.0.0')