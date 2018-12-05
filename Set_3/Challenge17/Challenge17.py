import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
import Function
import random
import base64

data = Function.File.loadLines(__file__)

# Assume this is a securly shared key
key = Function.Encryption.AES.randomKeyBase64()

def decryptAndCheckPadding(cipherText, output=False):

    blocks = Function.Encryption.splitBase64IntoBlocks(cipherText)
    iv = blocks[0]
    cipherText = Function.Base64_To.concat(blocks[1:])

    plainText = Function.Encryption.AES.CBC_Decrypt(iv, key, cipherText)

    if output: print(base64.b64decode(plainText))

    return Function.Encryption.PKCS7.isValidBase64Bool(plainText)

def selectStringAndEncrypt(data, force_line=None):

    iv = Function.Encryption.AES.randomKeyBase64()

    # Randomly selects a line
    rndIndex = random.randint(0, len(data) - 1)
    if force_line is not None:
        rndIndex = force_line

    line = data[rndIndex]

    linePadded = Function.Encryption.PKCS7.addBase64(line)

    print(base64.b64decode(linePadded))

    cipherText = Function.Encryption.AES.CBC_Encrypt(iv, key, linePadded)

    return Function.Base64_To.concat([iv, cipherText])

def findPaddingLength(cipherText):
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

    #decryptAndCheckPadding(cipherTextPrime, True)

    return cipherTextPrime, newPaddingChar

def discoverPlainTextByte(cipherText, paddingLen):

    newPaddingCharB64 = base64.b64encode(chr(paddingLen + 1).encode('utf-8'))

    originalCipherTextBytes = Function.Encryption.splitBase64IntoBlocks(cipherText, 1)

    # Trys all combinations of values
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

            # This imtermidate value then xored with the original ciphertext gives us the plaintext value
            char = base64.b64decode(Function.XOR.b64_Xor(intermidate, originalCipherTextBytes[targetByteIndex]))

            return char

    raise(Exception("Cannot find the next byte!"))

def task17():

    # TODO - The cipher texts with no padding causes issues with the detection
    # lines : 4, 8
    cipherText = selectStringAndEncrypt(data, 6)

    discoveredBytes = b""

    # Finds the padding length by working it's way through manipulating bits until there is an error
    # Once there is an error you can determin the first bit of the padding and thus its length
    paddingLen = findPaddingLength(cipherText)
    
    # Generates all the discovered paddings
    discoveredBytes = [chr(paddingLen).encode('utf-8')] * paddingLen

    # Loops round for a complete block
    for _ in range(0, 16  - paddingLen):
        
        # Increments the padding so we can extend it and create a new vaild pad
        # When the valid pad is created after the brute force, we will have discovered a byte of the plaintext
        paddingExtended, _ = extendPadding(cipherText, paddingLen, discoveredBytes)
        discoveredBytes.insert(0, discoverPlainTextByte(paddingExtended, paddingLen))
        paddingLen += 1

    print(b"".join(discoveredBytes))

if __name__ == "__main__":
    task17()
