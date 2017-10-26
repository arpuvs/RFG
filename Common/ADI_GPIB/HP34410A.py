# Author: Tom MacLeod
# Date: 12/18/2006
# Added: 'Current' property
# ---------------------------------------------------------------------
# Date: 10/27/2006
# Purpose: This module is a generic GPIB wrapper for:
# HP34401A Voltmeter
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass

class HP34410A(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        GPIBObjectBaseClass.__init__(self, 'Agilent Technologies,34410A', addr)
    
    def __GetVoltage__(self):
        '''This function gets the HP34401A Voltage'''
        return float(self.instr.ask('MEAS:VOLT:DC?'))

    def __GetCurrent__(self):
        '''This function gets the HP34401A Current'''
        return float(self.instr.ask('MEAS:CURR:DC?'))

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
    CheckContinuity = property(__CheckContinuity__, None, None, "Checks for HP34401A Continuity")
    
if __name__ == '__main__':
    ps = HP34410A(22)
    
    print ps.Voltage