import sys ; sys.path += ['.', '../..']
import Function

"""
>>> Break fixed-nonce CTR mode using substitutions
"""

data = Function.File.loadLines(__file__)

# Random key
key = Function.Encryption.AES.randomKeyBase64()

def encrypt(data):

    cipherTexts = []
    for d in data:
        cipherTexts.append(Function.Encryption.AES.CTR.Encrypt_Decrypt(0, key, d.strip()))

    return cipherTexts

def task19():

    cipherTexts = encrypt(data)

    plainTexts = Function.Encryption.AES.CTR.sameNonceStatisticalAttack(cipherTexts)

    # Prints the answers
    for pt in plainTexts:
        print(pt)

if __name__ == '__main__':
    task19()