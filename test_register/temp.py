import json
import hashlib
data = {}
user_data={}
with open("sample.json", "r") as file: 
    data = json.load(file)
    user_data = data["users"]
while True:
    username = input("Username (type 'exit' to quit): ")
    if username=="exit":
        break
    email = input("Email: ")
    password = input("Password: ")
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()
    hobbies_menu = ["Programming", "Music", "Basketball", "Exit", "Option: "]
    hobbies_menu='\n'.join(hobbies_menu)
    user_data[username] = {"email": email, "password": hash_password, "hobbies":[]}
    while (len(user_data[username]["hobbies"])==0) or (user_data[username]["hobbies"][-1] != "Exit"):
        new_hobby=input(hobbies_menu)
        user_data[username]["hobbies"].append(new_hobby)
    user_data[username]["hobbies"].remove("Exit")
    print(user_data)
    data["users"]=user_data
    with open("sample.json", "w") as file: 
        json.dump(data, file)