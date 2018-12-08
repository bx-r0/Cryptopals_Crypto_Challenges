import sys ; sys.path += ['.', '../..']
import MT19937 as MT

"""
>>> Clone an MT19937 RNG from its output
"""

m = MT.MT19937(seed=1000)

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

def generateRandomNumbers():
    # Gets the minimum number required to reverse the state
    for _ in range(0, 624):
        values.append(m.getInt())

def task23():
    generateRandomNumbers()

    recoveredState = []

    # Recovers all the states of the MT
    for v in values:
        recoveredState.append(undoTemper(v))

    if m.state == recoveredState:
        print("State recovered!")

    # Splices in the new state
    clonedGen = MT.MT19937(0)
    clonedGen.state = recoveredState

    # Generates an integer from the orginal and cloned
    # PRNGs
    newInt = m.getInt()
    newIntCloned = clonedGen.getInt()

    if newInt == newIntCloned:
        print("PRNG Successfully cloned!")

if __name__ == "__main__":
    task23()