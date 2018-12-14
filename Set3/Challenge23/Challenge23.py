import sys ; sys.path += ['.', '../..']
from SharedCode import MT19937 as MT

"""
>>> Clone an MT19937 RNG from its output
"""

values = []

def undoTemper(y):

    # General algorithms that end up reversing the process of the bitshifts
    # They work by gradually covering the 32 bit integer over a loop
    def undoLeft(y, shift, mask):

        i = 0

        runningTotal = y
        while i * shift < 32:

            runningTotal = y ^ ((runningTotal << shift) & mask)
            i += 1

        return runningTotal
    def undoRight(y, shift):
        i = 0

        runningTotal = y
        while i * shift < 32:

            runningTotal = y ^ (runningTotal >> shift)

            i += 1

        return runningTotal

    y = undoRight(y, 18)
    y = undoLeft(y, 15, 0xefc60000)
    y = undoLeft(y, 7, 0x9d2c5680)
    y = undoRight(y, 11)

    return y

def generateRandomNumbers(PRNG):
    # Gets the minimum number required to reverse the state
    for _ in range(0, 624):
        values.append(PRNG.getInt())

def task23():
    originalMT = MT.MT19937(seed=1000)

    generateRandomNumbers(originalMT)

    recoveredState = []

    # Recovers all the states of the MT
    for v in values:
        recoveredState.append(undoTemper(v))

    # Splices in the new state
    clonedMT = MT.MT19937(0)
    clonedMT.state = recoveredState

    return originalMT, clonedMT

if __name__ == "__main__":
    originalMT, clonedMT = task23()

    # Generates an integer from the orginal and cloned
    # PRNGs
    newInt = originalMT.getInt()
    newIntCloned = clonedMT.getInt()

    if newInt == newIntCloned:
        print("PRNG Successfully cloned!")
