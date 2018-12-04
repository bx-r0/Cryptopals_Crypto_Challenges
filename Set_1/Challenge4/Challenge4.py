import codecs
import collections
import re
import sys
import string
sys.path.insert(0, './')
sys.path.insert(0, '..')
sys.path.insert(0, '../..')
import Function

"""
>>> Detect single-character XOR

    One of the 60-character strings in this file has been encrypted by single-character XOR.

    Find it.

    (Your code from #3 should help.) 
"""


# ETAOIN SHRDLU - Most common frequency of letters in the english langaug in order of frequency
common_characters = []

def task4():
    """
    Detect single-character XOR
    One of the 60-character strings in this file has been encrypted by single-character XOR.
    """

    input = Function.File.loadLines(__file__)

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
            k = Function.XOR.hexXor(most_common, char)

            key = k * round(len(line) / 2)
            answer = Function.XOR.hexXor(line, key)

            if Function.HexTo.utf8_check(answer):
                answer = Function.HexTo.utf8(answer)

                if re.match('^[A-Za-z _.,!"\'$]*$', answer) is not None:
                    if all(c in string.printable for c in answer) and answer != "":
                        return k, answer

if __name__ == "__main__":
    task4()
