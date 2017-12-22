from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import string

class KeysightN5424A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'N6705B', addr)
        self.__delay__ = delay

        # VNA.__SetSweepType(1, 'LOG')#
        # VNA.__SetStartf__(1, 10e06)#
        # VNA.__SetStopf__(1, 10.01e09)#
        # VNA.__SetNumPoints__(1, 1e3)
        # VNA.__SetAvg__(1, 16)
        # VNA.__SetTime__(1, 1)
        # VNA.__SetTrigType__('MAN')
        # VNA.__SetContinuous__(1, False)
        # VNA.__EnableAvg(1, True)
        # VNA.__EnableTrigAvg__(True)

    def __CheckStatus__(self, maxWait):
        endtime = time.time() + maxWait
        while True:
            try:
                return self.instr.ask('*OPC?')
                break
            except:
                time.sleep(0.1)
                if time.time() > endtime:
                    raise Exception('Maximum wait time exceeded')

    def __SetSweepType__(self, trace, type):  # May be different for PXA - see [:SENSe]:SWEep:TYPE FFT|SWEep***
        self.instr.write(':SENS%d:SWE:TYPE %s' % (trace, type))

    def __SetStartf__(self, trace, freq):  # Same on PXA
        self.instr.write(':SENS%d:FREQ:STAR %g' % (trace, freq))

    def __SetStopf__(self, trace, freq):  # Same on PXA
        self.instr.write(":SENS%d:FREQ:STOP %g" % (trace, freq))

    def __SetNumPoints__(self, trace, pts):  # Same on PXA
        self.instr.write(":SENS%d:SWE:POIN %g" % (trace, pts))

    def __SetAvg__(self, trace, num):  # Same on PXA
        self.instr.write(":SENS%d:AVER:COUN %g" % (trace, num))

    def __SetAutoTime__(self, trace, enab):  # Same on PXA
        self.instr.write(":SENS%d:SWE:TIME:AUTO %d" % (trace, enab))

    def __SetTrigType__(self, typ):  # Same on PXA (I think?)
        self.instr.write(":TRIG:SOUR %s" % typ)

    def __SetContinuous__(self, trace, enab):  # Same on PXA
        if enab:
            self.instr.write(":INIT%d:CONT ON" % trace)
        else:
            self.instr.write(":INIT%d:CONT OFF" % trace)

    def __EnableAvg__(self, trace, enab):  # Same on PXA
        if enab:
            self.instr.write(":SENS%d:AVER ON" % trace)
        else:
            self.instr.write(":SENS%d:AVER OFF" % trace)

    def __EnableTrigAvg__(self, enab):  # Can't find on PXA***
        if enab:
            self.instr.write(":TRIG:AVER ON")
        else:
            self.instr.write(":TRIG:AVER OFF")

    def __SetActiveTrace__(self, channel, trace):  # Can't find on PXA***
        # self.instr.write(":CALC%d:PAR%d:SEL" % (channel, trace))
        # self.instr.write("CALC:PAR:SEL \'CH1_S11_1\'")
        self.instr.write('CALC%d:PAR:SEL \'%s\'' % (channel, trace))

    def __SetBBalParam__(self, channel, trace, param):  # Can't find on PXA***
        # self.instr.write(":CALC%d:FSIM:BAL:PAR%d:BBAL %s" % (channel, trace, param))
        self.instr.write(":CALC%d:FSIM:BAL:PAR:BBAL %s" % (channel, param))

    def __SetActiveFormat__(self, channel, format):  # Can't find on PSA: see CALCulate:EVM:MARKer[1]|2|...|12:CFORmat RECTangular|POLar***
        self.instr.write(":CALC%d:FORM %s" % (channel, format))

    def __InitMeas__(self, channel):  # Same on PXA
        self.instr.write('INIT%d' % channel)

    def __SingleTrig__(self):   # Can't find on PXA***
        self.instr.write(':TRIG:SING')

    def __SetTopology__(self, channel, topology):
        # Options = BBAL, BALS, SBAL, SSBAL
        self.instr.write(':CALC%d:FSIM:BAL:DEV %s' % (channel, topology))

    def __SetPorts__(self, channel, p1Pos, p1Neg, p2Pos, p2Neg):
        self.instr.write(':CALC%d:FSIM:BAL:TOP:BBAL %d,%d,%d,%d' % (channel, p1Pos, p1Neg, p2Pos, p2Neg))

    def __EnableBal__(self, channel):
        self.instr.write('CALC%d:FSIM:BAL:PAR:STAT 1' % channel)

    def __GetFreq__(self, channel):
        return self.instr.ask('CALC%d:X?' % channel)

    def __LoadState__(self, fname='default.csa'):
        self.instr.write('MMEM:LOAD \"%s\"' % fname)

    def __AddWindow__(self, window):
        self.instr.write('DISP:WIND%d ON' % window)

    def __AddMeas__(self, channel, name, meastype, subtype):
        # meastypes: S11,S21..., Gain Compression, Gain Compression Converters, Noise Figure Cold Source,
        # Noise Figure Converters, Swept IMD, Swept IMD Converters, IM Spectrum, IMx Specrtrum Converters,
        # Differential I/Q
        self.instr.write('CALC%d:CUST:DEF \'%s\', \'%s\', \'%s\'' % (channel, name, meastype, subtype))

    def __AddTrace__(self, window, trace, name):
        self.instr.write('DISP:WIND%d:TRAC%d:FEED \'%s\'' % (window, trace, name))

    def __RemoveTrace__(self, window, trace):
        self.instr.write('DISP:WIND%d:TRAC%d:DEL' % (window, trace))

    def __IMDDelta__(self, channel, spacing):
        self.instr.write('SENS%d:IMD:FREQDFR %g' % (channel, spacing))

    def __IMDStart__(self, channel, frequency):
        self.instr.write('SENS%d:IMD:FREQ:FCEN:STAR %g' % (channel, frequency))

    def __IMDStop__(self, channel, frequency):
        self.instr.write('SENS%d:IMD:FREQ:FCEN:STOP %g' % (channel, frequency))

    def __IMDPower__(self, window, level):
        self.instr.write('SENS%d:IMD:TPOW:F1 %d' % (window, level))
        self.instr.write('SENS%d:IMD:TPOW:F2 %d' % (window, level))

    def __IMDPowType__(self, window, type):
        # Could use input or output
        self.instr.write('SENS%d:IMD:TPOW:LEV %s' % (window, type))

    def __Preset__(self, type = 'partial'):
        if type.lower() == 'full':
            self.instr.write('SYST:FPR')
        else:
            self.instr.write('SYST:PRES')

    def __SetAttenuation__(self, level):
        self.instr.write('SENS:POW:ATT AREC,%d' % level)
        self.instr.write('SENS:POW:ATT BREC,%d' % level)

    def __RecallCal__(self, filename):
        self.instr.write('SENS:CORR:CSET:ACT \"%s\", 1' % filename)

    def __GainCompMaxLevel__(self, channel, level):
        self.instr.write('SENS%d:GCS:POW:STOP:LEV %d' % (channel, level))

    def __FinishAvg__(self, channel, maxWait):
        endtime = time.time() + maxWait
        while True:
            check = int(self.instr.ask('STAT:OPER:AVER%d:COND?' % channel))
            # print check
            if check != 0:
                return 1
            else:
                time.sleep(0.25)
                if time.time() > endtime:
                    raise Exception('Maximum wait time exceeded')


    def __GetData__(self, channel):  # Can't find on PXA**
        return self.instr.ask("CALC%d:DATA? FDATA" % channel)
        # self.instr.ask('CALC:DATA? FDATA')
        # time.sleep(5)
        # return self.instr.read()
        # endtime = time.time() + 120
        # while True:
        #     try:
        #         return self.instr.ask("CALC%d:DATA? FDAT" % channel)
        #         break
        #     except:
        #         time.sleep(0.1)
        #         if time.time() > endtime:
        #             raise Exception('Maximum wait time exceeded')
