import sys ; sys.path += ['.', '../..']
from SharedCode import Function
from CryptoCode.MD4 import MD4


md4 = MD4(b"HelloThisIsACollision")


# Condition:
# a[1][6] = b[0][6]

# calculate the new value for a[1] in the normal fashion
md4.nextStep()

A_16 = md4.getBitIndexOfSection(md4.A, 1, 5)
B_06 = md4.getBitIndexOfSection(md4.B, 0, 5)

md4.A[1] ^= ((A_16 ^ B_06) << 6)


m0 = int(md4.messageChunks[0], 2)

m0 ^= MD4.LeftRotate(md4.A[1], 3) \
    - md4.A[0] - MD4.F(md4.B[0], md4.C[0], md4.D[0])

md4.messageChunks[0] = bin(m0)[2:].zfill(512)
print()

