import sys ; sys.path += ['.', '..']
from SharedCode import Function
from Crypto.Hash import SHA256
from random import randint
import base64

"""
>>> Implement Diffie-Hellman
"""

class DiffieHellman():

    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.GenLocal()

    def GenLocal(self):
        """
        Creates private key variables from p and q
        """

        # This should remain privite (Private Key)
        self.x = randint(1, 10000) % self.p

        # This can be sent out to the other party (Public Key)
        self.X = pow(self.g, self.x, self.p)

    def GenKey(self, O):
        """
        Creates shared secrets
        """

        s = pow(O, self.x, self.p)
        return DiffieHellman.hSHA256(s)

    @staticmethod
    def hSHA256(msg):
        h = SHA256.new()
        h.update(str(msg).encode("utf-8"))
        digestBytes = h.digest()
        return base64.b64encode(digestBytes)
