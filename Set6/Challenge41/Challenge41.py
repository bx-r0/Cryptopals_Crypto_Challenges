import sys ; sys.path += ['.', '../..']
from SharedCode.Function import RSA
import requests
import random
import time

url = "http://127.0.0.1:8000/challenge41"

def send(c):
    return requests.get(url + f"?rsa_c={c}").text

if __name__ == "__main__":

    # Servers pub key
    pubKey = [3, 23972364954525701100074439346600406628053907869627676187659733934293347473199616148003202451101931079593587192200986038652767376949166896763799319115321296486027259924033020029203446670323251351916358289089263744735560092803559656273502732499748627375167943391262726702851855210414814830771164530207200332013506246190590521861014759294360511974261245618777454245835087891386015109056060169411039180819317967284084662518115552280660767822286603756634641574473844890648952100339020324230763532418257570880549446778347391728565077611121670925373744507034512690512050396822655759750881613118075426753037251236482584827079]
    e = pubKey[0]
    n = pubKey[1]

    # Simulate other user sending c
    m = "{time: " + str(int(time.time())) + ", secret-key: 2ee0593ce5bd49e4ae89734ffca1ec6d}"

    c = RSA.encrypt(m, pubKey)
    send(c)
    print("[*] Intercepted some cipher text: ", hex(c)[:25], "...")

    # Try sending c again
    print("[*] Trying to replay intercepted cipher text")
    r = send(c)

    print(f"[!] Error: \"{r}\"")
    
    print("[!] Attacking Oracle...")
    # Attack code
    s = 14
    
    c_prime = (pow(s, e, n) * c) % n
    p_prime = int(send(c_prime), 16)

    i = RSA.invmod(s, n)
    m_hex = hex((p_prime * i) % n)[2:]


    print("[!] Decrypted cipher text:")
    print(">>> ", RSA.hex_to_string(m_hex))

    

