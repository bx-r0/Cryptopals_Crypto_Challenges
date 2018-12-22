import sys ; sys.path += ['.', '../..']
from CryptoCode import MT19937 as M
from SharedCode import Function
from random import randint
import base64

# Generation methods
def generateRandomSeed():
    # Generates a 16 bit value
    return randint(0, 65535)
def generatePlainText(message):
    """
    Prepends and random number of characters
    """

    characterLen = randint(1, 100)

    # Ascii range
    low = 97
    high = 122

    string = b""
    for _ in range(characterLen):
        string += bytes([(randint(low, high))])

    return string + message

def PRNG_Stream_Generation(PRNG, byteLength):
    """
    Generates a key stream of a specific length
    """

    def MTOuputToBase64BytesList(integer):
        """
        Returns a list with 4 base64 encoded bytes from a 32 bit integer
        """

        hexValue = hex(integer)[2:]

        # Makes sure it is 4 bytes
        hexValue = hexValue.zfill(8)

        base64Value = Function.HexTo.base64(hexValue)

        # Splits value into bytes
        return Function.Encryption.splitBase64IntoBlocks(base64Value, 1)

    # Each generation of a value produces 4 bytes
    numberOfGenerations = round(byteLength / 4)

    # If not an exact match we need to generate more
    if byteLength % 4 != 0:
        numberOfGenerations += 1

    diff = abs((numberOfGenerations * 4) - byteLength)

    # Converts the output of the PRNG into a list of base64 values
    values = []
    for _ in range(numberOfGenerations):
        randomNumber = PRNG.getInt()
        values += MTOuputToBase64BytesList(randomNumber)

    # Stips of any needless remainder
    values = values[:len(values) - diff]

    return values

def encrypt(PRNG, message):

    plainText = base64.b64encode(message)
    plainTextBytesLen = len(Function.Encryption.splitBase64IntoBlocks(plainText, 1))

    streamBytes = PRNG_Stream_Generation(PRNG, plainTextBytesLen)
    stream = Function.Base64_To.concat(streamBytes)

    cipherText = Function.XOR.b64_Xor(plainText, stream)

    return cipherText

def bruteForceSeed(targetBytes):
    """
    Because stream ciphers work byte-by-byte we can just compare the position
    of our chosen plaintext. The method works through all 16 bit seed values
    and checks for the output at the position of our payload. If they match the seed is found
    """

    # Allows recreation of a cipher text with a similar length later
    targetBytesLen = len(targetBytes)

    payloadStartPosition =  targetBytesLen - 14

    # Brute force of the seed
    for seed in range(0, 65535):
        newMT = M.MT19937(seed)

        # Places Xs where the random data is
        # and A's where the orginal payload was placed
        plainText = (b"X" * (targetBytesLen - 14)) + (b"A" * 14)

        newEncryptedBytes = Function.Encryption.splitBase64IntoBlocks(encrypt(newMT, plainText), 1)

        # Just count the last 14 bytes of the ciphertext
        targetBytesPayload = targetBytes[payloadStartPosition:]
        newEncryptedBytes = newEncryptedBytes[payloadStartPosition:]

        if targetBytesPayload == newEncryptedBytes:
            return seed
    
    # Should not occur!
    raise Exception("No seed value found!")

def task24(seed):
    m = M.MT19937(seed)

    e = encrypt(m, generatePlainText(b"A" * 14))
    cipherTextBytes = Function.Encryption.splitBase64IntoBlocks(e, blocksize=1)

    seed = bruteForceSeed(cipherTextBytes)
    return seed

if __name__ == "__main__":
    seed = generateRandomSeed()
    foundSeed = task24(seed)

    print(f"Seed found: {foundSeed}")