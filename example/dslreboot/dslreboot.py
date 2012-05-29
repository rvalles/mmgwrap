#!/usr/bin/python
from __future__ import division #1/2 = float, 1//2 = integer, python 3.0 behaviour in 2.6, to make future port to 3 easier.
import libxml2
import xmlrpclib
import time
import logging
def main():
	config = libxml2.parseFile("config.xml")
	for node in config.xpathEval('/dslrebootcfg/url'):
		url = node.content
	mmgwrap = xmlrpclib.ServerProxy(url)
	mmgwrap.reboot()
if __name__ == '__main__':
        main()
