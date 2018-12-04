import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
import Function
import re

paddingChar = "\x04"
exceptionMessage = "Error: Invalid PKCS#7 padding"

def validPKCS7(string):
    """
    Validates valid PKCS7. If padding is valid it will return True and a stripped string
    No padding will be determined valid.
    On invalid padding the method will throw an exception
    """

    padding = []
    for char in reversed(string):

        # Should not having padding values that are higher than 16 in ascii
        if ord(char) < 16:
            padding.append(char)

    
    # Checks if the whole padding is the target char
    for pad in padding:
        if pad != paddingChar:
           raise(Exception(exceptionMessage))

    # Removes padding
    string = string.replace(paddingChar, "")

    return string

def task15():
    validPKCS7("ICE ICE BABY\x01\x02\x03\x04")

if __name__ == "__main__":
    task15()