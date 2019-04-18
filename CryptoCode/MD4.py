import sys
sys.path += ['.', '../..']
import struct
import binascii
from SharedCode import Function
from bitstring import BitArray

A_INIT = 0x67452301
B_INIT = 0xefcdab89
C_INIT = 0x98badcfe
D_INIT = 0x10325476




class MD4():

    @staticmethod
    def LeftRotate(m, n): return (m << n) | (m >> (32 - n))

    # Functions
    @staticmethod
    def F(x, y, z): return ((x & y) | (~x & z))
    @staticmethod
    def G(x, y, z): return ((x & y) | (x & z) | (y & z))
    @staticmethod
    def H(x, y, z): return (x ^ y ^ z)

    def __init__(self, message):
        self.messageBinary = BitArray(bytes=message).bin
        self.messageLength = len(self.messageBinary)

        # Pads the message
        self.messageBinary = MD4.addPadding(self.messageBinary, self.messageLength)
        self.messageChunks = Function.splitStringIntoChunks(self.messageBinary, size=512)

        # TODO: Make this work with multiple chunks?
        chunk = self.messageChunks[0]
        self.x = MD4.chunkToWordArray(chunk)

        self.A = []
        self.B = []
        self.C = []
        self.D = []

        self.A.append(A_INIT)
        self.B.append(B_INIT)
        self.C.append(C_INIT)
        self.D.append(D_INIT)

        self.step = 0

    def nextStep(self, stepJump=None):

        if not stepJump is None:
            self.step = stepJump
        else:
            self.step += 1

        print(f"MD4 Step now: {self.step}")

        A, B, C, D = MD4._round(A_INIT, B_INIT, C_INIT, D_INIT, self.x, maxStep=self.step)

        self.A.append(A)
        self.B.append(B)
        self.C.append(C)
        self.D.append(D)

    def fullHash(self):
        for x in range(48):
            self.nextStep()
        self.printSectorsAsHash()

    def printSectors(self):
        print(f"A: {self.A} - B: {self.B} - C: {self.C} - D: {self.D}")

    def printSectorsAsHash(self):

        A = (self.A[self.step] + A_INIT) & 0xffffffff
        B = (self.B[self.step] + B_INIT) & 0xffffffff
        C = (self.C[self.step] + C_INIT) & 0xffffffff
        D = (self.D[self.step] + D_INIT) & 0xffffffff

        print(MD4.sectorsToHexHashFormat(A, B, C, D))

    def getBitIndexOfSection(self, sector, step, index):

        sectorBin = bin(sector[step])
        return int(sectorBin[index])


    @staticmethod
    def createDigest(message, ml=None, A=A_INIT, B=B_INIT, C=C_INIT, D=D_INIT):

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

            m = MD4.chunkToWordArray(chunk)

            A,B,C,D = MD4._round(A,B,C,D, m)

            A = (A + AA) & 0xffffffff
            B = (B + BB) & 0xffffffff
            C = (C + CC) & 0xffffffff
            D = (D + DD) & 0xffffffff

        hexHash = MD4.sectorsToHexHashFormat(A, B, C, D)
        return Function.HexTo.base64(hexHash)

    @staticmethod
    def sectorsToHexHashFormat(A, B, C, D):
        return binascii.hexlify(struct.pack('<IIII', A, B, C, D)).decode()

    @staticmethod
    def chunkToWordArray(chunk):
        # Splits into 16 words
        words = Function.splitStringIntoChunks(chunk, size=32)

        # Converts all the words to bytes
        wordBytes = []
        for w in words:
            wordBytes.append(Function.BinaryTo.byteString(w))

        # Converts all byte values into little endian integers
        return list(map(lambda y: int.from_bytes(y, 'little'), wordBytes))

    @staticmethod
    def _round(A, B, C, D, m, maxStep=48):

        counter = 0

        for i in range(16):
            counter += 1
            if counter > maxStep: return A,B,C,D
            k = i

            if i % 4 == 0:
                A = MD4.LeftRotate((A + MD4.F(B, C, D) + m[k]) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = MD4.LeftRotate((D + MD4.F(A, B, C) + m[k]) & 0xffffffff, 7)
            elif i % 4 == 2:
                C = MD4.LeftRotate((C + MD4.F(D, A, B) + m[k]) & 0xffffffff, 11)
            elif i % 4 == 3:
                B = MD4.LeftRotate((B + MD4.F(C, D, A) + m[k]) & 0xffffffff, 19)

        for i in range(16):
            counter += 1
            if counter > maxStep: return A,B,C,D

            k = (i // 4) + (i % 4) * 4

            if i % 4 == 0:
                A = MD4.LeftRotate(
                    (A + MD4.G(B, C, D) + m[k] + 0x5a827999) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = MD4.LeftRotate(
                    (D + MD4.G(A, B, C) + m[k] + 0x5a827999) & 0xffffffff, 5)
            elif i % 4 == 2:
                C = MD4.LeftRotate(
                    (C + MD4.G(D, A, B) + m[k] + 0x5a827999) & 0xffffffff, 9)
            elif i % 4 == 3:
                B = MD4.LeftRotate(
                    (B + MD4.G(C, D, A) + m[k] + 0x5a827999) & 0xffffffff, 13)

        order = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        for i in range(16):
            counter += 1
            if counter > maxStep: return A,B,C,D

            k = order[i]

            if i % 4 == 0:
                A = MD4.LeftRotate(
                    (A + MD4.H(B, C, D) + m[k] + 0x6ed9eba1) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = MD4.LeftRotate(
                    (D + MD4.H(A, B, C) + m[k] + 0x6ed9eba1) & 0xffffffff, 9)
            elif i % 4 == 2:
                C = MD4.LeftRotate(
                    (C + MD4.H(D, A, B) + m[k] + 0x6ed9eba1) & 0xffffffff, 11)
            elif i % 4 == 3:
                B = MD4.LeftRotate(
                    (B + MD4.H(C, D, A) + m[k] + 0x6ed9eba1) & 0xffffffff, 15)

        print(counter)

        return A, B, C, D

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
