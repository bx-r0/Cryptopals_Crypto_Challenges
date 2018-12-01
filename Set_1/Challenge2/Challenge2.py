import codecs


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

    input1 = "1c0111001f010100061a024b53535009181c"
    input2 = "686974207468652062756c6c277320657965"
    output = fXOR(input1, input2)

    return output

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

if __name__ == "__main__":
    task2()
