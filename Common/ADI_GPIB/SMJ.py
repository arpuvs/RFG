# Author: Tom MacLeod
# ################################
# --IMPORTANT USAGE TIPS--
# --To set the frequency, try either:--
#   obj = ADI_GPIB.SMJ(smj_addr)
#   obj.Frequency = 10e6    # <-sets channel 1's frequency
#   obj.Channel = 2         # <-changes the current channel
#   obj.Frequency = 20e6    # <-sets channel 2's frequency
#
#       --or--
#
#   obj = ADI_GPIB.SMJ(smj_addr)
#   obj.Frequency = (1, 10e6)  # <-sets channel 1's frequency
#   obj.Frequency = (2, 20e6)  # <-sets channel 2's frequency
#
#
# --To set the level, try either:--
#   obj = ADI_GPIB.SMJ(smj_addr)
#   obj.Level = -10     # <-sets channel 1's level
#   obj.Channel = 2     # <-changes the current channel
#   obj.Level = -20     # <-sets channel 2's level
#
#       --or--
#
#   obj = ADI_GPIB.SMJ(smj_addr)
#   obj.Level = (1, -10)  # <-sets channel 1's level
#   obj.Level = (2, -20)  # <-sets channel 2's level
#
# ################################
# Rev History --------------------
# Date: 08/08/2008
# Created: Debugged!
# --------------------------------
# Date: 07/30/2008
# Created (Not Debugged!)
# --------------------------------
# Purpose: This module is a generic GPIB wrapper for:
# ROHDE & SCHWARZ SMJ Generators
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import types

class SMJ(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.025):
        GPIBObjectBaseClass.__init__(self, 'ROHDE&SCHWARZ,SMJ', addr)
        
        self._ch = '1'
        
        self.__delay__ = delay
    
    def _gen_write_freq_str(self, Frequency):
        '''Generates the write frequency string'''
        try:
            if type(Frequency) == types.TupleType:
                ch = Frequency[0]
                if ch == 2:
                    self._ch = '2'
                else:
                    self._ch = '1'
                f  = str(Frequency[1])
            else:
                f = str(Frequency)
            
            return 'SOURCE%s:FREQ %s' % (self._ch, f)
        except:
            return ''
    
    def _gen_read_freq_str(self):
        '''Generates the write frequency string'''
        return 'SOURCE%s:FREQ?' % (self._ch)
        
    def _gen_write_level_str(self, Level):
        '''Generates the write level string'''
        try:
            if type(Level) == types.TupleType:
                ch = Level[0]
                if ch == 2:
                    self._ch = '2'
                else:
                    self._ch = '1'
                l  = str(Level[1])
            else:
                l = str(Level)
            
            return 'SOURCE%s:POW %s' % (self._ch, l)
        except:
            return ''
    
    def _gen_read_level_str(self):
        '''Generates the write frequency string'''
        return 'SOURCE%s:POW?' % (self._ch)
    
    def __SetFrequency__(self, Frequency):
        '''This function sets the SMJ frequency'''
        st = self._gen_write_freq_str(Frequency)
        if st:
            self.instr.write(st)
            time.sleep(self.__delay__)
        else:
            print 'Error: Invalid set frequency request'
            
    def __GetFrequency__(self):
        '''This function gets the SMJ frequency'''
        st = self._gen_read_freq_str()
        return self.instr.ask(st)
        
    def __SetChannel__(self, ch):
        '''This function sets the SMJ channel'''
        if ch == 1 or ch == 2:
            self._ch = str(ch)
        else:
            print 'Error: Invalid set channel request'

    def __GetChannel__(self):
        '''This function gets the SMJ channel'''
        return int(self._ch)
    
    def __SetLevel__(self, Level):
        '''This function sets the SMJ level'''
        st = self._gen_write_level_str(Level)
        if st:
            self.instr.write(st)
            time.sleep(self.__delay__)
        else:
            print 'Error: Invalid set level request'
            
    def __GetLevel__(self):
        '''This function gets the SMJ level'''
        st = self._gen_read_level_str()
        return self.instr.ask(st)
   
##    def __SetEnable__(self, Enabled):
##        '''This function enables the RF On/Off for the SMJ'''
##        if Enabled:
##            self.instr.write('L:RF:ON;')
##        else:
##            self.instr.write('L:RF:OFF;')
##        time.sleep(self.__delay__)
        
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    Frequency = property(__GetFrequency__, __SetFrequency__, None, "Gets/Sets the SMJ Frequency")
    Freq      = property(__GetFrequency__, __SetFrequency__, None, "Gets/Sets the SMJ Frequency")
        
    Level     = property(__GetLevel__, __SetLevel__,     None, "Gets/Sets the SMJ Level")
    
    Channel   = property(__GetChannel__, __SetChannel__, None, "Gets/Sets the SMJ Channel")
    Ch        = property(__GetChannel__, __SetChannel__, None, "Gets/Sets the SMJ Channel")
    
    #Enabled   = property(None, __SetEnable__,    None, "Sets the SMJ RF On/Off")
    
    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")
    
if __name__ == '__main__':
    obj = SMJ(22)
    
    #obj.Freq = 1.95e9
    #print obj.Freq
    
    obj.Level = -20
    print obj.Level
    
##    obj.Frequency = 10e6
##    obj.Channel = 2
##    
##    obj.Freq = 20e6
##    obj.Freq = (1, 10e6)
##    
##    obj.Level = (2, -1)
##    obj.Level = (1, -10)
##    
##    x = obj.Frequency
##    x = obj.Level
    