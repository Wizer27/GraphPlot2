import json
from werkzeug.security import check_password_hash

def load():
    with open('/Users/ivanvinogradov/GraphPlot2/users.json','r') as file:
        return json.load(file)
def autor(username,password):
    users = load()
    print(users)
    if username in users and  users[username] == hash(password):
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
