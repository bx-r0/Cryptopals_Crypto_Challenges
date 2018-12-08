class MT19937():
    
    # TGFSR(R) tempering bitmasks
    _b, _c = 0x9d2c5680, 0xefc60000

    # TGFSR(R) tempering bit shifts
    _s, _t = 7, 15

    # Additional Mersenne Twister tempering bit shifts/masks
    _u, _l = 11, 18

    # For MT19937 the values are:
    _r, _w = 31, 32
    _f, _a = 0x6c078965, 0x9908b0df
    _n, _m = 624, 397

    # Mask creations
    _lmask = (1 << _r) - 1 #0x7fffffff
    _umask = -~_lmask      ##0x80000000 - Adds one to the lmask

    def __init__(self, seed):

        self.index = self._n
        self.state = [0] * self._n
        self.state[0] = seed & 0xffffffff

        # Populates the state
        for i in range(1, self._n):
            self.state[i] = self._f * (self.state[i - 1] ^ self.state[i - 1] >>  self._w - 2) + i & 0xffffffff

    def getInt(self):
        if self.index >= self._n:
            self._twist()
        y = self.temper(self.state[self.index])
        self.index += 1
        return y

    # g
    @staticmethod
    def temper(y):
        y ^= y >> MT19937._u
        y ^= y << MT19937._s & MT19937._b  
        y ^= y << MT19937._t & MT19937._c 
        y ^= y >> MT19937._l
        return y

    # f
    def _twist(self): 
        for i in range(self._n):
            y = (self.state[i] & self._umask) \
                + (self.state[(i + 1) % self._n] & self._lmask)
            self.state[i] = self.state[(i + self._m) % self._n] ^ y >> 1
            if y % 2 != 0:
                self.state[i] ^= self._a
        self.index = 0