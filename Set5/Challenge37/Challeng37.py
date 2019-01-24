import sys
import sys ; sys.path += ['.', '../..']

import requests
from Set5.Challenge36.Challenge36 import Client
from SharedCode import Function

url = "http://127.0.0.1:8000/SRP/action"

userLoggedIn = "User already logged in"

c = None

def createRequestBody(username, commandNo, data):
    return \
    {
        'username': username,
        'commandNo': commandNo,
        'data':data
    }

def beginSession(username, password):

    # C & S
    #     Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
    # S

    #         Generate salt as random integer
    #         Generate string xH=SHA256(salt|password)
    #         Convert xH to integer x somehow (put 0x on hexdigest)
    #         Generate v=g**x % N
    #         Save everything but x, xH
    step1()


    # C->S
    #     Send I, A=g**a % N (a la Diffie Hellman)
    # S->C
    #     Send salt, B=kv + g**b % N
    # S, C
    #     Compute string uH = SHA256(A|B), u = integer of uH
    # C

    #         Generate string xH=SHA256(salt|password)
    #         Convert xH to integer x somehow (put 0x on hexdigest)
    #         Generate S = (B - k * g**x)**(a + u * x) % N
    #         Generate K = SHA256(S)

    # S

    #         Generate S = (A * v**u) ** b % N
    #         Generate K = SHA256(S)
    step2()

    # C->S
    #     Send HMAC-SHA256(K, salt)
    # S->C
    #     Send "OK" if HMAC-SHA256(K, salt) validates
    step3()


def step1():
    data = c.step1([])

    # STEP 1
    body = createRequestBody(username, 1, data)

    r = requests.post(url, data=body)
    
    if r.text != "ACK":
        Function.COLOURS.printRed("[*]" + r.text)
        exit()

def step2():
    # STEP 2

    # I, A
    data = c.step2([])

    ##############################################
    #       Variable to change the value of A    #
    ##############################################
    replacedA = None
    # replacedA = 0               # 0 mod N = 0
    # replacedA = c.N             # Works because A is a multiple of N 
    # replacedA = c.N * 2         # Same as above

    # Changes the value of A that is sent to the server
    if replacedA != None:
        print("A =", replacedA)
        data[1] = replacedA
        c.A = replacedA

    body = createRequestBody(username, 2, data)

    r = requests.post(url, data=body)

    if r.status_code != 200:
        raise(Exception("[Client] - Error in step 2 of SRP"))

    # Removes [ (1) and ] (-1) and splits by a comma
    serverData = r.headers['data'][1:-1].split(",")
    serverData = list(map(int, serverData))

    # salt, B
    c.step3(serverData)
    c.step4([])

    # If the value of A is altered the key will always be zero
    if replacedA != None:
        c.K = Function.Hash.SHA256_Hex(b"0")

def step3():
    data = c.step5([])

    body = createRequestBody(username, 3, data)
    r = requests.post(url, data=body)

    if r.text != "OK":
        Function.COLOURS.printRed("[*] - HMAC verification failed!")
    else:
        Function.COLOURS.printGreen("[*] HMAC passed, user validated!")

if __name__ == "__main__":

    username = input("Username: ")
    password = input("Password: ")

    c = Client(username, password)

    beginSession(username, password)
    print()