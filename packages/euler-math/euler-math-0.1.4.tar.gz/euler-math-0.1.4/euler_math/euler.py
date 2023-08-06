import numpy as np
import operator
from sys import setrecursionlimit
setrecursionlimit(4000)

# utility methods ------------------------------------


def memoize(f):

    class memodict(dict):
        __slots__ = ()

        def __missing__(self, key):
            self[key] = ret = f(key)
            return ret

    return memodict().__getitem__


def timer(f):
    from timeit import default_timer
    start = default_timer()
    result = f()
    end = default_timer()
    print 'result:', result, '(%.2fs)' % (end - start)


def readlines(file):
    return open(file).read().splitlines()


fst = operator.itemgetter(0)
snd = operator.itemgetter(1)

# number theory methods ---------------------------------------

# prime list cache
_primes = [2]


def _grow_primes():
    p0 = _primes[len(_primes) - 1] + 1
    b = np.ones(p0, dtype=bool)
    for di in _primes:
        i0 = p0 / di * di
        if i0 < p0:
            b[i0 + di - p0::di] = False
        else:
            b[i0 - p0::di] = False
    _primes.extend(np.where(b)[0] + p0)


def primes():
    i = 0
    while True:
        if i >= len(_primes):
            _grow_primes()
        yield _primes[i]
        i += 1


def prime(n):
    while n >= len(_primes):
        _grow_primes()
    return _primes[n]


def is_prime(n):
    if n < 1:
        return False
    ps = primes()
    p = ps.next()
    while p * p <= n:
        if n % p == 0:
            return False
        p = ps.next()
    return True


def PrimeQ(n):
    """yields true if a prime number and yields false otherwise"""
    return is_prime(n)


def PrimePi(n):
    """gives the number of primes less than or equal to n"""
    i = 0
    while prime(i) <= n:
        i += 1
    return i


def GCD(a, b):
    """https://reference.wolfram.com/language/ref/GCD.html"""
    while b:
        a, b = b, a % b
    return a


def LCM(a, b):
    """https://reference.wolfram.com/language/ref/LCM.html"""
    return a / GCD(a, b) * b


def FactorInteger(n):
    """https://reference.wolfram.com/language/ref/FactorInteger.html"""
    from itertools import groupby
    factors = []
    ps = primes()
    m = n
    p = ps.next()
    while p * p <= m:
        if m % p == 0:
            m /= p
            factors.append(p)
        else:
            p = ps.next()
    factors.append(m)
    return list((item, len(list(group)))
                for item, group in groupby(sorted(factors)))


def DivisorSigma(n):
    """https://reference.wolfram.com/language/ref/DivisorSigma.html"""
    import operator
    return reduce(operator.mul, [(x[1] + 1) for x in FactorInteger(n)], 1)
