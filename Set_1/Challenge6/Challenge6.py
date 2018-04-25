import sys
sys.path.insert(0, '../..')
import Function
import re
import string

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


def task6():
    DATA = load()

    possible_key_size = 0
    smallest_hamming_value = None

    # Splits data into chunk sizes
    # And works out the possible key size
    for key_size in KEY_SIZE_RANGE:

        # BASE64 -> HEX conversion going on below
        key_chunks = split_into_bytes(DATA, key_size)

        hamming_dist_normalised = (calculate_hamming_distance(key_chunks[0], key_chunks[1])) / key_size

        # TODO: Add a ranking system so the smallest few values are present
        if smallest_hamming_value is None or hamming_dist_normalised < smallest_hamming_value:
            smallest_hamming_value = hamming_dist_normalised
            possible_key_size = key_size

    print("Possible key size: ", possible_key_size)
    possible_key_size = 29

    # Breaks the cipher into key size blocks
    data_chunks = split_into_bytes(DATA, possible_key_size)

    # Transposes all the bytes of the chunks
    transpose_chunks = []
    for key_pos in range(0, possible_key_size):
        string = ""
        for x in data_chunks:
            # Splits into separate bytes and then grabs the current
            # position of bytes
            each_hex_byte = re.findall("..", x)
            string += each_hex_byte[key_pos]

        transpose_chunks.append(string)

    disovered_key = []
    # Loops round each letter as a key
    for transpose_byte in transpose_chunks:
        frequency_lists = []
        for letter in KEY_SPACE:
            # XORs the key attempt with the transposed byte
            key_attempt = Function.rm_byte(Function.ASCIIToHex(letter * (len(Function.HexToASCII(transpose_byte)))))
            xor = Function.strxor(transpose_byte, key_attempt)

            # Obtains the frequency of the letters for each key
            frequency = []
            for letter2 in ALPHABET:
                total_occurance = 0
                for char in xor:
                    if char == letter2:
                        total_occurance += 1

                frequency.append(total_occurance)
            frequency_lists.append(frequency)

        # Works out the best key character
        current_best_key_char = ''
        smallest_difference = 100000000
        frequency_pos = 0
        for letter3 in ALPHABET:
            difference = compare_frequencies(ENGLISH_LANGUAGE_DISTRIBUTION, frequency_lists[frequency_pos])

            if float(difference) < float(smallest_difference):
                smallest_difference = difference
                current_best_key_char = letter3

            frequency_pos += 1
        disovered_key.append(current_best_key_char)

    # PRINTS KEY
    for x in disovered_key:
        print(x, end='')


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


def compare_frequencies(english_lang, cipher_text):
    """Compares how similar the two letter frequency distributions are.
    The lower the number the more similar"""

    total_diff_abs = 0
    position = 0
    for e in english_lang:
        total_diff_abs += abs(e - float(cipher_text[position]))
        position += 1

    return total_diff_abs


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
