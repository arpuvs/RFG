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
        i = 0
        amp = self.instr.ask(':CALC:MARK%d:Y?' % marker)
        while (float(amp) > 200) | (float(amp) < -400):
            time.sleep(0.5)
            amp = self.instr.ask(':CALC:MARK%d:Y?' % marker)
            i = i + 1
            if i > 100:
                raise Exception('Valid marker amplitude cannot be found')
        return amp

    def __MarkerMax__(self, marker):
        self.instr.write('CALC:MARK%d:MAX' % marker)

    def __GetSpan__(self):
        return self.instr.ask('FREQ:SPAN?')

    def __SetSpan__(self, span):
        self.instr.write('FREQ:SPAN %g' % span)

    def __GetAverage__(self):
        return self.instr.ask(':AVER:COUN?')

    def __SetAverage__(self, average):
        self.instr.write(':AVER:COUN %d' % average)

    def __ClearAverage__(self):
        self.instr.write(':AVER:CLE')

    def __Align__(self):
        self.instr.write(':CAL')

    def __SetBW__(self, bw):
        self.instr.write(':BAND %d' % bw)

    def __SetAutoAtten__(self, state):
        self.instr.write(':POW:ATT:AUTO %d' % state)

    def __SetAtten__(self, attn):
        self.instr.write(':POW:ATT %d' % attn)

    def __GetAtten__(self):
        return self.instr.ask(':POW:ATT?')

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
