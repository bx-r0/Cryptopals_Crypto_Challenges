import codecs


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
    try:
        h = codecs.decode(hex, 'hex')
        u = codecs.decode(h, 'utf-8')
        return True
    except Exception as e:
        return False

# XOR Code
def fXOR(input1, input2):
    """
    XORing for two fixed strings
    """
    # Checks if it is not a byte object
    hex1 = codecs.decode(input1, 'hex')
    hex2 = codecs.decode(input2, 'hex')

    xored = bytes([a ^ b for a, b in zip(hex1, hex2)])
    return codecs.encode(xored, 'hex')


