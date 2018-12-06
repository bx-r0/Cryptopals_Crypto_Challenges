import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
import Function
import random
import base64

"""
>>> The CBC padding oracle attack
"""



# Assume this is a securely shared key
key = Function.Encryption.AES.randomKeyBase64()

def decryptAndCheckPadding(cipherText):
    """
    >>> Padding Oracle

    Decrypts the data and validates padding.
    Assume this method takes the role of a server consuming ciphertext and returning
    a message on the validity of the padding. The side channel information that is
    returned by the oracle can be used to decrypt the plaintext
    """

    blocks = Function.Encryption.splitBase64IntoBlocks(cipherText)
    iv = blocks[0]
    cipherText = Function.Base64_To.concat(blocks[1:])

    plainText = Function.Encryption.AES.CBC.Decrypt(iv, key, cipherText)

    return Function.Encryption.PKCS7.isValidBase64Bool(plainText)
def selectStringAndEncrypt(data, force_line=None):
    """
    >>> Client

    Randomly selects a line from the data.txt encrypts with a random key
    and appends the IV to it.
    Assume this method takes the form of the valid user sending over an encrypted cookie.
    """


    iv = Function.Encryption.AES.randomKeyBase64()

    # Randomly selects a line
    rndIndex = random.randint(0, len(data) - 1)

    # For testing purposes
    if force_line is not None:
        rndIndex = force_line

    line = data[rndIndex]

    linePadded = Function.Encryption.PKCS7.addBase64(line)

    cipherText = Function.Encryption.AES.CBC.Encrypt(iv, key, linePadded)

    return Function.Base64_To.concat([iv, cipherText])

def findPaddingLength(cipherText):
    """
    Discovers the padding length of the cipher text.
    It works by affecting the penultimate bytes to therefore affect the byte with padding.
    If a byte containing padding is corrupted we can therefore determine where the padding starts
    and therefore how long it is
    """

    # Discover padding length
    targetBlock = -2
    
    # Works it way through the entire byte
    for x in range(16):

        blocks = Function.Encryption.splitBase64IntoBlocks(cipherText)
        blockBytes = Function.Encryption.splitBase64IntoBlocks(blocks[targetBlock], 1)
        
        # Random change to that byte
        blockBytes[x] = Function.XOR.b64_Xor(blockBytes[x], base64.b64encode(b"x"))

        # Saves any changes made to the blocks
        blocks[targetBlock] = Function.Base64_To.concat(blockBytes)
        cipherTextPrime = Function.Base64_To .concat(blocks)

        if not decryptAndCheckPadding(cipherTextPrime):
            return 16 - x

def extendPadding(cipherText, paddingLen, currentChars):
    """
    Extends the padding for the setup of a new brute force.
    
    It will take cipher text that produces the plaintext:

    >>> "XXXX XX\x02\x02"

    And turn it into:

    >>> "XXXX XA\x03\x03" 

    To set it up for the brute force of A
    """


    # No padding extension is needed
    if paddingLen == 0:
        return cipherText

    cipherTextBytes = Function.Encryption.splitBase64IntoBlocks(cipherText, blocksize=1)

    # newPaddingChar is just the next increment of the current pad
    newPaddingChar = chr(paddingLen + 1).encode('utf-8')
    currentChars = currentChars[::-1] # Flips the list

    # Works it's way across all the padding value
    for offset in range(1, paddingLen + 1):

        # +16 is to move it to the previous block
        targetByte = -(offset + 16)

        # Manipulates bytes to be a higher padding value
        xor = Function.XOR.b64_Xor(cipherTextBytes[targetByte], base64.b64encode(currentChars[offset - 1]))
        cipherTextBytes[targetByte] = Function.XOR.b64_Xor(xor, base64.b64encode(newPaddingChar))

        cipherTextPrime = Function.Base64_To.concat(cipherTextBytes)

    return cipherTextPrime

def discoverPlainTextByte(cipherText, paddingLen):
    """
    Discovers the byte that gives valid padding
    For example if the last blocks plaintext (8 bytes) is manipulated to be:

        "XXXX XA\x03\x03"

    We can brute force A in attempt to try and get \x03 as the result. If we do the padding will
    be correct as determined by the oracle
    """


    newPaddingCharB64 = base64.b64encode(chr(paddingLen + 1).encode('utf-8'))

    originalCipherTextBytes = Function.Encryption.splitBase64IntoBlocks(cipherText, 1)

    # Tries all combinations of values
    for i in range(0, 256):
        cipherTextBytes = Function.Encryption.splitBase64IntoBlocks(cipherText, 1)

        # Grabs the byte we're going to bruteforce
        targetByteIndex = (len(cipherTextBytes) - 1) - paddingLen - 16

        # Encodes the char as a base64 value
        valueBase64 = base64.b64encode(chr(i).encode("utf-8"))

        # Makes changes to the bytes
        xor = Function.XOR.b64_Xor(newPaddingCharB64, valueBase64)
        cipherTextBytes[targetByteIndex] = Function.XOR.b64_Xor(cipherTextBytes[targetByteIndex], xor)

        # Creates a new cipher text C'
        cipherTextPrime = Function.Base64_To.concat(cipherTextBytes)

        if decryptAndCheckPadding(cipherTextPrime):

            # We known that our new Cipher text (C') and out new paintext (Padding (P)) XOR together to make
            # the intermediate cipher text (I)
            intermidate = Function.XOR.b64_Xor(cipherTextBytes[targetByteIndex], newPaddingCharB64)

            # This intermediate value then xored with the original ciphertext gives us the plaintext value
            char = base64.b64decode(Function.XOR.b64_Xor(intermidate, originalCipherTextBytes[targetByteIndex]))

            return char

    raise(Exception("Cannot find the next byte!"))

def removeLastBlock(cipherText):
    """
    Chops off the last block of the ciphertext
    """

    t = Function.Encryption.splitBase64IntoBlocks(cipherText)[:-1]
    return Function.Base64_To.concat(t)

def task17(cipherTextTestInput=None):

    data = Function.File.loadLines(__file__)

    answer = []

    # For testing purposes
    if cipherTextTestInput is not None:
        data = [cipherTextTestInput]

    cipherText = selectStringAndEncrypt(data)
    numberOfCipherTextBlocks = len(Function.Encryption.splitBase64IntoBlocks(cipherText))

    discoveredBytesFromBlock = b""

    # Finds the padding length by working it's way through manipulating bits until there is an error
    # Once there is an error you can determin the first bit of the padding and thus its length
    paddingLen = findPaddingLength(cipherText)

    # Generates all the discovered paddings
    discoveredBytesFromBlock = [chr(paddingLen).encode('utf-8')] * paddingLen

    # If the entire last block is padding remove it
    if paddingLen == 16:
        paddingLen = 0
        cipherText = removeLastBlock(cipherText)

        answer += discoveredBytesFromBlock
        discoveredBytesFromBlock = []

        # Reduce the number of blocks we need to search through
        numberOfCipherTextBlocks -= 1

    # Works through all blocks left to discover
    # Minus one for the iv
    for _ in range(0, numberOfCipherTextBlocks - 1):

        # Loops round for a complete block
        for _ in range(0, 16  - paddingLen):
            
            # Increments the padding so we can extend it and create a new valid pad
            # When the valid pad is created after the brute force, we will have discovered a byte of the plaintext
            paddingExtended = extendPadding(cipherText, paddingLen, discoveredBytesFromBlock)
            discoveredBytesFromBlock.insert(0, discoverPlainTextByte(paddingExtended, paddingLen))
            paddingLen += 1

        # When padding is 16, reset and chop of the end of the cipher text
        cipherText = removeLastBlock(cipherText)
        paddingLen = 0
        answer = discoveredBytesFromBlock + answer
        discoveredBytesFromBlock = []


    resultString = b"".join(answer)
    resultString = Function.Encryption.PKCS7.isValid(resultString.decode('utf-8'))
    return resultString

if __name__ == "__main__":
    print(task17())
