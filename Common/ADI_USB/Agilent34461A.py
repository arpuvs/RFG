#-----------------------------------------------------------------------------
# Name:        Agilent34461A.py
# Purpose:     Device Interface Wrapper for Agilent34461A
#              Spawned off from HP34401A Voltmeter
#
# Author:      Kaushal Shrestha
#
# Created:     2013/12/16
# RCS-ID:      $Id: Agilent34461A.py 421 2014-03-12 14:57:26Z kshresth $
# Copyright:   (c) Kaushal Shrestha, Analog Devices Inc.
# Licence:     Analog Devices Inc.
#-----------------------------------------------------------------------------
from ADI_USB.USBObject import USBObjectBaseClass as USBObjectBaseClass

class Agilent34461A(USBObjectBaseClass):
    def __init__(self, addr = None, delay=0.5):
        USBObjectBaseClass.__init__(self, 'Agilent Technologies,34461A', addr)
        self.__delay__ = delay
        #self.__SetRemoteMode__()
    
    def __GetVoltage__(self):
        '''This function gets the HP34401A Voltage'''
        return float(self.instr.ask('MEAS:VOLT:DC?'))

    def __GetCurrent__(self):
        '''This function gets the HP34401A Current'''
        return float(self.instr.ask('MEAS:CURR:DC?'))
    
    def __GetResistance__(self):
        '''This function gets the HP34401A Resistance'''
        return float(self.instr.ask('MEAS:RES?'))
    def __Get4wireResistance__(self):
        '''This function gets the HP34401A 4 Wire Resistance'''
        return float(self.instr.ask('MEAS:FRES?'))

    def __CheckContinuity__(self):
        '''This function Checks for HP34401A Continuity'''
        res = float(self.instr.ask('MEAS:CONT?')) / 1e6
        # return true if resistance is less that 5 ohms
        if res < 5.0:
            return True
        else:
            return False
        
    Voltage            = property(__GetVoltage__,         None, None, "Gets the Agilent34461A Voltage")
    Current            = property(__GetCurrent__,         None, None, "Gets the Agilent34461A Current")
    Resistance         = property(__GetResistance__,      None, None, "Gets the Agilent34461A 2-Wire Resistance")
    FourWireResistance = property(__Get4wireResistance__, None, None, "Gets the Agilent34461A 4-Wire Resistance")
    CheckContinuity    = property(__CheckContinuity__,    None, None, "Checks for Agilent34461A Continuity")