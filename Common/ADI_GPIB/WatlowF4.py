from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import string

class WatlowF4(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'WatlowF4', addr)
        self.__delay__ = delay

    def __GetTemp__(self):
        return self.instr.ask('R? 100,1')

    def __SetTemp__(self, Temp):
        if Temp >= 0:
            # print Temp
            self.instr.write('W 300,%d' % Temp)
            # return self.instr.ask('R? 300,1')
            # return self.instr.ask('R 602,1')
        else:
            Temp = 65536 + Temp
            self.instr.write('W 300,%d' % Temp)
        # self.instr.write()

    def __GetSP__(self):
        return self.instr.ask('R? 300,1')