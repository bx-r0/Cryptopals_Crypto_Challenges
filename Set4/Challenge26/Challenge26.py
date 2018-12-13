import sys ; sys.path += ['.', '../..']
import Function
import base64

"""
>>> CTR Bitflipping
"""

# Random key
key = Function.Encryption.AES.randomKeyBase64()
nonce = 0

def encrypt(key, data):
    """
    Encrypts using CTR Mode
    """
    return Function.Encryption.AES.CTR.Encrypt_Decrypt(nonce, key, data)

def decrypt_and_admin_search(key, data):
    """
    Simulates granting access to the admin system
    """

    target = "admin=true"
    
    d = Function.Encryption.AES.CTR.Encrypt_Decrypt(nonce, key, data)

    plainTextWithPadding = base64.b64decode(d)

    return target in str(plainTextWithPadding)

def bitflip(cipherText):
    """
    Code that performs the actual bitflipping
    """
    
    # This is the same block as the plaintext will be
    targetBlock = 2

    blocks = Function.Encryption.splitBase64IntoBlocks(cipherText)

    # Splits the block into single byte Base64 values
    chars = Function.Encryption.splitBase64IntoBlocks(blocks[targetBlock], 1)

    # The same byte as the target flip
    chars[5] = Function.BitFlippingAttacks.flip(chars[5], ":", "=")
   
    blocks[targetBlock] = Function.Base64_To.concat(chars)

    return Function.Base64_To.concat(blocks)

def task26():

    # Creates the string with placeholders
    data = Function.BitFlippingAttacks.createString("admin:true")
    cipherText = bitflip(encrypt(key, data))

    # If the encrypted text contains our ";admin=true;" string we have access
    if decrypt_and_admin_search(key, cipherText):
        Function.BitFlippingAttacks.colouredOutput(access=True)
        return True
    else:
        Function.BitFlippingAttacks.colouredOutput(access=False)
        return False

if __name__ == "__main__":
    task26()
    