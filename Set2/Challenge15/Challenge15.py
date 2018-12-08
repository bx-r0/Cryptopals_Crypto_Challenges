import sys ; sys.path += ['.', '../..']
import Function

def task15():

    # Some valid tests
    Function.Encryption.PKCS7.isValid("ICE ICE BABY\x04\x04\x04\x04")
    Function.Encryption.PKCS7.isValid("ICE ICE BABY\x05\x05\x05\x05\x05")

if __name__ == "__main__":
    task15()