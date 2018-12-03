import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
import Function
import base64
from Crypto.Cipher import AES

"""
>>> Byte-at-a-time ECB decryption (Simple)
"""

# Random key - this shouldn't be viewable
key = "M2Xmd7qkM31QFOKtwaHJbg=="

# Added to the plain text before encryption
appendString = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"


def createEncryption(pt):
    """
    Method that appends our chosen plaintext to the front of the provided plaintext
    """

    #Creates input data
    data = base64.b64encode(pt + base64.b64decode(appendString))

    # Encrypts the data
    e = Function.Encryption.AES.ECB_Encrypt(base64.b64decode(key), data)

    return e

def task12():

    # Determines how many blocks the original data hass
    noChosenPlaintextBlocks = Function.Encryption.split_base64_into_blocks(createEncryption(b""), 16)

    # Decrypted answer
    discoveredBytes = b""

    # Creates the values for the chosen plaintext
    # Ranging of values of "A" from 1 --> 15
    preComputedBlocks = []
    for length in range(0, 16):
        e = createEncryption(b"A" * length)
        preComputedBlocks.append(Function.Encryption.split_base64_into_blocks(e, 16))

    # Discovers all the blocks
    for x in range(0, len(noChosenPlaintextBlocks)):

        # Brute force a single block
        # Goes from 15 -> 0 (Number of A's)
        for ptLen in reversed(range(0, 16)):

            # Grabs the block we're looking for
            target = preComputedBlocks[ptLen][x]

            # Brute forces the single byte
            for byteChoice in range(0, 255):

                # Adds together chosen plaintext and previously discovered bytes
                # plus the brute force attempt
                plainText = (b"A" * ptLen) + discoveredBytes + bytes([byteChoice])

                # Encrpts and obtains the block
                e = Function.Encryption.AES.ECB_Encrypt(base64.b64decode(key), base64.b64encode(plainText))
                testBlocks = Function.Encryption.split_base64_into_blocks(e, 16)

                # If the blocks match, we've found the value!
                if testBlocks[x] == target:
                    discoveredBytes += bytes([byteChoice])
                    break

    # Removes padding if any
    discoveredBytes = discoveredBytes.decode('utf-8').rstrip("\x00")

    return discoveredBytes


if __name__ == "__main__":
    answer = task12()
    print(answer)
