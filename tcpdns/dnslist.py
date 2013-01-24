from config import *
from random import sample

class DNSList(object):
	def __init__(self,dnslist):
		self.dnslist=dnslist
	def randomDNS(self):
		return sample(self.dnslist,1)[0]
	def __str__(self):
		return "a dns list.\n"+str(self.dnslist)
dnslist=DNSList(DHOSTS)
if __name__=="__main__":		
	print dnslist
	print dnslist.randomDNS()