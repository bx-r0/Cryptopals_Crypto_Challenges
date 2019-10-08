import sys ; sys.path += ['.', '..']
from django.http import HttpResponse
from SharedCode import Function
from CryptoCode.MAC import HMAC
from time import sleep
import hashlib
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

def challenge41(request):
    return unpadded_message_oracle(request)


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


seen_messages = []
def unpadded_message_oracle(request):

    priv_key = [
        15981576636350467400049626231066937752035938579751784125106489289528898315466410765335468300734620719729058128133990692435178251299444597842532879410214197657351506616022013352802297780215500901277572192726175829823706728535706437515668488333165751583445295594175151135234570140276543220514109686804800221342129912751058189490408739306525860961810828727799484084943762044655004847973352667180584134062109852501127021100775941200763057498764401994582408764707448290839165096490923542570999336198506562040295461888270396886058043182394594784325201242953692201596854331452985638930342695968558104744946179582476723348923,
        23972364954525701100074439346600406628053907869627676187659733934293347473199616148003202451101931079593587192200986038652767376949166896763799319115321296486027259924033020029203446670323251351916358289089263744735560092803559656273502732499748627375167943391262726702851855210414814830771164530207200332013506246190590521861014759294360511974261245618777454245835087891386015109056060169411039180819317967284084662518115552280660767822286603756634641574473844890648952100339020324230763532418257570880549446778347391728565077611121670925373744507034512690512050396822655759750881613118075426753037251236482584827079
    ]
    

    responseCode = 200
    responseMsg  = "OK"

    ct = request.GET.get("rsa_c", None)

    if ct == None:
        responseCode = 400
        responseMsg  = "Incorrect Params"

    ct = int(ct)

    m = Function.RSA.decrypt_to_hex(ct, priv_key)

    h_msg = hashlib.md5(str.encode(m)).hexdigest()
    if h_msg in seen_messages:
        responseCode = 400
        responseMsg  = "Repeated Message"
    else:
        seen_messages.append(h_msg)
        responseMsg = m

    r = HttpResponse(responseMsg)
    r.status_code = responseCode
    return r
