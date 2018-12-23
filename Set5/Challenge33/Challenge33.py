import sys ; sys.path += ['.', '../..']
from CryptoCode.DiffieHellman import DiffieHellman

if __name__ == "__main__":

    # A sets p and g
    p = 64762727
    g = 2

    # Simulates the two parties exchanging values
    A = DiffieHellman(p, g)
    B = DiffieHellman(p, g)

    keyA = A.GenKey(B.X)
    keyB = B.GenKey(A.X)

    print(keyA)
    print(keyB)