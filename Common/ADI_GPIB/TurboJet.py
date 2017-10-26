# Author: Tom MacLeod
# Data: 12/10/2007
# Status: Removed the default AirFlow setvalue
# ----------------------------------------------------------------
# Author: Tom MacLeod
# Date: 11/11/2006
# Status: Added arm control functions and idlemode control
# ----------------------------------------------------------------
# Date: 11/09/2006
# Status: Debugged!
# Purpose: This module is a generic GPIB wrapper for:
# TurboJet
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time

AF_MAX = 15
AF_MED = 10
AF_MIN = 5

class TurboJet(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=30):
        GPIBObjectBaseClass.__init__(self, '', addr)
        #This code is to fix some odd bug in writing to the 
        #temp machine the first time
        self.__delay__ = 0.1
        self.__SetTemp__(25)
        self.__SetTemp__(25)
        
        #Continue with normal operation        
        self.__delay__   = delay
        
        
    def MoveArmUp(self):
        '''This function moves the TurboJet arm up'''
        self.instr.write('AU')
        time.sleep(4)
    
    def MoveArmDown(self):
        '''This function moves the TurboJet arm down'''
        self.instr.write('AD')
        time.sleep(4)
    
    def MoveArmIn(self):
        '''This function moves the TurboJet arm in'''
        self.instr.write('AI')
        time.sleep(4)
    
    def MoveArmOut(self):
        '''This function moves the TurboJet arm out'''
        self.instr.write('AO')
        time.sleep(4)
    
    def SetIdleMode(self):
        '''This function puts the TurboJet into idle mode'''
        self.instr.write('ID')
        
    def __SetTemp__(self, Temp):
        '''This function sets the TurboJet temperature'''
        
        Temp = clip(Temp, -60, 120)
        #self.instr.write('WI,10')
        #time.sleep(0.1)
        self.instr.write('RM')
        time.sleep(0.1)
        self.instr.write('SP,' + str(Temp))
        time.sleep(self.__delay__)
    
    def __SetAirFlow__(self, AirFlow):
        '''This function sets the TurboJet airflow'''
        self.__airflow__ = AirFlow
        self.instr.write('AF' + str(self.__airflow__))
        time.sleep(0.1)
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    Temp    = property(None,         __SetTemp__,     None, "Sets the TurboJet temperature")
    AirFlow = property(None,         __SetAirFlow__,  None, "Sets the TurboJet airflow")
    Delay   = property(__GetDelay__, __SetDelay__,    None, "Delay")