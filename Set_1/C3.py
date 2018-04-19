import codecs
import collections
import re
import sys
sys.path.insert(0, '..')
import Function

# ETAOIN SHRDLU - Most common frequency of letters in the english langaug in order of frequency
common_characters = ['e', 't', 'a', 'o', 'i', 'n', ' ', 's', 'h', 'r', 'd', 'l', 'u']


def task3():
    """
    Single-byte XOR cipher
    The hex encoded Input has been XOR'd against a single character. Find the key, decrypt the message.

    Input: "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    """

    input = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

    print("# Input:")
    print(input, '\n')

    # Uses regex to group values into hex pairs
    decode = re.findall('..', input)

    # Finds the most common hex pair
    most_common = collections.Counter(decode).most_common(1)[0][0]

    for char in common_characters:
        # The most common XORd with e will give the key
        k = Function.fXOR(most_common, Function.ASCIIToHex(char))
        k = str(codecs.decode(k, 'utf-8'))
        print("Key tried: ", k)

        key = k * round(len(input) / 2)

        answer = Function.fXOR(input, key)
        answer = Function.HexToASCII(answer)

        # Regex to check string contains alphanumeric values and punctuation
        if re.match('^[A-Za-z _.,!"\'$]*$', answer) is not None:
            print("### ANSWER FOUND:\'",  answer, '\'')
            print("Key was: \'", k, '\'')
            break


task3()
