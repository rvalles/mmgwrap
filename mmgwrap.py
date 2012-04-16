#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import libxml2
import DocXMLRPCServer
from time import time
from Modem import Modem
from ModemRpc import ModemRpc
def main():
	config = libxml2.parseFile("config.xml")
	for node in config.xpathEval('/mwmwrapcfg/host'):
		host = node.content
	for node in config.xpathEval('/mwmwrapcfg/user'):
		user = node.content
	for node in config.xpathEval('/mwmwrapcfg/password'):
		password = node.content
	bindip = "0.0.0.0"
	for node in config.xpathEval('/mwmwrapcfg/bindip'):
		bindip = node.content
	bindport = "12345"
	for node in config.xpathEval('/mwmwrapcfg/bindport'):
		bindport = int(node.content)
	pollinterval = 2
	for node in config.xpathEval('/mwmwrapcfg/pollinterval'):
		pollinterval = int(node.content)
	verbose = True
	for node in config.xpathEval('/mwmwrapcfg/verbose'):
		if node.content == "False":
			verbose = False
	modem = Modem(host,user,password)
	if verbose:
		print "Listening on: http://"+bindip+":"+str(bindport)+"/"
	server = DocXMLRPCServer.DocXMLRPCServer((bindip, bindport), DocXMLRPCServer.DocXMLRPCRequestHandler, verbose)
	rpc = ModemRpc(modem)
	server.register_instance(rpc)
	server.timeout = pollinterval
	lasttime = float(time())
	while True:
		server.handle_request()
		if (time()-lasttime) > pollinterval:
			modem.refreshSpeed()
			lasttime = float(time())
if __name__ == "__main__":
        main()
