# -*- coding: utf-8 -*-
# cody by linker.lin@me.com
# ver: 1.0
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.defaultencoding,unicode("中文")



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
from utils import *
from mainwindow import *


#--------------------------------------------------
# tcp dns request
#---------------------------------------------------
def queryDNS(server, port, querydata,is_tcpserver):
    # length
    Buflen = struct.pack('!h', len(querydata))
    sendbuf = Buflen + querydata
    try:
        print  "is_tcpserver:",is_tcpserver
        if is_tcpserver:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(config.TIMEOUT) # set socket timeout
            s.connect((server, int(port)))
            s.send(sendbuf)
            data = s.recv(2048)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(config.TIMEOUT) # set socket timeout            
            s.sendto(querydata,(server, int(port)))
            data = s.recvfrom(2048)
    except Exception,ex:
        print traceback.print_exc(sys.stdout),ex
        if s: s.close()
        return
      
    if s: s.close()
    return data



#-----------------------------------------------------
# send udp dns respones back to client program
#----------------------------------------------------
def transfer(querydata, addr, server):
    if not querydata: return
    domain = bytetodomain(querydata[12:-4])
    qtype = struct.unpack('!h', querydata[-4:-2])[0]
    print 'domain:%s, qtype:%x, thread:%d' %  (domain, qtype, threading.activeCount())
    s='domain:%s, qtype:%x, thread:%d' %  (domain, qtype, threading.activeCount())
    log2Q(s)     
    response= get_from_cache(domain,qtype)
    if response:
        server.sendto(response[2:], addr)
    DHOST,is_tcpserver = dnslist.randomDNS(domain)
    print DHOST,is_tcpserver
    response = queryDNS(DHOST, config.DPORT, querydata,is_tcpserver)
    if response:
        # udp dns packet no length
        server.sendto(response[2:], addr)
        set_cache(domain,qtype,response) 
    return

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    def __init__(self, s, t):
        SocketServer.UDPServer.__init__(self, s, t)

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        addr = self.client_address
        transfer(data, addr, socket)

#------------------------------------------------------
# main entry
#------------------------------------------------------
if __name__ == "__main__":
    print '>> Please wait program init....'
    print '>> Init finished!'
    print '>> Now you can set dns server to 127.0.0.1'
    log2Q("="*10)
    server = ThreadedUDPServer(('127.0.0.1', 53), ThreadedUDPRequestHandler)
    # on my ubuntu uid is 1000, change it 
    # comment out below line on windows platform
    #os.setuid(1000)

    server.serve_forever()
    server.shutdown()


