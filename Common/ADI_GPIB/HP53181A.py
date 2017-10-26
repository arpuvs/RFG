# Date: 1/3/2008
# Purpose: This module is a generic GPIB wrapper for:
# HP53181A Frequency Counter
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass

class HP53181A(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        GPIBObjectBaseClass.__init__(self, 'HEWLETT-PACKARD,53181A', addr)
    
    def __GetFreq__(self):
        '''This function gets the HP53181A Frequency on Configured Channel'''
        try:
            result = float(self.instr.ask('READ:FREQ?'))
        except:
            result = -1
        
        return result
    
    def ConfigureFreq(self, estimate=500e6, resolution=1e-3, chan=1):
        '''This function confiures the frequency measurement of the HP53181A Frequency specified chan.'''
        self.instr.write('CONF:FREQ %e,%e,(@%d)' % (estimate, resolution, chan))

    def __GetRatio__(self):
        '''This function gets the HP53181A Frequency on Configured Channel'''
        try:
            result = float(self.instr.ask('READ:FREQ:RATIO?'))
        except:
            result = -1
        
        return result
    
        
    def ConfigureRatio(self, estimate=1, resolution=1e-6, chan=1):
        '''This function confiures the frequency measurement of the HP53181A Frequency specified chan.'''
        if chan == 1:
            self.instr.write('CONF:FREQ:RATIO %e,%e,(@1),(@2)' % (estimate, resolution))    
        elif chan == 2:
            self.instr.write('CONF:FREQ:RATIO %e,%e,(@2),(@1)' % (estimate, resolution))
        
    Freq         = property(__GetFreq__,      None, None, "Gets the HP53181A Frequency Measurement for Configured Channel")
    Frequency    = property(__GetFreq__,      None, None, "Gets the HP53181A Frequency Measurement for Configured Channel")
    Ratio        = property(__GetRatio__,      None, None, "Gets the HP53181A Ratio Measurement for Configured Channel")