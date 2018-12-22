import sys ; sys.path += ['.', '../..']
import unittest
from CryptoCode.MD4 import MD4


class MD4Tests(unittest.TestCase):


    def testDigest1(self):
        self.MD4Hash([b"", "31d6cfe0d16ae931b73c59d7e0c089c0"])

    def testDigest2(self):
        self.MD4Hash([b"a", "bde52cb31de33e46245e05fbdbd6fb24"])
    
    def testDigest3(self):
        self.MD4Hash([b"abc", "a448017aaf21d8525fc10ae87aa6729d"])
    
    def testDigest4(self):
        self.MD4Hash([b"message digest", "d9130a8164549fe818874806e1c7014b"])
    
    def testDigest5(self):
        self.MD4Hash([b"abcdefghijklmnopqrstuvwxyz", "d79e1c308aa5bbcdeea8ed63df412da9"])
    
    def testDigest6(self):
        self.MD4Hash([b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", \
                        "043f8582f241db351ce627e153e7f0e4"])
                    
    def testDigest7(self):
        self.MD4Hash([b"12345678901234567890123456789012345678901234567890123456789012345678901234567890", \
                        "e33b4ddc9c38f2199c3e7b164fcc0536"])

    # testcase - [Input, Expected]
    def MD4Hash(self, testCase):
        actual = MD4.createDigestHex(testCase[0])
        expected = testCase[1]

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(MD4Tests)
    unittest.TextTestRunner(verbosity=2).run(suite)



