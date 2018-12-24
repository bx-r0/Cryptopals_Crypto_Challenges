import sys ; sys.path += ['.', '../..']
from CryptoCode.DiffieHellman import DiffieHellman
from SharedCode import Function
from SharedCode.BaseParty import BaseParty
import base64

"""
>>> Implement DH with negotiated groups, and break with malicious "g" parameters
"""

#----------------------------------------------
# Party A
#----------------------------------------------
class PartyA(BaseParty):

    def step1(self, data):

        # Create a value of p and g
        self.p = 647464
        self.g = 2

        return [self.p, self.g]

    def step2(self, data):
        self.DH = DiffieHellman(self.p, self.g)

        # Returns the public key
        return [self.DH.X]

    def step3(self, data):

        B = data[0]

        self.key = self.genAESKey(self.DH, B)

        # Encrypt a message
        msg = b"Meet me by the dock in 1 hour."

        return [self.encryptMessage(msg, self.key)]

    def step4(self, data):

        cipherTextAndIV = data[0]
        
        plainText = self.decryptCipherAndIV(cipherTextAndIV, self.key)

        self.PRINT(plainText)

#----------------------------------------------
# Party B
#----------------------------------------------
class PartyB(BaseParty):

    def step1(self, data):

        self.p = data[0]
        self.g = data[1]

        # Simulate a valid check of p and g
        self.PRINT("ACK")

    def step2(self, data):

        A = data[0]

        self.DH = DiffieHellman(self.p, self.g)
        self.key = self.genAESKey(self.DH, A)

        # Returns public key
        return [self.DH.X]

    def step3(self, data):

        cipherTextAndIV = data[0]

        msgFromA = self.decryptCipherAndIV(cipherTextAndIV, self.key)
        self.PRINT(msgFromA)

        msg = b"Okay. I'll meet you there."

        return [self.encryptMessage(msg, self.key)]

#----------------------------------------------
# MITM
#----------------------------------------------
class PartyM(BaseParty):
    
    def __init__(self, attackID):
        self.attackID = attackID

    def step1(self, data):
        p = data[0]
        g = data[1]

        # g = 1
        if self.attackID == 0:
            g = 1
        elif self.attackID == 1:
            g = p
        elif self.attackID == 2:
            g = p - 1

        return [p, g]

    def step2(self, data):

        A = data[0]

        A = 1

        return [A]

    def step3(self, data):
        # A recieving B public key

        # The public key for A is changed to be 1 
        # so the key for B is therfore always the hash of 1
        self.BKey = self.genAESKeyFromHash(1)
        self.AKey = None

        # g = 1
        if self.attackID == 0:

            # g = 1
            #
            # Key Calculation:
            #   1 % p = 1
            self.AKey = self.genAESKeyFromHash(1)

        # g = p
        elif self.attackID == 1:

            # g = p
            #
            # Key Calculation:
            #   p ^ x % p = 0
            self.AKey = self.genAESKeyFromHash(0)

        # g = p - 1
        elif self.attackID == 2:

            # g = p - 1
            #
            # Key Calculation:
            #   (p - 1) ^ x % p = 1
            # This is due to there always being 1 remainder
            self.AKey = self.genAESKeyFromHash(1)
            

        return data

    def step4(self, data):

        # Cipher text encrypted by A
        cipherTextAndIV = data[0]

        if self.AKey != None:
            # A --> B (cipherText)
            msg_for_b = self.decryptCipherAndIV(cipherTextAndIV, self.AKey)
            self.PRINT(msg_for_b)

        return data

    def step5(self, data):

        # Cipher text encrypted by B
        cipherTextAndIV = data[0]

        if self.BKey != None:
            # B --> A (cipherText)
            msg_for_a = self.decryptCipherAndIV(cipherTextAndIV, self.BKey)
            self.PRINT(msg_for_a)
        
        return data


def regularCommunication():

    print("\n## [Regular communication] ##\n")

    A, B = PartyA(), PartyB()

    # A -> B
    #   Send "p", "g"
    B.run(1, A.run(1, []))
    
    # A -> B
    #   Send "A"
    B_pubKey = B.run(2, A.run(2, [])) 

    # B -> A
    #   Send "B"
    cipherText_A = A.run(3, B_pubKey)

    # A -> B
    #   Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
    cipherText_B = B.run(3, cipherText_A)

    # B -> A
    #   Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
    A.run(4, cipherText_B)

def MITM(attackID):

    print("\n## [MITM Communication] ##\n")
    A, B, M = PartyA(), PartyB(), PartyM(attackID) 

    # A -> B
    #   Send "p", "g"
    B.run(1, M.run(1, A.run(1, [])))
    
    # A -> B
    #   Send "A"
    B_pubKey = B.run(2, M.run(2, A.run(2, [])))

    # B -> A
    #   Send "B"
    cipherText_A = A.run(3, M.run(3, B_pubKey))

    # A -> B
    #   Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
    cipherText_B = B.run(3, M.run(4, cipherText_A))

    # B -> A
    #   Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
    A.run(4, M.run(5, cipherText_B))

def task35():
    regularCommunication()

    # Performs the various attacks
    for x in range(3):
        MITM(x)

if __name__ == "__main__":
    task35()