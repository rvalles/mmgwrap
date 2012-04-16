#!/usr/bin/python
from __future__ import division #1/2 = float, 1//2 = integer, python 3.0 behaviour in 2.6, to make future port to 3 easier.
import libxml2
import xmlrpclib
import time
import logging
def main():
	config = libxml2.parseFile("config.xml")
	for node in config.xpathEval('/dslminspeedcfg/url'):
		url = node.content
	for node in config.xpathEval('/dslminspeedcfg/downstream'):
		mindown = int(node.content)
	for node in config.xpathEval('/dslminspeedcfg/upstream'):
		minup = int(node.content)
	for node in config.xpathEval('/dslminspeedcfg/uptime'):
		minuptime = int(node.content)
	for node in config.xpathEval('/dslminspeedcfg/pollinterval'):
		pollinterval = int(node.content)
	mmgwrap = xmlrpclib.ServerProxy(url)
	logging.basicConfig(format='%(asctime)s %(message)s')
	uptime = mmgwrap.getUptime()
	while True:
		if uptime<minuptime:
			time.sleep(minuptime-uptime)
		else:
			time.sleep(pollinterval)
		(currdown, currup) = mmgwrap.getSpeed()
		uptime = mmgwrap.getUptime()
		if uptime<minuptime:
			continue
		if (currup<minup) or (currdown<mindown):
			logging.warning("Speeds (%s/%s) are below threshold and connection uptime is high enough (%s). Forcing resync."%(currdown,currup,uptime))
			mmgwrap.resync()
if __name__ == '__main__':
        main()
