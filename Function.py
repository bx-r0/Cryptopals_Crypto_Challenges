from Crypto.Cipher import AES
from Crypto.Hash import SHA
import random
import codecs
import string
import base64
import sys
import re
import os


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
        del pathSections[-1]  # Deletes the file name

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
    def base64(string):
        """
        Hex --> Base64
        """

        # Ensures the hex value has the correct number of digits
        if len(string) % 2 is not 0:
            string = "0" + string

        input_bytes = codecs.decode(string, 'hex')
        return base64.b64encode(input_bytes)

    @staticmethod
    def utf8(string):
        """
        Hex --> UTF-8
        """

        b = codecs.decode(string, 'hex')
        return codecs.decode(b, 'utf-8')

    @staticmethod
    def binary(string):
        """
        Binary --> Hex
        """

        return bin(string)[2:]

    @staticmethod
    def utf8_check(string):
        """
        Checks a hex value produces a valid UTF-8 string
        """
        try:
            _ = codecs.decode(codecs.decode(string, 'hex'), 'utf-8')
            return True
        except Exception:
            return False


class Base64_To():
    @staticmethod
    def hexadecimal(string):
        """
        Base64 --> Hex
        """
        hexBytes = base64.b64decode(string)
        return codecs.encode(hexBytes, 'hex')

    @staticmethod
    def rawBytes(string):
        """
        Decodes a base64 value
        """
        return base64.b64decode(string)

    @staticmethod
    def utf8(string):
        """
        Base64 --> UTF-8
        """
        b = base64.b64decode(string)
        return b.decode('utf-8')

    @staticmethod
    def binary(string):
        """
        Base64 --> Binary
        """

        return bin(int(base64.b64decode(string).hex(), 16))[2:]

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

        @staticmethod
        def transpose_bytes(data_chunks):
            # Converts to hex for easer manipulation
            data_chunks = list(map(Base64_To.hexadecimal, data_chunks))

            chunkLen = round(len(data_chunks[0]) / 2)

            transposed = []

            # A new byte value will be created from the 1st of all
            # byte values, the 2nd and so on
            for pos in range(chunkLen):

                byteString = ""

                for chunk in data_chunks:
                    each_hex_byte = re.findall(
                        "..", Conversion.remove_byte_notation(chunk))
                    byteString += each_hex_byte[pos]

                transposed.append(byteString)

            return transposed

    class AES():

        @staticmethod
        def randomKeyHex(blocksize=16):
            """
            Method used to generated a 'random' key
            """
            key = ""
            for _ in range(blocksize):
                key += hex(random.randint(0, 255))[2:].zfill(2)

            return key

        @staticmethod
        def randomKeyBase64(blocksize=16):
            k = Encryption.AES.randomKeyHex(blocksize)
            return HexTo.base64(k)

        @staticmethod
        def generateCipherText(email, key):
            """
            Method used to generate valid cipher text
            """

            data = Encryption.profileFor(email)

            base64Profile = base64.b64encode(data.encode("utf-8"))
            return Encryption.AES.ECB.Encrypt(key, base64Profile)

        class ECB():

            @staticmethod
            def Encrypt(key, data, blocksize=16):
                """
                >>> All data must be base64 <<<
                Encrypts data under AES ECB mode
                """

                # Converts key to bytes
                key = base64.b64decode(key)

                cipher = AES.new(key, AES.MODE_ECB)

                def func(cipher, block): return cipher.encrypt(
                    base64.b64decode(block))
                e = Encryption.AES.ECB.__ECB__(func, cipher, data, blocksize)
                return base64.b64encode(e)

            @staticmethod
            def Decrypt(key, data, blocksize=16):
                """
                >>> All data must be base64 <<<
                Decrypts data in AES ECB mode
                """
                # Converts key to bytes
                key = base64.b64decode(key)

                cipher = AES.new(key, AES.MODE_ECB)

                def func(cipher, block): return cipher.decrypt(
                    base64.b64decode(block))
                e = Encryption.AES.ECB.__ECB__(func, cipher, data, blocksize)
                return base64.b64encode(e)

            @staticmethod
            def Detect(blocks):
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
            def __ECB__(encryptionFunc, cipher, data, blocksize=16):
                """
                PRIVATE - Call ECB_Encrypt or ECB_Decrypt instead.
                Designed to be a generic function
                """

                # Will split into blocks
                blocks = Encryption.splitBase64IntoBlocks(data, blocksize)

                plaintext = b""
                for block in blocks:
                    x = encryptionFunc(cipher, block)
                    plaintext += x

                return plaintext

        class CBC():

            @staticmethod
            def Encrypt(iv, key, data, blocksize=16):
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
                    ct = Encryption.AES.ECB.Encrypt(key, xor)

                    # Saved
                    cipherText.append(base64.b64decode(ct))
                    previous = ct

                cipherText = b"".join(cipherText)
                return base64.b64encode(cipherText)

            @staticmethod
            def Decrypt(iv, key, data, blocksize=16):
                """
                >>> All data must be Base64 <<<
                Decrypts data encrypted using AES CBC mode
                """

                blocks = Encryption.splitBase64IntoBlocks(data, blocksize)
                previous = iv
                plainText = b""

                for block in blocks:

                    # Decrypts the data
                    d = Encryption.AES.ECB.Decrypt(key, block)

                    pt = XOR.b64_Xor(previous, d)

                    plainText += base64.b64decode(pt)

                    previous = block

                return base64.b64encode(plainText)

        class CTR():

            @staticmethod
            def Encrypt_Decrypt(nonce, key, data, blocksize=16):
                """
                CTR Uses the same function to decrypt and encrypt, therefore, the
                same method can be used
                """

                # Little endian is used for the nonce and counter
                byteorder = "little"

                counter = 0
                cipherText = []

                nonceBytes = nonce.to_bytes(8, byteorder=byteorder)
                plainTextBlocks = Encryption.splitBase64IntoBlocks(data)

                for plainTextBlock in plainTextBlocks:
                    counterBytes = counter.to_bytes(8, byteorder=byteorder)
                    inputData = nonceBytes + counterBytes

                    # Encrypt
                    e = Encryption.AES.ECB.Encrypt(
                        key, base64.b64encode(inputData))

                    ct = XOR.b64_Xor(e, plainTextBlock)

                    cipherText.append(ct)

                    counter += 1

                return Base64_To.concat(cipherText)

            @staticmethod
            def sameNonceStatisticalAttack(cipherTexts):

                # Used to validate guesses
                validChars = string.ascii_letters + "\- ?!',.:;\'\"/" + "0123456789"

                keyStream = []
                plainTextStrings = []

                # Finds the length of the cipher texts.
                # The first length is taken due to all the cipher texts being the same length
                cipherTextLen = len(
                    Encryption.splitBase64IntoBlocks(cipherTexts[0], 1))

                # Transposes the bytes to solve it like a Vigenere cipher
                transposedCipherTexts = Encryption.Vigenere.transpose_bytes(
                    cipherTexts)
                transposedCipherTexts = list(
                    map(HexTo.base64, transposedCipherTexts))

                # Decrypts for the length of the cipherText
                for cipherTextGuess in range(0, cipherTextLen):

                    # Score, Plaintext, KeyByte
                    best = [None, None, None]

                    # Makes a guess for a key byte
                    for i in range(0, 256):

                        plainText = b""

                        # Converts into a single byte base64 value
                        char = bytes.fromhex(hex(i)[2:].zfill(2))
                        keyByteGuess = base64.b64encode(char)

                        ctBytes = Encryption.splitBase64IntoBlocks(
                            transposedCipherTexts[cipherTextGuess], blocksize=1)

                        for ctByte in ctBytes:
                            pt = XOR.b64_Xor(ctByte, keyByteGuess)
                            plainText += base64.b64decode(pt)

                        # If the decoding fails the plaintext is ignored
                        try:
                            strPt = plainText.decode(
                                'utf-8').replace("\x00", "")

                            # Helps filter out options that give invalid outputs
                            if re.match(f"^[{validChars}]+$", strPt):
                                score = Statistical.score_distribution(strPt)

                                if best[0] is None or best[0] > score:
                                    best[0] = score
                                    best[1] = plainText
                                    best[2] = keyByteGuess
                        except UnicodeDecodeError:
                            pass

                    # If there is an error finding a key candiate
                    if best[2] is None:
                        print("ERROR - Key candiate not found. Stopping...")
                        print()
                        break

                    # Adds the best keystream
                    keyStream.append(best[2])

                # XORs the intermediate data with the ciphertext to get the plaintext
                for cipher in cipherTexts:

                    plainText = b""
                    cipherTextBlock = Encryption.splitBase64IntoBlocks(
                        cipher, 1)

                    for index, keyByte in enumerate(keyStream):
                        pt = XOR.b64_Xor(keyByte, cipherTextBlock[index])
                        plainText += base64.b64decode(pt)

                    # To lower to filter out issues with upper case being counted
                    plainTextStrings.append(plainText.decode('utf-8').lower())

                return plainTextStrings

    class PKCS7():

        exceptionMessage = "Error: Invalid PKCS#7 padding"

        @staticmethod
        def isValid(string):
            """
            Validates valid PKCS7. If padding is valid it will return the stripped string
            On invalid padding the method will throw an exception
            """

            paddingLength = string[-1]
            paddingValue = ord(paddingLength)

            # Grabs the padding
            padding = string[len(string) - paddingValue:]

            for pad in padding:
                if ord(pad) != paddingValue:
                    raise(Exception())

            # Stips the padding
            return string[:len(string) - paddingValue]

        @staticmethod
        def isValidBool(string):
            try:
                Encryption.PKCS7.isValid(string)
                return True

            # If an exception is thrown, padding is invalid
            except Exception:
                return False

        @staticmethod
        def isValidBase64(base64String):
            """
            Validates PKCS#7 padding for a base64 encoded value
            """

            base64Bytes = Encryption.splitBase64IntoBlocks(
                base64String, blocksize=1)

            paddingLength = ord(base64.b64decode(base64Bytes[-1]))

            padding = base64Bytes[len(base64Bytes) - paddingLength:]

            # Checks for a correct final byte
            if paddingLength < 1 or paddingLength > 16:
                raise(Exception("Error: Invalid padding - Final byte was invalid"))

            # Checks the pad for the same value
            for pad in padding:
                if ord(base64.b64decode(pad)) != paddingLength:
                    raise(
                        Exception ("Error: Invalid padding - Padding is not formed correctly"))

            # Returns the string without the padding
            return Base64_To.concat(base64Bytes[:len(base64Bytes) - paddingLength])

        @staticmethod
        def isValidBase64Bool(base64String):
            try:
                Encryption.PKCS7.isValidBase64(base64String)
                return True

            # If an exception is thrown, padding is invalid
            except Exception:
                return False

        @staticmethod
        def add(string, blocksize=16):
            """
            Adds PKCS#7 padding to a provided string
            """

            # Finds the next closest block
            targetBlockNumber = int(len(string) / blocksize) + 1

            # Calculates how many characters are needed to get to the next block
            difference = (blocksize * targetBlockNumber) - (len(string))

            return string + chr(difference) * difference

        @staticmethod
        def addBase64(string, blocksize=16):
            """
            Adds padding to a base64 string
            """

            def addPadding(number, string):
                """
                Adds padding specified by the number to the string
                """

                paddingAndString = [string]

                # Adds the padding values acording to the specification
                paddingAndString += [base64.b64encode(
                    chr(number).encode('utf-8'))] * number

                # Creates one base64 value
                return Base64_To.concat(paddingAndString)

            numberOfBytes = len(Encryption.splitBase64IntoBlocks(string, 1))

            # Finds the next closest block
            targetBlockNumber = int(numberOfBytes / blocksize) + 1

            # Calculates how many characters are needed to get to the next block
            difference = (blocksize * targetBlockNumber) - numberOfBytes

            return addPadding(difference, string)

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
        hexString = Conversion.remove_byte_notation(Base64_To.hexadecimal(string))

        hexBytes = re.findall("..", hexString)

        # Adds padding if the lengths are not equal
        while len(hexBytes) % blocksize != 0:
            hexBytes.append("00")

        chunks = []
        for x in range(0, len(hexBytes), blocksize):
            chunk = ""

            for i in range(x, x + blocksize):
                chunk += hexBytes[i]
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


class SHA_MAC():
    
    @staticmethod
    def create(key, message):
        """
        Creates a tag for a message
        """

        messageB64 = base64.b64encode(message)
        hashData = Base64_To.concat([key, messageB64])
        mac = SHA_MAC.HashBase64(hashData)

        return mac

    @staticmethod
    def verify(key, message, mac):
        messageCheck = SHA_MAC.create(key, message)
        return messageCheck == mac

    @staticmethod
    def HashBase64(dataB64):
        h = SHA.new()
        h.update(base64.b64decode(dataB64))
        hB64 = base64.b64encode(h.digest())
        return hB64


class BitFlippingAttacks():
    
    # Terminal colours
    class COLOURS:
        RED = "\033[91m"
        GREEN = "\033[92m"
        RESET = "\033[0m"

    @staticmethod
    def createString(userData):
        """
        Formats and encrypts our string
        """

        # Special characters are returned
        userData = userData.replace(';', '\;')
        userData = userData.replace('=', '\=')

        pre = "comment1=cooking%20MCs;userdata="
        post = ";comment2=%20like%20a%20pound%20of%20bacon"

        string = pre + userData + post

        # Adds padding and returns
        plaintext = Encryption.PKCS7.add(string)

        # Encodes to base64 and returns
        return base64.b64encode(plaintext.encode('utf-8'))

    @staticmethod
    def colouredOutput(access):
        
        if access:
            print(BitFlippingAttacks.COLOURS.GREEN + 
            "Access granted!" + 
            BitFlippingAttacks.COLOURS.RESET)
        else:
            print(BitFlippingAttacks.COLOURS.RED + 
            "Access denied!" + 
            BitFlippingAttacks.COLOURS.RESET)

    @staticmethod
    def flip(currentVal, currentChar, targetChar):

        currentValHex = Base64_To.hexadecimal(currentVal)

        # XORs the values to produce the bit change
        xor = hex(int(currentValHex, 16) ^ ord(currentChar) ^ ord(targetChar))[2:]

        return HexTo.base64(xor)

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
