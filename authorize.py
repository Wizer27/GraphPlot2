import json
from werkzeug.security import check_password_hash


def load():
    with open('/Users/ivanvinogradov/GraphPlot2/users.json','r') as file:
        return json.load(file)
def autor(username,password):
    users = load()
    if username in users and check_password_hash(users[username], password):
        return True
    return False   
        