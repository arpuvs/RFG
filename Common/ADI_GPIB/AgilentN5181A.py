from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import string

class AgilentN5181A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'N5181A', addr)
        self.__delay__ = delay

    def __GetState__(self):
        return self.instr.ask(':OUTP:STAT?')

    def __SetState__(self, Enable = True):
        if Enable:
            self.instr.write(':OUTP:STAT 1')
        elif not Enable:
            self.instr.write(":OUTP:STAT 0")
        else: print('Bad Value')

    def __GetFreq__(self):
        return self.instr.ask(':FREQ?')

    def __SetFreq__(self, freq):
        self.instr.write(':FREQ %g' % freq)

    def __GetAmp__(self):
        return self.instr.ask(':POW?')

    def __SetAmp__(self, amp_in_dBm):
        self.instr.write(':POW %g dBm' % amp_in_dBm)
