import sys ; sys.path += ['.', '../..']
import Function
import base64

"""
>>> Implementation of CTR
"""

dataText = b"1234567812345678"

def task18():

    nonce = 0

    key = base64.b64encode(b"YELLOW SUBMARINE")

    # Full block of data
    data = base64.b64encode(dataText)

    e = Function.Encryption.AES.CTR.Encrypt_Decrypt(nonce, key, data)
    d = Function.Encryption.AES.CTR.Encrypt_Decrypt(nonce, key, e)

    return base64.b64decode(d)

