import sys ; sys.path += ['.', '../..']
from SharedCode import Function
import random
from Crypto.Hash import SHA256

class SRP():
    
    @staticmethod
    def randBits(n):
        return random.SystemRandom().getrandbits(64)

    @staticmethod
    def H(*args):

        # Concats the values
        a = "".join(str(a) for a in args)
        msgBytes = a.encode("utf-8")
        hashHex = Function.Hash.SHA256_Hex(msgBytes)

        # Converts hash to a value
        return int(hashHex, 16)

    def __init__(self, username, password, N, g=2, k=3):
        
        # Pre agreed variables
        self.N = N
        self.g = g
        self.k = k

        # Joins the string above
        self.I = username
        self.p = password
        self.salt = SRP.randBits(64)
        self.x = SRP.H(self.salt, self.p)
        self.v = pow(self.g, self.x, self.N)
        
        # Diffie-Hellman
        self.b = SRP.randBits(1024)
        self.B = (self.k * self.v + (pow(self.g, self.b, self.N))) % self.N
