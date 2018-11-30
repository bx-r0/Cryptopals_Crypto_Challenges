import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
import codecs
import collections
import string
import re
import Function
import os
import binascii

KEY_SIZE_RANGE = range(1, 30)

def task6():
    DATA=load()

    keys = []

    # Ranks the most likely key length
    key_size_and_hamming=rank_possible_key_length(DATA)

    for key_pair in key_size_and_hamming:
        possible_key_size=key_pair[0]

        # Breaks the cipher into key size blocks
        data_chunks=Function.split_into_bytes(DATA, possible_key_size)

        # Transposes all the bytes of the chunks
        transpose_chunks=transpose_bytes(data_chunks)

        disovered_key=[]

        # Loops round each key as a key
        for transpose_byte in transpose_chunks:
            disovered_key.append(breakSingleKey(transpose_byte))

        keys.append("".join(disovered_key))


    dataHex = Function.base64_to_hex(DATA)
    dataHex = Function.rm_byte(dataHex)

    # score, key, text
    best = (None, None, None)

    # Use keys to fully decrypt
    for key in keys:
        keyHex = Function.ASCIIToHex(key)
        keyHex = Function.rm_byte(keyHex)

        fullLengthKey = Function.gen_key(dataHex, keyHex)

        xor = Function.hexxor(dataHex, fullLengthKey)

        text = Function.HexToASCII(xor)

        score = Function.score_distribution(text)

        if best[0] is None or score < best[0]:
            best = (score, key, text)

    print("Best values:")
    print(f"KEY: {best[1]}")
    print(f"TEXT: \n {best[2]}")

def breakSingleKey(transpose_byte):

    bestScore = None
    bestKey = ""

    # Works through all possible keys
    for key in range(0, 255):

        # XORs the key attempt with the transposed byte
        key_attempt = format(key, '#04x')[2:] * round(len(transpose_byte) / 2)

        xor = Function.hexxor(transpose_byte, key_attempt)

        # Attepts a conversion to ascii, if that fails the key will be ignored
        try:
            output = Function.HexToASCII(xor)
            
            score = Function.score_distribution(output)
            
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
        key_chunks=Function.split_into_bytes(data, key_size)

        hamming_dist_normalised=(calculate_hamming_distance(
            key_chunks[0], key_chunks[1])) / key_size
        key_size_and_hamming.append([key_size, hamming_dist_normalised])
        key_size_and_hamming.sort(key=lambda x: x[1])

    return key_size_and_hamming

def calculate_hamming_distance(string1, string2):
    # Convert the strings to binary
    binary1=bin(int(Function.ASCIIToHex(string1), 16))
    binary2=bin(int(Function.ASCIIToHex(string2), 16))

    # Compares each binary value 1 for 1
    count=0
    for i in range(0, len(binary1)):
        if binary1[i] != binary2[i]:
            count += 1

    return count

def transpose_bytes(data_chunks):

    chunkLen=round(len(data_chunks[0]) / 2)

    transposed=[]

    # A new byte value will be created from the 1st of all
    # byte values, the 2nd and so on
    for pos in range(chunkLen):

        byteString=""

        for chunk in data_chunks:
            each_hex_byte=re.findall("..", chunk)
            byteString += each_hex_byte[pos]

        transposed.append(byteString)

    return transposed

def load():
    """
    Loads in the provided data for the challenge
    """

    data=""
    with open(f"{os.path.realpath(__file__)[:63]}/data.txt") as file:
        lines=file.readlines()

    for x in lines:
        data += x
    return data

task6()
