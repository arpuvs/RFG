# Author: Tom MacLeod
# Date: 12/18/2006
# Added: 'Current' property
# ---------------------------------------------------------------------
# Date: 10/27/2006
# 08/21/2012 - added  2&4 wire resistance - A. Arrants
# Purpose: This module is a generic GPIB wrapper for:
# HP34401A Voltmeter
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass

class HP34401A(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        GPIBObjectBaseClass.__init__(self, 'HEWLETT-PACKARD,34401A', addr)
    
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
        
    Voltage         = property(__GetVoltage__,      None, None, "Gets the HP34401A Voltage")
    Current         = property(__GetCurrent__,      None, None, "Gets the HP34401A Current")
    Resistance      = property(__GetResistance__,   None, None, "Gets the HP34401A 2-Wire Resistance")
    FourWireResistance      = property(__Get4wireResistance__,   None, None, "Gets the HP34401A 4-Wire Resistance")
    CheckContinuity = property(__CheckContinuity__, None, None, "Checks for HP34401A Continuity")