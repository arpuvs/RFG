# Date: 2/21/17
# Author: Lloyd Weida
# Purpose: This module is a generic GPIB wrapper for:
# Agilent E8257D RF Signal Generator
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
from numpy import pi as Pi


class AgilentE8257D(GPIBObjectBaseClass):
    #
    AMODE_HIGH = 'HPOW'
    AMODE_NORM = 'NORM'
    AMODE_AUTO = 'AUTO'

    def __init__(self, addr=-1, delay=0.01):
        GPIBObjectBaseClass.__init__(self, 'AgilentE8257D', addr)
        self.__delay__ = delay

    def __SetFrequency__(self, Frequency): #expects Frequency in MHz
        '''This function sets the frequency'''
        freq = Frequency*1e6
        # freq = "%.10f" % (Frequency/1e6)
        self.instr.write('FREQ:CW %7.6f' % (freq))
        time.sleep(self.__delay__)

    def __GetFrequency__(self):
        '''This function gets the CW frequency'''
        return float(self.instr.ask('FREQ:CW?'))

    def __SetLevel__(self, Level):
        '''This function sets the  level in dbm'''
        self.instr.write('POW:AMPL %2.2f' % (Level))
        time.sleep(self.__delay__)

    def __GetLevel__(self):
        '''This function gets the power level in dB'''
        return float(self.instr.ask('POW:AMPL?'))

    def __SetOut_ON__(self):
        '''This function turns the output on'''
        self.instr.write('OUTP ON')
        time.sleep(self.__delay__)

    def __SetOut_OFF__(self):
        '''This function turns the output on'''
        self.instr.write('OUTP OFF')
        time.sleep(self.__delay__)

    def __Set_CW_mode__(self):
        '''This function gets the power level in dB'''
        self.instr.write(':FREQuency:MODE CW')

    def __Set_MOD_OFF_mode__(self):
        '''This function gets the power level in dB'''
        self.instr.write(':OUTP:MOD OFF')
