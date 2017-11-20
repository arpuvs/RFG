#-----------------------------------------------------------------------------
# Name:        Keithley2230.py
# Purpose:     Device Interface Wrapper for Keithley 2230-30-1
#              Triple Channel DC Power Supply
#
# Author:      Kaushal Shrestha
#
# Created:     2013/05/22
# RCS-ID:      $Id: Keithley2230.py 471 2014-04-22 23:57:40Z kshresth $
# Copyright:   (c) 2013
# Licence:     Analog Devices Inc.
#-----------------------------------------------------------------------------

from ADI_USB.USBObject import USBObjectBaseClass as USBObjectBaseClass
from numpy import clip
import gc, time

# The Keithley 2230 was splitted into the inner class that instantiates the object
# and an outer class which calls the instantiation for every function executed
# because of the the lock problem on the Virtual GPIB line (emulated by USB)
# where a different process would hold on to the USB GPIB and not be able to
# make simultaneous connection.
class Keithley2230(object):
    class Keithley2230(USBObjectBaseClass):
        def __init__(self, addr):
            USBObjectBaseClass.__init__(self, 'Keithley instruments, 2230-30-1', addr)

    def __init__(self, addr = None, delay=0.1):
        self.__addr__  = addr
        self.__delay__ = delay

    def __CreateInstrumentObject__(self):
        instance = Keithley2230.Keithley2230(self.__addr__)
        #Set to Remove Mode
        instance.instr.write('SYST:REM')
        return instance

    def __GetV1Setting__(self):
        '''This function gets the Keithley2230 PS1 Voltage Setting'''
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 1')
        value = float(instance.instr.ask('VOLT?'))
        del instance
        gc.collect()
        return value

    def __GetV1__(self):
        '''This function gets the Keithley2230 PS1 Voltage'''
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 1')
        value = float(instance.instr.ask('MEAS:VOLT?'))
        del instance
        gc.collect()
        return value

    def __SetV1__(self, PS1):
        '''This function sets the Keithley2230 PS1 Voltage'''
        PS1 = clip(PS1, 0, 30)
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 1')
        instance.instr.write('VOLT ' + str(PS1))
        time.sleep(self.__delay__)
        del instance
        gc.collect()

    def __GetV2Setting__(self):
        '''This function gets the Keithley2230 PS1 Voltage Setting'''
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 2')
        value = float(instance.instr.ask('VOLT?'))
        del instance
        gc.collect()
        return value

    def __GetV2__(self):
        '''This function gets the Keithley2230 PS2 Voltage'''
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 2')
        value = float(instance.instr.ask('MEAS:VOLT?'))
        del instance
        gc.collect()
        return value

    def __SetV2__(self, PS2):
        '''This function sets the Keithley2230 PS2 Voltage'''
        PS2 = clip(PS2, 0, 30)
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 2')
        instance.instr.write('VOLT ' + str(PS2))
        time.sleep(self.__delay__)
        del instance
        gc.collect()

    def __GetV3Setting__(self):
        '''This function gets the Keithley2230 PS1 Voltage Setting'''
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 3')
        value = float(instance.instr.ask('VOLT?'))
        del instance
        gc.collect()
        return value

    def __GetV3__(self):
        '''This function gets the Keithley2230 PS3 Voltage'''
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 3')
        value = float(instance.instr.ask('MEAS:VOLT?'))
        del instance
        gc.collect()
        return value

    def __SetV3__(self, PS3):
        '''This function sets the Keithley2230 PS3 Voltage'''
        PS3 = clip(PS3, 0, 6)
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 3')
        instance.instr.write('VOLT ' + str(PS3))
        time.sleep(self.__delay__)
        del instance
        gc.collect()

    def __GetI1__(self):
        '''This function gets the Keithley2230 PS1 Current'''
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 1')
        value = float(instance.instr.ask('MEAS:CURR?'))
        del instance
        gc.collect()
        return value

    def __SetI1__(self, current):
        '''This function sets the Keithley2230 PS1 Current'''
        current = clip(current, 0, 20)
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 1')
        instance.instr.write('CURR ' + str(current))
        time.sleep(self.__delay__)
        del instance
        gc.collect()

    def __GetI2__(self):
        '''This function gets the Keithley2230 PS2 Current'''
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 2')
        value = float(instance.instr.ask('MEAS:CURR?'))
        del instance
        gc.collect()
        return value

    def __SetI2__(self, current):
        '''This function sets the Keithley2230 PS1 Current'''
        current = clip(current, 0, 20)
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 2')
        instance.instr.write('CURR ' + str(current))
        time.sleep(self.__delay__)
        del instance
        gc.collect()

    def __GetI3__(self):
        '''This function gets the Keithley2230 PS2 Current'''
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 3')
        value = float(instance.instr.ask('MEAS:CURR?').lower())
        del instance
        gc.collect()
        return value

    def __SetI3__(self, current):
        '''This function sets the Keithley2230 PS3 Current'''
        current = clip(current, 0, 20)
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('INST:NSEL 3')
        instance.instr.write('CURR ' + str(current))
        time.sleep(self.__delay__)
        del instance
        gc.collect()

    def __SetEnable__(self, Enabled):
        '''This function enables the On/Off for the Keithley2230'''
        instance = self.__CreateInstrumentObject__()
        if Enabled:
            instance.instr.write('OUTP ON')
        else:
            instance.instr.write('OUTP OFF')
        del instance
        gc.collect()

    def __GetEnable__(self):
        '''This function returns the On/Off state for the Keithley2230'''
        instance = self.__CreateInstrumentObject__()
        status = instance.instr.ask('OUTP?')
        del instance
        gc.collect()
        if (status == "1" or status == "ON" ):
            return True
        return False

    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d

    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__

    def Clear(self):
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('*CLS')
        del instance
        gc.collect()

    def Reset(self):
        instance = self.__CreateInstrumentObject__()
        instance.instr.write('*RST')
        del instance
        gc.collect()
    
    V1Set  = property(__GetV1Setting__, None, None, "Gets the Keithley2230 PS1 Voltage Setting")
    V2Set  = property(__GetV2Setting__, None, None, "Gets the Keithley2230 PS2 Voltage Setting")
    V3Set  = property(__GetV3Setting__, None, None, "Gets the Keithley2230 PS3 Voltage Setting")

    V1 = property(__GetV1__, __SetV1__, None, "Gets/Sets the Keithley2230 PS1 Voltage")
    V2 = property(__GetV2__, __SetV2__, None, "Gets/Sets the Keithley2230 PS2 Voltage")
    V3 = property(__GetV3__, __SetV3__, None, "Gets/Sets the Keithley2230 PS3 Voltage")

    I1 = property(__GetI1__,  __SetI1__, None, "Gets/Sets the Keithley2230 PS1 Current")
    I2 = property(__GetI2__,  __SetI2__, None, "Gets/Sets the Keithley2230 PS2 Current")
    I3 = property(__GetI3__,  __SetI3__, None, "Gets/Sets the Keithley2230 PS3 Current")

    Enabled = property(__GetEnable__, __SetEnable__, None, "Sets the Keithley2230 On/Off")

    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")

if __name__ == '__main__':
    supply = Keithley2230()
    for enabled in [ False, True]:
        supply.Enabled = enabled
        print "EN:", supply.Enabled
        #supply.V1 = 2
        print "V1:", supply.V1, "I1:", supply.I1, "V1_Set:", supply.V1Set
        #supply.V2 = 1
        print "V2:", supply.V2, "I2:", supply.I2, "V2_Set:", supply.V2Set
        #supply.V3 = 0
        print "V3:", supply.V3, "I3:", supply.I3, "V3_Set:", supply.V3Set
    supply.Enabled = False
    print "EN:", supply.Enabled
