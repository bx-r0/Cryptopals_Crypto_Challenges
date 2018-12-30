import sys ; sys.path += ['.', '../..']
from CryptoCode.SHA1 import SHA1
from CryptoCode.MD4 import MD4
import SharedCode.Function as Function
import base64

class MAC():
    
    class SHA():

        @staticmethod
        def create(key, message):
            """
            Creates a tag for a message
            """

            messageB64 = base64.b64encode(message)
            hashData = Function.Base64_To.concat([key, messageB64])
            mac = MAC.SHA.HashBase64(hashData)

            return mac

        @staticmethod
        def verify(key, message, mac):
            messageCheck = MAC.SHA.create(key, message)
            return messageCheck == mac

        @staticmethod
        def HashBase64(dataB64):
            return SHA1.createDigest(base64.b64decode(dataB64))

    class MD4():

        @staticmethod
        def create(key, message):
            """
            Creates a tag for a message
            """

            messageB64 = base64.b64encode(message)
            hashData = Function.Base64_To.concat([key, messageB64])
            mac = MAC.MD4.HashBase64(hashData)

            return mac

        @staticmethod
        def verify(key, message, mac):
            messageCheck = MAC.MD4.create(key, message)
            return messageCheck == mac

        @staticmethod
        def HashBase64(dataB64):
            return MD4.createDigest(base64.b64decode(dataB64))

class HMAC():

    class SHA():

        @staticmethod
        def create(keyBytes, messageBytes, blocksize=64):
            
            # If key is longer than the blocksize:
            if len(keyBytes) > blocksize:
                keyHashBase64 = SHA1.createDigest(keyBytes)
                keyBytes = base64.b64decode(keyHashBase64)
            # Padding
            else:
                while len(keyBytes) < blocksize:
                    keyBytes += b"\x00"

            # Creates pads
            opad = b"\x5c" * blocksize
            ipad = b"\x36" * blocksize

            # Xors pads with the key
            opad_key = Function.XOR.bytesXor(opad, keyBytes)
            ipad_key = Function.XOR.bytesXor(ipad, keyBytes)

            innerHash = SHA1.createDigest(ipad_key + messageBytes)
            innerHashBytes = base64.b64decode(innerHash)

            return SHA1.createDigest(opad_key + innerHashBytes)

        @staticmethod
        def verify(keyBytes, messageBytes, tag):

            newTagBytes = HMAC.SHA.create(keyBytes, messageBytes)

            # Checks the tag
            if newTagBytes == tag:
                return True

            return False

        @staticmethod
        def createHex(keyBytes, messageBytes, blocksize=64):
            base64Hash = HMAC.SHA.create(keyBytes, messageBytes, blocksize)
            return Function.Base64_To.hexadecimal(base64Hash)