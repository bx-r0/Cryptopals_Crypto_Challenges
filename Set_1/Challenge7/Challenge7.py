import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
from Crypto.Cipher import AES
import Function

key = "YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)


def load():

    data = ""
    with open("data.txt", 'r') as file:
        data = file.read()

    return data

data = load()

blocks = Function.split_into_bytes(data, 16)

plaintext = []
for x in blocks:
    plaintext.append(str(cipher.decrypt(x)))

pt = "".join(plaintext)
print(pt)