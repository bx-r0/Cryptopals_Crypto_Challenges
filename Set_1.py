import base64
import codecs
import operator


def task1():
    """
    Convert hex to base64
    Input:  "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    Output: "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    """

    input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    print()
    print("# Initial input (Hex)")
    print(input, '\n')

    input_bytes = codecs.decode(input, encoding='hex')
    print("# Bytes")
    print(input_bytes, '\n')

    output = base64.b64encode(input_bytes)
    print("# Output (base64)")
    print(output, '\n')

    # Check answer is valid:
    if output == b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t":
        print("# Task 1 passed!")
    else:
        print("# Task 1 failed!!")


def task2():
    """
    Fixed XOR:
     Write a function that takes two equal-length buffers and produces their XOR combination.

    Input:
        - "1c0111001f010100061a024b53535009181c"
        - "686974207468652062756c6c277320657965"
    
    Output:
        - "746865206b696420646f6e277420706c6179"
    """
    print('\n')

    input1 = "1c0111001f010100061a024b53535009181c"
    print("# Input 1:")
    print(input1, '\n')

    input2 = "686974207468652062756c6c277320657965"
    print("# Input 2:")
    print(input2, '\n')

    output = fXOR(input1, input2)
    print("# Output: ")
    print(output, '\n')

    # Checks answer is valid
    if output == b"746865206b696420646f6e277420706c6179":
        print("# Task 2 passed!")
    else:
        print("# Task 2 failed!!")


def fXOR(input1, input2):
    """
    XORing for two fixed strings
    """
    hex1 = codecs.decode(input1, 'hex')
    hex2 = codecs.decode(input2, 'hex')

    xored = bytes([a ^ b for a, b in zip(hex1, hex2)])
    return codecs.encode(xored, 'hex')
    

task1()
task2()
