# Author: Tom MacLeod & Rodney Kranz
# Date: 3/12/2008
# Purpose: This module is a generic GPIB wrapper for:
# KnL Filter, Digitally Controlled Tunable Filter
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class KnL_Filter(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.25):
        GPIBObjectBaseClass.__init__(self, '--Fill In--,D5TNF', addr)
        
        #Ask for the status of a bogus frequency, this will
        #return the current value
        response = self.instr.ask('S9999999')
        
        self.__addr__ = addr
        
        self.__freq__ = self.__str2freq__(response[1:])
        
        self.__delay__ = delay
        
    def __str2freq__(self, str):
        '''This function converts a string to a frequency (Hz)'''
        f = float(str) * 1000
        return f
    
    def __freq2str__(self, freq):
        '''This function converts a frequency (Hz) into a string'''
        s = str(int(freq / 1000.0))
        return s
    
    def __SetFreq__(self, freq):
        '''This function sets the frequency'''
        #Create GPIB Strings
        str_f = 'F' + self.__freq2str__(freq)
        str_s = 'S' + self.__freq2str__(freq) + '?'
        
        #Set frequency
        self.instr.write(str_f)
        
        #Poll until set
        response = self.instr.ask(str_s)
        
        #Assign new local frequency
        self.__freq__ = self.__str2freq__(response[1:])
        
        #Report an out-of-range message
        #if (self.__freq__ != freq):
        #print 'Old: %f, New: %f' % (freq, self.__freq__)
        if (abs(self.__freq__ - freq) > 1e5):
            print 'Warning: possible out-of-range value sent to KnL_Filter'
            print 'Address: %d, Frequency: %f' % (self.__addr__, freq)
                
        time.sleep(self.__delay__)
        
    def __GetFreq__(self):
        '''This function returns the current frequency'''
        return self.__freq__
        
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    Freq      = property(__GetFreq__, __SetFreq__, None, "Selects the Frequency")
    Frequency = property(__GetFreq__, __SetFreq__, None, "Selects the Frequency")
    
    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")
  
