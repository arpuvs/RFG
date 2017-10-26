# Predefined variables and functions
# evalapp - the eval app XML object
# topwin - the main frame class
# readAll - read all interfaces of all chips
# writeAll - write all settings to all chips
# getSavePath - ask the user for a path to save a file
# getOpenPath - ask the user for a path to open a file
# unloadBoards - unload the currently loaded boards
# loadBoard - load a new board from XML
# ProgressDialog - a class for showing progress of your script
#from GPIBObject import GPIBObject as GPIBObject
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass

#class TekBSA125B(GPIBObject):
#    def __init__(self, addr=-3):
#        GPIBObject.__init__(self, 'TEKTRONIX,BSA125B',addr)
 
class TekBSA125B(GPIBObjectBaseClass):
    def __init__(self, addr=-3):
        GPIBObjectBaseClass.__init__(self, 'TEKTRONIX,BSA125B',addr)
    
    def Cal_Gen_Delay_ack(self):        #calibrate generator at the present data rate and waits for done
        self.instr.write("GEN:PCAL") #Generator Data +\- outputs are not linked
        state= self.instr.ask("RSTATE?") 
        self.instr.write("GEN:PCAL") #Generator Data +\- outputs are not linked
        state= self.instr.ask("RSTATE?")                      
    
    def Cal_Gen_Delay(self):        #calibrate generator at the present data rate
        self.instr.write("GEN:PCAL") #Generator Data +\- outputs are not linked
    
    def Link_Data_Disable(self):
        self.instr.write("GEN:DOUT:LPNS 0") #Generator Data +\- outputs are not linked
    
    def Link_Data_Enable(self):
        self.instr.write("GEN:DOUT:LPNS 1") #Generator Data +\- outputs are linked
        
    def Link_Clock_Disable(self):
        self.instr.write("GEN:COUT:LPNS 0") #Clock Data +\- outputs are not linked
    
    def Link_Clock_Enable(self):
        self.instr.write("GEN:COUT:LPNS 1") #Clock Data +\- outputs are linked
    
    def Gen_RefIn_enable(self,enable):
        if enable:    self.instr.write("GENerator:REFIN:ENABLE 1") #enable the generator ref input
        if enable==0: self.instr.write("GENerator:REFIN:ENABLE 0") #disable the generator ref input
    
    def Gen_RefIn_freq(self,freq):    #10,25,100,106.25,156.25,133.33,166.67 or 200 MHz)         
        self.instr.write("GENerator:REFIN:FREQuency " +str(freq))    
    
    def Data_Disable(self):        
        self.instr.write("GEN:DOP:ENAB 0") #Turn off DataP 
        self.instr.write("GEN:DON:ENAB 0") #Turn off DataN
        
    def Data_Enable(self):
        self.instr.write("GEN:DOP:ENAB 1") #Turn on DataP 
        self.instr.write("GEN:DON:ENAB 1") #Turn on DataN
        
    def Clock_Disable(self):
        self.instr.write("GEN:COP:ENAB 0") #Turn off ClockP 
        self.instr.write("GEN:CON:ENAB 0") #Turn off ClockN 
        
    def Clock_Enable(self):
        self.instr.write("GEN:COP:ENAB 1") #Turn on ClockP 
        self.instr.write("GEN:CON:ENAB 1") #Turn on ClockN
        
    def Data_Termination_GEN(self,dpterm,dnterm):  
        self.instr.write("GEN:DOP:TVOL " +str(dpterm)) # mV Termination for DataP
        self.instr.write("GEN:DON:TVOL " +str(dnterm)) # mV Termination for DataN
        
    def Data_Termination_DET(self,dpterm):  
        self.instr.write("DET:DINP:TVOL " +str(dpterm)) # mV Termination for DataP
        #self.instr.write("DET:DON:TVOL" +str(dnterm)) # mV Termination for DataN
            
    def Clock_Termination(self,cpterm,cnterm):    
        self.instr.write("GEN:COP:TVOL " +str(cpterm)) #  mV Termination for ClockP 
        self.instr.write("GEN:CON:TVOL " +str(cnterm)) #  mV Termination for ClockN
        
    def Clock_Offset(self,cpoffset,cnoffset):   
        self.instr.write("GEN:COP:SLOF " +str(cpoffset)) #  mV Offset for DataP
        self.instr.write("GEN:CON:SLOF " +str(cnoffset)) #  mV Offset for DataN
      
    def Data_Offset(self,dpoffset,dnoffset):     
        self.instr.write("GEN:DOP:SLOF " + str(dpoffset)) # mV Offset for ClockP
        self.instr.write("GEN:DON:SLOF " + str(dnoffset)) # mV Offset for ClockN
        
    def Clock_Amplitude(self,cpamp,cnamp):
        self.instr.write("GEN:COP:SLAM " +str(cpamp)) #  mV  Amplitude for ClockP
        self.instr.write("GEN:CON:SLAM " +str(cnamp)) #  mV  Amplitude for ClockN   

    def Data_Amplitude(self,dpamp,dnamp):
        self.instr.write("GEN:DOP:SLAM " +str(dpamp)) #  mV  Amplitude for DataP
        self.instr.write("GEN:DON:SLAM " +str(dnamp)) #  mV  Amplitude for DataN  
        
    def Restore_ConfigButton(self,fpath,fname):
        self.instr.write('RCONfiguration "' + fpath + fname +'"') #restores configuration 
            
    def Save_ConfigButton(self,fpath,fname):
        self.instr.write('SCONFiguration "' + fpath + fname +'"') #saves configuration
        
    def Sine_Jitter_Enable(self):
        self.instr.write("GSM:SJitter:Enable 1") #1 = Enable 0 =  Disalbed
    
    def Sine_Jitter_Disable(self):
        self.instr.write("GSM:SJitter:Enable 0") #1 = Enable 0 =  Disable
        
    def Sine_Freq_Amp(self,sineFreq,sineAmp):             
        self.instr.write("GSM:SJitter:FREQ " +str(sineFreq)) #sets adjust frequency
        self.instr.write("GSM:SJitter:AMPU " +str(sineAmp)) #sets amplitude of frequency based on percentage of UI           
  
    def Sine_Freq(self,sineFreq):             
        self.instr.write("GSM:SJitter:FREQ " +str(sineFreq)) #sets adjust frequency
        
    def Sine_Amp(self,sineAmp):             
        self.instr.write("GSM:SJitter:AMPU " +str(sineAmp)) #sets amplitude of frequency based on percentage of UI           
       
    def check_if_sine_MOD_enab(self):
        return float(self.instr.ask("GSM:SJ:ENAB?"))  
    
## OLD    def get_Jitter_sine_ampl(self):
##        return float(self.instr.ask("GSM:SJitter:AMPUi?"))      
    
    def get_Jitter_sine_ampl(self):
        line=(self.instr.ask("GSM:SJitter:AMPUi?"))    
        nuVal=""
        for x in xrange(12):
            nuVal= nuVal + line[x]
            if(line[x+1] == " " ):
                break
        myfloat = float(nuVal)
        return myfloat
          
    def PMMOD_Freq(self,freq):             
        self.instr.write("GEN:PMMOD:FREQ " +str(freq)) #sets adjust frequency 
        
    def PMMOD_Jit_Amp(self,amp):
        self.instr.write("GEN:PMMOD:DEV " +str(amp))        
        
    def check_if_PM_MOD_enab(self):
        return float(self.instr.ask("GEN:PMMOD:ENAB?"))                    
     
    def PMMod_Jitter_Disable(self):
        self.instr.write("GEN:PMMOD:ENAB 0") #1 = Enable 0 =  Disabled      

    def PMMod_Jitter_Enable(self):
        self.instr.write("GEN:PMMOD:ENAB 1") #1 = Enable 0 =  Disabled   
        
    def get_Jitter_PMMOD_ampl(self):
        return float(self.instr.ask("GEN:PMMOD:DEV?"))             
     
    def SineLF_Jitter_Enable(self):
        self.instr.write("GSM:LFSJ:ENABLE 1") #1 = Enable 0 =  Disalbed
    
    def SineLF_Jitter_Disable(self):
        self.instr.write("GSM:LFSJ:ENABLE 0") #1 = Enable 0 =  Disable
        
    def SineLF_Freq_Amp(self,sineFreq,sineAmp):             
        self.instr.write("GSM:LFSJ:FREQ " +str(sineFreq)) #sets adjust frequency
        self.instr.write("GSM:LFSJ:AMPPS " +str(sineAmp)) #sets amplitude of frequency based on percentage of UI           
           
    def Sinusodial_Interference_Enable(self):
        self.instr.write("GSM:SI:ENAB 1") #1 = Enable,   0 =  Disabled
         
    def Sinusodial_Interference_Disable(self):
        self.instr.write("GSM:SI:ENAB 0") #1 = Enable,   0 =  Disabled
            
    def Sinusodial_Interference(self,interFreq,interAmp): 
        self.instr.write("GSM:SInterference:AMPL " +str(interAmp)) #Sinusoidal interference amplitude 100,000,000 to  2,5000,000,000            
        self.instr.write("GSM:SInterference:FREQ " +str(interFreq)) #Sinusoidal interference amplitude 10 to  400        
   
    def Random_Jitter_Enable(self):
        self.instr.write("GSM:RJitter:Enable 1") #1 = Enable 0 =  Disalbed
    
    def Random_Jitter_Disable(self):
        self.instr.write("GSM:RJitter:Enable 0") #1 = Enable 0 =  Disable   
   
    def Random_Jitter_Freq(self,randomFreq,randomAmp):
        self.instr.write("GSM:RJitter:FREQ " +str(randomFreq)) #sets adjust frequency
        self.instr.write("GSM:RJitter:AMPU " +str(randomAmp)) #sets amplitude of frequency

    def BUJ_Enable(self):
        self.instr.write("GSM:BUJitter:Enable 1") #1 = Enable 0 =  Disalbed
        
    def BUJ_Disable(self):
        self.instr.write("GSM:BUJitter:Enable 0") #1 = Enable 0 =  Disalbed
        
    def BUJ_Jitter_Freq_Amp(self,bujFreq,bujAmp):
        self.instr.write("GSM:BUJitter:FREQ " +str(bujFreq)) #sets adjust frequency in Hz
        self.instr.write("GSM:BUJitter:AMPU " +str(bujAmp)) #sets amplitude of frequency %UI 
    
    def Global_Stress_Disable(self):
        self.instr.write("GSM:Stress:Enable 0") #global stress disabled
        
    def Global_Stress_Enable(self):
        self.instr.write("GSM:Stress:Enable 1") #global stress enabled

    def Synth_Bit_Rate(self,synthBitRate):
       #scope1.write("GEN:ICL 9953000000") #Sets internal synthesizer to 9.953GHz
        self.instr.write("GEN:ICL " +str(synthBitRate)) #Sets internal synthesizer to 9.953GHz            
        self.instr.write("GEN:CSEL INT")

    def Synth_Bit_Rate_Get(self):
        return float(self.instr.ask("GENerator:DRATe?")) #Get ISI on primary channel BSAITS125.         
  
    def Divider(self,divider):
        self.instr.write("GEN:CLKDIV " +str(divider)) #Set value of clock Divider #1,2,4,8,16,32,64,128          

    def SubRate(self,subrate):
        self.instr.write("GEN:SUBR " +str(subrate)) #sets sub rate clock output divider for Generator internal clock synth
                                       #1,2,4,8,16,32,64,128.  1 is full rate
    def Error_Inject_Manual(self,event):
        self.instr.write("GENerator:EIMode MANual") #Manual Mode
        
    def Error_Inject_Continuous(self,event):
        self.instr.write("GENerator:EIMode CONT") #Continuous Mode

    def Error_Inject_OFF(self,event):
        self.instr.write("GENerator:EIMode OFF") #Continuous Mode

    def set_min_Err_inject_interval(self):
        self.instr.write("GEN:EIET 1BIT") #Continuous Mode

    def set_min_Err_inject_32bits_interval(self):
        self.instr.write("GEN:EIET 32BITS") #Continuous Mode

    def LoadMask(self,fpath,fname):
        #fpath ='D:\\BitAlyzer\\Mask\\JESD204B\\'
        #fname = 'OIF-CEI-26G-C.msk'           
        self.instr.write('MASK:MFName ' + '"' + fpath + fname  + '"') #Loads Mask file remotely

    def SaveMask(self,fpath,fname):
        #fpath ='D:\\BitAlyzer\\Mask\\JESD204B\\'
        #fname = 'OIF-CEI-26G-C.msk'
        self.instr.write('MASK:SMW ' + '"' + fpath + fname  + '"') #Saves Mask File remotely
            
    def EyeAutoScale(self):
        self.instr.write("EYE:ASCale") #Autoscales Eye Mask Screen on Bert Scope
        
    def Det_AutoAlign(self):
        self.instr.write('DET:PDC')
    
    def Det_AutoAlign_done(self):
        return float(self.instr.ask('DET:DCS?'))
    
    def Det_AutoAlign_sync(self):
        return float(self.instr.ask('DET:ISYNC?'))
            
    def DetectorClkDiv(self, event):
        self.instr.write("DETector:FULLRateclock 1")  #1 Detector is Full Rate Clock Mode  -  0 Detector is Half Rate Clock Mode
        
    def Jitter_units_perUI(self):
        self.instr.write("JMAP:JUNITS PERCENTUI")  #sets units for jitter map to percent UI
    
    def Jitter_P_P(self):
        return float(self.instr.ask("EYE:MVALue:JITTer?")) #Returns the Jitter P-P Query Only.

    def Jitter_RMS(self):
        return float(self.instr.ask("EYE:MVALue:JRMS?")) #Returns the Eye Jitter RMS Query Only.        
    
    def Jitter_BUJ(self):
        return float(self.instr.ask("JMAP:BUJ?")) #Returns the BUJ Query Only. 
        
    def Jitter_BUJ_Locked(self):
        return float(self.instr.ask("JMAP:BUJLOCKED?")) #Returns the BUJ Locked Query Only.
        
    def Jitter_DDJ(self):
        return float(self.instr.ask("JMAP:DDJ?")) #Returns the Data-Dependent Jitter Query Only.
            
    def Jitter_DJ(self):
        return float(self.instr.ask("JMAP:DJ?")) #Returns the Deterministic Jitter Query Only.   
        
    def Jitter_EJ(self):
        return float(self.instr.ask("JMAP:EJ?")) #Returns the EJ Locked Jitter Query Only. 
            
    def Jitter_EJTROF(self):
        return float(self.instr.ask("JMAP:EJTROF")) #Returns the Emphasis Jitter Transition Offset Query Only. 
        
    def Jitter_RJ(self):
        return float(self.instr.ask("JMAP:RJ?")) #Returns the Random Jitter Query Only. 
        
    def Jitter_TJ(self):
        return float(self.instr.ask("JMAP:TJ?")) #Returns the TJ Jitter Query Only. 
    
    def Jitter_ISI(self):
        return float(self.instr.ask("JMAP:ISI?")) #Returns the TJ Jitter Query Only. 
        
    def Jitter_DJIT(self):
        return float(self.instr.ask("JMAP:DJIT?")) #Returns the Deterministic Jitter Query Only. 
        
    def Jitter_Clear(self):
        self.instr.write("JITTer:CLEar") #Clear Jitter
        
    def Gen_Pattern(self,type):
        self.instr.write("GEN:PATT " +str(type)) #set pattern PN15 or PN7 and so on
        
    def Det_Pattern(self,type):
        self.instr.write("DET:PATT " +str(type)) #set pattern PN15 or PN7 and so on
        
    def Jitter_BER(self, BER):
        self.instr.write("JMAP:PPBEr " +str(BER)) #sets jitter map BER
    
    def DET_Run(self):
        self.instr.write("DET:RUIN 20") #Sets Run state to 20 seconds
        self.instr.write("RSTATE 1") #1 Starts Jitter; 0 Stops Jitter      
    def Jitter_Run(self):
        self.instr.write("DET:RUIN 20") #Sets Run state to 20 seconds
        self.instr.write("MASK:RSTATE 1") #1 Starts Jitter; 0 Stops Jitter
        
    def RUN(self):
        self.instr.write("MASK:RSTATE 1") #1 Starts 
        
    def STOP(self):
        self.instr.write("MASK:RSTATE 0") #1 Starts 
            
    def JMAP_Run(self):
        self.instr.write("JMAP:RUNMODE NORMAL") #Run IN Normal Mode
            
    def Detector_Bits(self):
        return float(self.instr.ask("DET:BITS?")) #Returns number of bits passed from duration run
        
    def Detector_Errors(self):
        return float(self.instr.ask("DET:ERR?")) #Returns number of error bits from duration run
        
    def Detector_DataCenter_Amplitude(self):
        return float(self.instr.ask("DETector:DCAMv?")) #Retrieve the data center amplitude in mV. Query only.
    
    def View_Eye(self):
        self.instr.write("View Eye") #view eye diagram
        
    def View_Det(self):
        self.instr.write("View Detector") #view detector 
        
    def View_Generator(self):
        self.instr.write("View Generator") #view detector 
        
    def View_JitterMap(self):
        self.instr.write("View JMAP_MAP") #view detector
        
    def View_StressedEye(self):
        self.instr.write("View STRESSedeye") #view detector
        
    def View_Mask(self):
        self.instr.write("View MASK") #view detector
    
    def Detector_EYE_Amplitude(self):
        return float(self.instr.ask("EYE:MVAL:AMPL?")) #Retrieve the eye amplitude
    
    def Detector_EYE_Voffset(self):
        return float(self.instr.ask("EYE:MVAL:VOFS?")) #Retrieve the eye amplitude
   
    def Detector_DataCenterUnit_Int(self):
        return float(self.instr.ask("DETector:DCUinterval?")) #Retrieve the data center unit interval. Query only. 
        
    def Mask_Center_Errors(self):
        return float(self.instr.ask("MASK:CPERrors?")) #Retrieve Mask Test Center Polygon Errors. Query only.
        
    def Mask_Lower_Errors(self):
        return float(self.instr.ask("MASK:LPERrors?")) #Retrieve Mask Test Lower Polygon Errors. Query only.
 
    def Mask_Upper_Errors(self):
        return float(self.instr.ask("MASK:UPERrors??")) #Retrieve Mask Test Upper Polygon Errors. Query only.

    def Eye_Time_Center_Offset(self,time_offset):
        self.instr.write("EYE:TCOFfset " +str(time_offset)) #Set the Eye center time offset of the Eye view.   

    def Eye_Time_Offset(self,time_offset):
        self.instr.write("EYE:TOOFfset " +str(time_offset)) #Set the time offset of the Eye view.  
        
    def ISI_Primary_SET(self,mode):
        self.instr.write("STRCmb:PRIIsi " +str(mode)) #Set ISI on primary channel BSAITS125. 
        
    def ISI_Secondary_SET(self,mode):
        self.instr.write("STRCmb:SECIsi " +str(mode)) #Set ISI on secondary channel BSAITS125.
    
    def ISI_PRIM_SEC_SET(self,mode):
        self.instr.write("STRCmb:CMBIsi " +str(mode)) #Set ISI when primary and secondary channels are linked 
        
    def EXT_Loss_SET(self,mode):
        self.instr.write("STRCmb:EXT1 " +str(mode)) #Set EXT loss BSAITS125.
        
    def CABLE_LOSS_SET(self,mode):
        self.instr.write("STRCmb:CABLoss " +str(mode)) #Set cable loss BSAITS125.
    
    def LINK_PRIM_SEC(self,mode):
        self.instr.write("STRCmb:LINKprisec " +str(mode)) #to link primary and secondary set to 1
         
    def REF_FREQ_SET(self,mode):
        self.instr.write("STRCmb:DATAhzauto " +str(mode)) #Set reference frequency BSAITS125.
        
    def ISI_Primary_Get(self,mode):
        return float(self.instr.ask("STRCmb:PRIIsi?")) #Get ISI on primary channel BSAITS125. 
        
    def ISI_Secondary_GET(self,mode):
        return float(self.instr.ask("STRCmb:SECIsi?")) #Get ISI on secondary channel BSAITS125.
        
    def EXT_Loss_GET(self,mode):
        return float(self.instr.ask("STRCmb:EXT1?")) #Get EXT loss BSAITS125.
        
    def CABLE_LOSS_GET(self,mode):
        return float(self.instr.ask("STRCmb:CABLoss?")) #Get cable loss BSAITS125.
       
    def REF_FREQ_GET(self,mode):
        return float(self.instr.ask("STRCmb:DATAhzauto?")) #Get reference frequency BSAITS125.   
    
    def IDN ( self ) :
        '''This function returns the identity of the Bertscope '''
        id= self.instr.ask( "*IDN?" ) 
        return id        
    
