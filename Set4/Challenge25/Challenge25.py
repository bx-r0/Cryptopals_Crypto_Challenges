import sys ; sys.path += ['.', '../..']
import Function
import base64

key = Function.Encryption.AES.randomKeyBase64()
nonce = 0

def exposedAPI(ciphertext, offset, newtext):
    """
    Simulates the exposed API
    """

    return edit(ciphertext, key, offset, newtext)

def edit(ciphertext, key, offset, newtext):
    
    plainText = Function.Encryption.AES.CTR.Encrypt_Decrypt(nonce, key, ciphertext)
    plainTextBytes = Function.Encryption.splitBase64IntoBlocks(plainText, blocksize=1)

    plainTextBytes[offset] = newtext

    plainText = Function.Base64_To.concat(plainTextBytes)
    ciphertextNew = Function.Encryption.AES.CTR.Encrypt_Decrypt(nonce, key, plainText)

    return ciphertextNew

def produceCipherText():
     # Data isn't exactly the data from the website
    # It's the output from challeng 7
    # It didn't make sense for me to repeat the code from challenge 7
    
    # Load in the entire data - warning SLOW
    #data = Function.File.loadData(__file__)

    # Load a single line
    data = b"SSdtIGJhY2sgYW5kIEknbSByaW5naW4nIHRoZSBiZWxs"

    return Function.Encryption.AES.CTR.Encrypt_Decrypt(nonce, key, data)

def task25():

    cipherText = produceCipherText()
    cipherTextBytes = Function.Encryption.splitBase64IntoBlocks(cipherText, blocksize=1)

    offset = 0
    recoveredPlainText = b""

    while offset < len(cipherTextBytes):
        blockVal = round(offset / 16) + 1
        blockEnd = (blockVal * 16) + 16

        # Only uses the cipher text that is required
        requiredCipherText = Function.Base64_To.concat(cipherTextBytes[:blockEnd])

        for c in range(0, 128):

            b64char = base64.b64encode(chr(c).encode('utf-8'))
            cipherTextNew = edit(requiredCipherText, key, offset, b64char)
            
            cipherTextNewBytes = Function.Encryption.splitBase64IntoBlocks(cipherTextNew, blocksize=1)

            orginalByte = cipherTextBytes[offset]
            newByte = cipherTextNewBytes[offset]

            # Found plaintext value!
            if orginalByte == newByte:
                
                char = base64.b64decode(b64char)
                recoveredPlainText += char

                # Prevents printing when running tests                
                if __name__ == "__main__":
                    print(char.decode('utf-8'), end="")
                
                break

        offset += 1

if __name__ == "__main__":
    print("\n")
    task25()
    print("\n")