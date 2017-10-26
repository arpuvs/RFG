# Author: Tom MacLeod / Tony Del Muro
# Date: 03/08/2007
# Version: 0.1 Beta!
# Purpose: This module is a generic GPIB wrapper for:
# Agilent / HP 8112A 50MHz Programmable Pulse Generator
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time
import string

class HP8112A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'HEWLETT-PACKARD,HP8112A', addr)
        self.__delay__ = delay
        
        #Trigger modes
        #NORM  = 'M1'
        #TRIG  = 'M2'
        #GATE  = 'M3'
        #E.WID = 'M4'
        #E.BUR = 'M5'
        self._M = 'M3'
        
        #Trigger control select
        #Trigger off            = 'T0'
        #Positive trigger slope = 'T1'
        #Negative trigger slope = 'T2'
        #Both edges             = 'T3'
        self._T = 'T1'
        
        #Timing parameters
        self._Period    = 10 #msec
        self._DutyCycle = 10 #percent
        
        #Level parameters
        self._HIL = 3 #voltz
        self._LOL = 0 #voltz
        
        #Output mode
        #comp output off = 'C0'
        #comp output on  = 'C1'
        #enable output   = 'D0'
        #disable output  = 'D1'
        self._CompOutputs = 'C0'
        self._Enabled     = 'D1'
        
        __SetTriggerMode__()
        __SetTimingParams__()
        __SetLevelParams__()
        __SetOutputMode__()
            
    def __SetPeriod__(self, val):
        '''This function sets the period'''
        self._Period = val
        __SetTimingParams__()
    
    def __SetDutyCycle__(self, val):
        '''This function sets the duty cycle'''
        self._DutyCycle = val
        __SetTimingParams__()
    
    def __SetHighLevel__(self, val):
        '''This function sets the high voltage level'''
        self._HIL = val
        __SetLevelParams__()
    
    def __SetLowLevel__(self, val):
        '''This function sets the low voltage level'''
        self._LOL = val
        __SetLevelParams__()
                        
    def __SetCompOutputs__(self, val):
        '''This function sets the outputs to be complemented or not'''
        if (val):
            self._CompOutputs = 'C0'
        else:
            self._CompOutputs = 'C1'
            
        __SetOutputMode__()
    
    def __SetEnabled__(self, val):
        '''This function sets the output enable'''
        if (val):
            self._Enabled = 'D0'
        else:
            self._Enabled = 'D1'
                
        __SetOutputMode__()
                        
    def __SetTriggerMode__(self):
        '''This function sets the trigger mode'''
        self.instr.write( self._M + ',' + self._T )
        time.sleep(self.__delay__)
    
    def __SetTimingParams__(self):
        '''This function sets the timing parameters'''
        self.instr.write( 'PER ' + str( self._Period ) + ' MS,DTY' + str( self._DutyCycle ) + ' %' )
        time.sleep(self.__delay__)
        
    def __SetLevelParams__(self):
        '''This function sets the level parameters'''
        self.instr.write( 'HIL ' + str( self._HIL ) + ' V,LOL' + str( self._LOL ) + ' V' )
        time.sleep(self.__delay__)
        
    def __SetOutputMode__(self):
        '''This function sets the output controls'''
        self.instr.write( self._CompOutputs + ',' + self._Enabled )
        time.sleep(self.__delay__)
            
    Period    = property(None, __SetPeriod__,    None, "Sets the 8112A Period (in msec)")
    DutyCycle = property(None, __SetDutyCycle__, None, "Sets the 8112A Duty Cycle (in percent)")
    LevelHigh = property(None, __SetHighLevel__, None, "Sets the 8112A high voltage level")
    LevelLow  = property(None, __SetLowLevel__,  None, "Sets the 8112A low voltage level")
    CompOutputs = property(None, __SetCompOutputs__, None, "Sets the 8112A complementary outputness")
    Enabled     = property(None, __SetEnabled__,     None, "Sets the 8112A output enabledness")
    
#This code is used to debug this module
if __name__ == '__main__':
    PG = HP8112A(12)
    
    PG.Period = 20
    PG.DutyCycle = 20
    PG.LevelHigh = 2.2
    PG.LevelLow = 0.1
    PG.CompOutputs = False
    PG.Enabled = True
    
    time.sleep(1)
    
    PG.Enabled = False
    
    print "Done!"