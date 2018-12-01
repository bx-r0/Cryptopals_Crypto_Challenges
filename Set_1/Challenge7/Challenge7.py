import os
import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
from Crypto.Cipher import AES
import Function
import base64

"""
>>> AES in ECB mode

    The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key

    "YELLOW SUBMARINE".

    (case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).

    Decrypt it. You know the key, after all.

    Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.
    Do this with code.

    >>> You can obviously decrypt this using the OpenSSL command-line tool, 
        but we're having you get ECB working in code for a reason. 
        You'll need it a lot later on, and not just for attacking ECB.

"""

key = "YELLOW SUBMARINE"

def AES_ECB_Decrypt(key, data):
    function = Function.Encryption.AES.ECB_Decrypt
    return Function.Encryption.AES.ECB(function, key, data)

def task7():
    # Reads in base64 data
    data = Function.File.LoadData(__file__)
    e =  AES_ECB_Decrypt(key, data)
    return e

if __name__ == "__main__":
    pt = task7()
    print(pt)