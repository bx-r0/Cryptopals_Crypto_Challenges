import base64
import unittest
import commonTestCode

# SET 3
import Set3.Challenge17.Challenge17 as c17
import Set3.Challenge18.Challenge18 as c18
import Set3.Challenge19.Challenge19 as c19
import Set3.Challenge20.Challenge20 as c20
import Set3.Challenge21.Challenge21 as c21
import Set3.Challenge22.Challenge22 as c22
import Set3.Challenge23.Challenge23 as c23


class C17(unittest.TestCase):

    def test(self):
        data = commonTestCode.loadLines("/../Set3/Challenge17/data.txt")
        
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

class C18(unittest.TestCase):
     
     def test(self):
        
        # Full block of data
        expected = c18.dataText

        actual = c18.task18()

        self.assertEqual(actual, expected)

class C19(unittest.TestCase):

    def test(self):
        c19.task19()

class C20(unittest.TestCase):

    def test(self):
        c20.task20()

class C21(unittest.TestCase):

    def test(self):

        expected = [2807145907, 882709079, 493951047, 2621574848, 4081433851]
        actual = c21.task21()

        self.assertEqual(actual, expected)

class C22(unittest.TestCase):

    # TODO
    def test(self):
        pass

class C23(unittest.TestCase):

    #TODO
    def test(self):
        pass