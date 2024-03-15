from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import time
import hashlib
import jwt

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
secret_key = "very_important_and_secret_key"

# Load users and clubs from JSON files
try:
    with open("data.json", "r") as file:
        data = json.load(file)
except (FileNotFoundError, ValueError):
    data = {"users": {}, "clubs": []}

def generate_token(myid):
    payload = {
        'exp': time.time() + 1800,
        'gen': time.time(),
        'myid': myid
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def validate_token(myid, token):
    decoded_token = jwt.decode(token, secret_key, algorithms='HS256')
    curr_time = time.time()
    if decoded_token["exp"] <= curr_time or decoded_token["myid"] != myid:
        print(decoded_token["exp"], curr_time, decoded_token["myid"], myid)
        return 401
    return 200

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

    myid = int(list(data["users"].keys()).index(username))
    return jsonify({"token": generate_token(myid), "myid": myid})

@app.route("/regenerate_token", methods=["POST"])
@cross_origin()
def regenerate_token():
    req_data = request.get_json()
    myid = int(req_data["myid"])
    token = req_data["token"]
    valid_code = validate_token(myid, token)
    if valid_code != 200:
        return "Unknown error occured", valid_code
    return jsonify({"token": generate_token(myid), "myid": myid})

@app.route("/send_message", methods=["POST"])
@cross_origin()
def send_message():
    req_data = request.get_json()
    myid = int(req_data["myid"])
    clubname = req_data["clubname"]
    message = req_data["message"]
    try:
        token = req_data["token"]
        valid_code = validate_token(myid, token)
    except:
        return "Token cannot be found", 401
    
    if valid_code != 200:
        return "Unknown error occured", valid_code
    
    if clubname not in data["clubs"]:
        return "Club not found", 404

    clubdata = {}
    try:
        with open(clubname + ".json", "r") as file:
            clubdata = json.load(file)
    except FileNotFoundError:
        pass

    timestamp = time.time()
    clubdata["messages"].append({"myid": myid, "message": message, "timestamp": timestamp})

    with open(clubname + ".json", "w") as file:
        json.dump(clubdata, file)

    return jsonify({"myid": myid, "message": message, "timestamp": timestamp})

@app.route("/get_message", methods=["POST"])
@cross_origin()
def get_message():
    req_data = request.get_json()
    clubname = req_data["clubname"]
    last_msg_ts = float(req_data["last_msg_ts"])
    print(last_msg_ts)
    myid = int(req_data["myid"])
    try:
        token = req_data["token"]
        valid_code = validate_token(myid, token)
    except:
        return "Token cannot be found", 401
    
    if valid_code != 200:
        return "Unknown error occured", valid_code
    
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
    data["users"][list(data["users"].keys())[myid]]["hobbies"].append(clubname)
    return jsonify(data["clubs"])

@app.route("/add_user_to_club", methods=["POST"])
@cross_origin()
def add_user_to_club():
    req_data = request.get_json()
    clubname = req_data["clubname"]
    myid = req_data["myid"]
    for clubs in clubname:
        data["users"][list(data["users"].keys())[myid]]["hobbies"].append(clubs)
    usr_dict = data["users"][list(data["users"].keys())[myid]]
    usr_dict["username"] = list(data["users"].keys())[myid]
    return jsonify(usr_dict)

@app.route("/get_user", methods=["POST"])
@cross_origin()
def get_user():
    req_data = request.get_json()
    myid = int(req_data["myid"])    
    usr_dict = data["users"][list(data["users"].keys())[myid]]
    usr_dict["username"] = list(data["users"].keys())[myid]
    return jsonify(usr_dict)

@app.route("/get_user_via_token", methods=["POST"])
@cross_origin()
def get_user_via_token():
    req_data = request.get_json()
    try:
        token = req_data["token"]
        decoded = jwt.decode(token, secret_key, algorithms='HS256')
    except:
        return "Token cannot be found", 401
    myid = int(decoded["myid"])
    
    usr_dict = data["users"][list(data["users"].keys())[myid]]
    usr_dict["username"] = list(data["users"].keys())[myid]
    return jsonify(usr_dict)

if __name__ == "__main__":
    app.run(host='0.0.0.0')