import sys ; sys.path += ['.', '../..']
from CryptoCode.DiffieHellman import DiffieHellman

if __name__ == "__main__":

    # Simulates the two parties exchanging values
    A = DiffieHellman()
    B = DiffieHellman()

    keyA = A.GenKey(B.X)
    keyB = B.GenKey(A.X)

    print(keyA)
    print(keyB)