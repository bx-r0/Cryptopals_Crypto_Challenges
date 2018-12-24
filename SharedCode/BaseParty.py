import sys ; sys.path += ['.', '../..']
from SharedCode import Function
from CryptoCode.DiffieHellman import DiffieHellman
import base64


class BaseParty():
    """
    Shared code for a Party class.
    This is used to simulate two entites communicating on a network connection
    """
    def __init__(self):
        self.options = {}

    def run(self, step, data):
        return self.options[step](data)

    def PRINT(self, msg):
        print(f"[{self.__class__.__name__}] > {msg}")

    @staticmethod
    def genAESKey(DH, X):
        return Function.Encryption.splitBase64IntoBlocks(DH.GenKey(X))[0]
        
    @staticmethod
    def genAESKeyFromHash(msg):

        msgHash = DiffieHellman.hSHA256(msg)

        return Function.Encryption.splitBase64IntoBlocks(msgHash)[0]

    @staticmethod
    def decryptCipherAndIV(cipherAndIV, key):
        blocks = Function.Encryption.splitBase64IntoBlocks(cipherAndIV)

        # Obtains the values from the cipher text pair
        cipherText = Function.Base64_To.concat(blocks[:len(blocks) - 1])
        iv = blocks[-1]

        msg = Function.Encryption.AES.CBC.Decrypt(iv, key, cipherText)

        return base64.b64decode(msg)

    @staticmethod
    def encryptMessage(msgBytes, key):
        msg = base64.b64encode(msgBytes)

        # Generates random AES key
        iv = Function.Encryption.AES.randomKeyBase64()

        cipherText = Function.Encryption.AES.CBC.Encrypt(iv, key, msg)


        return Function.Base64_To.concat([cipherText, iv])
