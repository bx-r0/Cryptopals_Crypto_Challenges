import sys ; sys.path += ['.', '..']
from SharedCode import Function
from Crypto.Hash import SHA256
from random import randint
import base64

"""
>>> Implement Diffie-Hellman
"""

class DiffieHellman():

    p = 2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633919
    g = 2

    def __init__(self):
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


if __name__ == "__main__":

    # Simulates the two parties exchanging values
    A = DiffieHellman()
    B = DiffieHellman()

    keyA = A.GenKey(B.X)
    keyB = B.GenKey(A.X)
