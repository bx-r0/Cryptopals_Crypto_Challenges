import sys ; sys.path += ['.', '../..']
import random
import json
from SharedCode.Function import Hash, RSA

class DSA():

    def __init__(self):
        # Simulates the generation of params
        with open("params.json") as file:
            data = file.read()

        params = json.loads(data)

        self.p = int(params['p'], 16)
        self.q = int(params['q'], 16)
        self.g = int(params['g'], 16)

        # Private Key
        self.x = random.randint(1, self.q - 1)

        # Public Key
        self.y = pow(self.g, self.x, self.p)

    def sign(self, msg):

        r = 0
        s = 0
        while r == 0 and s == 0:
            k = random.randint(1, self.q - 1)

            r = pow(self.g, k, self.p) % self.q

            # s  
            h = int(Hash.SHA256_Hex(msg), 16)
            k_inv = RSA.invmod(k, self.q)
            s = (k_inv * (h + (self.x * r))) % self.q

        return r, s

    def verify(self, msg, r, s):

        if r < 0 or r > self.q:
            return False

        if s < 0 or s > self.q:
            return False

        w = RSA.invmod(s, self.q)

        h = int(Hash.SHA256_Hex(msg), 16)

        u1 = h * w % self.q
        u2 = r * w % self.q

        gu1 = pow(self.g, u1, self.p)
        yu2 = pow(self.y, u2, self.p)

        v  = (gu1 * yu2) % self.q

        return v == r

if __name__ == "__main__":
    
    d = DSA()
    
    m = b"Hello"

    r, s = d.sign(m)

    print(d.verify(m, r, s))