import sys
sys.path.insert(0, '../..')
import Function
import re

KEY_SIZE_RANGE = range(1, 40)

def task6():
    DATA = load()

    possible_key_size = 0
    smallest_hamming_value = None

    # Splits data into chunk sizes
    # And works out the possible key size
    for key_size in KEY_SIZE_RANGE:
        key_chunks = split_into_bytes(DATA, key_size)

        hamming_dist_normalised = (calculate_hamming_distance(key_chunks[0], key_chunks[1])) / key_size

        # TODO: Add a ranking system so the smallest few values are present
        if smallest_hamming_value is None or hamming_dist_normalised < smallest_hamming_value:
            smallest_hamming_value = hamming_dist_normalised
            possible_key_size = key_size

    print("Possible key size: ", possible_key_size)

    # TODO - Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.

    # TODO - Now transpose the blocks: make a block that is the first byte of every block,
    # and a block that is the second byte of every block, and so on.

    # TODO - Solve each block as if it was single-character XOR. You already have code to do this.

    # TODO - For each block, the single-byte XOR key that produces the best looking histogram is the
    # repeating-key XOR key byte for that block. Put them together and you have the key.


def split_into_bytes(string, number):

    # Converts to hex
    hex = Function.rm_byte(Function.base64_to_hex(string))
    bytes = re.findall("..", hex)

    # Adds padding if the lengths are not equal
    while len(bytes) % number != 0:
        bytes.append("00")

    chunks = []
    for x in range(0, len(bytes), number):
        chunk = ""

        for i in range(x, x + number):
            chunk += bytes[i]
        chunks.append(chunk)

    return chunks


def baseX_to_binary(string, base):
    return bin(int(Function.ASCIIToHex(string), base))


def calculate_hamming_distance(string1, string2):
    # Convert the strings to binary
    binary1 = baseX_to_binary(string1, 16)
    binary2 = baseX_to_binary(string2, 16)

    # Compares each binary value 1 for 1
    count = 0
    for i in range(0, len(binary1)):
        if binary1[i] != binary2[i]:
            count += 1

    return count


def load():
    """
    Loads in the provided data for the challenge
    """

    data = ""
    with open("data.txt") as file:
        lines = file.readlines()

    for x in lines:
        data += x
    return data

task6()
