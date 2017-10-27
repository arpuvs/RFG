from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import string

class AgilentN9030A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'N5181A', addr)
        self.__delay__ = delay

    def __StoreState__(self, fname):
        self.instr.write(':MMEM:STOR:STAT "%s"' % fname)

    def __LoadState__(self,fname):
        self.instr.write(':MMEM:LOAD:STAT "%s"' % fname)

    def __Getfc__(self):
        return self.instr.ask(':FREQ:CENT?')

    def __Setfc__(self, freq):
        self.instr.write(':FREQ:CENT %g' % freq)

    def __GetMarkerFreq__(self, marker):
        return self.instr.ask(':CALC:MARK%d:X:CENT?' % marker)

    def __SetMarkerFreq__(self, marker, freq):
        self.instr.write(':CALC:MARK%d:X:CENT %g' % (marker, freq))

    def __GetMarkerAmp__(self, marker):
        return self.instr.ask(':CALC:MARK%d:Y?' % marker)

    def __MarkerMax__(self, marker):
        self.instr.write('CALC:MARK%d:MAX' % marker)

    def __GetSpan__(self):
        return self.instr.ask('FREQ:SPAN?')

    def __SetSpan__(self, span):
        self.instr.write('FREQ:SPAN %g' % span)