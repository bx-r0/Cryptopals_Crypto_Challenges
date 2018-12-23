import sys ; sys.path += ['.', '../..']
from bitstring import BitArray
from SharedCode import Function
from CryptoCode.MD4 import MD4
from CryptoCode.MAC import MAC
import struct
import base64

"""
>>> Break an MD4 keyed MAC using length extension
"""

#TODO - Add a randomisation of key from a dictionary
key = base64.b64encode(b"christmas")

message = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
appendString =b";admin=true"

def computePadding(message):
    """
    Computes the 'glue padding' for a message
    """

    messageBinary = BitArray(bytes=message).bin

    padding = MD4.addPadding(messageBinary, len(messageBinary))[len(messageBinary):]

    paddingStr = Function.BinaryTo.byteString(padding)

    return paddingStr

def convertRegisterToInt(registerBase64):
    """
    Converts the recovered register values from the resultant hash
    """

    return int(Function.Base64_To.hexadecimal(registerBase64), 16)

def task30():

    # Tries differnt lengths of keys
    for keyGuess in range(100):

        # Content of key does not matter, just its length
        messagePadding = computePadding(b"A" * keyGuess + message)

        # Grabs the original Mac
        mac = MAC.MD4.create(key, message)

        # Breaks into 32bit registers to recover the state of the
        # MD when the hashing finished
        # The hash is a little endian packed value
        registersInts = struct.unpack("<IIII", base64.b64decode(mac))

        # New message including the padding
        forgedMessage = message + messagePadding + appendString

        newMac = MD4.createDigest(appendString,
                            ml=(keyGuess + len(forgedMessage)) * 8,  
                            A=registersInts[0],
                            B=registersInts[1],
                            C=registersInts[2],
                            D=registersInts[3])
        
        if MAC.MD4.verify(key, forgedMessage, newMac): 
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
    task30()
