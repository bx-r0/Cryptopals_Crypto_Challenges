import unittest
from CryptoCode.SHA1 import SHA1


class SHATests(unittest.TestCase):
    
    def testDigest1(self):
        self.SHA1Hash([b"", "da39a3ee5e6b4b0d3255bfef95601890afd80709"])

    def testDigest2(self):
        self.SHA1Hash([b"a", "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8"])

    def testDigest3(self):
        self.SHA1Hash([b"abc", "a9993e364706816aba3e25717850c26c9cd0d89d"])

    def testDigest4(self):
        self.SHA1Hash([b"message digest", "c12252ceda8be8994d5fa0290a47231c1d16aae3"])

    def testDigest5(self):
        self.SHA1Hash([b"abcdefghijklmnopqrstuvwxyz", "32d10c7b8cf96570ca04ce37f2a19d84240d3a89"])

    def testDigest6(self):
        self.SHA1Hash([b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
                        "761c457bf73b14d27e9e9265c46f4b4dda11f940"])

    def testDigest7(self):
        self.SHA1Hash([b"12345678901234567890123456789012345678901234567890123456789012345678901234567890", 
                        "50abf5706a150990a08b2c5ea40fa0e585554732"])

    # testcase - [Input, Expected]
    def SHA1Hash(self, testCase):
        actual = SHA1.createDigestHex(testCase[0])
        expected = testCase[1]

        self.assertEqual(actual, expected)