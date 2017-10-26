# Author: Leah Magaldi
# ---------------------------------------------------------------------
# Last update 5/20/2014 added Define TJ BER threshold

# Date: 04/28/2014
# Purpose: This module is a generic GPIB wrapper for:
# Agilent 86100D DCAX scope 
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class Agilent86100d(GPIBObjectBaseClass):
    ##############################################################################################################################################
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'DCA', addr)
        self.__delay__ = delay
        self.Reset()
        self.instr.write(':SYSTem:HEADer OFF')
        self.Configurethresholdpercent_205080()
        

    
    
    ##############################################################################################################################################

    def Reset(self):
        '''Resets instrument to Power-Up default state'''
        self.instr.write('*RST')
        self.instr.write('*CLS')
        self.instr.write(':SYSTem:HEADer OFF')#this needs to be off to retrieve the data properly
        
    ##############################################################################################################################################
    def ClearDisp(self):
        '''clear the display'''
        self.instr.write(':cdisplay')
    ##############################################################################################################################################
    def setScopeRate(self, drate):
        self.instr.write(':CRECOVERY1:CRATe %d' % int(drate))
    ##############################################################################################################################################
    def AutoScale(self):
        '''AutoScale selected signal'''
        self.instr.write(':autoscale')
    ##############################################################################################################################################
    def Run(self):
        '''Run continuous data'''
        self.instr.write(':RUN')
    ##############################################################################################################################################
    def SingleSweep(self):
        '''Run one aquisition'''
        self.instr.write(':Single')
    ##############################################################################################################################################
    def Stop(self):
        '''stop the aquisiton'''
        self.instr.write(':STOP')
    ##############################################################################################################################################
    def AveragingState(self, state):
        '''turn on= 1/off=0 averaging, this doesn't apply to jitter mode'''
        self.instr.write(':ACQuire:AVERage %d' % int(state)) 
         
    ##############################################################################################################################################
    def SetNumAverags(self, number):
        '''set the number of averages in range 1 to 4096'''
        self.instr.write(':ACQUIRE:COUNT %d' % int(number))       
    ##############################################################################################################################################
    def Configurethresholdpercent_205080(self):
        '''Configure the scope to make measurements based on 20/80% for rise and fall times with midpoint relative to 50%'''
        self.instr.write(':measure:threshold:method P205080')       
         
         
    ##############################################################################################################################################
    def SetMode(self, mode):
        '''Select the scope mode choices:  [:SYSTem:MODE] {EYE | OSC | TDR | JITT}'''
        self.instr.write(':SYSTEM:MODE:%s' %str(mode))
    ##############################################################################################################################################
    def MeasureSource(self, source):
        '''Select the source to use for measurements. choices:  {CHANnel<N> | FUNCtion<N> |RESPonse<N> | WMEMory<N>}'''
        self.instr.write(':MEASure:SOURce %s' %str(source))
    ##############################################################################################################################################
    def SetFunction(self,funcnumb, chanA, chanB, operation):
        '''Creates a function. choices: ADD, Subtract, Multiply: 
            chanA, chanB choices can be {CHANnel<N> | FUNCtion<N> |RESPonse<N> | WMEMory<N>}'''
        self.instr.write(':FUNCTION%d:%s %s,%s' % funcnumb, str(operation), str(chanA), str(chanB))
    ##############################################################################################################################################
    def DisplayFunction_state(self,funcnum, state_ON_OFF):
        '''Turns on or off the waveform'''
        self.instr.write(':function%d:display %s' % funcnum, str(state_ON_OFF))
    ##############################################################################################################################################
    def DisplayChannel_state(self,channum, state_ON_OFF):
        '''Turns on or off the waveform'''
        self.instr.write(':channel%d:display %s' % channum, str(state_ON_OFF))
    ##############################################################################################################################################
    def DisplayAnnotations(self, state_ON_OFF):
        '''Turns on or off the annotation, send ON or OFF'''
        self.instr.write(':MEASure:ANNotation %s' % str(state_ON_OFF))
         
    ##############################################################################################################################################
    def TurnOffJitterShade(self):
        '''Turns off the jitter shade in Jitter mode'''
        self.instr.write(':disp:jitt:shade 1')
        self.instr.write(':disp:jitt:shade 0')
 
    ##############################################################################################################################################
    def DefineTJBER(self,BER):
        '''Defines what BER to use as a reference in Jitter mode'''
        self.instr.write(':measure:jitter:define:tjber %1.1E' % float(BER))
        
        
    ##############################################################################################################################################
    def SetTriggerBandwidth(self, triggerrate):
        '''Use when pattern lock is off and need to select the trigger range'''
        if triggerrate >= 3e9:   #good for rates 3 - 13GHz
            self.instr.write('TRIGger:BWLimit DIVIDED' )
        else:           #rates less than 3.2GHz'''
            self.instr.write('TRIGger:BWLimit HIGH')
      
    ##############################################################################################################################################
    def SetPrecisionTimebase(self, state):
        '''set the precision timebase 1=ON or 0=OFF'''
        currentstate = self.instr.ask(':TIMebase:PRECision?')
        '''state is already correct do nothing'''
        if currentstate != state: 
            self.instr.write(':TIMebase:PRECision:%d' %int(state))
    ##############################################################################################################################################
    def SetPrecisionTimebaseFrequency(self, frequency):
        '''Sets the precision timebase frequency , value is in seconds example: ":TIMEBASE:SCALE 10E-3" '''
        self.instr.write(':timebase:precision:rfrequency %0.3e' % frequency)
    ##############################################################################################################################################
    def ResetPrecisionTimebase(self):
        '''if the precision time base is enabled this resets the time reference" '''
        self.instr.write(':ptimebase1:rtreference')

    ##############################################################################################################################################
    def SetPatternLock(self, state):
        '''Set the pattern lock, also sets the trigger to the first bit for trigger consistancy'''
        self.instr.write('TRIGger:PLOCk:%d' %int(state))
        self.instr.write(':TRIGger:RBIT 0')
    ##############################################################################################################################################
    def SetPatternLockPatternLength(self, length):
        '''Sets pattern trigger length to value '''
        self.instr.write('TRIGger:plen %d' %int(length))
    ##############################################################################################################################################
    def ReaquireCDRLock(self):
        '''Attempts to re-aquire cdr lock to previously selected rate '''
        self.instr.write(':crecovery1:relock')
    ##############################################################################################################################################
    def isCDRlocked(self):
        '''set the precision timebase 1=ON or 0=OFF'''
        locked = self.instr.ask(':crecovery1:locked?')
        return locked
    ##############################################################################################################################################
    def SetPatternLockAuto(self):
        '''Sets trigger to autodetect, pattern, rate parameters '''
        self.instr.write(':TRIGger:PLOCk:AUTodetect')
        '''check if successful, return 0'''
        status = self.instr.ask(':TRIGger:PLOCk:AUTodetect?')
        if not status:
            return (-1)
        else:
            return (0)
    ##############################################################################################################################################
    def GetTimebase(self):
        '''returns the value of the timebase in seconds'''
        return(self.instr.ask(':timebase:scale?'))
    ##############################################################################################################################################
    def SetTimebase(self, timebase):
        '''Sets timebase, value is in seconds example: ":TIMEBASE:SCALE 10E-3" '''
        self.instr.write(':timebase:scale %0.3e' % timebase)
    ##############################################################################################################################################
    def SetYscale(self, level):
        '''Sets timebase, value is in seconds example: ":TIMEBASE:SCALE 10E-3" '''
        self.instr.write(':DIFF1A:YSCale %0.3e' % level)
    ##############################################################################################################################################
    def JitterShade(self, ON_OFF):
        '''hides or shows the jitter shade  '''
        self.instr.write(':display:sint:shade %s' % ON_OFF )
    ##############################################################################################################################################
    def SetFunctionDiff(self, funcnumber, chanA, chanB):
        '''Sets the selected function to subtract chanA form chanB,  operand {CHANnel<N> | FUNCtion<N> | RESPonse<N> | WMEMory<N> | <float_value> '''
        self.instr.write(':FUNCTION%d:SUBTRACT %s,%s' % funcnumber, chanA, chanB)
    ##############################################################################################################################################
    def SaveScreenImage(self, dirstring, plotnamejpg):
        '''saves to the directory the screen image, plotname.jpg style '''
        self.instr.write(':disk:simage %s\\%s, SCReen,INVert' % dirstring, plotnamejpg)
    ##############################################################################################################################################
    def JitterAmplitudeAnalysis(self, ON_OFF):
        '''Turns on the amplitude analysis in jitter mode (option must be installed to work  '''
        self.instr.write(':MEASure:AMPLitude:ANALysis %s' % ON_OFF )
    ##############################################################################################################################################
    def SetMaskMarginAuto(self):
        '''Turns on the margin mask test to auto (option must be installed to work  '''
        self.instr.write(':MTEST:Margin:method AUTO' )
    ##############################################################################################################################################
    def SetMaskMarginTestState(self, ON_OFF):
        '''Turns on the margin mask test to auto (option must be installed to work  '''
        self.instr.write(':MTEST:Margin:state %s' % ON_OFF )
         
    ##############################################################################################################################################
    def SaveEyeModeData(self):
        '''Works for EYE mode only, Reads all availible data for the data on the screen and saves it to a dict'''
        eyedic={}
        eyedic['EYE_Amplitude'] = float(self.instr.ask(':meas:cgr:AMPLitude?'))
        eyedic['EYE_Height'] = float(self.instr.ask(':meas:cgr:eheight?'))
        eyedic['EYE_Width'] = float(self.instr.ask(':meas:cgr:ewidth?'))
        eyedic['EYE_Cross'] =float( self.instr.ask(':meas:cgr:crossing?'))
        eyedic['EYE_Rise'] = float(self.instr.ask(':meas:cgr:risetime?'))
        eyedic['EYE_Fall'] = float(self.instr.ask(':meas:cgr:fall?'))
        eyedic['EYE_1level'] = float(self.instr.ask('meas:cgr:olevel?'))
        eyedic['EYE_0level'] =float( self.instr.ask(':meas:cgr:zlevel?'))
        eyedic['EYE_DCDDIST'] = float(self.instr.ask(':MEASURE:CGRADE:crossing?'))
        eyedic['EYE_RMS'] = (self.instr.ask(':MEASURE:eye:rj?'))
        eyedic['EYE_PP'] = (self.instr.ask(':MEASURE:eye:dj?'))
        eyedic['EYE_BITRATE'] = float(self.instr.ask(':meas:cgr:BITRate?'))
        return eyedic
    ##############################################################################################################################################
    def SaveEyeModeMaskData(self):
        '''Works for EYE mode only, Reads all availible data for the data on the screen and saves it to a dict'''
        eyedic={}
        eyedic['EYE_Amplitude'] = float(self.instr.ask(':meas:cgr:AMPLitude?'))
        eyedic['EYE_Height'] = float(self.instr.ask(':meas:cgr:eheight?'))
        eyedic['EYE_Width'] = float(self.instr.ask(':meas:cgr:ewidth?'))
        eyedic['EYE_Cross'] =float( self.instr.ask(':meas:cgr:crossing?'))
        eyedic['EYE_Rise'] = float(self.instr.ask(':meas:cgr:risetime?'))
        eyedic['EYE_Fall'] = float(self.instr.ask(':meas:cgr:fall?'))
        eyedic['EYE_1level'] = float(self.instr.ask('meas:cgr:olevel?'))
        eyedic['EYE_0level'] =float( self.instr.ask(':meas:cgr:zlevel?'))
        eyedic['EYE_DCDDIST'] = float(self.instr.ask(':MEASURE:CGRADE:DCDistortion?'))
        self.instr.write(':measure:eye:jitterFormat RMS')
        eyedic['EYE_RMS'] = float(self.instr.ask(':MEASURE:CGRADE:JITTER?'))
        self.instr.write(':measure:eye:jitterFormat PP')
        eyedic['EYE_PP'] = float(self.instr.ask(':MEASURE:CGRADE:JITTER?'))
        eyedic['EYE_BITRATE'] = float(self.instr.ask(':meas:cgr:BITRate?'))
        
        #mask specific reads
        eyedic['EYE_Mhits_centerpoly']= float(self.instr.ask(':MEASURE:MTEST:Hregion1?'))
        eyedic['EYE_Mhits_onelevelpoly']= float(self.instr.ask(':MEASURE:MTEST:Hregion2?'))
        eyedic['EYE_Mhits_zerolevelpoly']= float(self.instr.ask(':MEASURE:MTEST:Hregion3?'))
        eyedic['EYE_Mhits_total']= float(self.instr.ask(':MEASURE:MTESt:hits?'))
        eyedic['EYE_TotalWaveforms']= float(self.instr.ask(':MEASURE:MTESt:nWAVeforms?'))
        eyedic['EYE_SamplesperUI']= float(self.instr.ask(':MEASURE:MTESt:nsamples?'))
        eyedic['EYE_Margin'] = float(self.instr.ask(':MEASURE:MTESt:MARgin?'))
        
        
        return eyedic

    ##############################################################################################################################################
    def SaveOscilliscopeModeData(self):
        '''Works for Oscilliscope mode only, Reads all availible data for the data on the screen and saves it to a dict'''
        OscilliscopeDic={}
        OscilliscopeDic['OSCill_VPPAMPLITUDE'] = float(self.instr.ask(':meas:osc:vpp?'))
        OscilliscopeDic['OSCill_DUTYCYCLE'] = float(self.instr.ask(':meas:osc:duty?'))
        OscilliscopeDic['OSCill_AMPLITUDE'] = float(self.instr.ask(':meas:osc:vamp?'))
        OscilliscopeDic['OSCill_VTOP'] = float(self.instr.ask(':meas:osc:vtop?'))
        OscilliscopeDic['OSCill_VBOTTOM'] = float(self.instr.ask(':meas:osc:vbase?'))
        OscilliscopeDic['OSCill_VMAX'] = float(self.instr.ask(':meas:osc:vmaximum?'))
        OscilliscopeDic['OSCill_VMIN'] = float(self.instr.ask(':meas:osc:vminimum?'))
        self.instr.write(':meas:oscilloscope:vaverage:area cycle') #sets up vaverage to be determined by one cycle
        OscilliscopeDic['OSCill_VAVERAGE'] = float(self.instr.ask(':meas:osc:vaverage?'))
        OscilliscopeDic['OSCill_Rise'] = float(self.instr.ask(':meas:osc:ris?'))
        OscilliscopeDic['OSCill_Fall'] = float(self.instr.ask(':meas:osc:fall?'))
        OscilliscopeDic['OSCill_OVERSHOOT'] = float(self.instr.ask(':meas:osc:over?')) #this goes by the first edge on the screen so it can be based on Vtop or Vbottom
        OscilliscopeDic['OSCill_PRESHOOT'] = float(self.instr.ask(':meas:osc:preshoot?')) #this goes by the first edge on the screen so it can be based on Vtop or Vbottom
        OscilliscopeDic['OSCill_FREQ'] = float(self.instr.ask(':meas:osc:freq?'))
        OscilliscopeDic['OSCill_PERIOD'] = float(self.instr.ask(':meas:osc:PERiod?'))
        self.instr.write(':meas:osc:jitter:format  PP') # set up jitter measurement
        OscilliscopeDic['OSCill_JitterPP'] = float(self.instr.ask(':meas:osc:jitter?'))#this is measured on the first complete rise or fall edge
        self.instr.write(':meas:osc:jitter:format  RMS') # set up jitter measurement
        OscilliscopeDic['OSCill_JitterRMS'] = float(self.instr.ask(':meas:osc:jitter?'))
        
        
        return OscilliscopeDic
    ##############################################################################################################################################
    def SaveJitterModeData(self):
        '''Works for Jitter mode only, Reads all availible data for the data on the screen and saves it to a dict
           Assumes that the scope has the Amplitude analysis software add-on installed and enabled'''
        jitterdic={}
        jitterdic['JITTER_DJ'] = float(self.instr.ask(':meas:jitt:dj?'))
        jitterdic['JITTER_RJ'] = float(self.instr.ask(':meas:jitt:rj?'))
        jitterdic['JITTER_TJ'] = float(self.instr.ask(':meas:jitt:tj?'))
        jitterdic['JITTER_DCD'] = float(self.instr.ask(':meas:jitt:dcd?'))
        jitterdic['JITTER_DDJ'] = float(self.instr.ask(':meas:jitt:ddj?'))
        jitterdic['JITTER_ISI'] = float(self.instr.ask(':meas:jitt:isi?'))
        jitterdic['JITTER_PJ'] = float(self.instr.ask(':meas:jitt:pj?'))
        jitterdic['JITTER_PJrms'] = float(self.instr.ask(':meas:jitt:pjrms?'))
        jitterdic['JITTER_BUJRMS'] = float(self.instr.ask(':meas:jitt:bujrms?'))
        jitterdic['JITTER_BERAmp'] = float(self.instr.ask(':meas:ampl:samp?'))
        jitterdic['JITTER_VertEyeOpen'] = float(self.instr.ask(':MEASure:AMPLitude:EOPening?'))
        jitterdic['JITTER_ONE_LVL'] = float(self.instr.ask(':meas:ampl:olev?'))
        jitterdic['JITTER_ZERO_LVL'] = float(self.instr.ask(':meas:ampl:zlev?'))
        jitterdic['JITTER_TI_ONE_LVL'] = float(self.instr.ask(':MEASURE:AMPLITUDE:TIONEs?'))#TI stands for total interference for specified level
        jitterdic['JITTER_TI_ZERO_LVL'] = float(self.instr.ask(':MEASURE:AMPLITUDE:TIZEROs?'))
        jitterdic['JITTER_DI_ONE'] = float(self.instr.ask(':MEASURE:AMPLITUDE:DIONEs?')) #deterministic interference
        jitterdic['JITTER_DI_ZERO'] = float(self.instr.ask(':MEASURE:AMPLITUDE:DIZEROs?'))
        jitterdic['JITTER_ISI_ONE'] = float(self.instr.ask(':MEASURE:AMPLITUDE:ISIONEs?'))#isi of the one's
        jitterdic['JITTER_ISI_ZERO'] = float(self.instr.ask(':MEASURE:AMPLITUDE:ISIZEROs?'))#isi of the zero's
 

        
        # return the signed value of DCD based on one/zero interference levels values found above...
        if jitterdic['JITTER_TI_ONE_LVL']<9.9e37:
            if jitterdic['JITTER_TI_ONE_LVL'] > jitterdic['JITTER_TI_ZERO_LVL']: 
                jitterdic['JITTER_DCDSIGNED'] = -1 *jitterdic['JITTER_DCD'] 
            else:
                jitterdic['JITTER_DCDSIGNED'] = jitterdic['JITTER_DCD']
        else:
            jitterdic['JITTER_DCDSIGNED']=0
        return jitterdic
    ##############################################################################################################################################
    def Get_Rj(self):
        Rj = float(self.instr.ask(':meas:jitt:rj?'))
        
        return Rj          
    ##############################################################################################################################################
    def Get_tj(self):
        tj = float(self.instr.ask(':meas:jitt:tj?'))
        
        return tj          
    ##############################################################################################################################################
    def Get_dcd(self):
        dcd = float(self.instr.ask(':meas:jitt:dcd?'))
        
        return dcd  
        
    ##############################################################################################################################################
    def Get_dj(self):
        DJ = float(self.instr.ask(':meas:jitt:dj?'))
        
        return DJ            
    ##############################################################################################################################################
    def Get_ddj(self):
        ddj = float(self.instr.ask(':meas:jitt:ddj?'))
        
        return ddj          
    ##############################################################################################################################################
    def Get_isij(self):
        isi = float(self.instr.ask(':meas:jitt:isi?'))
        
        return isi          
    ##############################################################################################################################################
    def Get_pj(self):
        pj = float(self.instr.ask(':meas:jitt:pj?'))
        
        return pj  
    ##############################################################################################################################################
    def Get_pjrms(self):
        pjrms = float(self.instr.ask(':meas:jitt:pjrms?'))
        
        return pjrms 
    ##############################################################################################################################################
    def Get_bujrms(self):
        bujrms = float(self.instr.ask(':meas:jitt:bujrms?'))
        
        return bujrms
    ##############################################################################################################################################
    def MeasureTDelay_Chann1rise_to_Chann2rise(self):
        '''this function measure the time delay in seconds from the trigger to the first rising edge of channel1 and the delay from trigg
        for the first rising edge of channel2.  Channel2 result is subtracted from channel 1 to give the time skew between the two
        edges.  This requires that the scope be in oscilliscope mode, with channel1 and 2 on.  Both must display one rising edge '''
        delayfromtrig_chann1 = self.instr.ask(':MEASure:tedge? midd, +1, chan1')
        delayfromtrig_chann2 = self.instr.ask(':MEASure:tedge? midd, +1, chan2')
        tdelay= delayfromtrig_chann1 - delayfromtrig_chann2
        return tdelay
    ##############################################################################################################################################
    def StoreInstrumentSetup(self,memnum ):
        '''stores the state of the instrument to one of the  0-9 locations'''
        self.instr.write(':STORe:SETup %d' %memnum)
    ##############################################################################################################################################
    def RecallInstrumentSetup(self,pathfile_setx ):
        '''recalls the state of the instrument to that of the setup file'''
        self.instr.write('disk:setup:recall %s' %pathfile_setx)
    ##############################################################################################################################################
    def RecallInstruSetupNum(self,setupNum ):  #for recalling DCAJ setups 0 to 9 for setup0.set thru setup9.set
        '''recalls the state of the instrument to that of the setup file'''
        self.instr.write(':RECall:SETup %s' %setupNum)
    ##############################################################################################################################################
    def LoadMask(self, filemsk):
        ''' Mask should be loaded in directories A,  D_User Files, C:_scope_masks and any mapped network drive. file_nameis the
        filename, with the extension .msk or .pcm. :MTESt:LOAD FILE1.MSK'''
        self.instr.write(':MTESt:LOAD %s' %filemsk)
    ##############################################################################################################################################
    def AlignMask(self):
        '''loads mask that is in a directory...'''
        self.instr.write(':MTESt:ALIGn')
    ##############################################################################################################################################
    def MaskSamples(self):
        '''total number of samples captured in the current mask test run'''
        self.instr.write(':MTEST:COUNT:SAMPLES?')
    ##############################################################################################################################################
    def MaskHits(self):
        '''Automatically aligns and scales the mask to the current waveform.'''
        hits = self.instr.ask(':MTEST:COUNT:HITS? total')
        return (hits)
    ##############################################################################################################################################
    def screenshot_toPC(self, file_name):
        '''Take a screen shot and save it to a JPG file, must have directory set???? '''
        #current issue with this code, only works first time, can't write over an existing file on the scope
        #the delete command doesn't work on new flexdca software
        #also must set the output directory on pc prior to running this command....
        
        self.instr.write(':Disk:simage:invert ON')
        #self.instr.write(':Disk:simage:Fname "D:\\User Files\\Screen Images\\temp.jpg"')
        #self.instr.write(':Disk:simage:Fnam "temp.jpg"')
        path_name='"' + 'D:\\User Files\\Screen Images\\' + file_name + '"'
        self.instr.write(':Disk:simage:Fname %s' %path_name)
        self.instr.write(':Disk:sim:save')

        data = self.instr.ask(':Disk:bfile? %s' %path_name)
        
        #Delete the temp file from the scope so next time it will write properly
        #self.instr.write(':Disk:delete "D:\\User Files\\Screen Images\\temp.jpg"')
        '''
        data = data[1:]    # Remove starting "#" of the GPIB definite length block encoding
        length_field_length = int(data[0])
        image_data_length = int(data[1:1+length_field_length])
        data = data[1+length_field_length:]
        image_data = data[:image_data_length]
        try:
            file_handle = open(file_name, 'wb+')
            file_handle.write(image_data)
            file_handle.close()
        except:
            msg = 'Cannot save oscilloscope screenshot to '+file_name
            raise IOError(msg)'''
        
    ##############################################################################################################################################
    def screenshot(self, file_name):
        '''Take a screen shot and save it to a JPG file, must have directory set in D:\User Files
            can add a dir as part of file name to be a subset of the screen images folder  
            but the directory has to already exist on the system for this command to work
            the mkdir command is not part of the new flex dca software   '''
        self.instr.write(':Disk:simage:invert ON')
        path_name='"' + 'D:\\User Files\\Screen Images\\' + file_name + '"'
        self.instr.write(':Disk:simage:Fname %s' %path_name)
        self.instr.write(':Disk:sim:save')
        time.sleep(1)
        
        '''
        data = self.instr.ask(':Disk:bfile? %s' %path_name)
        data = data[1:]    # Remove starting "#" of the GPIB definite length block encoding
        length_field_length = int(data[0])
        image_data_length = int(data[1:1+length_field_length])
        data = data[1+length_field_length:]
        image_data = data[:image_data_length]
        try:
            file_handle = open(file_name, 'wb+')
            file_handle.write(image_data)
            file_handle.close()
        except:
            msg = 'Cannot save oscilloscope screenshot to '+file_name
            raise IOError(msg)'''
   
    ##############################################################################################################################################
    def save_jitterfile(self, file_name):
        '''Save the scope generated jitter file, send data over gpib...needs work '''
        self.instr.write(':Disk:jdatabase:fformat text')
        #self.instr.write(':disk:jdatabase:Fname "temp.csv"')
        path_name='"' + 'D:\\User Files\\Jitter Data\\' + file_name + '"'

        self.instr.write(':disk:jdatabase:Fname %s' %path_name)
        self.instr.write(':disk:jdatabase:save')

        #could transfer file but only if the text file is very small, PRBS7 was too big
        #data = self.instr.ask(':Disk:tfile? "temp.csv"')
        #quotefilename = 'copy "%s" ' % file_name
        #data = self.instr.ask(':Disk:tfile? %s' %quotefilename)
    ##############################################################################################################################################
    def save_waveform_database(self, source, file_name):
        '''Save the scope generated waveform database, must be in eye or scope mode with extention *.wfmx '''
        self.instr.write(':Disk:waveform:save:source %s' %source)
        #self.instr.write(':disk:jdatabase:Fname "temp.csv"')
        path_name='"' + 'D:\\User Files\\Waveforms\\' + file_name + '"'

        self.instr.write(':disk:waveform:Fname %s' %path_name)
        self.instr.write(':disk:waveform:save')
    ##############################################################################################################################################
    def save_waveformcolorgrade_database(self, source, file_name):
        '''Save the scope generated waveform database, must be in eye mode with extention *.cgsx
            Used to recall and do mask testing '''
        self.instr.write(':Disk:waveform:save:source %s' %source)
        #self.instr.write(':disk:jdatabase:Fname "temp.csv"')
        path_name='"' + 'D:\\User Files\\Colorgrade-Grayscale\\' + file_name + '"'

        self.instr.write(':disk:eye:Fname %s' %path_name)
        self.instr.write(':disk:eye:save')
    ##############################################################################################################################################
    def save_jitter_database(self, source, file_name):
        '''Save the scope generated waveform database, must be in jitter mode with extention *.jdx
            Used to recall and do mask testing '''
        self.instr.write(':Disk:jdatabase:fformat internal')
        self.instr.write(':Disk:jdatabase:source %s' %source)
        #self.instr.write(':disk:jdatabase:Fname "temp.csv"')
        path_name='"' + 'D:\\User Files\\Jitter Data\\' + file_name + '"'

        self.instr.write(':disk:jdatabase:Fname %s' %path_name)
        self.instr.write(':disk:jdatabase:save')


        
