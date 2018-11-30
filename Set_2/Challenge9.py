# Implement PKCS#7 padding

def padding(blocksize, string):
    if len(string) > blocksize:
        print("Error: string is bigger than the block!")
        return

    difference = blocksize - len(string)

    return string + "\x04" * difference

def challenge():
    inputStr = "YELLOW SUBMARINE"
    outputStr = "YELLOW SUBMARINE\x04\x04\x04\x04"    
    x = padding(20, inputStr)

    if x == outputStr:
        print("Challenge complete!")

challenge()