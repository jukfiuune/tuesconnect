import json
import random
with open("collection.json", "r") as file: 
    collection = json.load(file)
    decks=list(collection.keys())
print('\n'.join(decks))
deck=input("Add new deck \nOption: ")
if deck not in decks:
    collection[deck] = []

while True:
    option=int(input("1. Start session\n2. Add new card\nOption: "))
    if option==1:
        break
    else:
        front=input("front of card:")
        back=input("back of card")
        collection[deck].append([front,back])
sessioncards = collection[deck]
random.shuffle(sessioncards)
for card in sessioncards:
    print(card[0])
    input("Press enter to flip")
    print(card[1])
    input("Press enter to change to new card")
with open("collection.json", "w") as file: 
    collection = json.dump(collection,file)