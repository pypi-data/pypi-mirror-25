#!/usr/bin/env python3
import os.path as _path
import os
import base64 as _base64
import math as _math
import array as _array
import tarfile as _tarfile
import time
from hashlib import md5
__version__='4.3'
def _data_type():
    x=_array.array('L')
    if x.itemsize==8:return 'L'
    else:return 'Q'
_array_type=_data_type()
def _bytes8(b,m=8):
    n=m-len(b)%m
    b+=(chr(n)*n).encode()
    return b
def _compress_tarfile(dirname,outfile=None):
    '''make a direct to a tar.gz file'''
    ss=time.clock()
    dirname=_path.normpath(dirname)
    if outfile is None:
        outfile = dirname + '.tar.gz'
    tar=_tarfile.open(outfile,'w:gz',compresslevel=9)
    dr=_path.dirname(dirname)+os.sep
    for r,d,fs in os.walk(dirname):
        for f in fs:
            af=r+os.sep+f
            print('compress ',f)
            tar.add(af,af.replace(dr,''))
    tar.close()
    print(time.clock()-ss)
    return outfile
def _extarct_tarfile(filename,target_path=None):
    '''make a direct to a tar.gz file'''
    if target_path is None:target_path=_path.dirname(_path.abspath(filename))
    tar=_tarfile.open(filename,'r:gz')
    for f in tar.getnames():
        tar.extract(f,target_path)
        print('extract ',target_path+os.sep+f)
    tar.close()

def _getkey(passwd):
    if passwd is None:passwd=b'SGZ'
    if isinstance(passwd,str):passwd=passwd.encode()
    p1=md5(passwd).digest()
    p2=md5(p1).digest()
    key=p1+p2
    s=[key[i]*key[8+i]*key[16+i]*key[24+i]+(i*37) for i in range(8)]
    return s
def _enpt(x,key,order=None):
    n1,n2,n3,a,b,c,d,m=key
    if order!=None:n1,n2,n3=order
    for i in range(len(x)):
        n1,n2,n3=n2,n3,(a*n1+b*n2+c*n3+d)%m
        x[i]=(x[i]+n3)%0xffffffffffffffff
    return n1,n2,n3
def encrypt(parameter,output=None,passwd='11'*16):
    if _path.isdir(parameter):
        istar = True
        parameter=_compress_tarfile(parameter)
    else:
        istar=False
    key0=_getkey(passwd)
    if output==None:
        output=parameter+'.yxs'
    size=_path.getsize(parameter)
    filename=_path.split(parameter)[1]
    size_name=len(filename.encode())
    size_bu=8-(size+size_name+3)%8
    b=bytearray(3+size_bu)
    b[0]=size_bu
    b[1]=size_name//256
    b[2]=size_name%256
    b+=filename.encode()
    data=open(parameter,'rb')
    length=8*1024*1024
    b+=data.read(length-size_bu-size_name-3)
    order0=key0[:3]
    fp=open(output,'wb')
    s0=0
    while True:
        x=_array.array(_array_type)
        x.frombytes(b)
        order0=_enpt(x,key=key0,order=order0)
        fp.write(x.tobytes())
        b=data.read(length)
        if not b:break
        s0+=length
        print('%.3f' % (s0/size))
    fp.close()
    data.close()
    if istar:os.remove(parameter)
def _deph(x,key,order=None):
    n1,n2,n3,a,b,c,d,m=key
    if order!=None:n1,n2,n3=order
    for i in range(len(x)):
        n1,n2,n3=n2,n3,(a*n1+b*n2+c*n3+d)%m
        x[i]=(x[i]-n3)%0xffffffffffffffff
    return n1,n2,n3

def decipher(parameter,output=None,passwd='11'*16):
    key0=_getkey(passwd)
    data=open(parameter,'rb')
    size=_path.getsize(parameter)
    length=8*1024*1024
    b=data.read(8*1024)
    x=_array.array(_array_type)
    x.frombytes(b)
    order0=key0[:3]
    order0=_deph(x,key=key0,order=order0)
    b=x.tobytes()
    size_bu=b[0]
    size_name=b[1]*256+b[2]
    o_name=b[3+size_bu:3+size_bu+size_name].decode('utf8')
    if output is None:
        output=o_name
    fp=open(output,'wb')
    fp.write(b[3+size_bu+size_name:])
    size0=8*1024-3-size_bu-size_name
    while True:
        b=data.read(length)
        if not b:break
        size0+=length
        print('%.3f' % (size0/size))
        x=_array.array(_array_type)
        x.frombytes(b)
        order0=_deph(x,key=key0,order=order0)
        fp.write(x.tobytes())
    fp.close()
    if o_name[-7:]=='.tar.gz':
        target_path=_path.dirname(_path.abspath(parameter))
        _extarct_tarfile(output,target_path=target_path)
        os.remove(output)
def encode(b,passwd):
    key0=_getkey(passwd)
    x=_array.array(_array_type)
    x.frombytes(_bytes8(b))
    _enpt(x,key=key0)
    return x.tobytes()
def decode(b,passwd):
    key0=_getkey(passwd)
    x=_array.array(_array_type)
    x.frombytes(b)
    _deph(x,key=key0)
    b=x.tobytes()
    return b[:-b[-1]]
def b64encode(b,passwd=None):
    return _base64.b64encode(encode(b,passwd))
def b64decode(b,passwd=None):
    return decode(_base64.b64decode(b),passwd)
def spencode(b,passwd=None,str_set=b''):
    if not b:return b
    if len(str_set)<2:
        str_set=list(range(ord('A'),ord('A')+26))+list(range(ord('a'),ord('a')+26))+list(range(ord('0'),ord('0')+10))
    if passwd is None:b=_bytes8(b)
    else:b=encode(b,passwd)
    str_set=bytearray(str_set)
    nb,ns=len(b),len(str_set)
    x=_array.array(_array_type)
    w=_math.ceil(x.itemsize*_math.log(256)/_math.log(ns))
    x.frombytes(b)
    y=bytearray(len(x)*w)
    t=0
    for i in x:
        for j in range(w-1,-1,-1):
            y[t+j]=str_set[i%ns]
            i=i//ns
        t+=w
    return y
def spdecode(b,passwd=None,str_set=b''):
    if not b:return b
    if len(str_set)<2:
        str_set=list(range(ord('A'),ord('A')+26))+list(range(ord('a'),ord('a')+26))+list(range(ord('0'),ord('0')+10))
    str_set=bytearray(str_set)
    t_set=bytearray(256)
    for i,j in enumerate(str_set):
        t_set[j]=i
    nb,ns=len(b),len(str_set)
    x=_array.array(_array_type,[0])
    w=_math.ceil(x.itemsize*_math.log(256)/_math.log(ns))
    b=bytearray(b)
    x*=nb//w
    t=0
    for i in range(nb//w):
        s=0
        for j in range(t,t+w):
            s=s*ns+t_set[b[j]]
        t+=w
        x[i]=s
    b=x.tobytes()
    if passwd is None:b=b[:-b[-1]]
    else:b=decode(b,passwd)
    return b
if __name__=='__main__':
    pass
    # import time
    # ss=time.clock()
    # s='./file'
    # encrypt(s)
    # print(time.clock()-ss)
    # help(_array)
    # _compress_tarfile(s)
    # _extarct_tarfile(s)
    # import time
    # x=time.clock()
    # s=encode(('1'*100002).encode(),'gwdfdddddgefrgfgdfgr')
    # t=time.clock()
    # print((t-x))
    # x=time.clock()
    # k=decode(s,'gwdfdddddgefrgfgdfgr')
    # t=time.clock()
    # print((t-x))
    # print(len(k))
    # x=b64encode(b'sd', passwd='w')
    # print(x)
    # t=b64decode(x, passwd='w')
    # print(t)
    # s=b's'*899
    # g=spencode(s,passwd='wegewf')
    # print(g)
    # t=spdecode(g,passwd='wegewf')
    # print(s)
    # filename='x.py'
    # s=md5.md5(filename)
    # print(s)
    # encrypt(filename)
    # s=md5.md5(filename+'.yx')
    # print(s)
    # decipher(filename+'.yx','sd.py')
    # s=md5.md5('sd.py')
    # print(s)