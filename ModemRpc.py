from Modem import Modem
class ModemRpc(object):
	def __init__(self,modem):
		self.modem=modem
	def getSpeed(self):
		"""Returns sync speed down/up in kbps."""
		return self.modem.getSpeed()
	def getUptime(self):
		"""Returns connection uptime in seconds."""
		return self.modem.getUptime()
	def resync(self):
		"""Forces an ADSL reconnection."""
		self.modem.resync()
		return "ACK"
	def reboot(self):
		"""Restarts the router."""
		self.modem.reboot()
		return "ACK"
