import sys ; sys.path += ['.', '../..']
from Crypto.Util import number

"""
>>> Implement RSA
"""

def gen_prime(size=2048):
    return number.getPrime(size)

def invmod(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def string_to_hex(string):
    return str.encode(string).hex()

def hex_to_string(hexStr):
    return bytearray.fromhex(hexStr).decode()

def encrypt(msg, public_key):
    m = int(string_to_hex(msg), 16)

    return pow(m, public_key[0], public_key[1])

def decrypt(c, private_key):

    m = pow(c, private_key[0], private_key[1])
    return hex_to_string(hex(m)[2:])

def create_keys():
    d = None
    while d == None:
        p = gen_prime(1024)
        q = gen_prime(1024)
        n = p * q
        e = 3
        et = (p - 1) * (q - 1)
        d = invmod(e, et)

    public_key = [e, n]
    private_key = [d, n]

    return public_key, private_key


if __name__ == "__main__":
    
    create_keys()