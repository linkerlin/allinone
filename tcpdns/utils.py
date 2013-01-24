# -*- coding: utf-8 -*-
# cody by linker.lin@me.com
# ver: 1.0
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.defaultencoding,unicode("中文")


from java.lang import System
import os, sys
import socket
import struct
import threading
import thread
import SocketServer
import traceback
import random
import thread

from dnslist import dnslist
import config


#-------------------------------------------------------------
# Hexdump£¬Cool :)
# default width 16
#--------------------------------------------------------------
def hexdump( src, width=16 ):
    FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])
    result=[]
    for i in xrange(0, len(src), width):
        s = src[i:i+width]
        hexa = ' '.join(["%02X"%ord(x) for x in s])
        printable = s.translate(FILTER)
        result.append("%04X   %s   %s\n" % (i, hexa, printable))
    return ''.join(result)


#---------------------------------------------------------------
# bytetodomain
# 03www06google02cn00 => www.google.cn
#--------------------------------------------------------------
def bytetodomain(s):
    domain = ''
    i = 0
    length = struct.unpack('!B', s[0:1])[0]
    while length != 0 :
        i += 1
        domain += s[i:i+length]
        i += length
        length = struct.unpack('!B', s[i:i+1])[0]
        if length != 0 :
            domain += '.'
    return domain

mem={}
def get_from_cache(domain,qtype):
    key=str(domain)+str(qtype) 
    if key in mem:
        ret=mem[key]
        print "get from cache:",domain,qtype,hexdump(ret)
        if random.randint(1,100)>95: mem.pop(key)
        return ret
    else:
        return None
def set_cache(domain,qtype,response):
    mem[str(domain)+str(qtype)]=response


from Queue import Queue
#global mainQ
mainQ=Queue()
def log(x,t):
    t.text='\n'.join([t.text,x])
    if len(t.text)>500:
        t.text=x
def create_log(x,t):
    return lambda :log(x,t)


















