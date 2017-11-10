from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import string

class AgilentE5071C(GPIBObjectBaseClass):
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

    def __CheckStatus__(self):
        return int(self.instr.ask('*OPC?'))

    def __SetSweepType__(self, trace, type):
        self.instr.write(':SENS%d:SWE:TYPE %s' % (trace, type))

    def __SetStartf__(self, trace, freq):
        self.instr.write(':SENS%d:FREQ:STAR %g' % (trace, freq))

    def __SetStopf__(self, trace, freq):
        self.instr.write(":SENS%d:FREQ:STOP %g" % (trace, freq))

    def __SetNumPoints__(self, trace, pts):
        self.instr.write(":SENS%d:SWE:POIN %g" % (trace, pts))

    def __SetAvg__(self, trace, num):
        self.instr.write(":SENS%d:AVER:COUN %g" % (trace, num))

    def __SetAutoTime__(self, trace, enab):
        self.instr.write(":SENS%d:SWE:TIME:AUTO %d" % (trace, enab))

    def __SetTrigType__(self, typ):
        self.instr.write(":TRIG:SOUR %s" % typ)

    def __SetContinuous__(self, trace, enab):
        if enab:
            self.instr.write(":INIT%d:CONT ON" % trace)
        else:
            self.instr.write(":INIT%d:CONT OFF" % trace)

    def __EnableAvg__(self, trace, enab):
        if enab:
            self.instr.write(":SENS%d:AVER ON" % trace)
        else:
            self.instr.write(":SENS%d:AVER OFF" % trace)

    def __EnableTrigAvg__(self, enab):
        if enab:
            self.instr.write(":TRIG:AVER ON")
        else:
            self.instr.write(":TRIG:AVER OFF")

    def __SetActiveTracec__(self, channel, trace):
        self.instr.write(":CALC%d:PAR%d:SEL" % (channel, trace))

    def __SetBBalParam__(self, channel, trace, param):
        self.instr.write(":CALC%d:FSIM:BAL:PAR%d:BBAL %s" % (channel, trace, param))

    def __SetActiveFormat__(self, channel, format):
        self.instr.write(":CALC%d:FORM %s" % (channel, format))

    def __InitMeas__(self, channel):
        self.instr.write(':INIT%d' % channel)

    def __SingleTrig__(self):
        self.instr.write(':TRIG:SING')

    def __GetData__(self, channel):
        return self.instr.ask('"CALC1:DATA:FDAT?"')
