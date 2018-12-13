import sys ; sys.path += ['.', '../..']
import Function
import base64

"""
>>> Recover the key from CBC with IV=Key
"""

# Message of 3 blocks length
plainText = b"Jo made the sugar cookies; Susan decorated them."

key = Function.Encryption.AES.randomKeyBase64()
iv = key  #IV is set to key!

def decrypt(iv, key, data):
    """
    Decrypts and checks for high ascii. If high ascii is found an error is returned 
    including the plaintext
    """
    d = Function.Encryption.AES.CBC.Decrypt(iv, key, data)

    pt = base64.b64decode(d)
    ptBlocks = Function.Encryption.splitBase64IntoBlocks(d)

    for char in pt:
        if char > 128:
            return True, ptBlocks

    return False, ptBlocks

def encrypt(iv, key, data):
    return Function.Encryption.AES.CBC.Encrypt(iv, key, data)

def attackerModification(data):
    """
    Changes to the cipher text occur here
    """

    dataBlocks = Function.Encryption.splitBase64IntoBlocks(data)

    # Makes seconds block zero
    # And last block the same as the first
    dataBlocks[1] = Function.XOR.b64_Xor(dataBlocks[1], dataBlocks[1])
    dataBlocks[2] = dataBlocks[0]

    # Recompiles
    data = Function.Base64_To.concat(dataBlocks)
    return data

def task27():
    e = encrypt(iv, key, base64.b64encode(plainText))

    # Bad stuff happens here
    e = attackerModification(e)

    # Decrypt returns error with plaintext
    _, ptBlocks = decrypt(iv, key, e)

    keyTest = Function.XOR.b64_Xor(ptBlocks[0], ptBlocks[2])

    print(f"Key is: {keyTest}")

if __name__ == "__main__":
    task27()