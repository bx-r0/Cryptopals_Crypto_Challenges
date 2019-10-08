import sys ; sys.path += ['.', '../..']
from SharedCode.Function import RSA, Hash, COLOURS, cube_root
import hashlib
import struct
import re

from Crypto.Signature import PKCS1_v1_5

header     = b"\x00\x01"

# From: RFC 3447
sha256_asn = b"\x00\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20"

BLOCK_SIZE = 128 * 2# Bytes

class VulnRSASignature():

    def sign(self, msg, private_key):
        digest = Hash.SHA256_Hex(msg)
        
        block = format_signature(digest)
        block_int = int.from_bytes(block, byteorder='big')

        sig = RSA.encrypt_raw(block_int, private_key)

        return sig
        
    def verify(self, encryptedSig, message, public_key):
        
        decryptedSigInt = RSA.encrypt_raw(encryptedSig, public_key)
        decryptedSigBytes = decryptedSigInt.to_bytes(BLOCK_SIZE, 'big')

        r = re.compile(b"\x00\01\xff+?" + sha256_asn + b"(.{32})", re.DOTALL)
        regex_query = r.findall(decryptedSigBytes)

        if len(regex_query) == 0:
            raise Exception("Error in block format: Digest cannot be found")

        digest = regex_query[0]

        checkHash = Hash.SHA256_Hex(message)

        if digest.hex() == checkHash:
            COLOURS.printGreen("Valid Signature")
        else:
            COLOURS.printRed("Invalid Signature")

def format_signature(digest):

    digest_bytes = bytes.fromhex(digest)
    current_length = len(header) + len(sha256_asn) + len(digest_bytes)

    # Check length]
    if 0 > BLOCK_SIZE - current_length:
        raise Exception("Message too long")

    return header + b"\xff" * (BLOCK_SIZE - current_length) + sha256_asn + digest_bytes

def forge_signature(public_key, message):

    digest = Hash.SHA256_Hex(message)
    digest_bytes = bytes.fromhex(digest)

    signature = header + b"\xff" + sha256_asn + digest_bytes
    signature += b"\x00" * ((2048 // 8) - len(signature))

    signature_int = int.from_bytes(signature, byteorder='big')

    malicious_sig = cube_root(signature_int)
    return malicious_sig

if __name__ == "__main__":

    r = VulnRSASignature()
    pub, priv = RSA.create_keys(1024)

    message = b"testing this stuff"

    print("[*] Siging message normally: ")
    sig = r.sign(message, priv)
    print("[*] Signature: ", sig)
    valid = r.verify(sig, message, pub)

    print("\n[*] Forging signature for string \"hi mom\"...")
    malicious_message = b"hi mom"
    malicious_sig = forge_signature(pub, malicious_message)
    print("[*] Malicious signature: ", malicious_sig)
    r.verify(malicious_sig, malicious_message, pub)


    