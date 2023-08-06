import __builtin__
import itertools as _itertools
import functools as _functools
import operator as _operator


class Seq:

    def __init__(self, function):
        self.function = function

    def __rrshift__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return Seq(lambda x: self.function(x, *args, **kwargs))


# sequence initialization methods --------------------


def unfold(function, initial):
    x = initial
    while True:
        res = function(x)
        if res is None:
            raise StopIteration
        else:
            w, x = res
            yield w


def init(n, function):
    i = 0
    while i < n:
        yield function(i)
        i += 1


def initInfinite(function):
    i = 0
    while True:
        yield function(i)
        i += 1


# sequence methods ------------------------------------


@Seq
def sum(sequence):
    return __builtin__.sum(sequence)


@Seq
def sumBy(sequence, function):
    return __builtin__.sum(_itertools.imap(function, sequence))


@Seq
def scan(sequence, function, state):
    yield state
    for x in sequence:
        state = function(state, x)
        yield state


@Seq
def filter(sequence, function):
    return _itertools.ifilter(function, sequence)


@Seq
def takeWhile(sequence, function):
    return _itertools.takewhile(function, sequence)


@Seq
def skipWhile(sequence, function):
    return _itertools.dropwhile(function, sequence)


@Seq
def skip(sequence, n):
    for i in range(n):
        sequence.next()
    return sequence


@Seq
def nth(sequence, n):
    for i in range(n):
        sequence.next()
    return sequence.next()


@Seq
def map(sequence, function):
    return _itertools.imap(function, sequence)


@Seq
def mapi(sequence, function):
    return _itertools.imap(function, enumerate(sequence))


@Seq
def toList(sequence):
    return list(sequence)


@Seq
def toSet(sequence):
    return set(sequence)


@Seq
def append(sequence1, sequence2):
    return _itertools.chain(sequence2, sequence1)


@Seq
def take(sequence, n):
    return list(_itertools.islice(sequence, n))


@Seq
def max(sequence):
    return __builtin__.max(sequence)


@Seq
def min(sequence):
    return __builtin__.min(sequence)


@Seq
def reduce(sequence, function):
    return _functools.reduce(function, sequence)


@Seq
def window(sequence, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(sequence)
    result = tuple(_itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


@Seq
def product(sequence):
    return _functools.reduce(_operator.mul, sequence)


@Seq
def head(sequence):
    return next(_itertools.islice(sequence, 1))


@Seq
def find(sequence, function):
    return next(_itertools.ifilter(function, sequence), None)


@Seq
def findIndex(sequence, function):
    return next(
        _itertools.ifilter(lambda (i, x): function(x), enumerate(sequence)),
        None)[0]


@Seq
def rev(sequence):
    return reversed(list(sequence))


@Seq
def zip(sequence1, sequence2):
    return _itertools.izip(sequence1, sequence2)


@Seq
def flatten(sequence):
    return _itertools.chain.from_iterable(
        _itertools.imap(lambda x: x, sequence))


@Seq
def length(sequence):
    count = 0
    for x in sequence:
        count += 1
    return count


@Seq
def exists(sequence, function):
    return __builtin__.any(function(x) for x in sequence)


@Seq
def collect(sequence, function):
    for s in _itertools.imap(function, sequence):
        for x in s:
            yield x


@Seq
def distinct(seq):
    seen = set()
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        yield x


@Seq
def forall(sequence, function):
    for x in sequence:
        if not function(x):
            return False
    return True


@Seq
def maxBy(sequence, function):
    return __builtin__.max(sequence, key=function)


@Seq
def sort(sequence):
    return __builtin__.sorted(sequence)


@Seq
def sortBy(sequence, function):
    return __builtin__.sorted(sequence, key=function)
