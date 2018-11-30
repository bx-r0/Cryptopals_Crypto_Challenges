import sys
import codecs
sys.path.insert(0, '..')
import Function


key = "ICE"

input = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

target = "3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"


def task5():
    e = codecs.decode(encrypt(input), 'utf-8')

    if e == target:
        print("## Challenge 5 Passed!")
    else:
        print("Challenge 5 Failed!")


def encrypt(msg):
    xor = Function.strxor(Function.gen_key(msg), msg)
    return Function.ASCIIToHex(xor)


task5()
