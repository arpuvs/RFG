# Author: Tom MacLeod
# Date: 12/4/2006
# Purpose: This module is a generic GPIB wrapper for:
# ROHDE & SCHWARZ FSEA Spectrum Analyzer
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import string

class FSEA(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'Rohde&Schwarz,FSEA', addr)
        self.__delay__ = delay
        
    def __SetCenterFrequency__(self, CF):
        '''This function sets the FSEA center frequency'''
        self.instr.write( 'FREQ:CENT %sMHz' % (str(CF / 1e6)) )
        time.sleep(self.__delay__)
    def __GetCenterFrequency__(self):
        '''This function gets the FSEA center frequency'''
        return self.instr.ask('FREQ:CENT?')
    CenterFrequency = property(__GetCenterFrequency__, __SetCenterFrequency__, None, "Sets the FSEA Center Frequency")
    CF              = property(__GetCenterFrequency__, __SetCenterFrequency__, None, "Sets the FSEA Center Frequency")
    
    def __SetSpanFrequency__(self, S):
        '''This function sets the FSEA frequency span'''
        self.instr.write( 'FREQ:SPAN %sMHz' % (str(S / 1e6)) )
        time.sleep(self.__delay__)
    def __GetSpanFrequency__(self):
        '''This function gets the FSEA frequency span'''
        return self.instr.ask('FREQ:SPAN?')
    Span = property(__GetSpanFrequency__, __SetSpanFrequency__, None, "Sets the FSEA Frequency Span")

    def __SetReferenceLevel__(self, RL):
        '''This function sets the FSEA reference level'''
        self.instr.write('DISP:TRAC:Y:RLEV %sdBm' % (str(RL)) )
        time.sleep(self.__delay__)
    def __GetReferenceLevel__(self):
        '''This function gets the FSEA reference level'''
        return self.instr.ask('DISP:TRAC:Y:RLEV?')
    RefLevel       = property(__GetReferenceLevel__, __SetReferenceLevel__, None, "Sets the FSEA Reference Level")
    ReferenceLevel = property(__GetReferenceLevel__, __SetReferenceLevel__, None, "Sets the FSEA Reference Level")

    def __SetAttenLevel__(self, AL):
        '''This function sets the FSEA attenuation level'''
        self.instr.write('INP:ATT %s' % (str(AL)) )
        time.sleep(self.__delay__)
    def __GetAttenLevel__(self):
        '''This function gets the FSEA attenuation level'''
        return self.instr.ask('INP:ATT?')
    AttLevel         = property(__GetAttenLevel__, __SetAttenLevel__, None, "Sets the FSEA Attenuation Level")
    AttenuationLevel = property(__GetAttenLevel__, __SetAttenLevel__, None, "Sets the FSEA Attenuation Level")

    def __SetResBandwidth__(self, RB):
        '''This function sets the FSEA Resolution Bandwidth'''
        self.instr.write(':BAND %skHz' % (str(RB / 1.0e3)) )
        time.sleep(self.__delay__)
    def __GetResBandwidth__(self):
        '''This function gets the FSEA Resolution Bandwidth'''
        return self.instr.ask(':BAND?')
    ResBand             = property(__GetResBandwidth__, __SetResBandwidth__, None, "Sets the FSEA Resolution Bandwidth")
    ResolutionBandwidth = property(__GetResBandwidth__, __SetResBandwidth__, None, "Sets the FSEA Resolution Bandwidth")

    def __SetVideoBandwidth__(self, VB):
        '''This function sets the FSEA Video Bandwidth'''
        self.instr.write(':BAND:VID %skHz' % (str(VB / 1.0e3)) )
        time.sleep(self.__delay__)
    def __GetVideoBandwidth__(self):
        '''This function gets the FSEA Video Bandwidth'''
        return self.instr.ask(':BAND:VID?')
    VidBand        = property(__GetVideoBandwidth__, __SetVideoBandwidth__, None, "Sets the FSEA Video Bandwidth")
    VideoBandwidth = property(__GetVideoBandwidth__, __SetVideoBandwidth__, None, "Sets the FSEA Video Bandwidth")

    
    def __GetRawData__(self):
        '''This function gets the FSEA raw plot data'''
        points = string.split( self.instr.ask('TRAC? TRACE1'), ',' )
        retval = []
        for point in points:
            retval.append( float(point) )
        return retval
    RawData = property(__GetRawData__, None, None, "Gets the FSEA raw plot data")

    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")
    
    def __SetAveraging__(self, Enabled):
        '''Enables on/off of the averaging subsystem'''
        if Enabled:
            self.instr.write(':AVER ON')
        else:
            self.instr.write(':AVER OFF')
        time.sleep(self.__delay__)
    Aver      = property(None, __SetAveraging__, None, "Sets the FSEA Averaging Mode")
    Averaging = property(None, __SetAveraging__, None, "Sets the FSEA Averaging Mode")
    
    def __SetAveragingCount__(self, AC):
        '''Sets amount of measurements to include in an averaging count'''
        self.instr.write(':AVER:COUN %d' % AC)
        time.sleep(self.__delay__)
    AverCount      = property(None, __SetAveragingCount__, None, "Sets the FSEA Averaging Count")
    AveragingCount = property(None, __SetAveragingCount__, None, "Sets the FSEA Averaging Count")
    
    def __SetAveragingCountAuto__(self, Enabled):
        '''Enables auto determine amounf of measurements for an averaging count'''
        if Enabled:
            self.instr.write(':AVER:COUN:AUTO ON')
        else:
            self.instr.write(':AVER:COUN:AUTO OFF')
        time.sleep(self.__delay__)
    AverCountAuto      = property(None, __SetAveragingCountAuto__, None, "Sets the FSEA Averaging Count Auto Mode")
    AveragingCountAuto = property(None, __SetAveragingCountAuto__, None, "Sets the FSEA Averaging Count Auto Mode")
