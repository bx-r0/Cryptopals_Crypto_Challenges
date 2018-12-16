from SharedCode.SHA1 import SHA1
from SharedCode.MD4 import MD4
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