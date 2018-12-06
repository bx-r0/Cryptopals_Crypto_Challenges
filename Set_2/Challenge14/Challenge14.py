import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '../')
sys.path.insert(0, './')
import Function
import random
import base64

# Random key - this shouldn't be viewable
key = 'UWwj6bUR3BqgLULVODpzGA=='

# Creates a target value - In this case NASA Admin cookie
target_bytes = Function.UTF8.base64(Function.Encryption.profileFor("admin@nasa.com"))

# A random key can be used as a random string
randomBytes = Function.Encryption.AES.randomKeyBase64(random.randint(1, 100))

def encryption(attackerControlled):

    plainText = Function.Base64_To.concat([
                randomBytes, 
                Function.UTF8.base64(attackerControlled), 
                target_bytes])

    e = Function.Encryption.AES.ECB.Encrypt(key, plainText)
    return e

def findRepeatingBlocks(blockList):

    repeating = []
    seen = set()
    blockIndex = 0
    for block in blockList:
        if block in seen and not block in repeating:
            repeating.append(block)

        seen.add(block)
        blockIndex += 1

    return repeating

def findOffset():
    # Calculating the offset of the random data
    # This can be determined when we allign two blocks of 'A's

    # Consider:
    # PT: | foob arba zfoo baAA | AAAA AAAA AAAA AAAA | AAAA AAAA AAAA AA00 |

    # By adding two offset characters we can create two equal blocks
    # PT: | foob arba zfoo baBB | AAAA AAAA AAAA AAAA | AAAA AAAA AAAA AAAA |

    offset = 0
    startBlock = 0

    while True:
        e = encryption("B" * offset +  "A" * 32)
        blockList = Function.Encryption.splitBase64IntoBlocks(e, 16)

        # Looks for two repeating blocks
        r = findRepeatingBlocks(blockList)

        if len(r) > 0:
            
            # Finds where the first target block is
            for x in range(len(blockList)):
                if r[0] == blockList[x]:
                    startBlock = x

            break

        offset += 1

    return offset, startBlock

def task14():

    discoveredChars = ""

    # Finds the offset required to line the blocks up for the attack
    # It also finds which block we control, and thus, which block we should attack
    offset, startBlock = findOffset()

    # Creates the values for the chosen plaintext
    # Ranging of values of "A" from 1 --> 15
    preComputedBlocks = []
    for length in range(0, 16):
        e = encryption("B" * offset + "A" * length)
        preComputedBlocks.append(Function.Encryption.splitBase64IntoBlocks(e, 16))

    # Calulcates how many blocks of data the encryption produces
    numberOfBlocks = len(preComputedBlocks[0])

    # Starts at the target block
    for targetBlockIndex in range(startBlock - 1, numberOfBlocks):

        # Reduces the size of "A" after every discovery byte
        for AStringLength in reversed(range(0, 16)):

            # Crafts the plaintext
            chosenPlaintext = "B" * (offset) + "A" * AStringLength + discoveredChars
            
            # Grabs the data with a certain A string length at a certain block
            target = preComputedBlocks[AStringLength][targetBlockIndex]
            for i in range(0, 255):
                e = encryption(chosenPlaintext + chr(i))
                testBlocks = Function.Encryption.splitBase64IntoBlocks(e, 16)

                # If we have found the correct character!
                if target == testBlocks[targetBlockIndex]:
                    discoveredChars += chr(i)
                    break
    
    result = "".join(discoveredChars)
    result = Function.Encryption.removePadding("\x00", result)

    return result

if __name__ is "__main__":
    task14()