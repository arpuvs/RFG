#-----------------------------------------------------------------------------
# Name:        Agilent34970A.py
#
# Purpose:     Driver for the Agilent 34970A data acquisition/switch unit.
#              Functions are created primarily for DC voltage and current 
#              measurement on multiple channels.
#
# Author:      Dave Shoudy
#
# Created:     2007/08/09
#
# Mods:        2007/12/10
#		   GPIB comm error fixed
#		   
#		   2007/11/28
#              Syntax error fixed (Tom MacLeod)
#           
#              2007/10/18
#              Addition for digital output from the 34907A plug in module
#-----------------------------------------------------------------------------

from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class Agilent34970A(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        '''Initializes the GPIB interface'''
        GPIBObjectBaseClass.__init__(self, 'Agilent Technologies,34970A', addr)
 
    def __MeasVoltage__(self,channel=101,range=10,resolution=1e-5):
        '''This function gets the Voltage on the specified channel'''
        params = str(range) + ',' + str(resolution) + ',(@' + str(channel) + ')'
        return float(self.instr.ask('MEAS:VOLT:DC? %s' %params))
    
    def __MeasCurrent__(self,channel=121,range=1,resolution=1e-6):
        '''This function gets the Current on the specified channel'''
        params = str(range) + ',' + str(resolution) + ',(@' + str(channel) + ')'
        return float(self.instr.ask('MEAS:CURR:DC? %s' %params))

    def __MonitorChannel__(self,channel):
        '''This function puts the channel specified on the display of the 34970A for monitoring'''
        self.instr.write('ROUT:MON (@%s)' %str(channel))
    
    def __SetDigitalOut__(self,channel=201,byte=0):
        '''This function sets the digital output of the 34907A module based on 'byte' '''
        params = str(byte) + ',(@' + str(channel) + ')'
        self.instr.write('SOUR:DIG:DATA:BYTE %s' %params)
    
    def __GetDigitalOut__(self,channel=201):
        '''This function gets the digital output value of the specified channel'''
        params = '(@' + str(channel) + ')'
        dig = self.instr.ask('SOUR:DIG:DATA:BYTE? %s' %params)
        return int(dig)
    
    
    Voltage         = property(__MeasVoltage__,      None, None, "Gets the 34970A Voltage on the specified channel")
    Current         = property(__MeasCurrent__,      None, None, "Gets the 34970A Current on the specified channel")
    
    