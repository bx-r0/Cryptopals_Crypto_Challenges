import sys ; sys.path += ['.', '../..']
from bitstring import BitArray
from SharedCode import Function
from SharedCode.SHA1 import SHA1
import base64
import re

"""
>>> Break a SHA-1 keyed MAC using length extension
"""

#TODO - Add a randomisation of key from a dictionary
key = base64.b64encode(b"lemonade")

message = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
appendString =b";admin=true"

def computePadding(message):
    """
    Computes the 'glue padding' for a message to continue the SHA1 process
    """

    messageBinary = BitArray(bytes=message).bin

    padding = SHA1.addPadding(messageBinary, len(messageBinary))[len(messageBinary):]

    # All 8 bits
    chunks = re.findall(r".{8}", padding)

    # Turns all the chunks into bytes
    paddingStr = b""
    for chunk in chunks:
        binaryValue = (int(chunk, 2))
        paddingStr += bytes([binaryValue])

    return paddingStr

def convertRegisterToInt(registerBase64):
    """
    Converts the recovered register values from the resultant hash
    """

    return int(Function.Base64_To.hexadecimal(registerBase64), 16)

def task29():

    # Tries differnt lengths of keys
    for keyGuess in range(100):

        # Content of key does not matter, just its length
        messagePadding = computePadding(b"A" * keyGuess + message)

        # Grabs the original Mac
        mac = Function.SHA_MAC.create(key, message)

        # Breaks into 32bit registers to recover the state of the
        # MD when the hashing finished
        registers = Function.Encryption.splitBase64IntoBlocks(mac, blocksize=4)
        registersInts = list(map(convertRegisterToInt, registers))

        # New message including the padding
        forgedMessage = message + messagePadding + appendString

        newMac = SHA1.createDigest(appendString,
                            ml=(keyGuess + len(forgedMessage)) * 8,  
                            h0=registersInts[0],
                            h1=registersInts[1],
                            h2=registersInts[2],
                            h3=registersInts[3],
                            h4=registersInts[4])
        
        if Function.SHA_MAC.verify(key, forgedMessage, newMac): 
            print()
            print(f"> KEY LENGTH: {keyGuess}")
            print("> FORGED MESSAGE:")
            print(forgedMessage)
            Function.COLOURS.printGreen("Forged MAC Verified!")
            break
        else:
            print(f"> KEY GUESS: {keyGuess} ", end="")
            Function.COLOURS.printRed("Forged MAC Rejected!")

if __name__ == "__main__":
    task29()