import sys ; sys.path += ['.', '../..']
from SharedCode import Function
"""
>>> Detect AES in ECB mode

    In this file are a bunch of hex-encoded ciphertexts.

    One of them has been encrypted with ECB.

    Detect it.

    Remember that the problem with ECB is that it is stateless and deterministic;
    the same 16 byte plaintext block will always produce the same 16 byte ciphertext.
"""

def task8():
    data = Function.File.loadLines(__file__)

    ecb_candiates = []
    for line in data:
        # Removes new lines
        line = line.strip()

        lineb64 = Function.HexTo.base64(line)

        blocks = Function.Encryption.splitBase64IntoBlocks(lineb64, 16)

        if Function.Encryption.AES.ECB.Detect(blocks):
            ecb_candiates.append(line)

    return ecb_candiates

if __name__ == "__main__":
    print(task8())