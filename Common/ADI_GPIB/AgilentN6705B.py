from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import string

class AgilentN6705B(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'N6705B', addr)
        self.__delay__ = delay

    def __Enable__(self, Enable, channels):
        self.instr.write('OUTP %d,(@%s)' % (int(Enable), str(channels).strip('()[]')))
        # print 'OUTP %d (@%s)' % (int(Enable), str(channels).strip('()[]'))

    def __SetI__(self, i, channels):
        self.instr.write('CURR:LIMIT %g,(@%s)' % (i, str(channels).strip('[]()')))
        # print 'CURR %g,(@%s)' % (i, str(channels).strip('[]()'))

    def __GetI__(self, channels):
        # print 'CURR? (@%s)' % str(channels).strip('[]()')
        return self.instr.ask('MEAS:CURR? (@%s)' % str(channels).strip('[]()'))

    def __SetV__(self, v, channels):
        self.instr.write('VOLT %g,(@%s)' % (v, str(channels).strip('[]()')))

    def __GetV__(self, channels):
        return self.instr.ask('VOLT? (@%s)' % str(channels).strip('[]()'))
