import sys ; sys.path += ['.', '../..']
import Function

# Random key
key = Function.Encryption.AES.randomKeyBase64()

def prep(data):
    """
    Cuts all data down to the same length. Takes the shortes value
    """

    shortestLen = None
    for x in data:

        length = len(x)

        if shortestLen is None or length < shortestLen:
            shortestLen = length

    
    # Truncates all data
    newData = []
    for d in data:
        newData.append(Function.Encryption.splitBase64IntoBlocks(d, blocksize=shortestLen + 1)[0])

    return newData

def encrypt(data):

    cipherTexts = []
    for d in data:
        cipherTexts.append(Function.Encryption.AES.CTR.Encrypt_Decrypt(0, key, d.strip()))

    return cipherTexts

def task20():
    cipherTexts = encrypt(prep(data))

    plainTexts = Function.Encryption.AES.CTR.sameNonceStatisticalAttack(cipherTexts)

    # Prints the answers
    for pt in plainTexts:
        print(pt)

data = Function.File.loadLines(__file__)

if __name__ == "__main__":
    task20()
