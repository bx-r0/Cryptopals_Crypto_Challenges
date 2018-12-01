import os
import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
from Crypto.Cipher import AES
import Function
import base64

key = "YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)

def load(path):

    data = ""
    with open(f"{path}/data.txt", 'r') as file:
        data = file.read()

    return data

def task7():
    # Reads in base64 data
    data = load(Function.getRealPath(__file__))

    # Will split into hexidecimal blocks from base64
    blocks = Function.Encryption.split_base64_into_blocks(data, 16)

    plaintext = []
    for x in blocks:
        block = base64.b64decode(x)
        #block = x

        c = cipher.decrypt(block)
        plaintext.append(Function.Conversion.remove_byte_notation(c))

    return "".join(plaintext)

if __name__ == "__main__":
    pt = task7()
    print(pt)