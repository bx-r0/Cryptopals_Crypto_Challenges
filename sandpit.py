import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
import Function
import random
import base64

data = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
#data= base64.b64encode(b"1234567812345678")

key = base64.b64encode(b"YELLOW SUBMARINE")

e = Function.Encryption.AES.CTR.Encrypt_Decrypt(0, key, data)

pt = base64.b64decode(e)

print(pt)