import base64
import codecs


def task1():
    """
    Convert hex to base64
    Input:  "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    Output: "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    """

    input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    input_bytes = codecs.decode(input, encoding='hex')
    output = base64.b64encode(input_bytes)

    return output

if __name__ == "__main__":
    task1()
