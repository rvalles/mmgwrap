#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from time import time
import urllib2
from bs4 import BeautifulSoup
class Modem(object):
	def __init__(self,host,user,password):
		self.urlbase = "http://%s"%host
		auth_handler = urllib2.HTTPBasicAuthHandler()
		auth_handler.add_password(
			realm = "DSL Router",
			uri = self.urlbase,
			user = user,
			passwd = password
			)
		opener = urllib2.build_opener(auth_handler)
		urllib2.install_opener(opener)
		self.up = self.down = 0
		self.timeout = 3
		self.refreshSpeed()
	def reboot(self):
		try:
			urllib2.urlopen(self.urlbase+"/rebootinfo.cgi",None,self.timeout)
		except:
			return
	def __fetchSpeed(self):
		try:
			page = urllib2.urlopen(self.urlbase+"/wancfg.cmd?action=refresh",None,self.timeout)
		except:
			return (0,0)
		soup = BeautifulSoup(page.read())
		span = soup.find_all("span",{"class":"style1"})
		if len(span)<4:
			return (0,0)
		down=span[1].contents[0].rstrip(" kbps")
		if "N/A" in down:
			down = up = 0
		else:
			up = span[3].contents[0].rstrip(" kbps")
		return (int(down),int(up))
	def refreshSpeed(self):
		(down, up) = self.__fetchSpeed()
		if self.down==0 and down!=0:
			self.lastConnect = float(time())
		self.down = down
		self.up = up
	def getSpeed(self):
		return (self.down,self.up)
	def getUptime(self):
		#self.refreshSpeed()
		if self.down==0:
			return 0
		return int(time()-self.lastConnect)
	def resync(self):
		try:
			urllib2.urlopen(self.urlbase+"/adslcfgadv.cmd?adslTestMode=0",None,self.timeout)
		except:
			return
