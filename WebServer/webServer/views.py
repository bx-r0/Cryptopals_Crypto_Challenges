import sys ; sys.path += ['.', '..']
from django.shortcuts import render
from django.http import HttpResponse
from SharedCode import Function
from SharedCode.SHA1 import SHA1
from SharedCode.MAC import HMAC
import base64
from time import sleep
import re

# End points
def index(request):
    return HttpResponse("Index")

def challenge31(request):
    # 50ms wait
    return validateHMAC(request, 0.05)

def challenge32(request):
    # No artifical wait
    return validateHMAC(request, 0)

# Shared code
def validateHMAC(request, waitTime):
    key = b"lemonade"

    file = request.GET.get("file", None)
    signature = request.GET.get("signature", None)

    responseCode = 0

    if file != None and signature != None:
        checkedSignature = HMAC.SHA.createHex(key, file.encode('utf-8'))
        checkedSignature = Function.Conversion.remove_byte_notation(checkedSignature)

        responseCode = 500
        if insecureCompare(signature, checkedSignature, waitTime):
            responseCode = 200

    else:
        responseCode = 501

    r = HttpResponse()
    r.status_code = responseCode

    return r

def insecureCompare(signatureA, signatureB, sleepTime=0.05):

    signatureABytes = re.findall("..", signatureA)
    signatureBBytes = re.findall("..", signatureB)

    for a, b in zip(signatureABytes, signatureBBytes):
        if not a == b:
            return False
        if sleepTime > 0: sleep(sleepTime)
    return True