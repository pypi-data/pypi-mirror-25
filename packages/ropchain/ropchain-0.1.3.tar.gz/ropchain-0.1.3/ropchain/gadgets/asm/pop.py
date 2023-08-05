from ropchain import ropchain
from ropchain.gadgets.asm import mov, xor, inc, xchg, add, double
from ropchain.gadgets import util, gadget, toZero

'''
alt pop reg
| mov reg, imm; ret; (add reg, reg; ret;)*; ([inc reg], add reg, reg)*; ret
| mov reg, other; ret; (add reg, reg; ret;)*; ([inc reg], add reg, reg)*; ret
| xor reg, reg; ret; ([inc reg], add reg, reg)*; ret
| pop other; ret; mov reg, other; ret
| pop other; ret; xchg reg, other; ret
'''

def find(reg, dest, gadgets, canUse):
    rop = gadget.find(gadgets, 'pop', reg)
    if rop != None:
        rop =  ropchain.ROPChain(rop)
        rop.appendValue(dest)
        return rop

    rop = util.optMap(rop, fromIncAdd, dest, reg, gadgets, canUse)
    rop = util.optMap(rop, fromOtherReg, dest, reg, gadgets, canUse)

    return rop

'''
xor reg, reg; ret; ([inc reg], add reg, reg)*; ret
'''
def fromIncAdd(dest, reg, gadgets, canUse):
    zero = toZero.find(reg, gadgets, canUse)
    _inc = inc.find(reg, gadgets, canUse)
    _double = double.find(reg, gadgets, canUse)

    if zero != None and _inc != None and _double != None:
        ret = zero
        bits = bin(dest)[2:]
        bits = '0' * (32 - len(bits)) + bits
        for i in range(31):
            if bits[i] == '1':
                ret += _inc
            ret += _double
        if bits[31] == '1':
            ret += _inc

        return ret

    return None

'''
pop other; ret; mov reg, other; ret
pop other; ret; xchg reg, other; ret
'''
def fromOtherReg(dest, reg, gadgets, canUse):
    for r in canUse:
        _pop = find(r, dest, gadgets, canUse - set([r]))
        _mov = mov.find(reg, r, gadgets, canUse - set([reg, r]))

        if _pop != None and _mov != None:
            return _pop + _mov

        _xchg = xchg.find(reg, r, gadgets, canUse - set(r))
        if _pop != None and _xchg != None:
            return _pop + _xchg

    return None
