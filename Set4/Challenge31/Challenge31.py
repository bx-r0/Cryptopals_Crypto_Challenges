import sys ; sys.path += ['.', '../..']
from CryptoCode.MAC import HMAC
import requests
import timeit
import string
import sys
import os

"""
>>> Implement and break HMAC-SHA1 with an artificial timing leak
"""

key = b"lemonade"
address = "127.0.0.1:8000/challenge31"
maliciousFileName  = "virus.exe"
hexCharacterSet = string.ascii_letters + "0123456789"

def sendGetRequest(fileName, signature):
    requests.get(f"http://{address}?file={fileName}&signature={signature}")

def timeRequest(signatureTry):

    signature = "".join(signatureTry)
    s = f"sendGetRequest(\"{maliciousFileName}\", \"{signature}\")"
    return timeit.timeit(s, number=1, setup="from __main__ import sendGetRequest")

def task31():
    
    signatureTry = ["XX"] * 20
    previousTime = ""

    # Sets base time
    previousTime = timeRequest(signatureTry)
    
    for signatureCharPosition in range(0, 20):
        for i in range(0, 255):

            # Grabs hex value
            h = hex(i)[2:].zfill(2)

            # Breaks string formatting
            signatureTry[signatureCharPosition] = h
            newTime = timeRequest(signatureTry)

            if previousTime < newTime - 0.025:
                previousTime = newTime
                break

            print(" ".join(signatureTry), end='\r')

    # Final print
    print("".join(signatureTry))

task31()