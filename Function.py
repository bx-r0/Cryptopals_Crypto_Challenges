import codecs
import base64


englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99,
                     'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
                     'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}


def rm_byte(string):
    """
    Removes the 'b at the start of a byte string
    """
    return codecs.decode(string, 'utf-8')


def base64_to_hex(input):
    """
    TODO
    """
    bytes = base64.b64decode(input)
    return codecs.encode(bytes, 'hex')


def hex_to_base64(input):
    """
    TODO
    """
    input_bytes = codecs.decode(input, 'hex')
    return base64.b64encode(input_bytes)


def ASCIIToHex(string):
    """
    Converts an utf-8 string to a hex string
    """
    string = string.strip()
    b = codecs.encode(string, 'utf-8')
    return codecs.encode(b, 'hex')


def HexToASCII(hex):
    """
    Converts an hex string to a utf-8 string
    """

    b = codecs.decode(hex, 'hex')
    return codecs.decode(b, 'utf-8')


def HexToASCIICheck(hex):
    """
    TODO
    """
    try:
        h = codecs.decode(hex, 'hex')
        u = codecs.decode(h, 'utf-8')
        return True
    except Exception as e:
        return False


def hexxor(a, b):
    if len(a) != len(b):
        raise("Error: incorrect length in hexXor")

    length = len(a)

    binA = bin(int(a, 16))[2:].zfill(length)
    binB = bin(int(b, 16))[2:].zfill(length)

    xor = int(binA, 2) ^ int(binB, 2)

    # Format ensures that the hex values are always the same length
    hexOutput = format(xor, f"#0{length + 2}x")[2:]

    return hexOutput

def strxor(a, b):
    """
    XOR operation for two different strings.
    This method also supports differing length strings
    """
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


def create_distribution(text):
    """
    Creates the distrubution for a set of text
    :return:
    """

    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0,
                   'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0,
                   'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    total_size = len(text)

    for letter in text:
        
        # Ignores a space
        if letter.isalpha():
            letterCount[letter.capitalize()] += 1

    # Turns the values into percentages
    for char in letterCount:
        letterCount[char] = (letterCount[char] / total_size) * 100

    return letterCount


def score_distribution(text):
    """
    Calculates a score for how close the distribution is to
    english. Lower the better
    :return:
    """
    score = 0

    actual_freq = create_distribution(text)

    for letter in englishLetterFreq:
        english_freq_letter = englishLetterFreq[letter]
        actual_freq_letter = actual_freq[letter]

        score += abs(english_freq_letter - actual_freq_letter)

    return score