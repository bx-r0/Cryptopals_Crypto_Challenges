import sys ; sys.path += ['.', '../..']
import MT19937 as MT

def task21():
    mTwister = MT.MT19937(seed=1000)

    values = []
    
    # Generates 5 random values
    for _ in range(5):
       values.append(mTwister.getInt())

    return values


if __name__ == "__main__":
   task21()