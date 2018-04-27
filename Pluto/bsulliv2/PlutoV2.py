'''
Created on May 10, 2016

@author: cchouina

Edited by Chas Frick
12/17
'''
import clr
clr.AddReference('sdpApi1')
import sdpApi1 # Library to access the SDP card
from System import Array, Int16

class PlutoV2:
	'''
	classdocs
	'''

	PLUTO_BOARD_V0_ID = "6505456800000130"
	PLUTO_BOARD_V1_ID = "6505456800000131"
	PLUTO_BOARD_V2_ID = "6505456800000132"
	
	# Register declarations
	AMP_ATT_REG_ADDR = 0x19 
	AMP_GAIN_REG_ADDR = 0x1A
	AMP_PWR_MOD_REG_ADDR = 0x1A
	AMP_ENABLE_REG_ADDR = 0x18

	def __init__(self, verbose = 0, sclkFreq = 100000, lsbFirst = False, fourWire = True, dataWidth = 8, addrWidth = 8, rwPos = 16):
		'''
		Constructor
		verbose   : Control the amount of information printed to the console. Helps to debug code.
		sclkFreq  : SPI bus frequency
		LSBFirst  : Inidicate if the LSB is sent first, default = False
		FourWire  : Indicate if it is a 3 or 4 wire interface, default to 4.
		dataWidth : Width of the data, defaults to 8
		addrWidth : Width of the address field
		RWPos     : The location of the R/W bit, start at 1
		'''
		# Use the same naming convention as the HADEval modules
		# self.DUT_SPIReset = self.SPI_Reset
		#self.DUT_SPIRead  = self.SPI_Read
		#self.DUT_SPIWrite = self.SPI_Write
		
		self.__sclkFreq  = sclkFreq
		self.__lsbFirst  = lsbFirst
		self.__fourWire  = fourWire
		self.__dataWidth = dataWidth
		self.__addrWidth = addrWidth
		self.__rwPos     = rwPos
		# Create a SDP Base object to access it.
		# This creates the object but no connection is activated yet, the function 'connect'
		# must be called for that.
		self.__sdpBase = sdpApi1.SdpBase()
		self.verbose   = verbose
		self.lastError = 0
		print 'sdpApi1.Enum.SdpConnector.connectorB --- ',sdpApi1.Enum.SdpConnector.connectorB # should print 1
		
	def connect(self,daughterid):
		'''
		daughterid : ID of the SDP board, typical value are:
		
		PLUTO_BOARD_V0_ID = ""
		PLUTO_BOARD_V1_ID = ""
		PLUTO_BOARD_V2_ID = "0000000000000123"
		'''
		
		# Try to connect to the SDP board
		# The SPD-S only has one connector, so the second ID is set to ""
		# fixedIDOrder is set to False, but could most probably be True since there is only one connector
		_, self.__sdpBase = sdpApi1.SdpManager.connect(daughterid, "", False, self.__sdpBase)
		if (self.__sdpBase.connected == False):
			if (self.verbose > 0):
				print 'UNable to connect to the SDP-S board with ID = ', daughterid
		else:
			# Get a SPI and GPIO object to access them
			_, self.__sdpSpiA  = self.__sdpBase.newSpi( sdpApi1.Enum.SdpConnector.connectorA,sdpApi1.Enum.SpiSel.selA,16,False,False,False,self.__sclkFreq,0,None)
			_, self.__sdpSpiB  = self.__sdpBase.newSpi( sdpApi1.Enum.SdpConnector.connectorA,sdpApi1.Enum.SpiSel.selB,16,False,False,False,self.__sclkFreq,0,None)
			self.__sdpSpi = self.__sdpSpiA # Create an object that can hold the SPI for A or B
			
			_, self.__sdpGpio = self.__sdpBase.newGpio(sdpApi1.Enum.SdpConnector.connectorA, None) # gpio interface for connector A (0)
		
		if (self.verbose > 4):
			print "connected        = ", self.__sdpBase.connected
			print "IsAttached       = ", self.__sdpBase.IsAttached
			print "IsLocked         = ", self.__sdpBase.IsLocked
			print "Pid              = ", self.__sdpBase.Pid
			print "UniqueHardwareId = ", self.__sdpBase.UniqueHardwareId
			print "AppRequestCount  = ", self.__sdpBase.AppRequestCount

		if(daughterid == self.PLUTO_BOARD_V2_ID): 
			self.set_sdp_gpio() # Configure the GPIO to allow the board to power down the part

		return self.__sdpBase.connected

	def disconnect(self):
		self.lastError = self.__sdpBase.resetAndDisconnect()

	def flashLed(self):
		self.__sdpBase.flashLed1() # should blink led
		
	def flashProgramTime(self,programTime):
		self.__sdpBase.FlashProgramTime(programTime)
		
	def SPI_Write_16Bit(self, Address, Data):
		"""Write Register via SPI.
			Args:
				spi: SPI interface to use.
				Address: Address to write at
				Data: Data to Write
				Returns:
				   U32 : Data Read aback.
				Raises:
		"""
		# Write command
		readData  = []
		writeData = [ ((Address & 0x007FFF) << self.__dataWidth) | (Data & 0x0000FF)]
		# We read one sample at a time.
		_, readData = self.__sdpSpi.writeReadU24(writeData, 0x1, readData)
		
	def Set_SPI_Object(self, SPI_sel):
		'''
		SPI_sel: SPI chip select line letter ("A", "B", "C"}
		'''
		if(SPI_sel == "A"):
			self.__sdpSpi = self.__sdpSpiA
		elif(SPI_sel == "B"):
			self.__sdpSpi = self.__sdpSpiB
		else:
			return # Error!

	def Write16BitData(self, writeData):
	
		writeArray = Array[Int16]([writeData[0]]) # create the right arrays for CLR lib
		readArray = Array[Int16]([]) # create the right arrays for CLR lib
		
		self.__sdpSpi.writeReadU16(writeArray, 0x1, readArray)
		
		print "Wrote: array[0] = ", hex(writeArray[0])
		
	def Read8BitRegister(self, addressToRead, readDataBackFirst=True):
		# Read register
		if(readDataBackFirst): 
			readData = self.SPI_Read_8Bit(self.AMP_ATT_REG_ADDR)
			return readData
		else: # Testing
			return 0x00
			
	def Set_Amp_Trim(self, SPI_sel, AmpTrimCode, readDataBackFirst=True):
		"""Sets amp trim peaking code
			Args:
				spi: SPI interface to use.
				SPI_sel: SPI chip select line letter (A, B, C)
				AmpTrimCode: code from 0 to 15
				Returns:
				   U8 : Data Read back.
				Raises:
		"""
		self.Set_SPI_Object(SPI_sel) # Select correct SPI lines
		
		# Read Register based on flag
		readData = self.Read8BitRegister(self.AMP_ATT_REG_ADDR, readDataBackFirst)
		
		trimVal = 0x00
		
		if(AmpTrimCode > 15 or AmpTrimCode < 0):
			return # Error
		else:
			trimVal = AmpTrimCode
		
		# Combine previous reg value with hex reg
		dataForReg = (readData & 0xF0) | trimVal
		
		writeData = [(self.AMP_ATT_REG_ADDR << 8) | dataForReg]
		
		readArray = self.Write16BitData(writeData)
		
	def Set_Amp_Atten(self, SPI_sel, AmpAtten, readDataBackFirst=True):
		"""Sets amp attenuation.
			Args:
				spi: SPI interface to use.
				SPI_sel: SPI chip select line letter (A, B, C)
				AmpAtten: Attenuation of the amp in dB (Attenuation Range 1dB @ 0.1 steps 0 - 9 code) 0x00 = 0
				Returns:
				   U8 : Data Read back.
				Raises:
		"""
		self.Set_SPI_Object(SPI_sel) # Select correct SPI lines
		
		# Read Register based on flag
		readData = self.Read8BitRegister(self.AMP_ATT_REG_ADDR, readDataBackFirst)
		
		# Calculate attenuation
		hexAtten = 0x00
		
		if(AmpAtten > 1 or AmpAtten < 0):
			return # Error
		else:
			hexAtten = int(AmpAtten / 0.1)
		
		# Combine previous reg value with hex reg
		dataForReg = (hexAtten << 4) | (readData & 0x0F)
		
		writeData = [(self.AMP_ATT_REG_ADDR << 8) | dataForReg]
		
		readArray = self.Write16BitData(writeData)
		
	def Set_Amp_Gain(self, SPI_sel, GainValue, readDataBackFirst=True):
		"""Sets amp gain.
			Args:
				spi: SPI interface to use.
				SPI_sel: SPI chip select line letter (A, B, C)
				GainValue: 12 dB (0x00), 20 dB (0x01)   
							Value is one of: {"12dB", "20dB"}
				Returns:
				   U8 : Data Read back.
				Raises:
		"""
		self.Set_SPI_Object(SPI_sel) # Select correct SPI lines
		
		# Read Register based on flag
		readData = self.Read8BitRegister(self.AMP_GAIN_REG_ADDR, readDataBackFirst)

		gainForReg = 0x00
		
		if(GainValue != "12dB" and GainValue != "20dB"):
			return # Error
		elif(GainValue == "12dB"):
			gainForReg = 0x00
		elif(GainValue == "20dB"):
			gainForReg = 0x01
		
		# Combine previous reg value with hex reg
		dataForReg = (readData & 0xFE) | gainForReg
		
		writeData = [(self.AMP_GAIN_REG_ADDR << 8) | dataForReg]
		
		readArray = self.Write16BitData(writeData)
		
	def Set_Amp_Pwr_Mod(self, SPI_sel, PowerMode, readDataBackFirst=True):
		"""Sets amp power mode.
			Args:
				spi: SPI interface to use.
				SPI_sel: SPI chip select line letter (A, B, C)
				PowerMode: Lo (0x00) or Hi (0x01) 
							Value is one of: {"Lo", "Hi"}
				Returns:
				   U8 : Data Read back.
				Raises:
		"""
		self.Set_SPI_Object(SPI_sel) # Select correct SPI lines
		
		# Read Register based on flag
		readData = self.Read8BitRegister(self.AMP_GAIN_REG_ADDR, readDataBackFirst)
		
		powerModeForReg = 0x00
		
		if(PowerMode != "Lo" and PowerMode != "Hi"):
			return # Error
		elif(PowerMode == "Lo"):
			powerModeForReg = 0x00
		elif(PowerMode == "Hi"):
			powerModeForReg = 0x01
		
		# Combine previous reg value with hex reg
		dataForReg = (readData & 0xFD) | (powerModeForReg << 1)
		
		writeData = [(self.AMP_GAIN_REG_ADDR << 8) | dataForReg]
		
		readArray = self.Write16BitData(writeData)
		
	def Set_Amp_Enable(self, SPI_sel, AmpEnable, readDataBackFirst=True):
		"""Sets amp enable
			Args:
				spi: SPI interface to use.
				SPI_sel: SPI chip select line letter (A, B, C)
				AmpEnable: 0 = power down, 1 = power up
							Value is one of: {0, 1}
				Returns:
				   U8 : Data Read back.
				Raises:
		"""
		self.Set_SPI_Object(SPI_sel) # Select correct SPI lines
		
		# Read Register based on flag
		readData = self.Read8BitRegister(self.AMP_ENABLE_REG_ADDR, readDataBackFirst)
		
		if(AmpEnable != 0 and AmpEnable != 1):
			return # Error
		
		# Combine previous reg value with hex reg
		dataForReg = (readData & 0xFE) | AmpEnable
		
		writeData = [(self.AMP_ENABLE_REG_ADDR << 8) | dataForReg]
		
		readArray = self.Write16BitData(writeData)

	def SPI_Read_16Bit(self, Address):
		"""Read Register via SPI.
			Args:
				spi: SPI interface to use.
				Address: Address to write at
				Data: Data to Write
				Returns:
				   U32 : Data Read aback.
				Raises:
		"""
		readData = []
		writeData = [(0x1 << (self.__rwPos-1)) | ((Address & 0x007FFF) << 8)]  # Write command
		_, readData = self.__sdpSpi.writeReadU16(writeData, 1, readData)
		return readData[0] & 0x00FFFF
		
	def SPI_Read_8Bit(self, Address):
		"""Read Register via SPI.
			Args:
				spi: SPI interface to use.
				Address: Address to write at
				Data: Data to Write
				Returns:
				   U8 : Data Read aback.
				Raises:
		"""
		readData = []
		writeData = [(0x1 << (self.__rwPos-1)) | ((Address & 0x007FFF) << 8)]  # Write command
		#_, readData = self.__sdpSpi.writeReadU8(writeData, 1, readData)
		readDataArr = Array[Int16]([0])
		
		self.__sdpSpi.readU16(1, readDataArr, False)
		
		return readDataArr[0] & 0x000000FF
		
	def set_amp1_power_state(self, powerStr):
		'''
		Args:
			powerStr = {"ON", "OFF"}
		'''
		
		GPIOState = self.__sdpGpio.dataRead(0xFF) # Read State of Ports (Tuple position 1 holds state)
		#print GPIOState	
		GPIOState = GPIOState[1]
		
		if(powerStr.upper() == "ON"):
			print "Turning on AMP1"
			self.__sdpGpio.dataWrite(GPIOState | 0x01)
		elif(powerStr.upper() == "OFF"):
			print "Turning off AMP1"
			self.__sdpGpio.dataWrite(GPIOState & 0xFE)
		
	def set_amp2_power_state(self, powerStr):
		'''
		Args:
			powerStr = {"ON", "OFF"}
		'''
		
		GPIOState = self.__sdpGpio.dataRead(0xFF) # Read State of Ports
		#print GPIOState	
		GPIOState = GPIOState[1]
		
		if(powerStr.upper() == "ON"):
			print "Turning on AMP2"
			self.__sdpGpio.dataWrite(GPIOState | 0x02)
		elif(powerStr.upper() == "OFF"):
			print "Turning off AMP2"
			self.__sdpGpio.dataWrite(GPIOState & 0xFD)	
		

	def set_sdp_gpio(self):
		"""
		Pluto V2 GPIO Controls
		GPIO 0 -- PIN 43 -- Amp 1 (NOT) PD
		GPIO 1 -- PIN 78 -- Amp 2 (NOT) PD
		GPIO 2 -- PIN 44 -- NC
		GPIO 3 -- PIN 77 -- NC
		GPIO 4 -- PIN 45 -- NC
		GPIO 5 -- PIN 76 -- NC
		GPIO 6 -- PIN 47 -- NC
		GPIO 7 -- PIN 74 -- NC
		
		"""
		
		self.__sdpGpio.configOutput(0xff) # config all the GPIO to output; return err code
		self.__sdpGpio.dataWrite(0x03) # Turn on the two parts      