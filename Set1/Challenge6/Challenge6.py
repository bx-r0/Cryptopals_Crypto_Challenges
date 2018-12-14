import sys ; sys.path += ['.', '../..']
from SharedCode import Function
import re


"""
>>> Break repeating-key XOR
"""

KEY_SIZE_RANGE = range(1, 30)

def task6():
    DATA=Function.File.loadData(__file__)

    keys = []

    # Ranks the most likely key length
    key_size_and_hamming=rank_possible_key_length(DATA)

    for key_pair in key_size_and_hamming:
        possible_key_size=key_pair[0]

        # Breaks the cipher into key size blocks
        data_chunks=Function.Encryption.splitBase64IntoBlocks(DATA, possible_key_size)

        # Transposes all the bytes of the chunks
        transpose_chunks=transpose_bytes(data_chunks)

        disovered_key=[]

        # Loops round each key as a key
        for transpose_byte in transpose_chunks:
            disovered_key.append(breakSingleKey(transpose_byte))

        keys.append("".join(disovered_key))


    dataHex = Function.Base64_To.hexadecimal(DATA)
    dataHex = Function.Conversion.remove_byte_notation(dataHex)

    # score, key, text
    best = (None, None, None)

    # Use keys to fully decrypt
    for key in keys:
        keyHex = Function.UTF8.hexadecimal(key)
        keyHex = Function.Conversion.remove_byte_notation(keyHex)

        fullLengthKey = Function.Encryption.Vigenere.gen_key(dataHex, keyHex)

        xor = Function.XOR.hexXor(dataHex, fullLengthKey)

        text = Function.HexTo.utf8(xor)

        score = Function.Statistical.score_distribution(text)

        if best[0] is None or score < best[0]:
            best = (score, key, text)

    return str(best[1])

def breakSingleKey(transpose_byte):

    bestScore = None
    bestKey = ""

    # Works through all possible keys
    for key in range(0, 255):

        # XORs the key attempt with the transposed byte
        key_attempt = format(key, '#04x')[2:] * round(len(transpose_byte) / 2)

        xor = Function.XOR.hexXor(transpose_byte, key_attempt)

        # Attempts a conversion to ascii, if that fails the key will be ignored
        try:
            output = Function.HexTo.utf8(xor)
            
            score = Function.Statistical.score_distribution(output)
            
            if bestScore is None or bestScore > score:
                bestScore = score
                bestKey = chr(key)

        except UnicodeDecodeError:
            pass
    
    return bestKey

def rank_possible_key_length(data):
    key_size_and_hamming=[]

    # Splits data into chunk sizes
    # And works out the possible key size
    for key_size in KEY_SIZE_RANGE:
        # BASE64 -> HEX conversion going on below
        key_chunks=Function.Encryption.splitBase64IntoBlocks(data, key_size)

        hamming_dist_normalised=(calculate_hamming_distance(
            key_chunks[0], key_chunks[1])) / key_size
        key_size_and_hamming.append([key_size, hamming_dist_normalised])
        key_size_and_hamming.sort(key=lambda x: x[1])

    return key_size_and_hamming

def calculate_hamming_distance(string1, string2):

    hexString1 = Function.Base64_To.hexadecimal(string1)
    hexString2 = Function.Base64_To.hexadecimal(string2)

    # Convert the strings to binary
    binary1 = Function.HexTo.binary(int(hexString1, 16))
    binary2 = Function.HexTo.binary(int(hexString2, 16))

    binary1, binary2 = Function.makeBinaryEqualLength(binary1, binary2)

    # Compares each binary value 1 for 1
    count=0
    for i in range(0, len(binary1)):
        if binary1[i] != binary2[i]:
            count += 1

    return count

def transpose_bytes(data_chunks):

    # Converts to hex for easer manipulation
    data_chunks = list(map(Function.Base64_To.hexadecimal, data_chunks))

    chunkLen=round(len(data_chunks[0]) / 2)

    transposed=[]

    # A new byte value will be created from the 1st of all
    # byte values, the 2nd and so on
    for pos in range(chunkLen):

        byteString=""

        for chunk in data_chunks:
            each_hex_byte=re.findall("..", Function.Conversion.remove_byte_notation(chunk))
            byteString += each_hex_byte[pos]

        transposed.append(byteString)

    return transposed


if __name__ == "__main__":
    task6()
