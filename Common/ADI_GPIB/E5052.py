# Rev History --------------------
# Author: Michael Viamari
# Date: 3/30/2007
# Purpose: This module is a generic GPIB wrapper for:
# AGILENT E5052A Signal Source Analyzer
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class E5052(GPIBObjectBaseClass):
    
    _ActiveMarker=1
    
    def __init__(self, addr=-1, delay=0.5):
        GPIBObjectBaseClass.__init__(self, 'Agilent Technologies,E5052', addr)
        self.__delay__ = delay
        self.instr.write(":TRIG:SOPC ON")
        self.instr.write(":FORMAT:DATA ASCII")

    def SinglePNTrigger(self):
        '''This function triggers once the PhaseNoise mode of the E5052'''
        self.instr.write(':INIT:PN1:IMM')
        time.sleep(self.__delay__)
    
    def PNAveragingClear(self):
        '''This function restarts the PhaseNoise averaging'''
        self.instr.write(':SENS:PN1:AVER:CLEAR')
        time.sleep(self.__delay__)
    
    def __SetPNContinuousTrigger__(self, Enabled):
        '''This function enables on/off the continuous trigger for the PhaseNoise mode of the E5052'''
        if Enabled:
            self.instr.write(':INIT:PN1:CONT ON')
        else:
            self.instr.write(':INIT:PN1:CONT OFF')
        time.sleep(self.__delay__)
        
    def __SetTriggerMode__(self, mode):
        #Should be one of four:
        #PN1
        #SP1
        #FP1
        #TR1
        '''This function sets the trigger mode of the E5052'''
        self.instr.write(':TRIG:MODE %s' % mode)
        time.sleep(self.__delay__)

    def __GetTriggerMode__(self):
        #Should be one of four:
        #PN1
        #SP1
        #FP1
        #TR1
        '''This function gets the trigger mode of the E5052'''
        return self.instr.ask(':TRIG:MODE?')

    def __SetTriggerAverage__(self, Enabled):
        '''This function sets the trigger averaging mode of the E5052'''
        if Enabled:
            self.instr.write(':TRIG:AVER ON')
        else:
            self.instr.write(':TRIG:AVER OFF')
        time.sleep(self.__delay__)

    def __GetTriggerAverage__(self):
        '''This function gets the trigger averaging status of the E5052'''
        return self.instr.ask(':TRIG:AVER?')
    
    def __SetPNAveragingEnable__(self, Enabled):
        '''This function sets on/off phasenoise averaging'''
        if Enabled:
            self.instr.write(':SENS:PN1:AVER:STAT ON')
        else:
            self.instr.write(':SENS:PN1:AVER:STAT OFF')
        time.sleep(self.__delay__)

    def __GetPNAveragingEnable__(self):
        '''This function gets the status of phasenoise averaging (On/Off)'''
        return self.instr.ask(':SENS:PN1:AVER:STAT?')
    
    def __SetPNAveragingFactor__(self, factor):
        '''This function sets the averaging factor for the PhaseNoise mode of the E5052'''
        self.instr.write(':SENS:PN1:AVER:COUNT %d' % factor)
        time.sleep(self.__delay__)
    
    def __GetPNAveragingFactor__(self):
        return self.instr.ask(':SENS:PN1:AVER:COUNT?')
    
    def __SetPNCorrelationFactor__(self, factor):
        '''This function sets the averaging factor for the PhaseNoise mode of the E5052'''
        self.instr.write(':SENS:PN1:CORR:COUNT %d' % factor)
        time.sleep(self.__delay__)
    
    def __GetPNCorrelationFactor__(self):
        return self.instr.ask(':SENS:PN1:CORR:COUNT?')
    
    def __SetPNFrequencyBand__(self, band):
        '''This function sets the frequency band for the PhaseNoise mode of the E5052'''
        self.instr.write(':SENS:PN1:FBAN BAND%d' % band)
        time.sleep(self.__delay__)
    
    def __GetPNFrequencyBand__(self):
        return self.instr.ask('SENS:PN1:FBAN?')
        
    def __SetPNFrequencyLimits__(self, limits):
        '''This function sets the frequency limits for the PhaseNoise mode of the E5052'''
        self.instr.write(':SENS:PN1:FREQ:START %s' % limits[0])
        if not (self.PNFreqBand=='BAND1'):
            self.instr.write(':SENS:PN1:FREQ:STOP %s' % limits[1])
        else:
            if limits[1]=='10M' or limits[1]=='20M' or limits[1]=='40M':
                self.instr.write(':SENS:PN1:FREQ:STOP 5M')
            else:
                self.instr.write(':SENS:PN1:FREQ:STOP %s' % limits[1])
                
        time.sleep(self.__delay__)
    
    def __GetPNFrequencyLimits__(self):
        limits = [0,0]
        limits[0] = self.instr.ask(':SENS:PN1:FREQ:START?')
        limits[1] = self.instr.ask(':SENS:PN1:FREQ:STOP?')
        return limits
    
    def __SaveImage__(self, imagename):
        '''Dumps the screen image'''
        self.instr.write(':MMEM:STOR:IMAG "%s"' % imagename)
        time.sleep(.5)
    
    def __LoadState__(self, statename):
        '''Loads a specified state'''
        self.instr.write('MMEM:LOAD:STAT "%s"' % statename)
        time.sleep(self.__delay__)
    
    def __SavePNTrace__(self, tracename):
        '''Saves The Phase Noise Trace Data to a .csv'''
        self.instr.write('MMEM:PN1:TRAC1:STOR "%s"' % tracename)
        time.sleep(self.__delay__)
    
    def __GetXBDMState__(self):
        state = self.instr.write(':CALC:USER:TRAC:BDM:X:STAT?')
    
    def __SetXBDMState__(self, Enabled):
        '''This function enables on/off the X-Band Marker of the E5052'''
        if Enabled:
            self.instr.write(':CALC:PN:TRAC:BDM:X:STAT ON')
        else:
            self.instr.write(':CALC:PN:TRAC:BDM:X:STAT OFF')
        time.sleep(self.__delay__)
    
    def __GetXBDMLimits__(self):
        limits = [0,0]
        limits[0] = self.instr.ask(':CALC:PN1:TRAC1:BDM:X:START?')
        limits[1] = self.instr.ask(':CALC:PN1:TRAC1:BDM:X:STOP?')
        return limits
    
    def __SetXBDMLimits__(self, Limits):
        '''Sets the X BDM limits'''
        self.instr.write(':CALC:PN1:TRAC1:BDM:X:START %s' % Limits[0])
        self.instr.write(':CALC:PN1:TRAC1:BDM:X:STOP %s' % Limits[1])

    def __GetPNData__(self):
        data = self.StringToArray(self.instr.ask(':CALC:PN1:TRACE1:DATA:PDATA?'))
        xaxis = self.StringToArray(self.instr.ask(':CALC:PN1:DATA:XDATA?'))
        return zip(xaxis, data)
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    def StringToArray(self, data):
        array = []
        list = data.split(",")
        for each in list:
            array.append(float(each))
        return array

    def __GetPN__(self):
        data = self.StringToArray(self.instr.ask(':CALC:PN1:TRACE1:DATA:FDATA?'))
        return data

    def __GetXAXIS__(self):
        xaxis = self.StringToArray(self.instr.ask(':CALC:PN1:DATA:XDATA?'))
        return xaxis
    
    def __GetJitter__(self):
        properties = self.instr.ask(':CALC:PN1:TRAC1:FUNC:INT:DATA?')
        array = []
        list = properties.split(',')
        for each in list:
            array.append(float(each))
        return array [4]
    
    def __GetCarrier__(self):
        properties = self.instr.ask(':CALC:PN1:DATA:CARR?')
        array = []
        list = properties.split(',')
        for each in list:
            array.append(float(each))
        return (array [0]/(1e6))
    
    def __GetCarrierPow__(self):
        properties = self.instr.ask(':CALC:PN1:DATA:CARR?')
        array = []
        list = properties.split(',')
        for each in list:
            array.append(float(each))
        return (array [1])
    
    def __AverSetUp__(self):
        self.instr.write(":TRIG:AVER 1")
        self.instr.write(":TRIG:MODE PN1")
        self.instr.write(":TRIG:SOPC ON")
    
    def __SystemLock__(self, state):
        self.instr.write(':SYSTEM:KLOCK:KBD %s' % state[0])
        self.instr.write(':SYSTEM:KLOCK:MOUSE %s' % state[0])
        self.instr.write(':DISPLAY:ENABLE %s' % abs(state[0]-1))
        self.instr.write(':DISPLAY:ECHO:STATE %s' % state[1])
        self.instr.write(':DISPLAY:ECHO:FSIZE 36')
        self.instr.write(':DISPLAY:ECHO:CLEAR')
        self.instr.write(':DISPLAY:ECHO:ADD "TEST IN PROGRESS, PLEASE DO NOT TOUCH"')
    
    def __TraceRefresh__(self):
        self.instr.write(":DISPLAY:UPDATE:IMMEDIATE")
    
    def __GetPNActiveMarker__(self):
        ActMark=self.instr.ask(':CALC:PN1:TRAC1:ALLM:ACT?')
        return ActMark
    
    def __SetPNActiveMarker__(self, num):
        self._ActiveMarker=num
        self.instr.write(':CALC:PN1:TRAC1:ALLM:ACT %s' % num)
        return
    
    def __GetPNMarkerState__(self):
        state=self.instr.ask(':CALC:PN1:TRAC1:MARK%s:STAT?' % self._ActiveMarker)
        return state
    
    def __SetPNMarkerState__(self, state):
        self.instr.write(':CALC:PN1:TRAC1:MARK%s:STAT %s' % (self._ActiveMarker,state))
        return
    
    def __GetPNMarkerXSearchRange__(self):
        state=self.instr.ask(':CALC:PN1:TRAC1:ALLM:SEAR:DOM:X?')
        return state
    
    def __SetPNMarkerXSearchRange__(self, xrnge):
        '''Band Marker Search Range = 0, Full Search Range = 1'''
        if xrnge:
            self.instr.write(':CALC:PN1:TRAC1:ALLM:SEAR:DOM:X FRAN')
            return
        if not xrnge:
            self.instr.write(':CALC:PN1:TRAC1:ALLM:SEAR:DOM:X BDM')
            return
        
    def __GetPNMarkerYSearchRange__(self):
        state=self.instr.ask(':CALC:PN1:TRAC1:ALLM:SEAR:DOM:Y?')
        return state
    
    def __SetPNMarkerYSearchRange__(self, yrnge):
        '''Band Marker Search Range = 0, Full Search Range = 1'''
        if yrnge:
            self.instr.write(':CALC:PN1:TRAC1:ALLM:SEAR:DOM:Y FRAN')
            return
        if not yrnge:
            self.instr.write(':CALC:PN1:TRAC1:ALLM:SEAR:DOM:Y BDM')
            return
    
    def __GetPNMarkerData__(self,num=-1):
        '''Default is active marker. Returns (X,Y) array in (Hz, dBc/Hz)'''
        if num==-1:
            num=self._ActiveMarker
        xVal=self.instr.ask(':CALC:PN1:TRAC1:MARK%s:X?' % num)
        yVal=self.instr.ask(':CALC:PN1:TRAC1:MARK%s:Y?' % num)
        return [xVal,yVal]
    
    def __PNSearchMax__(self,num=-1):
        '''Default is the active marker.'''
        if num==-1:
            num=self._ActiveMarker
        self.instr.write(':CALC:PN1:TRAC1:MARKer%s:SEAR:EXEC:MAX' % num)
    
    def __GetPNSpurOmission__(self):
        state=(~(int(self.instr.ask(':CALC:PN1:TRAC1:SPUR:OMIS?'))) & 0x1)
        return state
    
    def __SetPNSpurOmission__(self, state=0):
        '''0=Spurs off 1= Spurs On. Off Default'''
        state= (~state) & 0x1
        self.instr.write(':CALC:PN1:TRAC1:SPUR:OMIS %s' % state)
        return
    
    def __GetPNSpurPower__(self):
        '''Returns Spur Power Measurement Type dBc/Hz=0, dBc=1'''
        state=self.instr.ask(':CALC:PN1:TRAC1:SPUR:POW?')
        return state
    
    def __SetPNSpurPower__(self, state):
        ''' Sets spur power measurement to Normalized (dBc/Hz)[0] or Power(dBc)[1]'''
        self.instr.write(':CALC:PN1:TRAC1:SPUR:POW %s' % state)
        
    
    PNActiveMarker        = property(__GetPNActiveMarker__, __SetPNActiveMarker__, None, "Gets/Sets Active Marker for PN Mode")
    
    PNMarkerState         = property(__GetPNMarkerState__, __SetPNMarkerState__, None, "On/Off Marker control for PN Mode")
    
    PNXMarkerSearchRange  = property(__GetPNMarkerXSearchRange__, __SetPNMarkerXSearchRange__, None, "Gets/Sets X Marker Search Range for PN Mode")
    PNXRange              = property(__GetPNMarkerXSearchRange__, __SetPNMarkerXSearchRange__, None, "Gets/Sets X Marker Search Range for PN Mode")
    
    PNYMarkerSearchRange  = property(__GetPNMarkerYSearchRange__, __SetPNMarkerYSearchRange__, None, "Gets/Sets Y Marker Search Range for PN Mode")
    PNYRange              = property(__GetPNMarkerYSearchRange__, __SetPNMarkerYSearchRange__, None, "Gets/Sets Y Marker Search Range for PN Mode")
    
    PNMarkerData          = property(__GetPNMarkerData__, __GetPNMarkerData__, None, "Returns Specified Marker Data (Array of form [Hz, dBc/Hz]) for PN Mode (Active Marker Default)")
    
    PNSearchMax           = property(__PNSearchMax__, __PNSearchMax__, None, "Sets the Specified Marker to the Maximum point Y value within the Search Ranges for PN Mode (Active Marker Default)")
    
    PNSpurState           = property(__GetPNSpurOmission__, __SetPNSpurOmission__, None, "Gets/Sets Spurious Inclusion (Spurs Off= Default)")
    
    PNSpurMeasType        = property(__GetPNSpurPower__, __SetPNSpurPower__, None, "Gets/Sets Spur Power Measurement Type (Normalized (dBc/Hz) = 0, Power(dBc) = 1)")
    
    PNContTrig            = property(None, __SetPNContinuousTrigger__, None, "Sets On/Off Continuous Trigger for PN Mode")
    PNContinuousTrigger   = property(None, __SetPNContinuousTrigger__, None, "Sets On/Off Continuous Trigger for PN Mode")
    
    PNFreqBand            = property(__GetPNFrequencyBand__, __SetPNFrequencyBand__, None, "Sets Frequency Band for PN Mode")
    PNFrequencyBand       = property(__GetPNFrequencyBand__, __SetPNFrequencyBand__, None, "Sets Frequency Band for PN Mode")
    
    PNFreqLimits          = property(__GetPNFrequencyLimits__, __SetPNFrequencyLimits__, None, "Sets Frequency Measure Limits for PN Mode")
    PNFrequencyLimits     = property(__GetPNFrequencyLimits__, __SetPNFrequencyLimits__, None, "Sets Frequency Measure Limits for PN Mode")

    PNCorrFactor          = property(__GetPNCorrelationFactor__, __SetPNCorrelationFactor__, None, "Sets PN Correlation Factor for PN Mode")
    PNCorrelationFactor   = property(__GetPNCorrelationFactor__, __SetPNCorrelationFactor__, None, "Sets PN Correlation Factor for PN Mode")
    
    PNAverFactor          = property(__GetPNAveragingFactor__, __SetPNAveragingFactor__, None, "Sets PN Averaging Factor for PN Mode")
    PNAveragingFactor     = property(__GetPNAveragingFactor__, __SetPNAveragingFactor__, None, "Sets PN Averaging Factor for PN Mode")
    
    PNAverEnable          = property(__GetPNAveragingEnable__, __SetPNAveragingEnable__, None, "Sets PN Averaging On/Off for PN Mode")
    PNAveragingEnable     = property(__GetPNAveragingEnable__, __SetPNAveragingEnable__, None, "Sets PN Averaging On/Off for PN Mode")
    
    PNData                = property(__GetPNData__, None, None, "Gets Unformatted PN data in dBc/Hz")
    
    TriggerMode           = property(__GetTriggerMode__, __SetTriggerMode__, None, "Sets Trigger Mode")
    
    TriggerAverage        = property(__GetTriggerAverage__, __SetTriggerAverage__, None, "Sets Trigger Average Mode")
    
    Delay                 = property(__GetDelay__, __SetDelay__, None, "Delay")
    
    DumpImage             = property(None, __SaveImage__, None, "Saves Screen Image")

    LoadState             = property(None, __LoadState__, None, "Loads Specified E5052A State")

    PNTraceData           = property(None, __SavePNTrace__, None, "Saves .csv of the Phase Noise Trace Data")

    XBDMState             = property(__GetXBDMState__, __SetXBDMState__, None, "Sets X Band Marker State")
 
    XBDMLimits            = property(__GetXBDMLimits__, __SetXBDMLimits__, None, "Sets X Band Marker Limits")

    PNAverSetUp           = property(__AverSetUp__, None, None, "Sets up 5052 for automated use with averaging")
    PNAveragingSetUp      = property(__AverSetUp__, None, None, "Sets up 5052 for automated use with averaging")

    SystemLock            = property(None, __SystemLock__, None, "Locks the 5052 user interface and turns off LCD trace updating")

    TraceRefresh          = property(__TraceRefresh__, None, None, "Refreshes the Trace image on the LCD the the updating is off")

    Jitter                = property(__GetJitter__, None, None, "Returns the RMS Jitter of the Trace Data")
    Carrier               = property(__GetCarrier__, None, None, "Returns Carrier Frequency of the Trace Data in MHz")
    CarrierPow            = property(__GetCarrierPow__, None, None, "Returns Carrier Power of the Trace Data in dBm")
    
    Xaxis                 = property(__GetXAXIS__, None, None, "Gets Unformatted PN Data in dBc")
    PN                    = property(__GetPN__, None, None, "Gets Unformatted X-Axis Data in Frequency Offset")