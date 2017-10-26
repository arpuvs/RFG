# Author: Tom MacLeod
# Date: 10/22/2008
# Version: 0.1 Beta!
# Purpose: This module is a generic GPIB wrapper for:
# Any Generic device.  This helps a programmer issue commands without
# the need for work arounds.
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import string

class AgilentN5181A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'N5181A', addr)
        self.__delay__ = delay

    def __GetState__(self):
        self.instr.ask(':OUTP:STAT?')

    def __SetState__(self, Enable = True):
        if Enable:
            self.instr.write(':OUTP:STAT 1')
        elif not Enable:
            self.instr.write(":OUTP:STAT 0")
        else: print('Bad Value')

