from config import *
from random import sample
import re

class DNSList(object):
	def __init__(self,dnslist,whilelist,whilelistservers):
		self.dnslist=dnslist
		self.whilelist=whilelist
		self.whilelistservers=whilelistservers
	def randomDNS(self,domain):
		for w in WHILELIST:
			if re.search(w,domain):
				return sample(self.whilelistservers,1)[0],False
		return sample(self.dnslist,1)[0],True
	def __str__(self):
		return "a dns list.\n"+str(self.dnslist)
dnslist=DNSList(DHOSTS,WHILELIST,WHILELISTSERVERS)
if __name__=="__main__":		
	print dnslist
	print dnslist.randomDNS()