import json
import datetime

data={}

with open("/home/uguuuu/tuesconnect/testchats.json", "r") as file:
    data = json.load(file)

usernames = list(data["users"].keys())

def login(username,password):
    if username in usernames:
        myindex = usernames.index(username)
        if password in data["users"][username]["password"]:
            print("Login Successful")
            return myindex
        else:
            print("Incorrect Password")
    else:
        print("Username not found")
        quit()

def chat(id):
    message = input(usernames[id] + ": ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["messages"].append({"id": id, "message": message, "timestamp": timestamp})

def printMessages():
    for message in data["messages"]:
        print(usernames[message["id"]] + ": " + message["message"] + " (" + message["timestamp"] + ")")

curruser = login(input("Username: "), input("Password: "))
printMessages()

while True:
    print("Do you want to chat? (Y/n): ")
    if input() == "n":
        break
    chat(curruser)
    chat(curruser)
    chat(curruser)
    chat(curruser)

with open("testchats.json", "w") as file:
    json.dump(data, file)

print("Bye")
