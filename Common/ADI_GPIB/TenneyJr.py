#-----------------------------------------------------------------------------
# Name:        TenneyJr.py
# Purpose:     Interface to automation of the TennyJr ETC Overn.
# Author:      Kaushal Shrestha
# Created:     2013/10/16
# RCS-ID:      $Id: TenneyJr.py 424 2014-03-13 00:31:00Z kshresth $
# Copyright:   (c) Analog Devices Inc, 2013
#-----------------------------------------------------------------------------
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import visa

class TenneyJr(GPIBObjectBaseClass):
    __BANK_CHAMBER__  = 100
    __BANK_SETPOINT__ = 300
    
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, '', addr)
        self.__delay__   = delay
    
    def __GetSetPoint__(self):
        '''This function gets the Tenney Jr. Set Point 1 temperature value'''
        command = 'R? %d, 1' % self.__BANK_SETPOINT__
        value = self.__Read__(command)
        return float(value)/10.0
        
    def __SetSetPoint__(self, Temp):
        '''This function sets the Tenney Jr. Set Point 1 temperature value'''
        command = 'W %d, %d' % (self.__BANK_SETPOINT__, int(round(10.0 * Temp)))
        self.__Write__(command)
    
    def __GetChamberTemp__(self):
        '''This function gets the Tenney Jr. actual chamber temperature'''
        command = 'R? %d, 1' % self.__BANK_CHAMBER__
        value = self.__Read__(command)
        return float(value)/10.0
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    def __Read__(self, command):
        value = 0
        try:
            value = self.instr.ask(command)
        except visa.VisaIOError, e:
            try:
                value = self.instr.ask(command)
            except visa.VisaIOError, e:
                try:
                    value = self.instr.ask(command)
                except visa.VisaIOError, e:
                    raise e
        return value
    
    def __Write__(self, command):
        self.instr.write(command)
        time.sleep(self.__delay__)

    Chamber  = property(__GetChamberTemp__, None,            None, "Gets the actural Tenney Jr. Chamber Temperature")
    SetPoint = property(__GetSetPoint__,    __SetSetPoint__, None, "Gets/Sets the Tenney Jr. Temperature SetPoint")
    Delay    = property(__GetDelay__,       __SetDelay__,    None, "Delay")
    
