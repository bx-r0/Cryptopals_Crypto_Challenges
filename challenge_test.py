import unittest
import Set_1.Challenge1.Challenge1 as c1
import Set_1.Challenge2.Challenge2 as c2
import Set_1.Challenge3.Challenge3 as c3
import Set_1.Challenge4.Challenge4 as c4
import Set_1.Challenge5.Challenge5 as c5
import Set_1.Challenge6.Challenge6 as c6
import Set_1.Challenge7.Challenge7 as c7

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

        # Output is too long to check verbatim
        # The test will just run and check for any exceptions
        c7.task7()

class C8(unittest.TestCase):

    def test(self):
        pass



if __name__ == '__main__':
    unittest.main()