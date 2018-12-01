import sys
import codecs
sys.path.insert(0, './')
sys.path.insert(0, '..')
sys.path.insert(0, '../..')
import Function

key = "ICE"

input = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""


def task5():
    return encrypt(input)

def encrypt(msg):
    k = Function.Encryption.Vigenere.gen_key(msg, key)

    msgHex = Function.UTF8.utf_to_hex(msg)
    keyHex = Function.UTF8.utf_to_hex(k)

    xor = Function.XOR.hexxor(msgHex, keyHex)
    
    # Removes the 0b
    return xor

if __name__ == "__main__":
    task5()
