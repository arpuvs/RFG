# Author: Tom MacLeod
# Rev History --------------------
# Date: 07/18/2008
# Created!
# Purpose: This module is a generic GPIB wrapper for:
# ROHDE & SCHWARZ SMIQ Generators
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

MHz = 1.0e6

class SMIQ(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.025):
        GPIBObjectBaseClass.__init__(self, 'ROHDE&SCHWARZ,SMIQ', addr)
        self.__delay__ = delay
        
    def __SetFrequency__(self, Frequency):
        '''This function sets the SMIQ frequency'''
        self.instr.write( 'FREQ %fMHz' % (Frequency / MHz) )
        time.sleep(self.__delay__)
    
    def __SetLevel__(self, Level):
        '''This function sets the SMIQ frequency in dBm'''
        self.instr.write( 'POW %fdBm' % (Level) )
        time.sleep(self.__delay__)

    def __GetLevel__(self):
        '''This function gets the SMIQ level'''
        # This is untested code, so I don't want it to break if it fails
        try:
            val = float( self.instr.ask('POW?') )
        except:
            val = -999
            
        return val

    def __SetEnable__(self, Enabled):
        '''This function enables the RF On/Off for the SMIQ'''
        if Enabled:
            self.instr.write('OUTP:STAT ON')
        else:
            self.instr.write('OUTP:STAT OFF')
        time.sleep(self.__delay__)
        
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    Frequency = property(None,         __SetFrequency__, None, "Sets the SMIQ Frequency")
    Level     = property(__GetLevel__, __SetLevel__,     None, "Sets the SMIQ Level")
    Enabled   = property(None,         __SetEnable__,    None, "Sets the SMIQ RF On/Off")
    
    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")
