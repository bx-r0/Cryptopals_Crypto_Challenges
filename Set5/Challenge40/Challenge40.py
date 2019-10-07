import sys ; sys.path += ['.', '../..']
from SharedCode.Function import RSA

m = "Lets meet by the riverside."

def cube(n):
    """Finds the cube root of n using binary search."""
    lo = 0
    hi = n

    while lo < hi:
        mid = (lo + hi) // 2
        if mid**3 < n:
            lo = mid + 1
        else:
            hi = mid

    return lo

if __name__ == "__main__":
    
    pk0, _ = RSA.create_keys(128)
    pk1, _ = RSA.create_keys(128)
    pk2, _ = RSA.create_keys(128)

    ct0 = RSA.encrypt(m, pk0)
    ct1 = RSA.encrypt(m, pk1)
    ct2 = RSA.encrypt(m, pk2)

    print("[*] 0: CT & PT: ", ct0, pk0)
    print("[*] 1: CT & PT: ", ct1, pk1)
    print("[*] 2: CT & PT: ", ct2, pk2)

    n0 = pk0[1]
    n1 = pk1[1]
    n2 = pk2[1]

    n012 = n0 * n1 * n2

    ms0 = n1 * n2
    ms1 = n0 * n2
    ms2 = n0 * n1
    
    t0 = ct0 * ms0 * RSA.invmod(ms0, n0)
    t1 = ct1 * ms1 * RSA.invmod(ms1, n1)
    t2 = ct2 * ms2 * RSA.invmod(ms2, n2)

    c = (t0 + t1 + t2) % (n0 * n1 * n2)

    x = RSA.hex_to_string(hex(cube(c))[2:])
    print("\n>>> ", x)