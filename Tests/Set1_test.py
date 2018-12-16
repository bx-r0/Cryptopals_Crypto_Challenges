import unittest

# SET 1
import Set1.Challenge1.Challenge1 as c1
import Set1.Challenge2.Challenge2 as c2
import Set1.Challenge3.Challenge3 as c3
import Set1.Challenge4.Challenge4 as c4
import Set1.Challenge5.Challenge5 as c5
import Set1.Challenge6.Challenge6 as c6
import Set1.Challenge7.Challenge7 as c7
import Set1.Challenge8.Challenge8 as c8


class Set1(unittest.TestCase):

    def test_C1(self):
        expected = b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        actual = c1.task1()

        self.assertEqual(actual, expected)

    def test_C2(self):
        expected = b"746865206b696420646f6e277420706c6179"
        actual = c2.task2()

        self.assertEqual(actual, expected)

    def test_C3(self):
        # Expected key value
        expected = "58"
        actual = c3.task3()

        self.assertEqual(actual, expected)

    def test_C4(self):
        expected = ("35", "Now that the party is jumping\n")
        actual = c4.task4()

        self.assertEqual(actual, expected)

    def test_C5(self):
        expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
        actual = c5.task5()

        self.assertEqual(actual, expected)

    def test_C6(self):

        # TODO - Why is the output from the task formatted strange?
        expected = "TERMINATOR\x00X\x1a\x00BRING\x00THE\x00NOISE"
        actual = c6.task6()

        self.assertEqual(actual, expected)

    def test_C7(self):

        c7.task7()

    def test_C8(self):
        expected = ["d880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a"]
        actual = c8.task8()

        self.assertEqual(expected, actual)
