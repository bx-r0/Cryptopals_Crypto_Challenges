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
import Set3.Challenge24.Challenge24 as c24


class Set3(unittest.TestCase):

    def test_C17(self):
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

    def test_C18(self):

        # Full block of data
        expected = c18.dataText

        actual = c18.task18()

        self.assertEqual(actual, expected)

    def test_C19(self):
        c19.task19()

    def test_C20(self):
        c20.task20()

    def test_C21(self):

        expected = [2807145907, 882709079, 493951047, 2621574848, 4081433851]
        actual = c21.task21()

        self.assertEqual(actual, expected)

    def test_C22(self):
        expected, actual = c22.task22()

        self.assertEqual(actual, expected)        

    def test_C23(self):
        originalMT, clonedMT = c23.task23()

        # Generates an integer from the orginal and cloned
        # PRNGs
        expected = originalMT.getInt()
        actual = clonedMT.getInt()

        self.assertEqual(actual, expected)

    def test_C24(self):
        expected = 123
        actual = c24.task24(expected)

        self.assertEqual(actual, expected)

        expected = 1
        actual = c24.task24(expected)

        self.assertEqual(actual, expected)
