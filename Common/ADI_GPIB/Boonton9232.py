# Author: Tom MacLeod and Ramya Ramachandran
# Date: 04/09/2008
# Purpose: This module is a generic GPIB wrapper for:
# Boonton 9232 Power Meter
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass

class Boonton9232(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        GPIBObjectBaseClass.__init__(self, 'Boonton,9232', addr)
        
        self.Measure_Volt()
        self.__channel = '1'
        
    def __GetChannel__(self):
        '''This function gets the current channel'''
        return int(self.__channel)
        
    def __SetChannel__(self, channel):
        '''This function sets the current channel'''
        self.__channel = str(channel)
                
    def __GetPower__(self):
        '''This function gets the Boonton 9232 Power'''
        self.instr.write('CH' + self.__channel)
        self.instr.write('TM0')
        return float(self.instr.ask('')[2:])
  
    def Measure_dB(self):
        '''This function sets the Boonton 9232's units of measurement to dB'''
        self.instr.write('DB')
        
    def Measure_Volt(self):
        '''This function sets the Boonton 9232's units of measurement to Volt'''
        self.instr.write('VOLT')
        

    Power = property(__GetPower__, None, None, "Gets the Boonton 9232 Power")
    Pow   = property(__GetPower__, None, None, "Gets the Boonton 9232 Power")
    
    Channel = property(__GetChannel__, __SetChannel__, None, "Gets/Sets the Boonton 9232 Channel")

# Test Code
if __name__ == '__main__':
    P = Boonton9232(13)
    print P.Power