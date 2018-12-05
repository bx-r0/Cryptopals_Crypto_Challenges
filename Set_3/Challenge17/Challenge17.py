import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
import Function
import random
import base64

paddingCharB64 = base64.b64encode("\x04".encode('utf-8'))

data = Function.File.loadLines(__file__)

# Assume this is a securly shared key
key = Function.Encryption.AES.randomKeyBase64()

def decryptAndCheckPadding(iv, cipherText):

    plainText = Function.Encryption.AES.CBC_Decrypt(iv, key, cipherText)

    t = base64.b64decode(plainText)

    return Function.Encryption.PKCS7.isValidBase64Bool(plainText)

def selectStringAndEncrypt(data):

    iv = Function.Encryption.AES.randomKeyBase64()

    # Randomly selects a line
    rndIndex = random.randint(0, len(data) - 1)
    line = data[rndIndex]

    linePadded = Function.Encryption.PKCS7.addBase64(line)

    print(base64.b64decode(linePadded))

    cipherText = Function.Encryption.AES.CBC_Encrypt(iv, key, linePadded)

    return iv, cipherText

def task17():

    discoveredBytes = b""

    iv, cipherText = selectStringAndEncrypt(data)

    targetPosition = -2

    for b in reversed(range(1, 16)):
        # Trys all byte combinations
        for x in range(1, 255):

            # Breaks ciphertext into blocks 
            blocks = Function.Encryption.splitBase64IntoBlocks(cipherText)

            # Breaks down a chosen block into bytes
            byteList = Function.Encryption.splitBase64IntoBlocks(blocks[targetPosition], 1)

            # Xors the byte with the random test value
            char64 = base64.b64encode(bytes([x]))
            xor = Function.XOR.b64_Xor(byteList[b], char64)
            byteList[b] = xor

            # Assigns the new bytes back to the block
            blocks[targetPosition] = Function.Base64_To.concat(byteList)

            # Creates the cipher text from all the block
            cipherText = Function.Base64_To.concat(blocks)

            # If valid padding has been created we've found our 
            if decryptAndCheckPadding(iv, cipherText):
                c = Function.XOR.b64_Xor(char64, paddingCharB64)
                discoveredBytes += base64.b64decode(c)
                break
            else:
                pass

    print(discoveredBytes[::-1])

if __name__ == "__main__":
    task17()