import sys ; sys.path += ['.', '../..']
from SharedCode import Function

"""
>>> Implement a SHA-1 keyed MAC
"""

key = Function.Encryption.AES.randomKeyBase64()

def task28():
    message = b"Meet me by the dock at dawn"

    mac = Function.SHA_MAC.create(key, message)

    # Should be correct
    if Function.SHA_MAC.verify(key, message, mac):
        print("MAC Correct!")
    else:
        print("MAC Incorrect!")

    # Change to message
    message = b"Meet me by the dock at noon"

    # Should be incorrect
    if Function.SHA_MAC.verify(key, message, mac):
        print("MAC Correct!")
    else:
        print("MAC Incorrect!")

if __name__ == "__main__":
    task28()


