# Author: Chas Frick
# Date: 8/2/2017
# Purpose: Provide a wrapper for the updated FMB Rev 2 Box designed in June to August 2017

from USBConnectionObjectLabPC import USBConnectionObject
#from USBConnectionObject import USBConnectionObject # This was the original using port.device, but that doesn't work on another PC, so using the generic solution above ^ 
from TCPIPConnectionObject import TCPIPConnectionObject

class FMB(object):
    
	def __init__(self, addr=None, filterDictionary = None, debug=True):
		
		if(addr is None):
			raise Exception("Addr must be specified as either COM# or 192.168.1.#")
		
		if(filterDictionary is None or filterDictionary is {}):
			raise Exception("filterDictionary must be provided")
		
		import re # regex 
		
		print re.findall(r"COM\d+", addr)
		print re.findall(r"com\d+", addr)
		print re.findall(r"\d+.\d+.\d+.\d+", addr)
		
		IPStrs = re.findall(r"\d+.\d+.\d+.\d+", addr)
		
		self.addrType =  None
		
		if(re.findall(r"COM\d+", addr) != [] or re.findall(r"com\d+", addr) != []):
			print "Using COM port to communicate with FMB"
			
			self.addrType = "COM"
			
			self.CommsObj = USBConnectionObject(addr, debug)
			
		elif(IPStrs != []):
			if(len(IPStrs[0].split(".")) != 4):
				raise Exception("FMB(addr=\'%s\') addr argument not recognized!\nAddr must be specified as either COM# or 192.168.1.#" % addr)
				
			try:
				import socket
				socket.inet_aton(IPStrs[0])
			except:
				raise Exception("FMB(addr=\'%s\') addr argument not recognized!\nAddr must be specified as either COM# or 192.168.1.#" % addr)
				
			print "Using TCP to communicate with FMB"
			self.addrType = "IP"
			
			self.CommsObj = TCPIPConnectionObject(addr, debug)
			
		else:
			raise Exception("FMB(addr=\'%s\') addr argument not recognized!\nAddr must be specified as either COM# or 192.168.1.#" % addr)
			
		self.addr = addr
		self.filterDictionary = filterDictionary
		
	def select_filter(self, filterNum):
		print ("Selecting Filter #%d (%s) ..." % (filterNum, self.filterDictionary[filterNum]))
		self.write_filter_information(filterNum)
		
	def get_filter_center_freq_hz(self, filterNum):
		filterFreqString = self.filterDictionary[filterNum]

		stringParts = filterFreqString.split(" ")

		unitsStr = stringParts[1]
		decimalPart = stringParts[0]

		multiplier = 1
		if(unitsStr == "GHz"):
			multiplier = 1e9
		elif(unitsStr == "MHz"):
			multiplier = 1e6
		else: # kHz
			multiplier = 1e3

		return float(decimalPart) * multiplier

	def write_filter_information(self, filterNum):
		
		self.addr = self.CommsObj.check_address(self.addr)
		
		commandStr = "Filter%d" % filterNum
		
		self.CommsObj.send_write_command(commandStr) # Sends command 
		
	def get_spi_sw_byte_from_list_of_positions(self, switchPositionList):
		
		SWByte = 0x00 
		
		for positionToEnable in switchPositionList:
			SWByte = SWByte | (1 << (positionToEnable - 1)) # Mapping (position - 1) to byte within the switch  
		
		print "0x%x" % SWByte,
		print "{0:b}".format(SWByte)
		
		return SWByte

	def send_raw_spi_bytes_to_fmb(self, listOfSPIBytes):

		commandStr = "SPIBytes:"
		if(len(listOfSPIBytes) == 0):
			return
		elif(len(listOfSPIBytes) == 1):
			commandStr += hex(listOfSPIBytes[0])
		else:
			for SPIByte in listOfSPIBytes[:-1]:
				commandStr += hex(SPIByte) + ","
			
			commandStr += hex(SPIByte)
		
		self.addr = self.CommsObj.check_address(self.addr)        
		self.CommsObj.send_write_command(commandStr) # Sends command 
        
if __name__ == "__main__":

	'''
	switchDictionaryGregRichBox = {'AuxButton': (0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x01, 0x08), 
							  'Button_Filter1': (0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x02, 0x04),
							  'Button_Filter2': (0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x04, 0x02),
							  'Button_Filter3': (0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x10, 0x01),
							  'Button_Filter4': (0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x08, 0x20),
							  'Button_Filter5': (0x0, 0x0, 0x0, 0x0, 0x20, 0x04, 0x20, 0x10), # note fix the 0xFF
							  'Button_Filter6': (0x0, 0x0, 0x0, 0x0, 0x01, 0x08, 0x20, 0x10),
							  'Button_Filter7': (0x0, 0x0, 0x0, 0x0, 0x02, 0x02, 0x20, 0x10),
							  'Button_Filter8': (0x0, 0x0, 0x0, 0x0, 0x04, 0x01, 0x20, 0x10),
							  'Button_Filter9': (0x0, 0x0, 0x0, 0x0, 0x08, 0x20, 0x20, 0x10),
							  'Button_Filter10': (0x0, 0x0, 0x01, 0x08, 0x10, 0x10, 0x20, 0x10),
							  'Button_Filter11': (0x0, 0x0, 0x20, 0x04, 0x10, 0x10, 0x20, 0x10),
							  'Button_Filter12': (0x0, 0x0, 0x02, 0x20, 0x10, 0x10, 0x20, 0x10),
							  'Button_Filter13': (0x0, 0x0, 0x04, 0x02, 0x10, 0x10, 0x20, 0x10),
							  'Button_Filter14': (0x0, 0x0, 0x08, 0x01, 0x10, 0x10, 0x20, 0x10),
							  'Button_Filter15': (0x01, 0x10, 0x10, 0x10, 0x10, 0x10, 0x20, 0x10),
							  'Button_Filter16': (0x20, 0x08, 0x10, 0x10, 0x10, 0x10, 0x20, 0x10),
							  'Button_Filter17': (0x02, 0x04, 0x10, 0x10, 0x10, 0x10, 0x20, 0x10),
							  'Button_Filter18': (0x10, 0x02, 0x10, 0x10, 0x10, 0x10, 0x20, 0x10),
							  'Button_Filter19': (0x04, 0x20, 0x10, 0x10, 0x10, 0x10, 0x20, 0x10),
							  'Button_Filter20': (0x08, 0x01, 0x10, 0x10, 0x10, 0x10, 0x20, 0x10)
						   }
	'''

	# To autogenerate this object automatically call the return_FMB_object_generic function in FMB_Resources.py (with updated .csv in FilterInformation folder
	# fmb = FMB('COM8', {1: "2.3 MHz", 2: "10.3 MHz", 3: "70 MHz", 4: "100.3 MHz",
	#         5: "200.3 MHz", 6: "300.3 MHz", 7: "400.3 MHz", 8: "500.3 MHz",
	#         9: "700.3 MHz", 10: "1000.3 MHz", 11: "1.5 GHz", 12: "2 GHz",
	#         13: "2.5 GHz", 14: "3.1 GHz", 15: "3.7 GHz", 16: "4.1 GHz",
	#         17: "4.5 GHz", 18: "5.0 GHz", 19: "5.5 GHz", 20: "6.0 GHz",
	#         21: "Aux"})

	# For Greg Rich's FMB
	# '192.168.1.2'
	fmb = FMB('192.168.1.2', {1: "2.5 MHz", 2: "5 MHz", 3: "33 MHz", 4: "78 MHz",
						5: "120 MHz", 6: "225.3 MHz", 7: "350.3 MHz", 8: "500 MHz",
						9: "800.3 MHz", 10: "1 GHz", 11: "1.5 GHz", 12: "2 GHz",
						13: "2.5 GHz", 14: "3 GHz", 15: "3.5 GHz", 16: "4 GHz",
						17: "4.5 GHz", 18: "5 GHz", 19: "5.5 GHz", 20: "5.9 GHz",
						21: "Aux"})

	## To autogenerate this object automatically call the return_FMB_object_generic function in FMB_Resources.py
	# fmb = FMB('192.168.1.2', {1: "2.3 MHz", 2: "10.3 MHz", 3: "70 MHz", 4: "100.3 MHz",
				# 5: "200.3 MHz", 6: "300.3 MHz", 7: "400.3 MHz", 8: "500.3 MHz",
				# 9: "700.3 MHz", 10: "1000.3 MHz", 11: "1.5 GHz", 12: "2 GHz",
				# 13: "2.5 GHz", 14: "3.1 GHz", 15: "3.7 GHz", 16: "4.1 GHz",
				# 17: "4.5 GHz", 18: "5.0 GHz", 19: "5.5 GHz", 20: "6.0 GHz",
				# 21: "Aux"})
		
	#fmb.CommsObj.send_write_command('Filter1')
	filterToSelect = 1
	fmb.select_filter(filterToSelect)
	centFreqHz = fmb.get_filter_center_freq_hz(filterToSelect)
	print "FilterCenter Freq (Hz) = ", centFreqHz

	
	import ADI_GPIB

	sigGen = ADI_GPIB.SMA(28)

	sigGen.Frequency = centFreqHz

	for filtNum in range(1,21): # stops before AUX

		fmb.select_filter(filtNum)
		centFreqHz = fmb.get_filter_center_freq_hz(filtNum)
		print "FilterCenter Freq (Hz) = ", centFreqHz

		sigGen.Frequency = centFreqHz
		
		raw_input("press enter")
		
	'''
	for filtNum in range(1,21): # stops before AUX

		fmb.select_filter(filtNum)
		centFreqHz = fmb.get_filter_center_freq_hz(filtNum)
		print "FilterCenter Freq (Hz) = ", centFreqHz

		#sigGen.Frequency = centFreqHz
		
		raw_input("press enter")

	#     import time
	#     for run in range(20):
	#         for filterNum in range(1,22):
	#             fmb.select_filter(filterNum)
	#             time.sleep(0.1)

	#fmb.CommsObj.send_write_command("filter77")
	 
	# SW8Byte = fmb.get_spi_sw_byte_from_list_of_positions([1,3,6]) # returns a byte to write to the ADG1414 for the positions 1,3,6 to be enabled
	# SW7Byte = fmb.get_spi_sw_byte_from_list_of_positions([1,2,3])
	# SW6Byte = fmb.get_spi_sw_byte_from_list_of_positions([4,5,6])
	# SW5Byte = fmb.get_spi_sw_byte_from_list_of_positions([3,5,6])
	# SW4Byte = fmb.get_spi_sw_byte_from_list_of_positions([1,2,3])
	# SW3Byte = fmb.get_spi_sw_byte_from_list_of_positions([1,2,3])
	# SW2Byte = fmb.get_spi_sw_byte_from_list_of_positions([4,5,6])
	# SW1Byte = fmb.get_spi_sw_byte_from_list_of_positions([3,5,6])
	   
	# listOfSwitchBytes = [SW1Byte, SW2Byte, SW3Byte, SW4Byte, SW5Byte, SW6Byte, SW7Byte, SW8Byte]
	   
	# fmb.send_raw_spi_bytes_to_fmb(listOfSwitchBytes)  
    '''