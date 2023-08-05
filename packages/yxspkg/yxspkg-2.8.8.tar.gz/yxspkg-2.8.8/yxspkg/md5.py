#!/usr/bin/env python3
import hashlib
__version__='1.0'
def md5(a):
    x=hashlib.md5()
    f=open(a,'rb')
    while a!=b'':
        a=f.read(8388608)
        x.update(a)
    f.close()
    return x.hexdigest()