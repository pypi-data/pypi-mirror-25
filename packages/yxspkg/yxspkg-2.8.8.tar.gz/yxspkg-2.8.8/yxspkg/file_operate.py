#!/usr/bin/env python3
import os
from os.path import getsize
import os.path as path
import shutil
version='0.1'
def _DeleteFiles(a):
    return
    if len(a)==0:
        print('No file need to be deleted')
        return
    else:
        for i in a:print(i)
        x=input('Do you want to delete these files?[Y/N]')
    if x.strip().lower()!='y':
        print('No thing to do.')
        return
    else:
        for i in a:os.remove(i)
def issame(file1,file2,index=0):
    xf=open(file1,'rb')
    yf=open(file2,'rb')
    x=xf.read()
    y=yf.read()
    xf.close()
    yf.close()
    if len(x)!=len(y):return False
    if x==y:
        return True
    else:
        if index==1:
            num=len(x)
            i=0
            k=0
            while i<num:
                if x[i]!=y[i]:k+=1
                i+=1
            k=float(k)/num
            if k<1e-5:
                return True
        return False  
def Bianli(dirname):
    y=os.walk(dirname)
    x=[]
    for i in y:
        x.extend([i[0]+os.sep+j for j in i[2]])
    return x           
def DeleteSameFiles(dirname,floor=0,index=0,pause=False):
    delfiles=[]
    if floor!=0:x=Bianli(dirname)
    else:x=[dirname+os.sep+i for i in os.listdir(dirname)]
    zong=float(len(x))
    x=[(i,getsize(i)) for i in x if path.isfile(i)]
    x.sort(key=lambda x:x[1])
    kk0=0
    for i in range(len(x)-1):
        kk=i/zong
        if kk-kk0>0.05:
            print(u'进度:%-5.3f%%' % (kk*100))
            kk0=kk
        if x[i][1]==x[i+1][1]:
            if issame(x[i][0],x[i+1][0],index):
                if x[i+1][0]<x[i][0]:
                    t=x[i]
                    x[i]=x[i+1]
                    x[i+1]=t
                delfiles.append(x[i][0])
    _DeleteFiles(delfiles)
def Operate(dirname,handle=None,floor=0):
    x=os.walk(dirname)
    if floor==0:x=[next(x)]
    for i in x:
        for j in i[2]:
            handle(i[0],j,i[0]+os.sep+j,getsize(i[0]+os.sep+j))

if __name__=='__main__':
    Operate('/home/yxs/D/music',handle=kk,floor=1)
    # x=time.time()
    # DeleteSameFiles('/home/yxs/E/学习/书/Calibre书库',floor=1)
    # print(time.time()-x)