import sys ; sys.path += ['.', '../..']
import Function
import random

"""
>>> An ECB/CBC ECB_Detectedion oracle
"""

# Random string created on RANDOM.org
data = "S2JLZ1lXbUhNamxwVWdYVHpTdGJUSzZYdWF1d3JxU1ZLYktnWVdtSE1qbHBVZ1hUelN0YlRLNlh1YXV3cnFTVg=="

def ModeChoice():
    """
    Method to determine CBC or ECB will be used
    """
    # 1 for CBC
    # 0 for ECB
    d = random.randint(0, 1)

    key = Function.Encryption.AES.randomKeyBase64()
    iv = Function.Encryption.AES.randomKeyBase64()

    if d is 1:
        e = Function.Encryption.AES.CBC.Encrypt(iv, key, data)
        mode = "CBC"
    else:
        e = Function.Encryption.AES.ECB.Encrypt(key, data)
        mode = "ECB"

    return e, mode

def ECB_or_CBC(cipherText):
    # Split data into blocks
    blocks = Function.Encryption.splitBase64IntoBlocks(cipherText, 16)
    ECB_Detected = Function.Encryption.AES.ECB.Detect(blocks)

    if ECB_Detected:
        return "ECB"
    else:
        return "CBC"

def task11():
    
    # Choses a mode and encrypts the data using it
    cipherText, mode = ModeChoice()

    # Grabs the guess
    mode_guess = ECB_or_CBC(cipherText)

    return mode, mode_guess

if __name__ == "__main__":
    task11()