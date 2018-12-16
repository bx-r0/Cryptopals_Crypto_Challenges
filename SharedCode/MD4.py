import sys ; sys.path += ['.', '../..']
from bitstring import BitArray
from SharedCode import Function
import binascii
import struct
import re

class MD4():
    
    LeftRotate = lambda x, n: (x << n) | (x >> (32 - n))

    @staticmethod
    def createDigest(message, ml=None, A=0x67452301, B=0xefcdab89, C=0x98badcfe, D=0x10325476):

        # Functions
        F = lambda x, y, z: ((x & y) | (~x & z))
        G = lambda x, y, z: ((x & y) | (x & z) | (y & z))
        H = lambda x, y, z: (x ^ y ^ z)

         # Converts to binary
        messageBinary = BitArray(bytes=message).bin

        if ml is None:
            ml = len(messageBinary)

        # Adds padding
        messageBinary = MD4.addPadding(messageBinary, ml)

        chunks = Function.splitStringIntoChunks(messageBinary, size=512)

        # main loop
        for chunk in chunks:

            AA, BB, CC, DD = A, B, C, D

            # Splits into 16 words
            words = Function.splitStringIntoChunks(chunk, size=32)

            # Converts all the words to bytes
            wordBytes = []
            for w in words:
                wordBytes.append(Function.BinaryTo.byteString(w))

            # Converts all byte values into little endian integers
            x = list(map(lambda y: int.from_bytes(y, 'little'), wordBytes))
            
            for i in range(16):
                k = i

                if i % 4 == 0:
                    A = MD4.LeftRotate((A + F(B, C, D) + x[k]) & 0xffffffff, 3)
                elif i % 4 == 1:
                    D = MD4.LeftRotate((D + F(A, B, C) + x[k]) & 0xffffffff, 7)
                elif i % 4 == 2:
                    C = MD4.LeftRotate((C + F(D, A, B) + x[k]) & 0xffffffff, 11)
                elif i % 4 == 3:
                    B = MD4.LeftRotate((B + F(C, D, A) + x[k]) & 0xffffffff, 19)

            for i in range(16):
                k = (i // 4) + (i % 4) * 4

                if i % 4 == 0:
                    A = MD4.LeftRotate((A + G(B, C, D) + x[k] + 0x5a827999) & 0xffffffff, 3)
                elif i % 4 == 1:
                    D = MD4.LeftRotate((D + G(A, B, C) + x[k] + 0x5a827999) & 0xffffffff, 5)
                elif i % 4 == 2:
                    C = MD4.LeftRotate((C + G(D, A, B) + x[k] + 0x5a827999) & 0xffffffff, 9)
                elif i % 4 == 3:
                    B = MD4.LeftRotate((B + G(C, D, A) + x[k] + 0x5a827999) & 0xffffffff, 13)


            order = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
            for i in range(16):
                k = order[i]

                if i % 4 == 0:
                    A = MD4.LeftRotate((A + H(B, C, D) + x[k] + 0x6ed9eba1) & 0xffffffff, 3)
                elif i % 4 == 1:
                    D = MD4.LeftRotate((D + H(A, B, C) + x[k] + 0x6ed9eba1) & 0xffffffff, 9)
                elif i % 4 == 2:
                    C = MD4.LeftRotate((C + H(D, A, B) + x[k] + 0x6ed9eba1) & 0xffffffff, 11)
                elif i % 4 == 3:
                    B = MD4.LeftRotate((B + H(C, D, A) + x[k] + 0x6ed9eba1) & 0xffffffff, 15)


            A = (A + AA) & 0xffffffff
            B = (B + BB) & 0xffffffff
            C = (C + CC) & 0xffffffff
            D = (D + DD) & 0xffffffff

        hexHash = binascii.hexlify(struct.pack('<IIII', A, B, C, D)).decode()
        return Function.HexTo.base64(hexHash)

    @staticmethod
    def createDigestHex(message, ml=None, A=0x67452301, B=0xefcdab89, C=0x98badcfe, D=0x10325476):
        hashBase64 = MD4.createDigest(message, ml, A, B, C, D)
        hashHex = Function.Base64_To.hexadecimal(hashBase64)
        return Function.Conversion.remove_byte_notation(hashHex)

    @staticmethod
    def addPadding(messageBinary, messageLength):
        """
        Adds padding defined in the SHA1 specification
        """

        if len(messageBinary) % 8 == 0:
            messageBinary += "1"

        # Adds zeros until padding is 64 bits away from 512
        while len(messageBinary) % 512 != 448:
            messageBinary += "0"

        # Add 64 bit integer of the length to make the message a multiple of 512
        lengthBin = messageLength.to_bytes(8, "little")
        for b in lengthBin:
            messageBinary += format(b, "08b")
        
        return messageBinary
