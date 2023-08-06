"""
I pulled out `this solution from Stack Overflow <https://stackoverflow.com/a/21614155>`_
a way to guarantee hashability.

In order to make it backwards compatible, I made it so the hash of an Integral is itself.
"""

from hashlib import sha256
from collections import Hashable, Set, Mapping, Iterable
from numbers import Real

class Deterministic_Hashable():
    def __fixed_hash__(self):
        return NotImplemented

def to_bytes(o):
    try:
        return o.encode('utf-8')
    except AttributeError:
        return o

def to_hash(o):
    return int(sha256(to_bytes(o)).hexdigest(), base=16)

def hash(o):
    if isinstance(o, Real) and o%1==0:
        return int(o)
    if isinstance(o, Deterministic_Hashable):
        return o.__fixed_hash__()
    if not isinstance(o, Hashable):
        raise TypeError("unhashable type: '"+ type({}).__name__+"'")
    try:
        return to_hash(o)
    except TypeError:
        pass
    if isinstance(o, Set):
        return to_hash(repr((type(o).__name__,) + tuple(sorted(frozen_hash(e) for e in o))))
    if isinstance(o, Mapping):
        return to_hash(repr((type(o).__name__,) + tuple(sorted(((frozen_hash(k),frozen_hash(v)) for k,v in o.items())))))
    if isinstance(o, Iterable):
        return to_hash(repr((type(o).__name__,) + tuple(frozen_hash(e) for e in o)))
    # This likely won't work. Probably due to python object default reprs.
    return to_hash(repr((type(o).__name__, repr(o))))

def frozen_hash(o):
    """
    This can hash the unhashable!
    """
    if isinstance(o, Real) and o%1==0:
        return int(o)
    if isinstance(o, Deterministic_Hashable):
        return o.__fixed_hash__()
    try:
        return to_hash(o)
    except TypeError:
        pass
    if isinstance(o, Set):
        return to_hash(repr((type(o).__name__,) + tuple(sorted(frozen_hash(e) for e in o))))
    if isinstance(o, Mapping):
        return to_hash(repr((type(o).__name__,) + tuple(sorted(((frozen_hash(k),frozen_hash(v)) for k,v in o.items())))))
    if isinstance(o, Iterable):
        return to_hash(repr((type(o).__name__,) + tuple(frozen_hash(e) for e in o)))
    # This likely won't work. Probably due to python object default reprs.
    return to_hash(repr((type(o).__name__, repr(o))))
