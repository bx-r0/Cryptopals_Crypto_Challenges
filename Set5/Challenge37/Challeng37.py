import requests

url = "http://127.0.0.1:8000/SRP/"
tokenFile = './Set5/Challenge37/token.skrt'

userLoggedIn = "User already logged in"

username = "JohnDoe"
password = "password"

def login():
    r = requests.post(url + "login", data={'username':username, 'password': password})

    if r.status_code == 200:

        if r.text == userLoggedIn:
            print("[!] User is already authenticated!")
            return loadToken()
        else:
            print("[*] User logged in!")
            token = r.text
            saveToken(token)
            return token

def saveToken(token):
    with open(tokenFile, 'w') as file:
        file.write(token)
def loadToken():
    
    token = None
    with open(tokenFile, 'r') as file:
        token = file.read()

    return token

def doAuthenticatedAction(token):

    data = {'username': username,'token' : token}

    r = requests.post(url + 'action', data=data)

    if r.status_code == 200:
        print(r.text)


token = login()
doAuthenticatedAction(token)