import unittest

# Set4
import Set4.Challenge25.Challenge25 as c25
import Set4.Challenge26.Challenge26 as c26
import Set4.Challenge27.Challenge27 as c27
import Set4.Challenge28.Challenge28 as c28
import Set4.Challenge29.Challenge29 as c29
import Set4.Challange30.Challenge30 as c30


class Set4(unittest.TestCase):

    def test_C25(self):
        c25.task25()

    def test_C26(self):
        c26.task26()

    def test_C27(self):
        expected = b"Iy+3X45YfPlOO3chczEXjA=="

        # Sets static values
        c27.key = expected
        c27.iv = expected

        actual = c27.task27()
        self.assertEqual(actual, expected)

    def test_C28(self):
        c28.task28()

    def test_C29(self):
        c29.task29()

    def test_C30(self):
        c30.task30()