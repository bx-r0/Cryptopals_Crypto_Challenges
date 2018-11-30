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


KEY_SIZE_RANGE = range(1, 40)
ALPHABET = string.ascii_uppercase
KEY_SPACE = string.ascii_uppercase + string.ascii_lowercase
ENGLISH_LANGUAGE_DISTRIBUTION = [8.2,
                                 1.5,
                                 2.8,
                                 4.3,
                                 12.7,
                                 2.2,
                                 2.0,
                                 6.1,
                                 7.0,
                                 0.2,
                                 0.8,
                                 4.0,
                                 2.4,
                                 6.7,
                                 7.5,
                                 1.9,
                                 0.1,
                                 6.0,
                                 6.3,
                                 9.1,
                                 2.8,
                                 1.0,
                                 2.4,
                                 0.2,
                                 2.0,
                                 0.1]
print(string.punctuation)



def breakSingleKey(transpose_byte):
    frequency_lists = []

    bestScore = None
    bestKey = ""

    # Works through all possible keys
    for key in range(0, 255):

        # XORs the key attempt with the transposed byte
        key_attempt = format(key, '#04x')[2:] * round(len(transpose_byte) / 2)

        if len(key_attempt) != len(transpose_byte):
            raise("issue!")

        xor = Function.hexxor(transpose_byte, key_attempt)

        # Attepts a conversion to ascii, if that fails the key will be ignored
        try:
            output = Function.HexToASCII(xor)
            
            #if re.match(r"^[a-zA-Z0-9 \n!\"\'\#\$\%\&\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\_\`\{\|\}\~\\]*$", output):
            score = Function.score_distribution(output)
            
            if bestScore is None or bestScore > score:
                bestScore = score
                bestKey = chr(key)

        except UnicodeDecodeError:
            pass
    
    return bestKey



def task6():
    DATA=load()

    # Ranks the most likely key length
    key_size_and_hamming=rank_possible_key_length(DATA)

    for key_pair in key_size_and_hamming:
        possible_key_size=key_pair[0]

        # Breaks the cipher into key size blocks
        data_chunks=split_into_bytes(DATA, possible_key_size)

        # Transposes all the bytes of the chunks
        transpose_chunks=transpose_bytes(data_chunks)

        disovered_key=[]

        # Loops round each key as a key
        for transpose_byte in transpose_chunks:
            disovered_key.append(breakSingleKey(transpose_byte))
            

        # PRINTS KEY
        print("Key Size:", possible_key_size, " - ", end='')
        for x in disovered_key:
            print(x, end='', flush=True)
        print()


def split_into_bytes(string, number):

    # Converts to hex
    hex=Function.rm_byte(Function.base64_to_hex(string))
    bytes=re.findall("..", hex)

    # Adds padding if the lengths are not equal
    while len(bytes) % number != 0:
        bytes.append("00")

    chunks=[]
    for x in range(0, len(bytes), number):
        chunk=""

        for i in range(x, x + number):
            chunk += bytes[i]
        chunks.append(chunk)

    return chunks


def baseX_to_binary(string, base):
    return bin(int(Function.ASCIIToHex(string), base))



def rank_possible_key_length(data):
    key_size_and_hamming=[]

    # Splits data into chunk sizes
    # And works out the possible key size
    for key_size in KEY_SIZE_RANGE:
        # BASE64 -> HEX conversion going on below
        key_chunks=split_into_bytes(data, key_size)

        hamming_dist_normalised=(calculate_hamming_distance(
            key_chunks[0], key_chunks[1])) / key_size
        key_size_and_hamming.append([key_size, hamming_dist_normalised])
        key_size_and_hamming.sort(key=lambda x: x[1])

    return key_size_and_hamming


def calculate_hamming_distance(string1, string2):
    # Convert the strings to binary
    binary1=baseX_to_binary(string1, 16)
    binary2=baseX_to_binary(string2, 16)

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


def single_key_crack(input_str):
    """
    TODO
    :param input_str:
    :return:
    """
    # Uses regex to group values into hex pairs
    decode=re.findall('..', input_str)

    # Finds the most common hex pair
    most_common=collections.Counter(decode).most_common(1)[0][0]

    # Adds all single character hex combinations for a key
    common_characters=[]
    for x in range(0, 255):
        common_characters.append(str(format(x, '02x')))

    for char in common_characters:
        # The most common XORd with e will give the key
        k=Function.strxor(most_common, Function.ASCIIToHex(char))
        k=str(codecs.decode(k, 'utf-8'))
        print("Key tried: ", k)

        key=k * round(len(input_str) / 2)

        answer=Function.strxor(input_str, key)
        answer=Function.HexToASCII(answer)

        # Regex to check string contains alphanumeric values and punctuation
        if re.match('^[A-Za-z _.,!"\'$]*$', answer) is not None:
            print("### ANSWER FOUND:\'", answer, '\'')
            print("Key was: \'", k, '\'')

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
