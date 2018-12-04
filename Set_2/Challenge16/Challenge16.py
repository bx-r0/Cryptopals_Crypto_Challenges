import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
import Function


key = Function.Encryption.AES.Random_Key_Base64()
iv = Function.Encryption.AES.Random_Key_Base64()

def createString(userData):
    pre = "comment1=cooking%20MCs;userdata="
    post = ";comment2=%20like%20a%20pound%20of%20bacon"

    string = pre + userData + post

    return Function.Encryption.PKCS7.add(16, string)

def encrypt(key, data):
    e = Function.Encryption.AES.CBC_Encrypt(iv, key, data)
    

def decrypt():
    pass

def task16():
    r = createString("money%20money%20money")

    pass

if __name__ == "__main__":
    task16()