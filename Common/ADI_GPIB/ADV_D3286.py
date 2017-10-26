'''
Created on Sept 14, 2017

@author: bsulliv2
Status:   created for Advantest D3286 Error Detector

'''
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time


class ADV_D3286(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=30):
        GPIBObjectBaseClass.__init__(self, '', addr)
        self.instr.term_chars = '\n'

        self.__delay__ = 0.1

        # Continue with normal operation
        self.__delay__ = delay

    def __AutoSearch__(self):
        self.instr.write("SRHGO")
        time.sleep(0.1)

    def __InputPolarity__(self, inverted=False):
        if inverted:
            self.instr.write('MPN')
        else: self.instr.write('MPI')

    def __PatternMode__(self, pattern='PRBS'):
        if pattern.lower() == 'prbs':
            self.instr.write('PRBS')
        elif pattern.lower() == 'word':
            self.instr.write('WORD')
        elif pattern.lower() == 'frame' | pattern.lower() == 'fram':
            self.instr.write('FRAM')
        else:
            return 'Not a valid pattern'
            print 'Not a valid pattern'

    def __PRBSLen__(self, length=7):
        options = (7, 9, 10, 11, 15, 23, 31)
        if length in options:
            self.instr.write('PB %s,0' % str(length))
        else:
            return 'Not a valid pattern'
            print 'Not a valid pattern'
