import os
import unittest
import base64

# SET 1
import Set_1.Challenge1.Challenge1 as c1
import Set_1.Challenge2.Challenge2 as c2
import Set_1.Challenge3.Challenge3 as c3
import Set_1.Challenge4.Challenge4 as c4
import Set_1.Challenge5.Challenge5 as c5
import Set_1.Challenge6.Challenge6 as c6
import Set_1.Challenge7.Challenge7 as c7
import Set_1.Challenge8.Challenge8 as c8

# SET 2
import Set_2.Challenge9.Challenge9 as c9
import Set_2.Challenge10.Challenge10 as c10
import Set_2.Challenge11.Challenge11 as c11
import Set_2.Challenge12.Challenge12 as c12
import Set_2.Challenge13.Challenge13 as c13
import Set_2.Challenge14.Challenge14 as c14
import Set_2.Challenge15.Challenge15 as c15
import Set_2.Challenge16.Challenge16 as c16

# SET 3
import Set_3.Challenge17.Challenge17 as c17


def loadData(extra):
    """
    Concatenates all data lines into one
    """

    lines = loadLines(extra)

    lines = list(map(str.strip, lines))

    return "".join(lines)

def loadLines(extra):
    """
    Returns all data lines in a list
    """

    path = os.path.realpath(__file__)
    pathSections = path.split('/')
    path = "/".join(pathSections[:-1])
    
    lines = []
    with open(path + extra, 'r') as file:
        lines = file.readlines()
        
    return lines

class C1(unittest.TestCase):
    
    def test(self):
        expected = b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        actual = c1.task1()

        self.assertEqual(actual, expected)

class C2(unittest.TestCase):

    def test(self):
        expected = b"746865206b696420646f6e277420706c6179"
        actual = c2.task2()

        self.assertEqual(actual, expected)

class C3(unittest.TestCase):
    
    def test(self):
        # Expected key value
        expected = "58"
        actual = c3.task3()

        self.assertEqual(actual, expected)

class C4(unittest.TestCase):
    
    def test(self):
        expected = ("35", "Now that the party is jumping\n")
        actual = c4.task4()

        self.assertEqual(actual, expected)

class C5(unittest.TestCase):
    
    def test(self):
        expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
        actual = c5.task5()

        self.assertEqual(actual, expected)

class C6(unittest.TestCase):
    
    def test(self):

        # TODO - Why is the output from the task formatted strange?
        expected = "TERMINATOR\x00X\x1a\x00BRING\x00THE\x00NOISE"
        actual = c6.task6()

        self.assertEqual(actual, expected)

class C7(unittest.TestCase):
    
    def test(self):

        c7.task7()

class C8(unittest.TestCase):

    def test(self):
        expected = ["d880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a"]
        actual = c8.task8()

        self.assertEqual(expected, actual)

class C9(unittest.TestCase):

    def test(self):
        expected = "YELLOW SUBMARINE\x04\x04\x04\x04"
        actual = c9.task9()

        self.assertEqual(actual, expected)

class C10(unittest.TestCase):


    def test(self):
        expected = loadData("/Set_2/Challenge10/data.txt")
        actual = str(c10.task10())[2:-1]

        self.assertEqual(actual, expected)

class C11(unittest.TestCase):

    def test(self):

        # Repeats the test
        for _ in range(1000):

            # Obtains the chosen mode, and the actual mode
            expected, actual = c11.task11()
            self.assertEqual(actual, expected)

class C12(unittest.TestCase):

    def test(self):
        expected = base64.b64decode(c12.appendString).decode('utf-8')
        actual = c12.task12()

        self.assertEqual(actual, expected)

class C13(unittest.TestCase):

    def test_decode(self):
        testInput = "foo=bar&baz=qux&zap=zazzle"

        expected = "{\n  foo: 'bar',\n  baz: 'qux',\n  zap: 'zazzle'\n}"
        actual = c13.decode(testInput)

        self.assertEqual(actual, expected)
    
    def test_encode(self):
        testInput = "{\n  foo: 'bar',\n  baz: 'qux',\n  zap: 'zazzle'\n}"

        expected = "foo=bar&baz=qux&zap=zazzle"
        actual = c13.encode(testInput)

        self.assertEqual(actual, expected)

    def test_encode_decode(self):
        testInput = "test=great&outcome=correct&time=wellspent&percentage=100"

        expected = testInput
        actual = c13.encode(c13.decode(testInput))

        self.assertEqual(actual, expected)

    def test_profile_gen(self):
        
        expected = "email=foo@bar.com&uid=10&role=user"
        actual = c13.profile_for("foo@bar.com")

        self.assertEqual(actual, expected)
    
    def test_profile_invalid(self):
        with self.assertRaises(Exception) as context:
            c13.profile_for("foo@bar.com&role=admin")

        # Checks exception message
        self.assertEqual("Invalid email!", context.exception.args[0])
        
    def test_encrypt_decrypt(self):
        expected = "test=great&outcome=correct&time=wellspent&percentage=100"
        
        # Super secret
        key = b'gHEvzQiiVFtkppxjAKiweg=='
        
        e = c13.encrypt_user_profile(expected, key)
        actual = c13.decrypt_user_profile(e, key)

        self.assertEqual(actual, expected)


class C14(unittest.TestCase):

    def test(self):
        # [2:-1] Is removing the b'' notation
        expected = str(base64.b64decode(c14.target_bytes))[2:-1]
        actual = c14.task14()

        self.assertEqual(actual, expected)


class C15(unittest.TestCase):

    def test(self):
        s1 = "ICE ICE BABY\x04\x04\x04\x04" # Valid
        s2 = "ICE ICE BABY"                 # Valid
        s3 = "ICE ICE BABY\x05\x05\x05\x05" # Invalid
        s4 = "ICE ICE BABY\x01\x02\x03\x04" # Invalid

        exceptionMsg = c15.exceptionMessage

        self.assertEqual(c15.validPKCS7(s1), "ICE ICE BABY")
        self.assertEqual(c15.validPKCS7(s2), "ICE ICE BABY")

        with self.assertRaises(Exception) as context:
            c15.validPKCS7(s3)
        self.assertEqual(exceptionMsg, context.exception.args[0])

        with self.assertRaises(Exception) as context:
            c15.validPKCS7(s4)
        self.assertEqual(exceptionMsg, context.exception.args[0])
        
class C16(unittest.TestCase):

    def test(self):
        self.assertEqual(c16.task16(), True)

class C17(unittest.TestCase):

    def test(self):
        data = loadLines("/Set_3/Challenge17/data.txt")
        
        lineIndex = 0
        for line in data:
            expected = base64.b64decode(line).decode('utf-8')

            actual = None
            try:
                actual = c17.task17(line.strip())
            except Exception as e:
                print(e)

            # Debugging
            if expected != actual:
                print(f"Error: on line: {lineIndex}")

            self.assertEqual(actual, expected)

            lineIndex += 1

        pass

if __name__ == '__main__':
    unittest.main()