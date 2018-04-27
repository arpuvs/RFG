'''
Created on May 10, 2016

@author: cchouina

Edited by Chas Frick
12/17
'''

import clr
clr.AddReference('sdpApi1')
import sdpApi1 # Library to access the SDP card
from System import Array, Byte, Int16

class PlutoV1:
	'''
	classdocs
	'''

	PLUTO_BOARD_V1_ID = "6505456800000131"

	ADG1414_DUT1_REGISTER = 0x00 # Determine defaults
	ADG1414_DUT2_REGISTER = 0x00 # Determine defaults

	def __init__(self, verbose = 1, sclkFreq = 100000, lsbFirst = False, fourWire = True, dataWidth = 8, addrWidth = 7, rwPos = 15):
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
		self.__dataStartPos = 0

		# print self.__sclkFreq
		# print self.__lsbFirst
		# print self.__fourWire
		# print self.__dataWidth
		# print self.__addrWidth
		# print self.__rwPos
		# print self.__dataStartPos

		# Create a SDP Base object to access it.
		# This creates the object but no connection is activated yet, the function 'connect'
		# must be called for that.
		self.__sdpBase = sdpApi1.SdpBase(555)
		self.verbose   = verbose
		self.lastError = 0
		print 'sdpApi1.Enum.SdpConnector.connectorB --- ',sdpApi1.Enum.SdpConnector.connectorB # should print 1
		
	def connect(self, DUT1_Default = 0x00, DUT2_Default = 0x00):

		# Try to connect to the SDP board
		# The SPD-S only has one connector, so the second ID is set to ""
		# fixedIDOrder is set to False, but could most probably be True since there is only one connector
		_, self.__sdpBase = sdpApi1.SdpManager.connect(self.PLUTO_BOARD_V1_ID, "", False, self.__sdpBase)
		if (self.__sdpBase.connected == False):
			if (self.verbose > 0):
				print 'Unable to connect to the SDP-S board with ID = ', self.PLUTO_BOARD_V1_ID
		else:
			# Get a SPI and GPIO object to access them
			_, self.__sdpSpiA  = self.__sdpBase.newSpi( sdpApi1.Enum.SdpConnector.connectorA,sdpApi1.Enum.SpiSel.selA,8,True,False,False,self.__sclkFreq,0,None)
			_, self.__sdpSpiB  = self.__sdpBase.newSpi( sdpApi1.Enum.SdpConnector.connectorA,sdpApi1.Enum.SpiSel.selB,8,True,False,False,self.__sclkFreq,0,None)
			self.__sdpSpi = self.__sdpSpiA # Create an object that can hold the SPI for A or B

			# print self.__sclkFreq
			# print self.__lsbFirst
			# print self.__fourWire
			# print self.__dataWidth
			# print self.__addrWidth
			# print self.__rwPos
			# print self.__dataStartPos

		if (self.verbose > 4):
			print "connected        = ", self.__sdpBase.connected
			print "IsAttached       = ", self.__sdpBase.IsAttached
			print "IsLocked         = ", self.__sdpBase.IsLocked
			print "Pid              = ", self.__sdpBase.Pid
			print "UniqueHardwareId = ", self.__sdpBase.UniqueHardwareId
			print "AppRequestCount  = ", self.__sdpBase.AppRequestCount	

		# Configure DUT1
		self.__sdpSpi = self.__sdpSpiA # Create an object that can hold the SPI for A or B
		self.ADG1414_DUT1_REGISTER = DUT1_Default
		writeData = [self.ADG1414_DUT1_REGISTER]
		#readArray = self.Write8BitData(writeData)
		
		# Configure DUT2
		self.__sdpSpi = self.__sdpSpiB
		self.ADG1414_DUT2_REGISTER = DUT2_Default
		writeData = [self.ADG1414_DUT2_REGISTER]
		#readArray = self.Write8BitData(writeData)
		
		# Reset chip select to SelA
		self.__sdpSpi = self.__sdpSpiA

		return self.__sdpBase.connected

	def disconnect(self):
		self.lastError = self.__sdpBase.resetAndDisconnect()

	def flashLed(self):
		self.__sdpBase.flashLed1() # should blink led
		
	def flashProgramTime(self,programTime):
		self.__sdpBase.FlashProgramTime(programTime)
		
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
	
	def GetReadDataRegisterValue(self, SPI_sel):
		if(SPI_sel == "A"):
			return self.ADG1414_DUT1_REGISTER
		elif(SPI_sel == "B"):
			return self.ADG1414_DUT2_REGISTER
		else:
			return self.ADG1414_DUT1_REGISTER
			
	def UpdateDataRegisters(self, SPI_sel, dataForRegister):
		if(SPI_sel == "A"):
			self.ADG1414_DUT1_REGISTER = dataForRegister
		elif(SPI_sel == "B"):
			self.ADG1414_DUT2_REGISTER = dataForRegister
		else:
			self.ADG1414_DUT1_REGISTER = dataForRegister
			
	def Set_Amp_Enable(self, SPI_sel, AmpEnable):
		"""Sets amp to power down or power up
			Args:
				spi: SPI interface to use.
				SPI_sel: SPI chip select line letter (A, B, C)
				AmpEnable: 1 or 0 (powered on or powered off)
				Returns:
				   U8 : Data Read back.
				Raises:
		"""
		self.Set_SPI_Object(SPI_sel) # Select correct SPI lines

		# Read register 
		#(no readback so have to assume using correct value)
		readData = self.GetReadDataRegisterValue(SPI_sel)
		#readData = self.SPI_Read_8Bit(self.ADG1414_SPI_REGISTER)
		
		if(AmpEnable != 0 and AmpEnable != 1):
			return # Error
		
		# Combine previous reg value with hex reg
		dataForReg = (readData & 0xF7) | (AmpEnable << 3)
		#dataForReg=(readData & 0xFB) | (AmpEnable << 2)
		
		writeData = [dataForReg]
		readArray = self.Write8BitData(writeData)
		
		# Update dataRegs
		self.UpdateDataRegisters(SPI_sel, dataForReg)
		
	def Set_Amp_Atten(self, SPI_sel, AmpAtten):
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

		# Read register
		#(no readback so have to assume using correct value)
		readData = self.GetReadDataRegisterValue(SPI_sel)
		#readData = self.SPI_Read_8Bit(self.ADG1414_SPI_REGISTER)
		
		# Calculate attenuation
		hexAtten = 0x00
		
		if(AmpAtten > 1 or AmpAtten < 0):
			return # Error
		else:
			hexAtten = int(AmpAtten / 0.1) # Mod rev BKS
		
		# Combine previous reg value with hex reg
		dataForReg = (hexAtten << 4) | (readData & 0x0F)
		
		writeData = [dataForReg]
		readArray = self.Write8BitData(writeData)
		
		# Update dataRegs
		self.UpdateDataRegisters(SPI_sel, dataForReg)
		
		
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
		readDataArr = Array[Byte]([0])
		
		self.__sdpSpi.readU8(1, readDataArr, False)
		
		return readDataArr[0] & 0x000000FF

	def Write16BitData(self, writeData):

		writeArray=Array[Int16]([writeData[0]])  # create the right arrays for CLR lib
		readArray=Array[Int16]([])  # create the right arrays for CLR lib

		self.__sdpSpi.writeReadU16(writeArray, 0x1, readArray)

		print "Wrote: array[0] = ", hex(writeArray[0])
	
	def Write8BitData(self, writeData):
		# print self.__sclkFreq
		# print self.__lsbFirst
		# print self.__fourWire
		# print self.__dataWidth
		# print self.__addrWidth
		# print self.__rwPos
		# print self.__dataStartPos
		writeArray = Array[Byte]([writeData[0]]) # create the right arrays for CLR lib
		readArray = Array[Byte]([]) # create the right arrays for CLR lib
		
		self.__sdpSpi.writeReadU8(writeArray, 0x1, readArray)
		
		print "Wrote: array[0] = ", hex(writeArray[0])