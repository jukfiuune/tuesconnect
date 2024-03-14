import json
import datetime
import hashlib

# username - tues
# pass - imali66rimi

data={}

with open("data.json", "r") as file:
    data = json.load(file)

def register(username, email, password, hobbies):
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()
    data["users"][username] = {"email": email, "password": hash_password, "hobbies": hobbies}
    return list(data["users"].keys())
usernames = register(input("Username: "), input("Email: "), input("Password: "), input("Hobbies: "))
def login(username,password):
    if username in usernames:
        myindex = usernames.index(username)
        hash_object = hashlib.sha256()
        hash_object.update(password.encode())
        hash_password = hash_object.hexdigest()
        if hash_password in data["users"][username]["password"]:
            print("Login Successful")
            return myindex
        else:
            print("Incorrect Password")
    else:
        print("Username not found")
        quit()

def chat(id, clubdata):
    message = input(usernames[id] + ": ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clubdata["messages"].append({"id": id, "message": message, "timestamp": timestamp})
    return clubdata

def selectClub():
    print("Select a club to chat with: ")
    for club in data["clubs"]:
        print(club)
    clubname = input("Club name: ")
    if clubname in data["clubs"]:
        return clubname
    else:
        print("Club not found")
        quit()
    

def printMessages(clubdata):
    for message in clubdata["messages"]:
        print(usernames[message["id"]] + ": " + message["message"] + " (" + message["timestamp"] + ")")

curruser = login(input("Username: "), input("Password: "))
clubname = selectClub()
clubdata = {}
with open(clubname + ".json", "r") as file:
    clubdata = json.load(file)

printMessages(clubdata)

while True:
    print("Do you want to chat? (Y/n): ")
    if input() == "n":
        break
    clubdata = chat(curruser,clubdata)
    clubdata = chat(curruser,clubdata)
    clubdata = chat(curruser,clubdata)
    clubdata = chat(curruser,clubdata)

with open(clubname + ".json", "w") as file:
    json.dump(clubdata, file)

with open("data.json", "w") as file:
    json.dump(data, file)

print("Bye")
