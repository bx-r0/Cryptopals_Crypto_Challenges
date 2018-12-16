import sys ; sys.path += ['.', '../..', '../../..']
from django.shortcuts import render
from django.http import HttpResponse
from SharedCode import Function
from SharedCode.SHA1 import SHA1
from SharedCode.MAC import HMAC
import base64
from time import sleep
import re

key = b"lemonade"

def index(request):

    file = request.GET.get("file", None)
    signature = request.GET.get("signature", None)


    responseCode = 0

    if file != None and signature != None:
        checkedSignature = HMAC.SHA.createHex(key, file.encode('utf-8'))
        print(checkedSignature)
        checkedSignature = Function.Conversion.remove_byte_notation(checkedSignature)

        responseCode = 500
        if insecureCompare(signature, checkedSignature):
            responseCode = 200

    else:
        responseCode = 501

    r = HttpResponse()
    r.status_code = responseCode

    return r

def insecureCompare(signatureA, signatureB):

    signatureABytes = re.findall("..", signatureA)
    signatureBBytes = re.findall("..", signatureB)

    for a, b in zip(signatureABytes, signatureBBytes):
        if not a == b:
            return False
        sleep(0.02)
    return True