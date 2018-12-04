import codecs
import base64
import re
import os
import random
import binascii
from Crypto.Cipher import AES


englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99,
                     'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
                     'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

class File():

    @staticmethod
    def loadLines(callingFile):
        """
        Loads all data from file as a list of lines
        """

        filePath = File.getRealPath(callingFile) + "/data.txt"

        with open(filePath, 'r') as file:
            data = file.readlines()
        
        return data

    @staticmethod
    def loadData(callingFile):
        """
        Loads all data from file as a single data chunk
        """
        
        filePath = File.getRealPath(callingFile) + "/data.txt"

        with open(filePath, 'r') as file:
            data = file.read()
        
        return data

    @staticmethod
    def getRealPath(file):
        """
        Gets raw path of the current script
        """
        path = os.path.realpath(file)

        pathSections = path.split("/")
        del pathSections[-1] # Deletes the file name

        return "/".join(pathSections)

class Conversion():

    @staticmethod
    def remove_byte_notation(string):
        """
        Forceful way of removing the byte notation
        """
        return str(string)[2:-1]

class HexTo():
        @staticmethod
        def base64(input):
            """
            Hex --> Base64
            """

            # Ensures the hex value has the correct number of digits
            if len(input) % 2 is not 0:
                input = "0" + input


            input_bytes = codecs.decode(input, 'hex')
            return base64.b64encode(input_bytes)
        
        @staticmethod
        def utf8(hex):
            """
            Hex --> UTF-8
            """

            b = codecs.decode(hex, 'hex')
            return codecs.decode(b, 'utf-8')
        
        @staticmethod
        def binary(hex):
            """
            Binary --> Hex 
            """

            return bin(hex)[2:]

        @staticmethod
        def utf8_check(hex):
            """
            Checks a hex value produces a valid UTF-8 string
            """
            try:
                _ = codecs.decode(codecs.decode(hex, 'hex'), 'utf-8')
                return True
            except Exception:
                return False

class Base64_To():
    @staticmethod
    def hexadecimal(input):
        """
        Base64 --> Hex
        """
        bytes = base64.b64decode(input)
        hex = codecs.encode(bytes, 'hex')
        return hex

    @staticmethod
    def rawBytes(input):
        """
        Decodes a base64 value
        """
        return base64.b64decode(input)

    @staticmethod
    def utf8(input):
        """
        Base64 --> UTF-8
        """
        b = base64.b64decode(input)
        return b.decode('utf-8')

    @staticmethod
    def binary(input):
        """
        Base64 --> Binary
        """

        return bin(int(base64.b64decode(input).hex(), 16))[2:]

    @staticmethod
    def concat(inputList):
        """
        Combines a list of base64 values in a single value
        """

        byteValues = b""
        for x in inputList:
            byteValues += base64.b64decode(x)

        return base64.b64encode(byteValues)

class UTF8():
    @staticmethod
    def hexadecimal(string):
        """
        Converts an utf-8 string to a hex string
        """
        b = codecs.encode(string, 'utf-8')
        return codecs.encode(b, 'hex')

    @staticmethod
    def base64(string):
        """
        Converts an utf-8 string to a base64 string
        """
        return base64.b64encode(string.encode('utf-8'))

class XOR():

    @staticmethod
    def b64_Xor(a, b):
        """
        Produces an XOR Result of two equal length Base64 encoded values
        """
        
        bytesA = base64.b64decode(a)
        bytesB = base64.b64decode(b)

        result = []
        for b1, b2 in zip(bytesA, bytesB):
            result.append(bytes([b1 ^ b2]))
        
        result = b"".join(result)
        return base64.b64encode(result)

    @staticmethod
    def hexXor(a, b):
        """
        Produces an XOR result of two equal length Hex values
        """

        if len(a) != len(b):
            raise("Error: incorrect length in hexXor")

        length = len(a)

        binA = bin(int(a, 16))[2:].zfill(length)
        binB = bin(int(b, 16))[2:].zfill(length)

        xor = int(binA, 2) ^ int(binB, 2)

        # Format ensures that the hex values are always the same length
        hexOutput = format(xor, f"#0{length + 2}x")[2:]

        return hexOutput
    
class Statistical():
    
    @staticmethod
    def score_distribution(text):
        """
        Calculates a score for how close the distribution is to
        english. The lower the score, the better
        """

        def create_distribution(text):
            """
            Creates the distrubution for a set of text
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

    class AES():

        @staticmethod
        def randomKeyHex(blocksize=16):
            """
            Method used to generated a 'random' key
            """
            key = ""
            for _ in range(blocksize):
                key += hex(random.randint(0,255))[2:].zfill(2)

            return key

        @staticmethod
        def randomKeyBase64(blocksize=16):
            k = Encryption.AES.randomKeyHex(blocksize)
            return HexTo.base64(k)

        @staticmethod
        def ECB_Encrypt(key, data, cipher=None, blocksize=16):
            """
            >>> All data must be base64 <<<
            Encrypts data under AES ECB mode
            """

             # Converts key to bytes
            key = base64.b64decode(key)

            if cipher is None:
                cipher = AES.new(key, AES.MODE_ECB)

            func = lambda cipher, block: cipher.encrypt(base64.b64decode(block))
            e = Encryption.AES.__ECB__(func, cipher, data, blocksize)
            return base64.b64encode(e)

        @staticmethod
        def ECB_Decrypt(key, data, cipher=None, blocksize=16):
            """
            >>> All data must be base64 <<<
            Decrypts data in AES ECB mode
            """
             # Converts key to bytes
            key = base64.b64decode(key)

            if cipher is None:
                cipher = AES.new(key, AES.MODE_ECB)

            func = lambda cipher, block: cipher.decrypt(base64.b64decode(block))
            e = Encryption.AES.__ECB__(func, cipher, data, blocksize)
            return base64.b64encode(e)
        
        @staticmethod
        def __ECB__(encryptionFunc, cipher, data, blocksize=16):
            """
            PRIVATE - Call ECB_Encrypt or ECB_Decrypt instead
            """

            # Will split into blocks
            blocks = Encryption.splitBase64IntoBlocks(data, blocksize)

            plaintext = b""
            for block in blocks:
                x = encryptionFunc(cipher, block)
                plaintext += x

            return plaintext

        @staticmethod
        def CBC_Encrypt(iv, key, data, blocksize=16):
            """
            >>> All data must be Base64 <<<
            Encrypts data in AES CBC mode
            """

            blocks = Encryption.splitBase64IntoBlocks(data, blocksize)
            
            # Initalisation
            previous = iv
            cipherText = []

            for block in blocks:
            
                # XORed with the previous
                xor = XOR.b64_Xor(previous, block)

                # Encrypted
                ct = Encryption.AES.ECB_Encrypt(key, xor)

                # Saved
                cipherText.append(base64.b64decode(ct))
                previous = ct

            cipherText = b"".join(cipherText)
            return base64.b64encode(cipherText)

        @staticmethod
        def CBC_Decrypt(iv, key, data, blocksize=16):
            """
            >>> All data must be Base64 <<<
            Decrypts data encrypted using AES CBC mode            
            """

            blocks = Encryption.splitBase64IntoBlocks(data, blocksize)
            previous = iv
            plainText = b""

            for block in blocks:
                
                # Decrypts the data
                d = Encryption.AES.ECB_Decrypt(key, block)
                
                pt = XOR.b64_Xor(previous, d)

                plainText += base64.b64decode(pt)

                previous = block

            return base64.b64encode(plainText)

        @staticmethod
        def ECB_Detect(blocks):
            """
            Used to check for any repeating blocks.
            This is a sign ECB is being used
            """
            seen = set()
            for block in blocks:
                if block in seen:
                    return True
                
                seen.add(block)
            return False

        @staticmethod
        def generateCipherText(email, key):
            """
            Method used to generate valid cipher text
            """

            data = Encryption.profileFor(email)

            base64Profile = base64.b64encode(data.encode("utf-8"))
            return Encryption.AES.ECB_Encrypt(key, base64Profile)

    class PKCS7():

        paddingChar = "\x04"
        exceptionMessage = "Error: Invalid PKCS#7 padding"

        @staticmethod
        def isValid(string):
            """
            Validates valid PKCS7. If padding is valid it will return the stripped string
            On invalid padding the method will throw an exception

            Note: No padding will be determined valid.
            """

            padding = []
            for char in reversed(string):

                # Should not having padding values that are higher than 16 in ascii
                if ord(char) < 10:
                    padding.append(char)

            
            # Checks if the whole padding is the target char
            for pad in padding:
                if pad != Encryption.PKCS7.paddingChar:
                    raise(Exception(Encryption.PKCS7.exceptionMessage))

            # Removes padding
            string = string.replace(Encryption.PKCS7.paddingChar, "")

            return string

        @staticmethod
        def add(blocksize, string):
            """
            Adds PKCS#7 padding to a provided string
            """

            # Finds the next closest block
            targetBlockNumber = int(len(string) / blocksize) + 1

            # Calculates how many characters are needed to get to the next block
            difference = (blocksize * targetBlockNumber) - (len(string))

            return string + "\x04" * difference

    @staticmethod
    def removePadding(padding, string):
        """
        Simple method designed to quickly remove padding from a strings
        """

        return string.replace(padding, "")

    @staticmethod
    def splitBase64IntoBlocks(string, blocksize=16):
        """
        Takes a base64 string and returns a list of certain length blocks
        """

        # Converts to hex
        hex= Conversion.remove_byte_notation(Base64_To.hexadecimal(string))
        bytes=re.findall("..", hex)

        # Adds padding if the lengths are not equal
        while len(bytes) % blocksize != 0:
            bytes.append("00")

        chunks=[]
        for x in range(0, len(bytes), blocksize):
            chunk=""

            for i in range(x, x + blocksize):
                chunk += bytes[i]
            chunks.append(HexTo.base64(chunk))

        return chunks

    @staticmethod
    def profileFor(email, admin=False):
        """
        Generates a user cookie for a provided email
        """

        r = re.match(r"^[^=&]+$", email)

        if r is None:
            raise(Exception("Invalid email!"))

        uid = 10

        if admin:
            role = "admin"
        else:
            role = "user"

        string = f"email={email}&uid={uid}&role={role}"

        return string

def makeBinaryEqualLength(bin1, bin2):
    """
    Makes sure two binary values are the same length
    """

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
