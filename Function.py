import codecs
import base64
import re
import os


englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99,
                     'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
                     'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

class Conversion():

    @staticmethod
    def remove_byte_notation(string):
        """
        Forceful way of removing the byte notation
        """
        return str(string)[2:-1]

    @staticmethod
    def baseX_to_binary(string, base, min_length):
        return str(bin(int(string, base)))[2:].zfill(min_length)

class Hex():
        @staticmethod
        def hex_to_base64(input):
            """
            TODO
            """
            input_bytes = codecs.decode(input, 'hex')
            return base64.b64encode(input_bytes)
        
        @staticmethod
        def hex_to_utf(hex):
            """
            Converts an hex string to a utf-8 string
            """

            b = codecs.decode(hex, 'hex')
            return codecs.decode(b, 'utf-8')
        
        @staticmethod
        def hex_to_binary(h):
            return bin(h)[2:]

        @staticmethod
        def hex_to_utf_check(hex):
            """
            TODO
            """
            try:
                _ = codecs.decode(codecs.decode(hex, 'hex'), 'utf-8')
                return True
            except Exception:
                return False

class Base_64():
    @staticmethod
    def base64_to_hex(input):
        """
        TODO
        """
        bytes = base64.b64decode(input)
        hex = codecs.encode(bytes, 'hex')
        return hex

    @staticmethod
    def base64_to_raw_bytes(input):
        """
        Decodes a base64 value
        """
        return base64.b64decode(input)

    @staticmethod
    def base64_to_utf(input):
        """
        Converts a base64 value into a utf-8 string
        """
        b = base64.b64decode(input)
        return Conversion.remove_byte_notation(b)

class UTF8():
    @staticmethod
    def utf_to_hex(string):
        """
        Converts an utf-8 string to a hex string
        """
        b = codecs.encode(string, 'utf-8')
        return codecs.encode(b, 'hex')

class XOR():

    @staticmethod
    def hexxor(a, b):
        if len(a) != len(b):
            raise("Error: incorrect length in hexXor")

        length = len(a)

        binA = bin(int(a, 16))[2:].zfill(length)
        binB = bin(int(b, 16))[2:].zfill(length)

        xor = int(binA, 2) ^ int(binB, 2)

        # Format ensures that the hex values are always the same length
        hexOutput = format(xor, f"#0{length + 2}x")[2:]

        return hexOutput
    
    @staticmethod
    def strxor(a, b):
        """
        XOR operation for two different strings.
        This method also supports differing length strings
        """
        if len(a) > len(b):
            return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
        else:
            return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

class Statistical():
    
    @staticmethod
    def score_distribution(text):
        """
        Calculates a score for how close the distribution is to
        english. Lower the better
        :return:
        """

        def create_distribution(text):
            """
            Creates the distrubution for a set of text
            :return:
            """

            letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0,
                        'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0,
                        'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

            total_size = len(text)

            for letter in text:
                
                # Ignores a space
                if letter.isalpha():
                    letterCount[letter.capitalize()] += 1

            # Turns the values into percentages
            for char in letterCount:
                letterCount[char] = (letterCount[char] / total_size) * 100

            return letterCount

        score = 0

        actual_freq = create_distribution(text)

        for letter in englishLetterFreq:
            english_freq_letter = englishLetterFreq[letter]
            actual_freq_letter = actual_freq[letter]

            score += abs(english_freq_letter - actual_freq_letter)

        return score

class Encryption():

    class Vigenere():

        @staticmethod
        def gen_key(string, key): 
            """
            Generates the repeating sequence of the Vigenere key
            """
            length = len(string)

            total_key = ""
            looper = 0
            for _ in range(0, length):

                total_key += key[looper]

                # If the looper goes over the boundary reset
                if looper >= len(key) - 1:
                    looper = 0
                else:
                    looper += 1

            return total_key

    @staticmethod
    def split_base64_into_blocks(string, number):
        """
        Takes a base64 string and returns a list of certain length blocks
        """

        # Converts to hex
        hex= Conversion.remove_byte_notation(Base_64.base64_to_hex(string))
        bytes=re.findall("..", hex)

        # Adds padding if the lengths are not equal
        while len(bytes) % number != 0:
            bytes.append("00")

        chunks=[]
        for x in range(0, len(bytes), number):
            chunk=""

            for i in range(x, x + number):
                chunk += bytes[i]
            chunks.append(Hex.hex_to_base64(chunk))

        return chunks


def getRealPath(file):
    """
    Gets raw path of the current script
    """
    path = os.path.realpath(file)

    pathSections = path.split("/")
    del pathSections[-1] # Deletes the file name

    return "/".join(pathSections)

def make_binary_equal_length(bin1, bin2):
    b1Len = len(bin1)
    b2Len = len(bin2)

    if b1Len == b2Len:
        return bin1, bin2
    else:
        if b1Len > b2Len:
            bin2 = bin2.zfill(b1Len)
        else:
            bin1 = bin1.zfill(b2Len)

        return bin1, bin2


