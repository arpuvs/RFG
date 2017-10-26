# Author: Kaushal Shrestha
# Data: 10/22/2010
# Status: Used TurboJet module to start off AirJetXE75

# ENSURE AIR FLOW CONTROL IS SET TO 2 CFM

from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time

class AirJetXE75(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=30):
        GPIBObjectBaseClass.__init__(self, '', addr)
        #This code is to fix some odd bug in writing to the 
        #temp machine the first time
        self.__delay__ = 0.1
        self.__SetTemp__(25)
        self.__SetTemp__(25)
        
        #Continue with normal operation        
        self.__delay__   = delay        
        
    def SetIdleMode(self):
        '''This function puts the AirJetXE75 into idle mode'''
        self.instr.write('ID')
    
    def __GetTemp__ ( self ) :
        '''This function returns the AirJetXE75 temperature'''
        return self.instr.ask( '?TA' )
        
    def __SetTemp__(self, Temp):
        '''This function sets the AirJetXE75 temperature'''        
        Temp = clip(Temp, -100, 200)  # I edited the fixed temps of -60 & 100 - Darren
        #self.instr.write('WI,10')
        #time.sleep(0.1)
        self.instr.write('RM')
        time.sleep(0.1)
        self.instr.write('SP,' + str(Temp))
        time.sleep(self.__delay__)
    
    def __SetAirFlow__(self, AirFlow):
        '''This function sets the AirJetXE75 airflow'''
        self.__airflow__ = AirFlow
        self.instr.write('AF' + str(self.__airflow__))
        time.sleep(0.1)
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    Temp    = property(__GetTemp__,  __SetTemp__,     None, "Gets the AirJetXE75 Temperature")    
    Delay   = property(__GetDelay__, __SetDelay__,    None, "Delay")