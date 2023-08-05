from .bits import Bits
from .bv import BV, BVV, BVS
from .base import make_op
from .structure import ASTStructure

import logging
l = logging.getLogger('claripy.ast.string')

class String(Bits):
    def concat(self, *others):
        return StrConcat(self, *others)

    def size(self):
        return StrSize(self)

    def __getitem__(self, k):
        if isinstance(k, slice):
            if k.step is not None:
                raise ValueError("You may not slice a claripy String with a stride")
            start = k.start if k.start is not None else 0
            end = k.end if k.end is not None else 0
            if not isinstance(start, (int, long)) or not isinstance(end, (int, long)):
                raise TypeError("String slices of non-int values are unsupported")
            if start < 0 or end < 0:
                raise ValueError("String slices of negative values are unsupported")
            if start >= end:
                raise ValueError("start must be less than end for string slice")

            return StrSubstr(self, start, end - start)
        elif isinstance(k, (int, long)):
            return StrIndex(self, BVV(k, 32))
        elif isinstance(k, BV):
            # XXX: length check?
            return StrIndex(self, k)
        else:
            raise TypeError("Invalid type for String index: %r" % k)


def normalize(val):
    if isinstance(val, BV):
        if len(val) % 8 != 0:
            raise ValueError("BV value for ConString does not have byte-aligned size")
        return val
    elif isinstance(val, bytes): # alias for str in py2
        return BVV(val)
    elif isinstance(val, unicode):
        l.warning("Normalizing unicode value to bytes")
        return BVV(val.encode('utf-8'))
    else:
        raise TypeError("Bad type for instanciating ConString: %r" % type(val))

def ConString(val):
    nval = normalize(val)
    return String(ASTStructure('ConString', (nval,)))

def VarString(name, val):
    nval = normalize(val)
    #maxlen = len(nval) / 8
    #maxlenbits = math.ceil(math.log(maxlen, 2))
    maxlenbits = 32
    slen = BVS(name + '_len', maxlenbits)
    sval = BVS(name, len(nval))

    return String(ASTStructure('VarString', (sval, slen, nval)))

from .. import operations

StrConcat = make_op('StrConcat', String, String)
StrSize = make_op('StrSize', (String,), BV)
StrIndex = make_op('StrIndex', (String, BV), BV)
StrSubstr = make_op('StrSubstr', (String, int, int), String)
