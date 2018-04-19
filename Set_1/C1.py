import base64
import codecs


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


task1()
