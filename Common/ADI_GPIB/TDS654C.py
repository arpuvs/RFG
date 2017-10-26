# Author: Tom MacLeod
# Date: 11/01/2006
# Testing screencapture
# Rev History --------------------
# Date: 10/27/2006
# Purpose: This module is a generic GPIB wrapper for:
# Tektronix TDS 654C Oscilliscope
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import StringIO
#import Image

class TDS654C(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        GPIBObjectBaseClass.__init__(self, 'TEKTRONIX,TDS 654C', addr)

    def __GetBMP__(self):
        '''Gets the screencap from the TDS654C Oscilloscope'''
        self.instr.write('HARDCOPY:PORT GPIB')
        self.instr.write('HARDCOPY START')
        self.__bmpstr__ = self.instr.read()
        self.__bmp__    = Image.open(StringIO.StringIO(self.__bmpstr__))
        return self.__bmp__.rotate(-90)
        
    
    BMP = property(__GetBMP__, None, None, "Gets the screencap from the TDS654C")