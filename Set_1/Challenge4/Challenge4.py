import codecs
import collections
import re
import sys
import string
sys.path.insert(0, '../..')
import Function

# ETAOIN SHRDLU - Most common frequency of letters in the english langaug in order of frequency
common_characters = []

def task4():
    """
    Detect single-character XOR
    One of the 60-character strings in this file has been encrypted by single-character XOR.
    """

    input = load()

    # Adds all single character hex combinations for a key
    for x in range(0, 255):
        common_characters.append(str(format(x, '02x')))

    # Removes new line char
    for line in input:
        line = line.strip()  # Removes the line ending char

        # Uses regex to group values into hex pairs
        decode = re.findall('..', line)

        # Finds the most common hex pair
        most_common = collections.Counter(decode).most_common(1)[0][0]

        for char in common_characters:

            # The most common XORd with e will give the key
            k = Function.strxor(most_common, char)
            k = str(codecs.decode(k, 'utf-8'))

            key = k * round(len(line) / 2)
            answer = Function.strxor(line, key)

            if Function.HexToASCIICheck(answer):
                answer = Function.HexToASCII(answer)

                if re.match('^[A-Za-z _.,!"\'$]*$', answer) is not None:
                    if all(c in string.printable for c in answer) and answer != "":
                        print_poss(line, key, answer)


def print_poss(line, key, answer):
    print()
    print("## Possibility ##")
    print("Cipher:          ", line)
    print("Key:             ", key)
    print("Possible Answer: ", answer)
    print()


def load():
    file = open('data.txt')
    return file.readlines()


task4()
