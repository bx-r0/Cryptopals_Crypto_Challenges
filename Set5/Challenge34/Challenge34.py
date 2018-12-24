import sys ; sys.path += ['.', '../..']
from CryptoCode.DiffieHellman import DiffieHellman
from SharedCode import Function
from SharedCode.BaseParty import BaseParty
import base64

"""
>>> Implement a MITM key-fixing attack on Diffie-Hellman with parameter injection
"""

#----------------------------------------------
# Party A
#----------------------------------------------
class PartyA(BaseParty):

    def step1(self, data):
        # A sets p and g
        p = 64762727
        g = 2

        self.DH = DiffieHellman(p, g)

        return [self.DH.p, self.DH.g, self.DH.X]
    
    def step2(self, data):
        """
        A will recieve B_PubKey and return AES Rand CBC
        with key
        """

        # Generates the shared key
        B = data[0]
        self.key = Function.Encryption.splitBase64IntoBlocks(self.DH.GenKey(B))[0]

        # Generate random IV 
        iv = Function.Encryption.AES.randomKeyBase64()

        msg = base64.b64encode(b"Hello anyone there?")

        cipherText = Function.Encryption.AES.CBC.Encrypt(iv, self.key, msg)

        # Appends the IV
        cipherText = Function.Base64_To.concat([cipherText, iv])

        return cipherText

    def step3(self, data):
        
        cipherTextAndIV = data[0]\

        plaintext = self.decryptCipherAndIV(cipherTextAndIV, self.key)

        self.PRINT(plaintext)

#----------------------------------------------
# Party B
#----------------------------------------------
class PartyB(BaseParty):

    def step1(self, data):
        """
        B recieves p, g, A in a list
        """
        p = data[0]
        g = data[1]
        A = data[2]

        B = DiffieHellman(p, g)

        # Truncates and saves key
        self.key = Function.Encryption.splitBase64IntoBlocks(B.GenKey(A))[0]

        return B.X

    def step2(self, data):

        # Obtains data passed in
        cipherAndIV = data[0]

        # Prints the message from A
        self.PRINT(self.decryptCipherAndIV(cipherAndIV, self.key))

        newCipherText = self.encryptMessage(b"Yes, it's me Andrew!", self.key)

        return newCipherText

#----------------------------------------------
# MITM
#----------------------------------------------
class PartyM(BaseParty):

    def step1(self, data):

        # Saved for later
        self.p = data[0]
        g = data[1]

        # Repacks the data but without A
        return [self.p, g, self.p]

    def step2(self, data):

        # Ignores B and returns p instead
        return [self.p]

    # A encyption relay
    def step3(self, data):
        cipherTextAndIV = data[0]

        # The key is just the hash of zero
        # This is due to:
        #    p^x % p == 0
        self.key = Function.Encryption.splitBase64IntoBlocks(DiffieHellman.hSHA256(0))[0]

        plainText = self.decryptCipherAndIV(cipherTextAndIV, self.key)

        self.PRINT(plainText)

        # Relay
        return data

    # B encryption relay
    def step4(self, data):
        cipherTextAndIV = data[0]

        plaintext = self.decryptCipherAndIV(cipherTextAndIV, self.key)

        self.PRINT(plaintext)

        # relay
        return data



def regularCommunication():
    print("\n## [Regular communication] ##\n")

    # Creates the party objects
    A, B = PartyA(), PartyB()

    # A -> B
    #   Send "p", "g", "A"
    B_pubKey = B.run(1, A.run(1, []))

    # B -> A
    #   Send "B"
    A_encryption = A.run(2, [B_pubKey])

    # A -> B
    #   Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
    B_encryption = B.run(2, [A_encryption])

    # B -> A
    #   Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
    A.run(3, [B_encryption])

def MITM_KeyFixing():
    print("\n## [MITM Key Fixing] ##\n")

    # Everything before will be relayed through M
    A, B, M = PartyA(), PartyB(), PartyM()

    # A -> M
    #   Send "p", "g", "A"
    # M -> B
    #   Send "p", "g", "p"
    B_pubKey = B.run(1, M.run(1, A.run(1, [])))

    # B -> M
    #   Send "B"
    # M -> A
    #   Send "p"
    A_encryption = A.run(2, M.run(2, [B_pubKey]))

    # A -> M -> B
    #   Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
    B_encryption = B.run(2, M.run(3, [A_encryption]))

    # B -> M -> A
    #   Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
    A.run(3, M.run(4, [B_encryption]))

def task34():
    regularCommunication()
    MITM_KeyFixing()

if __name__ == "__main__":
    task34()
    