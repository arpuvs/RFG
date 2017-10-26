# Author: Jeff Ugalde

# Purpose: This module is a generic GPIB wrapper for:
# HP661XC Power Supply
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class HP661XC(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'HP661XC', addr)
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
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
   