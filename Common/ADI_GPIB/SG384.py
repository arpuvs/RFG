# --------------------------------------------------
# Rev. History
# Author: Rodney Kranz
# Date: 02/27/2013
# Original Release
# --------------------------------------------------
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time, numpy
from numpy import pi as Pi

class SG384(GPIBObjectBaseClass):
    
    def __init__(self, addr=-1, delay=0.01):
        GPIBObjectBaseClass.__init__(self, 'Stanford Research Systems,SG384', addr)
        self.__delay__ = delay
        
    def __SetPhaseDeg__(self, PhaseDeg):
        '''This function sets the SG384 phase'''
        if (PhaseDeg < -360) or (PhaseDeg > 360):
            print 'Error in ADI_GPIB.SG384.__SetPhaseDeg__().  Phase requested exceeds +/-360.'
        else:
            current_phase = self.__GetPhaseDeg__()
            total_shift = PhaseDeg - current_phase
            if abs(total_shift) > 360: # step incrementally if the requested phase change exceeds 360.
                if total_shift >=0:
                    phase_list = numpy.arange(current_phase, PhaseDeg, 360)
                else:
                    phase_list = numpy.arange(current_phase, PhaseDeg, -360)
                if phase_list[len(phase_list)-1] <> PhaseDeg: # if the list does not contain the final value needed
                    phase_list = numpy.append(phase_list, PhaseDeg)
                phase_list = numpy.delete(phase_list, 0) # erase the first element
                for phase in phase_list:
                    self.instr.write( 'PHAS %s' % (str(phase)) )
                    time.sleep(self.__delay__)
            else:
                self.instr.write( 'PHAS %s' % (str(PhaseDeg)) )
                time.sleep(self.__delay__)
        
    def __GetPhaseDeg__(self):
        '''This function gets the SG384 phase'''
        phase = self.instr.ask( 'PHAS?' )
        return float( phase )
        
    def __SetFrequency__(self, Frequency):
        '''This function sets the SG384 frequency'''
        freq = "%.10f" % (Frequency/1e6)
        freq = freq.split('.')
        freq_1 = freq[0]
        freq_2 = freq[1][:8]
        self.instr.write( 'FREQ %s.%sMHz' % (freq_1, freq_2) )
        time.sleep(self.__delay__)
   
    def __GetFrequency__(self):
        '''This function gets the SG384 frequency'''
        freq = self.instr.ask( 'FREQ?' )
        return float( freq )
        
    def __SetLevel__(self, Level):
        '''This function sets the SG384 level'''
        self.instr.write( 'AMPR %s' % (str(Level)) )
        time.sleep(self.__delay__)
    
    def __GetLevel__(self):
        '''This function gets the SG384 level'''
        return float( self.instr.ask( 'AMPR?' ) )
            
    def __SetEnable__(self, Enabled):
        '''This function enables the RF On/Off for the SG384'''
        if Enabled:
            self.instr.write('ENBR 1')
        else:
            self.instr.write('ENBR 0')
        time.sleep(self.__delay__)
    
    def __GetEnable__(self):
        '''This function gets the RF On/Off status for the SG384'''
        return bool(int(self.instr.ask('ENBR?')))
        
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    Frequency = property(__GetFrequency__, __SetFrequency__, None, "Gets/Sets the SG384 Frequency")
    Level     = property(__GetLevel__, __SetLevel__, None, "Gets/Sets the SG384 Level")
    Enabled   = property(__GetEnable__, __SetEnable__,        None, "Gets/Sets the SG384 RF On/Off")
    PhaseDeg  = property(__GetPhaseDeg__, __SetPhaseDeg__, None, "Gets/Sets the SG384 Phase in Degrees")
    
    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")
    
