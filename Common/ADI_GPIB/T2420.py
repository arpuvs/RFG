# Author: Tom MacLeod
# Date: 07/17/2007
# Status: Beta!
# Purpose: This module is a generic GPIB wrapper for:
# T-2420 Precision Temperature Forcing System
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

# I can't seem to find how to set the air flow via GPIB
#AF_MAX = 450
#AF_MIN = 25

class T2420(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=30):
        GPIBObjectBaseClass.__init__(self, '', addr)
        #This code is to fix some odd bug in writing to the 
        #temp machine the first time
        self.__delay__   = 0.1
        #self.__airflow__ = AF_MIN
        self.__SetTemp__(25)
        
        #Continue with normal operation        
        self.__delay__   = delay
        #self.__airflow__ = AF_MAX
                
    def MoveArmUp(self):
        '''This function moves the T2420 arm up'''
        self.instr.write('HU')
        time.sleep(4)
    
    def MoveArmDown(self):
        '''This function moves the T2420 arm down'''
        self.instr.write('HD')
        time.sleep(4)
    
    #def SetIdleMode(self):
    #    '''This function puts the TurboJet into idle mode'''
    #   self.instr.write('ID')
        
    def __SetTemp__(self, Temp):
        '''This function sets the T2420 temperature'''
        
        # Temperature sensing mode
        #self.instr.write('FX')  # fixture-sense mode
        self.instr.write('DS')  # DUT single-loop
        #self.instr.write('DD')  # DUT dual-loop
        time.sleep(0.1)
        
        # Determine the temperature of the air and set
        # the appropriate mode
        if Temp == 25:
            self.instr.write('AF')
        elif Temp > 25:
            self.instr.write('AH')
            self.instr.write('TH' + str(Temp))
        else:
            self.instr.write('AC')
            self.instr.write('TC' + str(Temp))
        
        # Wait    
        time.sleep(self.__delay__)
                
    #def __SetAirFlow__(self, AirFlow):
    #    '''This function sets the TurboJet airflow'''
    #    self.__airflow__ = AirFlow
    #    self.instr.write('AF' + str(self.__airflow__))
    #    time.sleep(0.1)
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    Temp    = property(None,         __SetTemp__,     None, "Sets the T2420 temperature")
    #AirFlow = property(None,         __SetAirFlow__,  None, "Sets the T2420 airflow")
    Delay   = property(__GetDelay__, __SetDelay__,    None, "Delay")
    
    
    
if __name__ == '__main__':
    
    temp_machine = T2420(5)
    
    temp_machine.Delay = 10
    
    temp_machine.MoveArmDown()
    
    temp_machine.Temp = 30
    
    temp_machine.Temp = 25
    
    temp_machine.MoveArmUp()
    
    