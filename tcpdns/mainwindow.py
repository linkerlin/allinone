# -*- coding: utf-8 -*-
# cody by linker.lin@me.com
# ver: 1.0
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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

from dnslist import dnslist
import config
from utils import *

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

