# Author: Leah Magaldi
# ---------------------------------------------------------------------
# Date: 01/24/2016
# Purpose: This module is a generic GPIB wrapper for:
# Keithley 2400 SMU
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass

import time

class Keithley2400SMU(GPIBObjectBaseClass):
    ###################################################################################################################

    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, '2400', addr)
        self.__delay__ = delay
        self.Reset()
     ###################################################################################################################

    def Reset(self):
        """Resets instrument to Power-Up default state"""
        self.instr.write('*RST;')
        self.instr.write('*CLS;')
    ###################################################################################################################

    def BeeperOff(self):
        """turn off the annoying beeping"""

        self.instr.write(':SYST:BEEP:STAT OFF;')
    ###################################################################################################################

    def DisplayState(self,state):
        """set the state of the display to on or off as it generates some noise on the output seen at low levels"""
        if state == 1:
            string='ON'
        else:
            string='OFF'
        self.instr.write(':DISP:ENAB %s' %state)
    ###################################################################################################################

    def OutputEnable(self,state):
        """set the state of the output to on or off"""
        if state == 1:
            string='ON'
        else:
            string='OFF'
        self.instr.write(':OUTPUT %s;' %string)
    ###################################################################################################################

    def SetVolt(self,level):
        """sets the voltage level to source"""
        self.instr.write(':SOURCE:VOLT %1.3f;' %level)
    ###################################################################################################################

    def SetCurrent(self,level):
        """sets the Current level to source"""
        self.instr.write(':SOURCE:Current %1.3f;' %level)
    ###################################################################################################################

    def SetOverVoltProt(self,levelovp):
        """sets the voltage compliance level to levelovp"""

        self.instr.write(':SENSE:VOLTAGE:PROTECTION %1.3f;' %levelovp)
    ###################################################################################################################

    def SetComplianceCurrent(self,compcurrent):
        """sets the current compliance level to compcurrent"""

        self.instr.write(':SENSE:CURR:PROT %1.3f;' %compcurrent)
    ###################################################################################################################

    def QueryCurrentCompliance(self):
        """Check if unit is in current compliance 1=yes, 0=no"""

        trip=self.instr.query(':SENS:CURR:PROT:TRIP?;')

        return trip
    ###################################################################################################################

    def MeasureCurrent(self):
        """Measure current when in voltage mode"""
        self.instr.write(':FORM:ELEM CURRENT;')
        current=self.instr.query(':MEASURE?;')

        return float(current)
    ###################################################################################################################

    def MeasureVoltage(self):
        """ Measure voltage when in current mode """
        self.instr.write(':FORM:ELEM VOLTAGE;')
        voltage=self.instr.query(':MEASURE?;')

        return float(voltage)
    ###################################################################################################################

    def DMMFunc_MeasureVoltage_ForceZeroCurrent(self):
        """put the unit into current mode, set voltage compliance to 2V, set output on and return voltage measurement """
        self.instr.write(':SOUR:FUNC curr;')
        self.instr.write(':SENSe:FUNC "VOLT"')
        self.instr.write(':SOUR:curr:LEV 0')
        self.instr.write(':FORM:ELEM volt')
        self.instr.write(':OUTP ON')

        voltage=self.instr.query(':READ?')

        return float(voltage)
    ###################################################################################################################

    def DMMFunc_MeasureCurrent_ForceZeroVoltage(self):
        """put the unit into current mode, set voltage compliance to 2V, set output on and return voltage measurement """
        self.instr.write(':SOUR:FUNC Volt;')
        self.instr.write(':SENS:FUNC "CURR"')
        self.instr.write(':SOUR:Volt:LEV 0')
        self.instr.write(':FORM:ELEM Curr')
        self.instr.write(':OUTP ON')
        current=self.instr.query(':READ?')

        return float(current)
    ###################################################################################################################

    def DMMFunc_MearsureResistance2Wire(self):
        """put the unit into current mode, set voltage compliance to 2V, set output on and return voltage measurement """
        self.instr.write(':FUNC "RES"')
        self.instr.write(':SENSe:RESistance:OCOMpensated OFF')
        self.instr.write(':SOURce:FUNCtion current')
        self.instr.write(':SYSTem:RSENse OFF')
        self.instr.write(':FORM:ELEM RES')

        self.instr.write(':OUTPut ON')
        resistance=self.instr.query(':READ?')

        return float(resistance)
    ###################################################################################################################

    def SelectFrontRearTerminals(self, location):
        """Select the front '1' default or the rear '0' terminal.  Useful when connecting to sensative circuit nodes """
        if location == 1:
            string='FRONT'
        else:
            string='REAR'
        self.instr.write(':ROUT:TERM %s;' %string)
    ###################################################################################################################

