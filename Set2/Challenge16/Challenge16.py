import sys ; sys.path += ['.', '../..']
from SharedCode import Function
import base64

# Random key and IV are created on every execution
key = Function.Encryption.AES.randomKeyBase64()
iv = Function.Encryption.AES.randomKeyBase64()

def encrypt(key, data):
    return Function.Encryption.AES.CBC.Encrypt(iv, key, data)

def decrypt_and_admin_search(key, data):
    """
    Simulates granting access to the admin system
    """

    target = ";admin=true;"
    
    d = Function.Encryption.AES.CBC.Decrypt(iv, key, data)
    plainTextWithPadding = base64.b64decode(d)

    return target in str(plainTextWithPadding)

def bitflip(cipherText):
    
    # The block that contains the payload
    targetBlock = 1

    blocks = Function.Encryption.splitBase64IntoBlocks(cipherText)

    # Splits the block into single byte Base64 values
    chars = Function.Encryption.splitBase64IntoBlocks(blocks[targetBlock], 1)

    # The outcome value is determed by XORing the actual cipher text byte (A) with its previous plaintext
    #  value (PA) then applying the desired value (PD) 
    #  A' = A ⊕ PA ⊕ PD
    #       https://masterpessimistaa.wordpress.com/2017/05/03/cbc-bit-flipping-attack/
    chars[0] = Function.BitFlippingAttacks.flip(chars[0], ":", ";")
    chars[6] = Function.BitFlippingAttacks.flip(chars[6], ":", "=")
    chars[11] = Function.BitFlippingAttacks.flip(chars[11], ":", ";")
   
    blocks[targetBlock] = Function.Base64_To.concat(chars)

    return Function.Base64_To.concat(blocks)

def task16():

    # Creates the string with placeholders
    data = Function.BitFlippingAttacks.createString(":admin:true:")
    cipherText = bitflip(encrypt(key, data))

    # If the encrypted text contains our ";admin=true;" string we have access
    if decrypt_and_admin_search(key, cipherText):
        Function.BitFlippingAttacks.colouredOutput(access=True)
        return True
    else:
        Function.BitFlippingAttacks.colouredOutput(access=False)
        return False

if __name__ == "__main__":
    output = True
    task16()
    