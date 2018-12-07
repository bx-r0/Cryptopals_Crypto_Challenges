import sys ; sys.path += ['.', '../..']
import Function
import base64

# Stops output being produced when tests are being run
output = False

# Terminal colours
class COLOURS:
    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

# Random key and IV are created on every execution
key = Function.Encryption.AES.randomKeyBase64()
iv = Function.Encryption.AES.randomKeyBase64()

def createString(userData):
    """
    Formats and encrypts our string
    """

    # Special characters are returned
    userData = userData.replace(';', '\;')
    userData = userData.replace('=', '\=')

    pre = "comment1=cooking%20MCs;userdata="
    post = ";comment2=%20like%20a%20pound%20of%20bacon"

    string = pre + userData + post

    if output: 
        print()
        print(f"Original Plaintext:\n{string}")

    # Adds padding and returns
    plaintext = Function.Encryption.PKCS7.add(string)

    # Encodes to base64 and returns
    return base64.b64encode(plaintext.encode('utf-8'))

def encrypt(key, data):
    return Function.Encryption.AES.CBC.Encrypt(iv, key, data)

def decrypt_and_admin_search(key, data):
    """
    Simulates granting access to the admin system
    """

    target = ";admin=true;"
    
    d = Function.Encryption.AES.CBC.Decrypt(iv, key, data)

    plainTextWithPadding = base64.b64decode(d)

    if output:
        print()
        print(f"Plaintext:\n {plainTextWithPadding}")

    if target in str(plainTextWithPadding):
        return True
    else:
        return False


def flip(currentVal, currentChar, targetChar):

    currentValHex = Function.Base64_To.hexadecimal(currentVal)

    # XORs the values to produce the bit change
    xor = hex(int(currentValHex, 16) ^ ord(currentChar) ^ ord(targetChar))[2:]

    return Function.HexTo.base64(xor)

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
    chars[0] = flip(chars[0], ":", ";")
    chars[6] = flip(chars[6], ":", "=")
    chars[11] = flip(chars[11], ":", ";")
   
    blocks[targetBlock] = Function.Base64_To.concat(chars)

    return Function.Base64_To.concat(blocks)

def task16():

    # Creates the string with placeholders
    data = createString(":admin:true:")
    cipherText = bitflip(encrypt(key, data))

    # If the encrypted text contains our ";admin=true;" string we have access
    if decrypt_and_admin_search(key, cipherText):
        if output: print(COLOURS.GREEN + "Access granted!" + COLOURS.RESET)
        return True
    else:
        if output: print(COLOURS.RED + "Access denied!" + COLOURS.RESET)
        return False

if __name__ == "__main__":
    output = True
    task16()
    