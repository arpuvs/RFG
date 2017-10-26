# Author: Tom MacLeod
# Date: 12/4/2006
# Purpose: This module is a generic GPIB wrapper for:
# Agilent E4443A Spectrum Analyzer
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import string

class E4443A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'Rohde&Schwarz,E4443A', addr)
        self.__delay__ = delay
        
    def __SetCenterFrequency__(self, CF):
        '''This function sets the E4443A center frequency'''
        self.instr.write( 'FREQ:CENT %sMHz' % (str(CF / 1e6)) )
        time.sleep(self.__delay__)
    def __GetCenterFrequency__(self):
        '''This function gets the E4443A center frequency'''
        return self.instr.ask('FREQ:CENT?')
    CenterFrequency = property(__GetCenterFrequency__, __SetCenterFrequency__, None, "Sets the E4443A Center Frequency")
    CF              = property(__GetCenterFrequency__, __SetCenterFrequency__, None, "Sets the E4443A Center Frequency")
    
    def __SetSpanFrequency__(self, S):
        '''This function sets the E4443A frequency span'''
        self.instr.write( 'FREQ:SPAN %sMHz' % (str(S / 1e6)) )
        time.sleep(self.__delay__)
    def __GetSpanFrequency__(self):
        '''This function gets the E4443A frequency span'''
        return self.instr.ask('FREQ:SPAN?')
    Span = property(__GetSpanFrequency__, __SetSpanFrequency__, None, "Sets the E4443A Frequency Span")

    def __SetReferenceLevel__(self, RL):
        '''This function sets the E4443A reference level'''
        self.instr.write('DISP:WIND:TRAC:Y:RLEV %s dBm' % (str(RL)) )
        time.sleep(self.__delay__)
    def __GetReferenceLevel__(self):
        '''This function gets the E4443A reference level'''
        return self.instr.ask('DISP:WIND:TRAC:Y:RLEV?')
    RefLevel       = property(__GetReferenceLevel__, __SetReferenceLevel__, None, "Sets the E4443A Reference Level")
    ReferenceLevel = property(__GetReferenceLevel__, __SetReferenceLevel__, None, "Sets the E4443A Reference Level")

    def __SetAttenLevel__(self, AL):
        '''This function sets the E4443A attenuation level'''
        self.instr.write('POW:ATT %s' % (str(AL)) )
        time.sleep(self.__delay__)
    def __GetAttenLevel__(self):
        '''This function gets the E4443A attenuation level'''
        return self.instr.ask('POW:ATT?')
    AttLevel         = property(__GetAttenLevel__, __SetAttenLevel__, None, "Sets the E4443A Attenuation Level")
    AttenuationLevel = property(__GetAttenLevel__, __SetAttenLevel__, None, "Sets the E4443A Attenuation Level")

    def __SetResBandwidth__(self, RB):
        '''This function sets the E4443A Resolution Bandwidth'''
        self.instr.write('BAND %s kHz' % (str(RB / 1.0e3)) )
        time.sleep(self.__delay__)
    def __GetResBandwidth__(self):
        '''This function gets the E4443A Resolution Bandwidth'''
        return self.instr.ask('BAND?')
    ResBand             = property(__GetResBandwidth__, __SetResBandwidth__, None, "Sets the E4443A Resolution Bandwidth")
    ResolutionBandwidth = property(__GetResBandwidth__, __SetResBandwidth__, None, "Sets the E4443A Resolution Bandwidth")

    def __SetVideoBandwidth__(self, VB):
        '''This function sets the E4443A Video Bandwidth'''
        self.instr.write('BAND:VID %s kHz' % (str(VB / 1.0e3)) )
        time.sleep(self.__delay__)
    def __GetVideoBandwidth__(self):
        '''This function gets the E4443A Video Bandwidth'''
        return self.instr.ask('BAND:VID?')
    VidBand        = property(__GetVideoBandwidth__, __SetVideoBandwidth__, None, "Sets the E4443A Video Bandwidth")
    VideoBandwidth = property(__GetVideoBandwidth__, __SetVideoBandwidth__, None, "Sets the E4443A Video Bandwidth")

    
    def __GetRawData__(self):
        '''This function gets the E4443A raw plot data'''
        points = string.split( self.instr.ask('TRAC? TRACE1'), ',' )
        retval = []
        for point in points:
            retval.append( float(point) )
        return retval
    RawData = property(__GetRawData__, None, None, "Gets the E4443A raw plot data")

    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")
    