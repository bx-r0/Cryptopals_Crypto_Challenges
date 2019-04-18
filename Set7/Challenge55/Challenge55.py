import sys ; sys.path += ['.', '../..']
from SharedCode import Function
from CryptoCode.MD4 import MD4
import hashlib
import base64
import struct

EQUAL = 'equal'
ZERO = 'zero'
ONE = 'one'

#TODO - Check these
# first round constraints
conditions = [
    # a1
    [
      [EQUAL, 6]
    ],

    # d1
    [
      [ZERO, 6],
      [EQUAL, 7],
      [EQUAL, 10]
    ],

    # c1
    [
      [ONE, 6],
      [ONE, 7],
      [ZERO, 10],
      [EQUAL, 25]
    ],

    # b1
    [
      [ONE, 6],
      [ZERO, 7],
      [ZERO, 10],
      [ZERO, 25]
    ],

    # a2
    [
      [ONE, 7],
      [ONE, 10],
      [ZERO, 25],
      [EQUAL, 13]
    ],

    # d2
    [
      [ZERO, 13],
      [EQUAL, 18],
      [EQUAL, 19],
      [EQUAL, 20],
      [EQUAL, 21],
      [ONE, 25]
    ],

    # c2
    [
      [EQUAL, 12],
      [ZERO, 13],
      [EQUAL, 14],
      [ZERO, 18],
      [ZERO, 19],
      [ONE, 20],
      [ZERO, 21]
    ],

    # b2
    [
      [ONE, 12],
      [ONE, 13],
      [ZERO, 14],
      [EQUAL, 16],
      [ZERO, 18],
      [ZERO, 19],
      [ZERO, 20],
      [ZERO, 21]
    ],

    # a3
    [
      [ONE, 12],
      [ONE, 13],
      [ONE, 14],
      [ZERO, 16],
      [ZERO, 18],
      [ZERO, 19],
      [ZERO, 20],
      [EQUAL, 22],
      [ONE, 21],
      [EQUAL, 25]
    ],

    # d3
    [
      [ONE, 12],
      [ONE, 13],
      [ONE, 14],
      [ZERO, 16],
      [ZERO, 19],
      [ONE, 20],
      [ONE, 21],
      [ZERO, 22],
      [ONE, 25],
      [EQUAL, 29]
    ],
    
    # c3
    [
      [ONE, 16],
      [ZERO, 19],
      [ZERO, 20],
      [ZERO, 21],
      [ZERO, 22],
      [ZERO, 25],
      [ONE, 29],
      [EQUAL, 31]
    ],

    # b3
    [
      [ZERO, 19],
      [ONE, 20],
      [ONE, 21],
      [EQUAL, 22],
      [ONE, 25],
      [ZERO, 29],
      [ZERO, 31]
    ],

    # a4
    [
      [ZERO, 22],
      [ZERO, 25],
      [EQUAL, 26],
      [EQUAL, 28],
      [ONE, 29],
      [ZERO, 31]
    ],

    # d4
    [
      [ZERO, 22],
      [ZERO, 25],
      [ONE, 26],
      [ONE, 28],
      [ZERO, 29],
      [ONE, 31]
    ],

    # c4
    [
      [EQUAL, 18],
      [ONE, 22],
      [ONE, 25],
      [ZERO, 26],
      [ZERO, 28],
      [ZERO, 29]
    ],

    #b4
    [
      [ZERO, 18],
      [EQUAL, 25],
      [ONE, 26],
      [ONE, 28],
      [ZERO, 29]
    ],
  ]

def undoLittleEndian(littleEndianWords):

    byteList = []
    for word in littleEndianWords:
        byteList.append(struct.pack("<I", word))

    return b"".join(byteList)

def gen_likly_collisions():

    m = base64.b64decode(Function.Encryption.AES.randomKeyBase64(64))
    m_little_endian_words = MD4.byteChunkToWordArray(m)

    sectors = ['a', 'd', 'c', 'b'] * 4
    shifts = [3, 7, 11, 19] * 4

    initial_state = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
    state = initial_state.copy()

    for i in range(16):
        work(state, sector_to_index(sectors[i]), i, shifts[i], m_little_endian_words, conditions[i])

    m = undoLittleEndian(m_little_endian_words)
    m_prime = create_colliding_message(m)

    return m, m_prime

# TODO - what does this actually do>
def create_colliding_message(m):
  x = MD4.byteChunkToWordArray(m)
  x[1] = (x[1] + (1 << 31)) % (1 << 32)
  x[2] = (x[2] + ((1 << 31) - (1 << 28))) % (1 << 32)
  x[12] = (x[12] - (1 << 16)) % (1 << 32)
  return undoLittleEndian(x)

def work(state, starts, i, shift, message, constraints):
    # Performs the MD4 operation

    # (starts + x % 4) makes sure to loop around to start of the state list:
    # i.e. if the start is 'd' the next value will loop around to 'a'

    s1 = state[(starts + 0) % 4]
    s2 = state[(starts + 1) % 4]
    s3 = state[(starts + 2) % 4]
    s4 = state[(starts + 3) % 4]

    v = MD4.LeftRotate(s1 + MD4.F(s2, s3, s4) + message[i], shift)

    for c in constraints:

        if c[0] == EQUAL:
            v = correct_bit_equal(v, s2, c[1])
        elif c[0] == ONE:
            v = correct_bit_one(v, c[1])
        elif c[0] == ZERO:
            v = correct_bit_zero(v, c[1])

    # compute the correct message word using algebra
    message[i] = MD4.RightRotate(v, shift) - s1 - MD4.F(s2, s3, s4)
    message[i] = message[i] % (1 << 32)

    # update the state
    state[starts % 4] = v
    return

# TODO - Do the maths on these, see why they work
def correct_bit_equal(v, n, i):
  v ^= ((v ^ n) & (1 << i))
  return v

def correct_bit_zero(v, i):
  v &= ~(1 << i)
  return v

def correct_bit_one(v, i):
  v |= (1 << i)
  return v

def sector_to_index(sector_char):

    # Uses the ascii value of 'a' to push all the character vars to 0-3
    return ord(sector_char) - 97


if __name__ == "__main__":

    count = 0
    while (True):
        m, m_prime = gen_likly_collisions()

        h = hashlib.new("md4", m).hexdigest()
        h_prime = hashlib.new("md4", m_prime).hexdigest()

        # h = MD4.createDigest(message=m)
        # h_prime = MD4.createDigest(message=m_prime)

        if h == h_prime:
            print("\n ### COLLISION FOUND ###")
            print("M : ", m)
            print("M': ", m_prime)
        count += 1
        if count % 1000 == 0: print(str(count) + "\r")