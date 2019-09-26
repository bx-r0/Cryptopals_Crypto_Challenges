import sys ; sys.path += ['.', '../..']
from SharedCode.BaseParty import BaseParty
from CryptoCode.SRP import SRP
from CryptoCode.MAC import HMAC
from SharedCode import Function
import base64

"""
>>> Implement Secure Remote Password (SRP)
"""

username = "test"
password = "password"

#----------------------------------------------
# Client
#----------------------------------------------
class Client(BaseParty):


    def __init__(self, username, password):
        super().__init__()
        self.I = username
        self.P  = password
    
    # [C] & S
    #   Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
    def step1(self, data):

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

    # C
    #   Generate string xH=SHA256(salt|password)
    #   Convert xH to integer x somehow (put 0x on hexdigest)
    #   Generate S = (B - k * g**x)**(a + u * x) % N
    #   Generate K = SHA256(S)
    def step4(self, data):

        xH = Function.Hash.SHA256_Hex((str(self.salt) + self.P).encode('utf-8'))
        x = int(xH, 16)

        S = pow((self.B - self.k * pow(self.g, x, self.N)), (self.a + self.u * x), self.N)
        self.K = Function.Hash.SHA256_Hex(str(S).encode('utf-8'))


    # [C] -> S
    #   Send HMAC-SHA256(K, salt)
    def step5(self, data):

        keyBytes = base64.b64decode(Function.HexTo.base64(self.K))
        messageBytes = str(self.salt).encode('utf-8')

        # Creates the tag
        tagBase64 = HMAC.SHA.create(keyBytes, messageBytes)

        return [tagBase64, self.salt]

#----------------------------------------------
# Server
#----------------------------------------------
class Server(BaseParty):

    # C & [S]
    #   Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
    def step1(self, data):

        self.N = int(data[0])
        self.g = int(data[1])
        self.k = int(data[2])

        self.I = data[3]
        self.p = data[4]

        self.PRINT("ACK")
        return "ACK"

    # [S]
    #     Generate salt as random integer
    #     Generate string xH=SHA256(salt|password)
    #     Convert xH to integer x somehow (put 0x on hexdigest)
    #     Generate v=g**x % N
    #     Save everything but x, xH
    def step2(self, data):

        # Generates SRP object
        self.srp = SRP(self.I, self.p, self.N, self.g, self.k)

    # C -> [S]
    #   Send I, A=g**a % N (a la Diffie Hellman)
    def step3(self, data):
        
        I = data[0]
        self.A = data[1]

        #Check username
        if I != self.srp.I:
            raise("Incorrect username!")

    # [S] -> C
    #   Send salt, B=kv + g**b % N
    def step4(self, data):

        m = (str(self.A) + str(self.srp.B)).encode('utf-8')

        self.u = int(Function.Hash.SHA256_Hex(m), 16)

        return [self.srp.salt, self.srp.B]

    # S
    #   Generate S = (A * v**u) ** b % N
    #   Generate K = SHA256(S)
    def step5(self, data):
        S = pow((self.A * pow(self.srp.v, self.u, self.N)), (self.srp.b), self.N)

        self.K = Function.Hash.SHA256_Hex(str(S).encode('utf-8'))
        print("[C36]", self.K)


    # C -> [S]
    #   Send HMAC-SHA256(K, salt)
    def step6(self, data):
        tag = data[0]
        msg = data[1]

        keyBytes = base64.b64decode(Function.HexTo.base64(self.K))
        messageBytes = str(msg).encode('utf-8')
        
        verified = HMAC.SHA.verify(keyBytes, messageBytes, tag)

        if verified: 
            self.PRINT("OK")
            return "OK"
        else:
            return None


if __name__ == "__main__":
    
    C, S = Client(username, password), Server()

    # C & S
    #   Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
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


    # C -> S
    #   Send HMAC-SHA256(K, salt)
    # S -> C
    #   Send "OK" if HMAC-SHA256(K, salt) validates
    S.run(6, C.run(5))

   