# -*- coding: utf-8 -*-
# cody by linker.lin@me.com
# ver: 1.0
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.defaultencoding,unicode("中文")


from java.awt import Color
from javax.swing import ImageIcon
from javax.swing import JButton
from javax.swing import JFrame
from javax.swing import JPanel
from java.lang import System

from java.awt import Dimension

from javax.swing import JButton
from javax.swing import JFrame
from javax.swing import JPanel
from javax.swing import BoxLayout
from javax.swing import Box
from javax.swing import *

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

from Queue import Queue
mainQ=Queue()
def log(x,t):
    t.text='\n'.join([t.text,x])
    if len(t.text)>500:
        t.text=x
def create_log(x,t):
    return lambda :log(x,t)
class MainWindow(JFrame):                 
    def __init__(self,queue):
        self.queue=queue
        super(MainWindow, self).__init__()
        self.initUI()
    def initUI(self):
        basic = JPanel()
        basic.setLayout(BoxLayout(basic, BoxLayout.Y_AXIS))
        self.add(basic)
        basic.add(Box.createVerticalGlue())
        bottom = JPanel()
        bottom.setAlignmentX(1.0)
        bottom.setLayout(BoxLayout(bottom, BoxLayout.X_AXIS))
        #okButton = JButton("OK", actionPerformed=self.onQuit)
        self.text_area = JTextArea(editable = False,
              wrapStyleWord = True,
              lineWrap = True,)
        basic.add(self.text_area)
        self.text_area.text=str(config.DHOSTS)
        closeButton = JButton(u"Close 关闭", actionPerformed=self.onQuit)
        #bottom.add(okButton)
        bottom.add(Box.createRigidArea(Dimension(5, 0)))
        bottom.add(closeButton)
        bottom.add(Box.createRigidArea(Dimension(15, 0)))
        basic.add(bottom)
        basic.add(Box.createRigidArea(Dimension(0, 15)))
        self.setTitle(u"A DNS Proxy using TCP...一个使用TCP协议的DNS代理")
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setSize(500, 300)
        self.setLocationRelativeTo(None)
        self.setVisible(True)
    def onQuit(self,event):
        System.exit(0)
class UIThread(threading.Thread):
    def __init__(self,mainwin,queue):
        self.mainwin=mainwin
        self.queue=queue
        threading.Thread.__init__(self)
        
    def run(self):
        while True:
            job=self.queue.get()
            job()
mainwin=MainWindow(mainQ)
uithread=UIThread(mainwin,mainQ)
uithread.setDaemon(True)
uithread.start()
def log2Q(message):
    mainQ.put(create_log(message,mainwin.text_area))
print "after mainwin inited..."
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


