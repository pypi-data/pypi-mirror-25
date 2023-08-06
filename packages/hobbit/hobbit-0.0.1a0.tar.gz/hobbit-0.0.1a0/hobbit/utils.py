from collections import Iterable


def flatten(iterator):
    for i in iterator:
        if isinstance(i, Iterable):
            for j in flatten(i):
                yield j
        else:
            yield i

def foreach(func, iterator):
    for item in iterator:
        func(item)
