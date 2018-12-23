import requests
import timeit
import string

"""
>>> Break HMAC-SHA1 with a slightly less artificial timing leak
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

def task32():
    print()

    signatureTry = ["XX"] * 20
    print(" ".join(signatureTry), end='\r')
    
    # Sets base time
    baseTime = timeRequest(signatureTry)
    
    for signatureCharPosition in range(0, 20):

        timings = []
        for i in range(0, 255):

            # Grabs hex value
            h = hex(i)[2:].zfill(2)

            # Breaks string formatting
            signatureTry[signatureCharPosition] = h
            newTime = timeRequest(signatureTry)

            timings.append([baseTime - newTime, newTime,  i])

        timings.sort()

        hexByte = hex(timings[0][2])[2:].zfill(2)

        # Adds new value to the list
        signatureTry[signatureCharPosition] = hexByte

        # Sets a new base time
        baseTime = timings[0][1]

        # Resets timings
        timings = []

        print(" ".join(signatureTry), end='\r')

    # Final print
    print("".join(signatureTry))

task32()
