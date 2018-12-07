import base64
import unittest
import commonTestCode

# SET 3
import Set3.Challenge17.Challenge17 as c17
import Set3.Challenge18.Challenge18 as c18
import Set3.Challenge19.Challenge19 as c19
import Set3.Challenge20.Challenge20 as c20

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