import __builtin__
import itertools as _itertools
import functools as _functools


class List:

    def __init__(self, function):
        self.function = function

    def __rrshift__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return List(lambda x: self.function(x, *args, **kwargs))


# list methods ------------------------------------


@List
def sum(list):
    return __builtin__.sum(list)


@List
def sumBy(list, function):
    return __builtin__.sum(_itertools.imap(function, list))


@List
def filter(list, function):
    return [x for x in list if function(x)]


@List
def map(list, function):
    return [function(x) for x in list]


@List
def max(list):
    return __builtin__.max(list)


@List
def reduce(list, function):
    return _functools.reduce(function, list)


@List
def collect(list, function):

    def gen():
        for s in _itertools.imap(function, list):
            for x in s:
                yield x

    return [x for x in gen()]
