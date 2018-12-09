import sys ; sys.path += ['.', '../..']
import Function
import base64
import re

"""
>>> ECB cut-and-paste

Write a k=v parsing routine, as if for a structured cookie. The routine should take:

>>> foo=bar&baz=qux&zap=zazzle

and produce:

>>> {
>>>   foo: 'bar',
>>>   baz: 'qux',
>>>   zap: 'zazzle'
>>> }
"""

# Disallowed Characters
dChars = "&=}{:"

def decode(string):

    # Matches pattern for string
    r = re.match(rf"^(([^{dChars}]+\=[^{dChars}]+)&)+([^{dChars}]+\=[^{dChars}]+)$", string)

    if r is None:
        raise(Exception("String format is invalid!"))

    sections = string.split("&")

    result = "{\n"

    # Adds all but the last section
    index = 0
    length = len(sections)
    for section in sections:

        parts = section.split('=')
        key = parts[0]
        value = parts[1] 

        # Checks the value is a number
        if not re.match(r"[0-9]+", value):

            # Encases non integers in single quotes
            value = f"\'{value}\'"

        result += f"  {key}: {value}"

        # Adds a comma if it is not the last value
        if not index == length - 1:
            result += ","

        result += "\n"
        index += 1


    result += "}"
    return result

def encode(string):
    # These are required because of the issue including them in a formatted string
    startBracket = "{"
    endBracket = "}"

    string = string.strip()

    pattern = fr"^{startBracket}([^{dChars}]+\:[^{dChars}]+\,)+([^{dChars}]+\:[^{dChars}]+){endBracket}$"

    r = re.match(pattern, string)

    if r is None:
        raise(Exception("encode() - Incorrect object format!"))

    lines = string.split('\n')

    # Removes brackets
    del lines[0], lines[-1]

    keyValuePairs = []
    for line in lines:
        keyAndValue = line.split(":")
        keyAndValue = list(map(str.strip, keyAndValue))

        key = keyAndValue[0]
        
        # If value is a string
        value = keyAndValue[1]

        # Removes comma
        if ',' in value:
            value = value[:-1]

        # Stript single quotes
        if "'" in value:
            value = value[1:-1]
        else:
            value = int(value)

        keyValuePairs.append((key, value))

    result = ""
    index = 0
    lastIndex = len(keyValuePairs) - 1
    for key, value in keyValuePairs:

        result += f"{key}={value}"
        
        if not index == lastIndex:
            result += "&"

        index += 1

    return result

def profile_for(email):
    return Function.Encryption.profileFor(email)

def encrypt_user_profile(user_profile, key):
    base64Profile = base64.b64encode(user_profile.encode("utf-8"))
    return Function.Encryption.AES.ECB.Encrypt(key, base64Profile)

def decrypt_user_profile(encryptionDataBase64, key):
    d = Function.Encryption.AES.ECB.Decrypt(key, encryptionDataBase64)
    d = base64.b64decode(d)
    d = Function.Conversion.remove_byte_notation(d)
    
    # Remove padding
    d = d.replace("\\x00", "")

    return d

def task13():
    key = b'gHEvzQiiVFtkppxjAKiweg=='
    #key = Function.Encryption.AES.Random_Key_Base64()

    x = "test=great&outcome=correct&time=wellspent&percentage=100"
    e = encrypt_user_profile(x, key)
    d = decrypt_user_profile(e, key)

    print(d)

if __name__ == "__main__":
    task13()