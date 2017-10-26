# Author: Leah Magaldi
# Date: 01/24/2016
# Purpose: This module is a generic GPIB wrapper for:
# Keysight E3633A Power Supply single output, dual range (0-8V, 20A or 0-20V, 10A)
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class E3633A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'E3633A', addr)
        self.__delay__ = delay

    def __GetV__(self):
        '''This function gets the V Voltage'''
        return float( self.instr.ask('MEASure:VOLTage?') )
    def __SetV__(self, V1):
        '''This function sets the V Voltage'''
        self.instr.write( 'VOLTage ' + str(V1) )
        time.sleep(self.__delay__)

    def __GetI__(self):
        '''This function gets the I Current'''
        return float( self.instr.ask('MEASure:CURRent?') )
    def __SetI__(self, I1):
        '''This function sets the I Current'''
        self.instr.write( 'CURRent ' + str(I1) )
        time.sleep(self.__delay__)

    def __SetEnable__(self, Enabled):
        '''This function enables the On/Off for the PST-3202'''
        if Enabled:
            self.instr.write('OUTPut:STATe ON')
        else:
            self.instr.write('OUTPut:STATe OFF')
    def __GetEnable__(self):
        '''This function returns the On/Off state'''
        status = self.instr.ask('OUTPut:STATe?')
        if (status.strip() == "1" ):
            return True
        return False

    def SetOCP(self, OCP):
        '''This function sets the Maximum compliance current'''
        self.instr.write( 'Current:prot ' + str(OCP) )
        time.sleep(self.__delay__)

    def SetOVP(self, OVP):
        '''This function sets the over voltage protection'''
        self.instr.write( 'VOLTage:prot ' + str(OVP) )
        time.sleep(self.__delay__)



