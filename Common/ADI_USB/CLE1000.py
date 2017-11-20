'''
Created on May 13, 2016

Purpose:     control Artek cle1000 ISI box

@author: lweida


'''
# --------------------------------------------------------------------------

# from ADI_USB.USBObject import USBObjectBaseClass as USBObjectBaseClass

from serial import Serial
from numpy import clip
import gc, time


# legacy information :
# The this  was splitted into the inner class that instantiates the object
# and an outer class which calls the instantiation for every function executed
# because of the the lock problem on the Virtual GPIB line (emulated by USB)
# where a different process would hold on to the USB GPIB and not be able to
# make simultaneous connection.

class CLE1000(object):
    class CLE1000(object):
        def __init__(self, addr):
            # USBObjectBaseClass.__init__(self, 'Variable ISI Channel', addr)
            #self.instr = Serial('COM5', 9600, timeout=10)
             self.instr = Serial('COM4', 9600, timeout=10)
            # self.instr = Serial('COM4', 115200, timeout=10)

    def __init__(self, addr=None, delay=0.2):
        self.__addr__ = addr
        self.__delay__ = delay

    def __CreateInstrumentObject__(self):
        instance = CLE1000.CLE1000(self.__addr__)
        # Set to Remove Mode
        instance.instr.write('SYST:REM\n')
        return instance

    def __setISILevel__(self, PC_level):
        '''This function sets the CLE1000 output level from 0 to 100 percent'''
        instance = self.__CreateInstrumentObject__()
        # print 'OUTP:ISI:LEVEl ' + str(PC_level)
        time.sleep(.5)
        instance.instr.write('OUTP:ISI:LEVEl ' + str(PC_level) + "\n")

        #         print float(instance.instr.ask('OUTP:ISI:LEVEl?\n'))
        #         value = float(instance.instr.ask('OUTP:ISI:LEVEl?\n'))

        time.sleep(self.__delay__)
        del instance
        gc.collect()

    def __Set_ISI_on__(self, ON):
        '''This function sets on or off the CLE1000 ISI output'''
        instance = self.__CreateInstrumentObject__()
        if ON:
            instance.instr.write('OUTP:ISI:STAT ON\n')
        elif ON == 0:
            instance.instr.write('OUTP:ISI:STAT OFF\n')
        time.sleep(self.__delay__)
        del instance
        gc.collect()

# ===============================================================================
#     def __GetV1Setting__(self):
#         '''This function gets the Keithley2230 PS1 Voltage Setting'''
#         instance = self.__CreateInstrumentObject__()
#         instance.instr.write('INST:NSEL 1')
#         value = float(instance.instr.ask('VOLT?'))
#         del instance
#         gc.collect()
#         return value
#
#     def __GetV1__(self):
#         '''This function gets the Keithley2230 PS1 Voltage'''
#         instance = self.__CreateInstrumentObject__()
#         instance.instr.write('INST:NSEL 1')
#         value = float(instance.instr.ask('MEAS:VOLT?'))
#         del instance
#         gc.collect()
#         return value
#
#     def __SetV1__(self, PS1):
#         '''This function sets the Keithley2230 PS1 Voltage'''
#         PS1 = clip(PS1, 0, 30)
#         instance = self.__CreateInstrumentObject__()
#         instance.instr.write('INST:NSEL 1')
#         instance.instr.write('VOLT ' + str(PS1))
#         time.sleep(self.__delay__)
#         del instance
#         gc.collect()
# ===============================================================================



# ===============================================================================
#
#     V1Set  = property(__GetV1Setting__, None, None, "Gets the Keithley2230 PS1 Voltage Setting")
#     V2Set  = property(__GetV2Setting__, None, None, "Gets the Keithley2230 PS2 Voltage Setting")
#     V3Set  = property(__GetV3Setting__, None, None, "Gets the Keithley2230 PS3 Voltage Setting")
#
#     V1 = property(__GetV1__, __SetV1__, None, "Gets/Sets the Keithley2230 PS1 Voltage")
#     V2 = property(__GetV2__, __SetV2__, None, "Gets/Sets the Keithley2230 PS2 Voltage")
#     V3 = property(__GetV3__, __SetV3__, None, "Gets/Sets the Keithley2230 PS3 Voltage")
#
#     I1 = property(__GetI1__,  __SetI1__, None, "Gets/Sets the Keithley2230 PS1 Current")
#     I2 = property(__GetI2__,  __SetI2__, None, "Gets/Sets the Keithley2230 PS2 Current")
#     I3 = property(__GetI3__,  __SetI3__, None, "Gets/Sets the Keithley2230 PS3 Current")
#
#     Enabled = property(__GetEnable__, __SetEnable__, None, "Sets the Keithley2230 On/Off")
#
#     Delay = property(__GetDelay__, __SetDelay__, None, "Delay")
#
# if __name__ == '__main__':
#     supply = Keithley2230()
#     for enabled in [ False, True]:
#         supply.Enabled = enabled
#         print "EN:", supply.Enabled
#         #supply.V1 = 2
#         print "V1:", supply.V1, "I1:", supply.I1, "V1_Set:", supply.V1Set
#         #supply.V2 = 1
#         print "V2:", supply.V2, "I2:", supply.I2, "V2_Set:", supply.V2Set
#         #supply.V3 = 0
#         print "V3:", supply.V3, "I3:", supply.I3, "V3_Set:", supply.V3Set
#     supply.Enabled = False
#     print "EN:", supply.Enabled
# ===============================================================================
