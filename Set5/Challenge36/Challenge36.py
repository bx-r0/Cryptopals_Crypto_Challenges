import sys ; sys.path += ['.', '../..']
from SharedCode.BaseParty import BaseParty
from CryptoCode.SRP import SRP
from SharedCode import Function

"""
>>> Implement Secure Remote Password (SRP)
"""

# TODO - Issue with high 'pow()' calculations halting progress

#----------------------------------------------
# Server
#----------------------------------------------
class Client(BaseParty):
    
    # [C] & S
    #   Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
    def step1(self, data):

        self.I = "jDoe666"
        self.P  = "pa$$word"

        # Agrement for other variables

        # Large safe prime
        N = '''
        00c037c37588b4329887e61c2da332
        4b1ba4b81a63f9748fed2d8a410c2f
        c21b1232f0d3bfa024276cfd884481
        97aae486a63bfca7b8bf7754dfb327
        c7201f6fd17fd7fd74158bd31ce772
        c9f5f8ab584548a99a759b5a2c0532
        162b7b6218e8f142bce2c30d778468
        9a483e095e701618437913a8c39c3d
        d0d4ca3c500b885fe3
        '''

        self.N = int("".join(x.strip() for x in N.split("\n")), 16)
        self.g = 2
        self.k = 3

        return [self.N, self.g, self.k, self.I, self.P]

    # [C] -> S
    #   Send I, A=g**a % N (a la Diffie Hellman)
    def step2(self, data):

        self.a = SRP.randBits(1024)
        self.A = pow(self.g, self.a, self.N)

        return [self.I, self.A]
    
    # S -> [C]
    #   Send salt, B=kv + g**b % N
    def step3(self, data):
        
        self.salt = data[0]
        self.B = data[1]

        m = (str(self.A) + str(self.B)).encode('utf-8')

        uH = Function.Hash.SHA256_Hex(m)
        self.u = int(uH, 16)

        print()

    # C
    #   Generate string xH=SHA256(salt|password)
    #   Convert xH to integer x somehow (put 0x on hexdigest)
    #   Generate S = (B - k * g**x)**(a + u * x) % N
    #   Generate K = SHA256(S)
    def step4(self, data):

        xH = Function.Hash.SHA256_Hex((str(self.salt) + self.P).encode('utf-8'))
        x = int(xH, 16)

        l = self.B - self.k * pow(self.g, x)
        r = self.a + self.u * x

        S = pow(l, r, self.N)

        self.K = Function.Hash.SHA256_Hex(str(S).encode('utf-8'))

#----------------------------------------------
# Server
#----------------------------------------------
class Server(BaseParty):

    # C & [S]
    #   Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
    def step1(self, data):

        self.N = data[0]
        self.g = data[1]
        self.k = data[2]
        self.I = data[3]
        self.p = data[4]

        self.PRINT("ACK")

    # [S]
    #     Generate salt as random integer
    #     Generate string xH=SHA256(salt|password)
    #     Convert xH to integer x somehow (put 0x on hexdigest)
    #     Generate v=g**x % N
    #     Save everything but x, xH
    def step2(self, data):

        # Generates SRP object
        self.SRP = SRP(self.I, self.p, self.N, self.g, self.k)

    # C -> [S]
    #   Send I, A=g**a % N (a la Diffie Hellman)
    def step3(self, data):
        
        I = data[0]
        self.A = data[1]

        #Check username
        if I != self.SRP.I:
            raise("Incorrect username!")

    # [S] -> C
    #   Send salt, B=kv + g**b % N
    def step4(self, data):

        m = (str(self.A) + str(self.SRP.dPublic)).encode('utf-8')

        uH = Function.Hash.SHA256_Hex(m)

        self.u = int(uH, 16)

        return [self.SRP.salt, self.SRP.dPublic]

    # S
    #   Generate S = (A * v**u) ** b % N
    #   Generate K = SHA256(S)
    def step5(self, data):
        
        S = pow((self.A * pow(self.SRP.v, self.u)), (self.SRP.dPrivate), self.N)

        self.K = Function.Hash.SHA256_Hex(str(S).encode('utf-8'))


if __name__ == "__main__":
    
    # C & S
    #   Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
    C, S = Client(), Server()

    S.run(1, C.run(1))

    # S
    #     Generate salt as random integer
    #     Generate string xH=SHA256(salt|password)
    #     Convert xH to integer x somehow (put 0x on hexdigest)
    #     Generate v=g**x % N
    #     Save everything but x, xH
    S.run(2)

    #   C -> S
    # Send I, A=g**a % N (a la Diffie Hellman)
    S.run(3, C.run(2))

    #   S -> C
    # Send salt, B=kv + g**b % N
    C.run(3, S.run(4))

    # C
    #   Generate string xH=SHA256(salt|password)
    #   Convert xH to integer x somehow (put 0x on hexdigest)
    #   Generate S = (B - k * g**x)**(a + u * x) % N
    #   Generate K = SHA256(S)
    C.run(4)

    # S
    #   Generate S = (A * v**u) ** b % N
    #   Generate K = SHA256(S)
    S.run(5)

    print(S.K)
    print(C.K)