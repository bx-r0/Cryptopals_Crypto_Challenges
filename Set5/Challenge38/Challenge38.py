import sys ; sys.path += ['.', '../..']
from SharedCode.BaseParty import BaseParty
from CryptoCode.SRP import SRP
from CryptoCode.MAC import HMAC
from SharedCode import Function
import base64
import hmac
import random

from hashlib import sha256

"""
>>> Implement Secure Remote Password (SRP)
"""

# Large safe prime
N = int(
"""
00c037c37588b4329887e61c2da332\
4b1ba4b81a63f9748fed2d8a410c2f\
c21b1232f0d3bfa024276cfd884481\
97aae486a63bfca7b8bf7754dfb327\
c7201f6fd17fd7fd74158bd31ce772\
c9f5f8ab584548a99a759b5a2c0532\
162b7b6218e8f142bce2c30d778468\
9a483e095e701618437913a8c39c3d\
d0d4ca3c500b885fe3
""", 16)

def SHA256(string):
    return int(sha256(str.encode(string)).hexdigest(), 16)

def H_SHA256(K, salt):
    K_bytes = K.to_bytes(1000, byteorder='big')
    h = hmac.new(K_bytes, str.encode(salt), sha256)
    return h.hexdigest()


WORDLIST = []
def load_wordlist():
    with open("./wordlist.txt") as file:
        wordlist = file.readlines()

    wordlist = list(map(str.strip, wordlist))

    return wordlist


#----------------------------------------------
# Client
#----------------------------------------------
class Client():


    def __init__(self, username, password):
        super()
        self.n = N
        self.g = 2
        self.k = 3

        self.a = SRP.randBits(1024)

        self.I = username
        self.P = password
        self.A = pow(self.g, self.a, self.n)

    # [C] -> S
    #   I, A = g**a % n
    def step1(self):
        return self.I, self.A 

    # [S] -> C
    # salt, B = g**b % n, u = 128 bit random number
    def step2(self, data):

        self.salt   = data[0]
        self.B      = data[1]
        self.u      = data[2]

    # C
    #   x = SHA256(salt|password)
    #   S = B**(a + ux) % n
    #   K = SHA256(S)
    def step3(self):
        self.x = SHA256(self.salt + self.P)

        aux = self.a + (self.u * self.x)
        self.S = pow(self.B, aux, self.n)
        self.K = SHA256(hex(self.S)[2:])

    # [C] -> S
    #     Send HMAC-SHA256(K, salt)
    def step4(self):
        return H_SHA256(self.K, self.salt)


#----------------------------------------------
# Server
#----------------------------------------------
class Server():

    def __init__(self, username, password):
        super()

        self.P = password
        self.salt = "upZn72da"

        self.n = N
        self.g = 2
        self.k = 3

    # S
    #   x = SHA256(salt|password)
    #   v = g**x % n
    def step1(self):
        self.x = SHA256(self.salt + self.P)
        self.v = pow(self.g, self.x, self.n)

    # C -> [S]
    #   I, A = g**a % n
    def step2(self, data):
        self.I = data[0]
        self.A = data[1]

    # [S] -> C
    #   salt, B = g**b % n, u = 128 bit random number
    def step3(self):
        self.b = SRP.randBits(1024)
        self.B = pow(self.g, self.b, self.n)
        self.u = SRP.randBits(128)

        return self.salt, self.B, self.u

    # S
    #   S = (A * v ** u)**b % n
    #   K = SHA256(S)
    def step4(self):
        
        Avu = self.A * pow(self.v, self.u, self.n)

        self.S = pow(Avu, self.b, self.n)
        self.K = SHA256(hex(self.S)[2:])

    # C -> [S]
    #     Send HMAC-SHA256(K, salt)
    def step5(self, MAC):
        self.c_mac = MAC
        self.s_mac = H_SHA256(self.K, self.salt)

        if self.c_mac == self.s_mac:
            print("OK!!!")


#----------------------------------------------
# Attacker
#----------------------------------------------
class Attacker():

    def __init__(self):
        super()

        self.salt = "upZn72da"

        self.n = N
        self.g = 2
        self.k = 3

    # S
    #   x = SHA256(salt|password)
    #   v = g**x % n
    def step1(self):
        pass

    # C -> [S]
    #   I, A = g**a % n
    def step2(self, data):
        self.I = data[0]
        self.A = data[1]

    # [S] -> C
    #   salt, B = g**b % n, u = 128 bit random number
    def step3(self):
        self.b = SRP.randBits(1024)
        self.B = pow(self.g, self.b, self.n)
        self.u = SRP.randBits(128)

        return self.salt, self.B, self.u

    # S
    #   S = (A * v ** u)**b % n
    #   K = SHA256(S)
    def step4(self):
        # Cannot calculate these values
        pass

    # C -> [S]
    #     Send HMAC-SHA256(K, salt)
    def step5(self, MAC):
        # This is where we do the cracking!

        for password in WORDLIST:

            print(f"Trying: {password}", end="\r")

            x = SHA256(self.salt + password)
            v = pow(self.g, x, self.n)
            S = pow(self.A * pow(v, self.u, self.n), self.b, self.n)
            K = SHA256(hex(S)[2:])

            attempt = H_SHA256(K, self.salt)

            if attempt == MAC:
                print(f"Password cracked: \"{password}\"")

                break



if __name__ == "__main__":

    WORDLIST = load_wordlist()

    # Chooses a random password to crack
    username = "User"
    password = random.choice(WORDLIST)
    print(f"[*] Actual password: {password}\n")

    # Swap these for the different modes
    S = Attacker()
    # S = Server(username, password)

    C = Client(username, password)

    # S
    #   x = SHA256(salt|password)
    #   v = g**x % n
    S.step1()

    # C -> S
    #   I, A = g**a % n
    S.step2(C.step1())

    # S -> C
    #   salt, B = g**b % n, u = 128 bit random number
    C.step2(S.step3())

    # C
    #   x = SHA256(salt|password)
    #   S = B**(a + ux) % n
    #   K = SHA256(S)
    C.step3()

    # S
    #   S = (A * v ** u)**b % n
    #   K = SHA256(S)
    S.step4()

    # C -> S
    #     Send HMAC-SHA256(K, salt)
    S.step5(C.step4())

