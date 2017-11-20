

class ConnectionObject(object):

	def __init__(self, addr, debug):
		
		self.addr = addr
		self.debug = debug
		
	def send_write_command(self, commandToSend):
		raise Exception("sendWriteCommand not implemented!")
	
	def send_query_command(self, commandToSend):
		raise Exception("sendQueryCommand not implemented!")
	
	def check_address(self, address):
		raise Exception("Not implemented")
			
	def update_address(self, newAddress):
		self.addr = newAddress
	
	def close(self):
		raise Exception("not implemented")