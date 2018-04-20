import codecs
import base64


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


def strxor(a, b):
    """
    XOR operation for two different strings.
    This method also supports differing length strings
    """
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


