import json
import hashlib


def hash_password(password:str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = hashlib.sha256(password_bytes).hexdigest()
    return hashed 
def load():
    with open('/Users/ivanvinogradov/GraphPlot2/users.json','r') as file:
        return json.load(file)
def autor(username,password):
    users = load()
    print(users)
    if username in users and  users[username] == hash_password(password):
        return True
    return False   
def evens(iterable: iter) -> list:
    even = []
    for i in iter:
        if i % 2 == 0:
            even.append(i)
    return even
#assert evens([1,2,3,4,5,6,7])
#assert evens([1,3,5])   
#check_password_hash(users[username], password) 
