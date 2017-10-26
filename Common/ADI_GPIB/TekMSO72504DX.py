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
# REVISION HISTORY: Aug 24, 2015 Leah Magaldi made edits, added another plot type
#from GPIBObject import GPIBObject as GPIBObject
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass

import wx
#print "this is the file for the TekMSO scope"
class TekMSO72504DX(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        GPIBObjectBaseClass.__init__(self, 'TEKTRONIX,DSA72504D',addr)
		
    def ClearGPIB(self):
        self.instr.write('*CLS')
		
    def GetAcqPar(self):
        return self.instr.ask('ACQ?')
    
    def GetFreq(self):
        self.instr.write('MEASU:IMM:TYP FREQ')
        return float(self.instr.ask('MEASU:IMM:VAL?'))
    
    def MeasFreq(self, source):
        self.instr.write('MEASU:MEAS1:TYP FREQ')
        self.instr.write('MEASU:MEAS1:SOURCE CH' + str(source))
        return self.instr.ask('MEASU:MEAS1:MEAN?')
    
    def GetMeasuredMean(self,MEAS):
        #self.instr.write('MEASU:MEAS1:PKPKJitter')
        return float(self.instr.ask('MEASU:'+MEAS+':MEAN?'))
    
    def GetSRC1(self):
        print "test"
        self.instr.write('MEASU:IMM:SOURCE[10000]?')
        return float(self.instr.ask('MEASU:IMM:VAL?'))
        
    def GetSRC2(self):
        self.instr.write('MEASU:IMM:SOURCE2?')
        #return float(self.instr.ask('MEASU:IMM:VAL?'))
    
    def GetDely(self):
        self.instr.write('MEASU:IMM:TYP DEL')
        return float(self.instr.ask('MEASU:IMM:VAL?'))
    
    def GetUnits(self):
        self.instr.write('MEASU:IMM:TYP UNI?')
        return float(self.instr.ask('MEASU:IMM:VAL?'))
    
    def FastAcqOn(self):
        self.instr.write(':FastAcq:state 1')
    
    def FastAcqOff(self):
        self.instr.write(':FastAcq:state 0')  
    
    def SetJitter(self, Source):
        self.instr.write('HIS:SOU '+Source)
    
    def GetJitterPKPK(self,MEAS):
        #self.instr.write('MEASU:MEAS1:PKPKJitter')
        return float(self.instr.ask('MEASU:'+MEAS+':VAL?'))
    
    def GetJitterRMS(self,MEAS):
        #self.instr.write('MEASU:MEAS1:PKPKJitter')
        return float(self.instr.ask('MEASU:'+MEAS+':VAL?'))
    def GetMeasuredValue(self,MEAS):
        #self.instr.write('MEASU:MEAS1:PKPKJitter')
        return float(self.instr.ask('MEASU:'+MEAS+':VAL?'))
    
    def GetMeasuredMax(self,MEAS):
        #self.instr.write('MEASU:MEAS1:PKPKJitter')
        return float(self.instr.ask('MEASU:'+MEAS+':MAX?'))
    
    def GetMeasuredMin(self,MEAS):
        #self.instr.write('MEASU:MEAS1:PKPKJitter')
        return float(self.instr.ask('MEASU:'+MEAS+':MINI?'))
    
    def GetMeasuredSTD(self,MEAS):
        #self.instr.write('MEASU:MEAS1:PKPKJitter')
        return float(self.instr.ask('MEASU:'+MEAS+':STD?'))
    
    
    def SetSingle(self):
        self.instr.write('ACQuire:STOPAFTER SEQUENCE') #sets the single button
        
    def SetAcqON(self):
        print "test1"
        self.instr.write('ACQuire:STATE RUN') #sets the single button
        
    def SetAcqOFF(self):
        self.instr.write('ACQuire:STATE STOP') #sets the single button
        
    #def SetSEQ(self):
        #self.instr.write('ACQuire:STOPAFTER SEQUENCE') #sets the single button
        
    def SetTriggerEdgeSource(self,x):
        self.instr.write('TRIGger:A:EDGE:SOUrce '+str(x))  #sets horizontal trigger location 
        
    def GetTriggerEdgeSource(self):
        return self.instr.ask('TRIGger:A:EDGE:SOUrce?')  #sets horizontal trigger location 
    
    def SetTriggerEdgeSlope(self,x):
        self.instr.write('TRIGger:A:EDGE:SLOpe '+str(x))  #sets horizontal trigger location 
        
    def GetTriggerEdgeSlope(self):
        return self.instr.ask('TRIGger:A:EDGE:SLOpe?')
    
    def SetTriggerEdgeCoupling(self,x):
        self.instr.write('TRIGger:A:EDGE:COUPling '+str(x))
        
    def GetTriggerEdgeCoupling(self):
        return self.instr.ask('TRIGger:A:EDGE:COUPling?')
    
    def AcqState(self):
        return self.instr.ask('ACQ:STATE?')
        
    def SetRun(self):
        self.instr.write('ACQuire:STOPAFTER RUNSTOP') #sets run/stop  
    
    def HorizontalMode(self,x):
        self.instr.write('HORizontal:MODE ' +str(x)) # the modes are AUTO, CONSTANT, MANUAL
    def SampleRate(self,x):
        self.instr.write('HORizontal:MODE:SAMPLERATE ' +str(x)) # sets the sample rate
        
    def TimeBase(self,y):
        self.instr.write('HORizontal:MODE:SCAle '+str(y)) #sets horizontal time base
    
    def SetVertTriggerPos1(self,x):
        self.instr.write('TRIGger:A:Level:CH1 '+str(x))  #sets vertical trigger position on CH1   
        
    def SetVertTriggerPos2(self,x):
        self.instr.write('TRIGger:A:Level:CH2 '+str(x))  #ssets vertical trigger position on CH2
        
    def SetVertTriggerPos3(self,x):
        self.instr.write('TRIGger:A:Level:CH3 '+str(x))  #sets vertical trigger position on CH3
        
    def SetVertTriggerPos4(self,x):
        self.instr.write('TRIGger:A:Level:CH4 '+str(x))  #sets vertical trigger position on CH4
        
    def SetTriggerPos(self,x):
        self.instr.write('HORizontal:TRIGger:POSition '+str(x))  #sets horizontal trigger location 
        
    def GetTriggerPos(self):
        return float(self.instr.ask('HORizontal:TRIGger:POSition?'))  #gets horizontal trigger location 
        
    def SetTrigger50(self):
        self.instr.write('TRIGger:A: SETLevel')  #sets horizontal trigger location 
    
    def DelayTime(self,x):
        self.instr.write('HORizontal[:MAIn]:DELay:TIMe '+str(x))
        
    def DelayPosition(self,x):
        self.instr.write('HORizontal[:MAIn]:DELay:POSition '+str(x))
        
    #.....DPOJET Functions....................................................................................    
        
    def DpoJet(self):
        self.instr.write('DPOJET:Ver?')  #starts DPOJET automatically
        
    def DpoJet_Clear_All(self):
        self.instr.write('DPOJET:CLEARALLMeas')  #clears DPOJET measurements
        
    def DpoJet_Clear_Meas(self):
        self.instr.write('DPOJET:CLEAR Meas')  #clears DPOJET measurements
        
    def DpoJet_Stop(self):
        self.instr.write('DPOJET:STATE STOP')  #STOP DPOJET measurements
    
    def DpoJet_Single(self):
        #self.instr.write('DPOJET:STATE START')  #START DPOJET measurements
        self.instr.write('DPOJET:STATE SINGLE')  #START DPOJET measurements
        
    def DpoJet_Run(self):
        self.instr.write('DPOJET:STATE RUN')  #START DPOJET measurements
            
    def Scope_Factory(self):
        self.instr.write('FACTORY')  #Resets scope to factory setup
       
    def Scope_AutoSet(self):
        self.instr.write('AUTOSET EXEC')  #Autosets scope measurements
        
    def Scope_DPO_AutoSet(self):
        self.instr.write('DPOJET:SourceA Both')  #Autosets Horizontal and Veritacal scaling   
        
    def Scope_DPO_Resolution(self,resolution):
        self.instr.write("HOR:MODE:RECO "+ str(resolution))
    
    def Scope_DPO_SouMeas(self,meascount,math_a):            
        self.instr.write("DPOJET:MEAS" + str(meascount)+ ":SOU " + math_a)   #meascount is line number in tests and math_a is Math1, Math2...  
        
    def Scope_CH1_ON(self):
        self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
    
    def Scope_CH2_ON(self):
        self.instr.write('SEL:CH2 ON')  #Autosets scope measurements
        
    def Scope_CH3_ON(self):
        self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
        
    def Scope_CH4_ON(self):
        self.instr.write('SEL:CH4 ON')  #Autosets scope measurements
    
    def Scope_CH1_OFF(self):
        self.instr.write('SEL:CH1 OFF')  #Autosets scope measurements
        
    def Scope_CH2_OFF(self):
        self.instr.write('SEL:CH2 OFF')  #Autosets scope measurements
        
    def Scope_CH3_OFF(self):
        self.instr.write('SEL:CH3 OFF')  #Autosets scope measurements
        
    def Scope_CH4_OFF(self):
        self.instr.write('SEL:CH4 OFF')  #Autosets scope measurements
    
    def Scope_CHANNEL_CONTROL(self,stat1,stat2,stat3,stat4):        
        #self.instr.write('SEL:CH1 ' + '"' + stat1 + ';' + '"')# + 'CH2' + stat2; + '"' + 'CH3' + stat3; + '"' + 'CH4' + stat4 + '"')  #Autosets scope measurements
        #self.instr.write('SEL:CH1 ' + '"' + stat1 + ';' + 'CH2' + stat2 + ';' + 'CH3' + stat3 + ';' + 'CH4' + stat4 + '"')  #Autosets scope measurements       
        self.instr.write('SEL:CH1 ' + stat1) 
        self.instr.write('SEL:CH2 ' + stat2)
        self.instr.write('SEL:CH3 ' + stat3)
        self.instr.write('SEL:CH4 ' + stat4)
        
    def Scope_CH_OFF_CONTROL(self):
        self.instr.write('SEL:CH1 OFF;CH2 OFF;CH3 OFF; CH4 OFF')  #Autosets scope measurements

    def SamplingModeRT(self):
        self.instr.write('ACQuire:SAMPlingmode RT')
        self.instr.write('CH1:BANdwidth:ENHanced:FORCe ON')
                   
    def ZoomON(self):
        self.instr.write('ZOOm:MODe ON')
        self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 200')
        self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 1')
        

    def DpoJet_Recall_Setup(self):
        self.instr.write('RECALL:SETUP ' + '"' + "c:\File Path .set" + '"')  #Recall Setup
    
    def DpoJet_Recall_Mask(self,fpath,fname):
        self.instr.write('DPOJET:ADDM MASKHits')         # measurement 6 _ Plot 1
        self.instr.write('DPOJET:MEAS1:MASKF ' + '"' + fpath + fname  + '"')
        #fpath = C:/TekApplications/DPOJET/Masks/JESDB/
        #wrtmsg(scope,'DPOJET:MEAS6:MASKF ' + '"' + fpath + fname + '"')   # mask file location
        
    def DpoJet_PLL_Setup(self,frequency):
        self.instr.write('DPOJET:MEAS1:BITTYPE ALLBITS')
        self.instr.write('DPOJET:MEAS1:CLOCKRECOVERY:METHOD CUSTOM') #SET TO WHATEVER METHOD USER WANTS
        self.instr.write('DPOJET:MEAS1:CLOCKRECOVERY:MODEL ONE') #CAN BE EITHER ONE OR TWO -  FILTER ROLLOFF
        self.instr.write('DPOJET:MEAS1:CLOCKRECOVERY:LoopBandwidth ' + str((frequency)/1667))
        #scope1.write("DPOJET:MEAS1:CLOCKRECOVERY:LoopBandwidth " + str(datarate(variable)/1667)
        #scope1.write("DPOJET:MEAS1:CLOCKRECOVERY:LoopBandwidth " + str(6.144e9/1667))
    
    def JESD204BCT_PLL_Setup(self,test_number,frequency):
        i=1
        while (i<test_number+1):
            if(i<>4):
                self.instr.write('DPOJET:MEAS'+str(i)+':BITTYPE ALLBITS')
                self.instr.write('DPOJET:MEAS'+str(i)+':CLOCKRECOVERY:METHOD CUSTOM') #SET TO WHATEVER METHOD USER WANTS
                self.instr.write('DPOJET:MEAS'+str(i)+':CLOCKRECOVERY:MODEL ONE') #CAN BE EITHER ONE OR TWO -  FILTER ROLLOFF
                self.instr.write('DPOJET:MEAS'+str(i)+':CLOCKRECOVERY:LoopBandwidth ' + str((frequency)/1667))
                i += 1
            if(i==4):
                i += 1
            
    def JESD204BCT_RJDJ_BER_Target(self,test_number,ber):
        i=1
        while (i<test_number+1):
            self.instr.write('DPOJET:MEAS'+str(i)+':RJDJ:BER '+ str(ber))
            self.instr.write('DPOJET:MEAS'+str(i)+':BER:TARGETBER '+ str(ber))
            i += 1
            
    def JESD204BCT_RJDJ_Pattern_Length(self,test_number,pattern):
        i=1
        while (i<test_number+1):
            self.instr.write('DPOJET:MEAS'+str(i)+':RJDJ:DETECTPLEN '+str(0))
            self.instr.write('DPOJET:MEAS'+str(i)+':RJDJ:PATL '+ str(pattern))
            i += 1
            
    def DpoJet_Load_Test(self,test_name):
        self.instr.write('DPOJET:ADDM ' + str(test_name))
    
    def DpoJet_Set_Math1(self,CH_A,CH_B,Operand):
        self.instr.write('MATH1:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  #sets up Math1  
        self.instr.write('SEL:MATH1 ON') 
        
    def DpoJet_Set_Math2(self,CH_A,CH_B,Operand):
        self.instr.write('MATH2:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  #sets up Math2  
        self.instr.write('SEL:MATH2 ON')      
    
    def DpoJet_Set_Math3(self,CH_A,CH_B,Operand):
        self.instr.write('MATH3:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  #sets up Math3  
        self.instr.write('SEL:MATH3 ON')      
        
    def DpoJet_Set_Math4(self,CH_A,CH_B,Operand):
        self.instr.write('MATH4:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  #sets up Math4  
        self.instr.write('SEL:MATH4 ON') 
        
    def DpoJet_TurnOffChannels(self):
        self.instr.write('SEL:CH1 OFF')  #Autosets scope measurements
        self.instr.write('SEL:CH2 OFF')  #Autosets scope measurements
        self.instr.write('SEL:CH3 OFF')  #Autosets scope measurements
        self.instr.write('SEL:CH4 OFF')  #Autosets scope measurements 
        self.instr.write('SEL:MATH1 OFF')  #Autosets scope measurements 
        self.instr.write('SEL:MATH2 OFF')  #Autosets scope measurements 
        
        
    def DpoJet_Set_LaneA(self, vterm, zoom='ON'):
        #self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
        #self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
        self.instr.write('MATH1:DEFINE "CH1-CH3"')   #sets up Math1  
        self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
        self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
        self.instr.write('SEL:MATH1 ON')
        self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH1:OFFSet ' + str(1.5*vterm))
        self.instr.write('CH2:OFFSet ' + str(1.5*vterm))
        self.instr.write('CH3:OFFSet ' + str(1.5*vterm))
        self.instr.write('CH4:OFFSet ' + str(1.5*vterm))
        self.instr.write('ZOOm:MODe ' + str(zoom))
        self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 10000')
        self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 2')
        self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 2')
        self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
        self.instr.write('CH1:POSition 0')
        self.instr.write('CH3:POSition 0')
        self.instr.write('TRIGger:A:EDGE:SOUrce:CH1')  #sets trigger source
        #self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
        #wx.MilliSleep(5000) #
        self.instr.write('TRIGger:A SETLevel')  #sets trigger location
        
    def DpoJet_Set_LaneB(self, vterm, zoom='ON'):
        #self.instr.write('SEL:CH2 ON')  #Autosets scope measurements
        #self.instr.write('SEL:CH4 ON')  #Autosets scope measurementsself.instr.write('MATH2:DEFINE "CH2-CH4"')  #sets up Math1  
        self.instr.write('MATH2:DEFINE "CH2-CH4"')   #sets up Math1        
        self.instr.write('SEL:CH2 ON')  #Autosets scope measurements
        self.instr.write('SEL:CH4 ON')  #Autosets scope measurements 
        self.instr.write('SEL:MATH2 ON')
        self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH1:OFFSet ' + str(1.5*vterm))
        self.instr.write('CH2:OFFSet ' + str(1.5*vterm))
        self.instr.write('CH3:OFFSet ' + str(1.5*vterm))
        self.instr.write('CH4:OFFSet ' + str(1.5*vterm))
        self.instr.write('ZOOm:MODe ' + str(zoom))
        self.instr.write('ZOOm:ZOOM1:CH2:HORizontal:SCAle 10000')
        self.instr.write('ZOOm:ZOOM1:CH2:VERtical:SCAle 2')
        self.instr.write('ZOOm:ZOOM1:CH4:VERtical:SCAle 2')
        #self.instr.write('ZOOm:ZOOM1:Math2:DISplay OFF')
        self.instr.write('CH2:POSition 0')
        self.instr.write('CH4:POSition 0')
        self.instr.write('TRIGger:A:EDGE:SOUrce:CH2')  #sets trigger source
        #self.instr.write('TRIGger:A:LEVel:CH3 ' + str((vterm+1)/2))
        #wx.MilliSleep(5000) #
        self.instr.write('TRIGger:A SETLevel')  #sets trigger location
        
    def DpoJet_Set_DiffProbeCh1(self, vterm, zoom='ON'):
        #self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
        #self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
        #self.instr.write('MATH1:DEFINE "CH1-CH3"')   #sets up Math1  
        self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
        self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH1:OFFSet ' + str(vterm))
        self.instr.write('CH2:OFFSet ' + str(vterm))
        self.instr.write('CH3:OFFSet ' + str(vterm))
        self.instr.write('CH4:OFFSet ' + str(vterm))
        self.instr.write('ZOOm:MODe ' + str(zoom))
        self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 10000')
        self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 1')
        #self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 1')
        #self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
        self.instr.write('CH1:POSition 0')
        self.instr.write('TRIGger:A:EDGE:SOUrce:CH1')  #sets trigger source
        #self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
        #wx.MilliSleep(5000) #
        self.instr.write('TRIGger:A SETLevel')  #sets trigger location
        
    def DpoJet_Set_DiffProbeCh3(self, vterm, zoom='ON'):
        #self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
        #self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
        #self.instr.write('MATH1:DEFINE "CH1-CH3"')   #sets up Math1  
        self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
        self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH1:OFFSet ' + str(vterm))
        self.instr.write('CH2:OFFSet ' + str(vterm))
        self.instr.write('CH3:OFFSet ' + str(vterm))
        self.instr.write('CH4:OFFSet ' + str(vterm))
        self.instr.write('ZOOm:MODe ' + str(zoom))
        self.instr.write('ZOOm:ZOOM1:CH3:HORizontal:SCAle 10000')
        #self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 1')
        self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 1')
        #self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
        self.instr.write('CH3:POSition 0')
        self.instr.write('TRIGger:A:EDGE:SOUrce:CH3')  #sets trigger source
        #self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
        #wx.MilliSleep(5000) #
        self.instr.write('TRIGger:A SETLevel')  #sets trigger location
    
    def DpoJet_Measure(self,channel,measure):
        self.instr.write('MEASU:IMM:SOU ' + channel) 
        self.instr.write('MEASU:IMM:TYPE ' + measure) 
        return self.instr.ask('MEASU:IMM:VALUE?')   
        #wrtmsg(scope,"SAVE:SETUP 10")
        #wrtmsg(scope,"RECALL:SETUP 10")
        
    def DpoJet_Indivdual_Measure(self,meascount,measure):
        stuff = self.instr.ask('DPOJET:MEAS' +  str(meascount) + ':RESULts:ALLAcqs:' + str(measure) + '?')
        #stuff.rstrip('\r\n')
        return  stuff     

        
    def DpoJet_Intra_Pair(self):
        # Measure Intra pair Skew
        self.instr.write("DPOJET:ADDM SKEW")             # measurement 14
        self.instr.write("DPOJET:MEAS1:CUST 'Intra-pair skew'") #sets name of test on screen(Custom measurement Name)
        self.instr.write("DPOJET:MEAS1:SOU1 CH1")
        self.instr.write("DPOJET:MEAS1:SOU2 CH3")
        self.instr.write("DPOJET:MEAS1:EDGE1 RISE")
        self.instr.write("DPOJET:MEAS1:EDGE2 FALL")
        
    def DpoJet_Intra_Pair1_3(self,testnum):
        # Measure Intra pair Skew
        self.instr.write("DPOJET:ADDM SKEW")             # measurement 14
        self.instr.write("DPOJET:MEAS"+str(testnum)+":CUST 'Intra-pair skew'") #sets name of test on screen(Custom measurement Name)
        self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH1")
        self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH3")
        self.instr.write("DPOJET:MEAS"+str(testnum)+":EDGE1 BOTH")
        self.instr.write("DPOJET:MEAS"+str(testnum)+":TOE OPP") # To Edge opposite of from edge
        
    def DpoJet_Intra_Pair2_4(self,testnum):
        # Measure Intra pair Skew
        self.instr.write("DPOJET:ADDM SKEW")             # measurement 14
        self.instr.write("DPOJET:MEAS"+str(testnum)+":CUST 'Intra-pair skew'") #sets name of test on screen(Custom measurement Name)
        self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH2")
        self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH4")
        self.instr.write("DPOJET:MEAS"+str(testnum)+":EDGE1 BOTH")
        self.instr.write("DPOJET:MEAS"+str(testnum)+":TOE OPP") # To Edge opposite of from edge
        
    def DpoJet_CM_Source(self,testnum,lane):
        if (lane==00):
            self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH1")
            self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH3")
        if (lane==01):
            self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH2")
            self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH4")
        if (lane==10):
            self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH1")
            self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH1")
        if (lane==11):
            self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH3")
            self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH3")
        
    def DpoJet_AddBathtub(self,testnum):
        self.instr.write("DPOJET:ADDP BATH, MEAS" + str(testnum))#plot is added based on measurement number
        self.instr.write("DPOJET:PLOT3:BATH:BER 16")

    def DpoJet_AddEye(self,testnum):
        self.instr.write("DPOJET:ADDP EYE, MEAS" + str(testnum)) #plot is added based on measurement number

    def DpoJet_AddWaveform(self,testnum):
        self.instr.write("DPOJET:ADDP WAVE, MEAS" + str(testnum)) #plot is added based on measurement number
        
    def DpoJet_AddHistogram(self,testnum):
        self.instr.write("DPOJET:ADDP HISTO, MEAS" + str(testnum))
        
    def DpoJet_AddSpectrum(self,testnum):
        self.instr.write("DPOJET:ADDP SPECtrum, MEAS" + str(testnum))

    def DpoJet_RiseFall20_80(self,testnum):
        self.instr.write('DPOJET:REFLevels:CH1:PERcent:FALLHigh 80')
        self.instr.write('DPOJET:REFLevels:CH2:PERcent:FALLHigh 80')
        self.instr.write('DPOJET:REFLevels:CH3:PERcent:FALLHigh 80')
        self.instr.write('DPOJET:REFLevels:CH4:PERcent:FALLHigh 80')
        self.instr.write('DPOJET:REFLevels:Math1:PERcent:FALLHigh 80')
        self.instr.write('DPOJET:REFLevels:Math2:PERcent:FALLHigh 80')
        self.instr.write('DPOJET:REFLevels:CH1:PERcent:FALLLow 20')
        self.instr.write('DPOJET:REFLevels:CH2:PERcent:FALLLow 20')
        self.instr.write('DPOJET:REFLevels:CH3:PERcent:FALLLow 20')
        self.instr.write('DPOJET:REFLevels:CH4:PERcent:FALLLow 20')
        self.instr.write('DPOJET:REFLevels:Math1:PERcent:FALLLow 20')
        self.instr.write('DPOJET:REFLevels:Math2:PERcent:FALLLow 20')
        self.instr.write('DPOJET:REFLevels:CH1:PERcent:RISEHigh 80')
        self.instr.write('DPOJET:REFLevels:CH2:PERcent:RISEHigh 80')
        self.instr.write('DPOJET:REFLevels:CH3:PERcent:RISEHigh 80')
        self.instr.write('DPOJET:REFLevels:CH4:PERcent:RISEHigh 80')
        self.instr.write('DPOJET:REFLevels:Math1:PERcent:RISEHigh 80')
        self.instr.write('DPOJET:REFLevels:Math2:PERcent:RISEHigh 80')
        self.instr.write('DPOJET:REFLevels:CH1:PERcent:RISELow 20')
        self.instr.write('DPOJET:REFLevels:CH2:PERcent:RISELow 20')
        self.instr.write('DPOJET:REFLevels:CH3:PERcent:RISELow 20')
        self.instr.write('DPOJET:REFLevels:CH4:PERcent:RISELow 20')
        self.instr.write('DPOJET:REFLevels:Math1:PERcent:RISELow 20')
        self.instr.write('DPOJET:REFLevels:Math2:PERcent:RISELow 20')
        
    def BathtubPlotBugFixSave(self):
        self.instr.write('SAVE:SETUP 10')
        
    def BathtubPlotBugFixRecall(self):
        self.instr.write('RECALL:SETUP 10')
    
    def DpoJet_Measure_State(self):
        return self.instr.ask('DPOJET:STATE?')
        
    #def DpoJet_Intra_Pair(self):    
    #   wrtmsg(scope,"DPOJET:ADDP HISTO, MEAS5")    
    
    #........End DPOJET Functions...................................................................................... 
        
    def HistogramBox(self, a, b, c, d):
        self.instr.write('HIStogram:Box '+str(a)+', '+str(b)+', '+str(c)+', '+str(d))  #sets histogram box parameters
        
    def HistogramModeHor(self):#sets the histogram mode: horizaontal or vertical
        self.instr.write('HIStogram:MODe Horizontal')
        
    def HistogramModeVer(self):#sets the histogram mode: horizaontal or vertical
        self.instr.write('HIStogram:MODe VERTICAL')
        
    def HistogramSource(self,Source):
        self.instr.write('HIStogram:SOU '+Source)
        
    def DelayMeasureDirection(self,direction):
        self.instr.write('MEASUrement:IMMed:DELay:DIREction '+direction)  #sets search direction for delay measurement  
        
    def DelayMeasureTo(self, Source2):
        self.instr.write('MEASUrement:IMMed:SOURCE2 ' + Source2)  #sets to edge in delay measurement
        
    def DelayMeasureFrom(self, Source1):
        self.instr.write('MEASUrement:IMMed:SOURCE[1] ' + Source1)  #sets from edge in delay measurement
        
    def ImmediateMeasureDelay(self):
        self.instr.write('MEASUrement:IMMed:TYPe DEL')  #sets immediate measurement type
        
    def ImmediateMeasureHits(self):
        self.instr.write('MEASUrement:IMMed:TYPe HITS')  #sets immediate measurement type
        
    def ImmediateMeasurePhase(self):
        self.instr.write('MEASUrement:IMMed:TYPe PHAse')  #sets immediate measurement type
        
    def ImmediateMeasurementValue(self):
        return float(self.instr.ask('MEASUrement:IMMed:VALue?'))  #returns measurement value
    
    def Resolution(self,Resolution):
        self.instr.write('HOR:RESO ' + str(Resolution))
    
    #Olie's inputs
    def GetTriggerPosition(self):
        return float(self.instr.ask('WFMOutpre:PT_Off?'))  #find trigger position in samples         
     
    def Xinc(self):
        return float(self.instr.ask('WFMOutpre:XINcr?'))  #time increment per sample
    
    def GetHscale(self):
        return float(self.instr.ask('HORizontal:MAIn:SCAle?'))  #get time/div
    
    def SetHscale(self, hscale):
        self.instr.write('HORizontal:MAIn:SCAle ' + str(hscale))
   
    def GetVscale(self, Source2):
        return float(self.instr.ask(Source2 + ":SCALe?"))

    def SetVscale(self, ch, vscale):
        self.instr.write(str(ch) + ':SCAle ' + str(vscale))

    def SetVscaleAll(self, vscale):
        self.instr.write('CH1:SCAle ' + str(vscale))
        self.instr.write('CH2:SCAle ' + str(vscale))
        self.instr.write('CH3:SCAle ' + str(vscale))
        self.instr.write('CH4:SCAle ' + str(vscale))
        self.instr.write('Math1:SCAle ' + str(vscale*2))
        self.instr.write('Math2:SCAle ' + str(vscale*2))
        
    def SetVterm(self, ch, vterm):
        self.instr.write(str(ch) + ':VTERm:BIAS ' + str(vterm))
        
    def SetPosition(self, ch, position):
        self.instr.write(str(ch) + ':POSition ' + str(position))  
          
    def SetOffset(self, ch, offset):
        self.instr.write(str(ch) + ':OFFSet ' + str(offset))    
                   
    def SetSRC2(self, Source2):
        self.instr.write('MEASUrement:IMMed:SOURCE2 ' + Source2)  #sets to edge in delay measurement
    
    def SetSRC1(self, Source1):
        self.instr.write('MEASUrement:IMMed:SOURCE[1] ' + Source1)  #
            
    #def SetSrc1(self, Source1):
    #    self.instr.write('MEASUrement:IMMed:SOURCE[1] ' + Source1)  #sets from edge in delay measurement
    #def Set1Src1(self):
    #    return str(self.instr.ask('MEASUrement:IMMed:SOURCE[1]?')) 
    
    def SetChanDelay(self,Chan,Delay):
        self.instr.write(Chan+':DESKew '+Delay)  #sets from edge in delay measurement
        
    def GetChanDelay(self,Chan):
        return float(self.instr.ask(Chan+':DESKew?'))  #sets from edge in delay measurement
     
    def SetDelay(self):
        self.instr.write('MEASUrement:IMMed:TYPe DELay')  #sets from edge in delay measurement
       
    def SetFreq(self):
        self.instr.write('MEASUrement:IMMed:TYPe FREQuency')  #sets from edge in delay measurement
      
    def SetPeriod(self):
        self.instr.write('MEASUrement:IMMed:TYPe PERIOD')  #sets from edge in delay measurement

    def SetDuty(self):
        self.instr.write('MEASUrement:IMMed:TYPe PDUty')  #sets from edge in delay measurement  
            
    def Edge1(self):
        self.instr.write('MEASUrement:IMMed:DELay:EDGE1 RISE')  #sets from edge in delay measurement
        
    def DelayMeasureEdge1(self,edge):
        self.instr.write('MEASUrement:IMMed:DELay:EDGE1 '+edge)
    
    def Edge2(self):
        self.instr.write('MEASUrement:IMMed:DELay:EDGE2 RISE')  #sets from edge in delay measurement
        
    def DelayMeasureEdge2(self,edge):
        self.instr.write('MEASUrement:IMMed:DELay:EDGE2 '+edge)
    
    def DirectBackards(self):
        self.instr.write(':MEASUREMENT:IMMED:DELAY:DIRECTION BACKWARDS')  #sets from edge in delay measurement
    
    def DirectForward(self):
        self.instr.write(':MEASUREMENT:IMMED:DELAY:DIRECTION FORWARDs')  #sets from edge in delay measurement
        
    def GetValue(self):
        return float(self.instr.ask('MEASUrement:IMMed:VALue?'))  #gets efined value 
    
    def DefineTrig(self, Source1):
        self.instr.write('DATA:SOURCE ' + Source1)  #sets from edge in delay measurement    
        
    def DefineTrig1(self, Source1):
        self.instr.write('TRIGger:A:EDGE:SOUrce ' + Source1) 
         
    def SetHigh(self):
        self.instr.write('MEASUrement:IMMed:TYPe HIGH')  #sets from edge in delay measurement  
        
    def SetMax(self):
        self.instr.write('MEASUrement:IMMed:TYPe MAX')  #sets from edge in delay measurement
        
    def SetMin(self):
        self.instr.write('MEASUrement:IMMed:TYPe MINI')  #sets from edge in delay measurement


    def SetMeaSRC2(self, number, Source2):
        self.instr.write('MEASUrement:MEAS'+str(number)+':SOURCE[2] ' + Source2)  #
    
    def SetMeasSRC1(self, number, Source1):
        self.instr.write('MEASUrement:MEAS'+str(number)+':SOURCE[1] ' + Source1)  #
        
    def SetMeasureMax(self,number):
        self.instr.write('MEASUrement:MEAS'+str(number)+':TYPe MAX')  #sets from edge in delay measurement
        
    def SetMeasureMin(self,number):
        self.instr.write('MEASUrement:MEAS'+str(number)+':TYPe MINI')
        
    def MeasureMax(self,number):
        return float(self.instr.ask('MEASUrement:MEAS'+str(number)+':MAX?'))  #sets from edge in delay measurement
        
    def MeasureMin(self,number):
        return float(self.instr.ask('MEASUrement:MEAS'+str(number)+':MINI?'))
    
    def MeasureMean(self,number):
        return float(self.instr.ask('MEASUrement:MEAS'+str(number)+':MEAN?'))
    
    def MeasureCount(self,number):
        return float(self.instr.ask('MEASUrement:MEAS'+str(number)+':COUNt?'))
    
    def SetLow(self):
        self.instr.write('MEASUrement:IMMed:TYPe LOW')  #sets from edge in delay measurement 
        
    def SetAmplitude(self):
        self.instr.write('MEASUrement:IMMed:TYPe AMP')  #sets from edge in delay measurement
        
    def SetHist(self, Source2):
        self.instr.write('HIStogram:SOUrce ' + Source2)  #sets from edge in delay measurement    
    
    def SetHistStateON(self):
        self.instr.write('HIStogram:STATE ON')  #sets from edge in delay measurement
        
    def SetHistBox(self, leftp, topp, rightp, bottomp):
        self.instr.write('HIStogram:Box ' + str(leftp) + "," + str(topp) + "," + str(rightp) + "," + str(bottomp))  #sets from edge in delay measurement
        
    def HeaderOFF(self):
        self.instr.write('HEADer OFF')
    
    def runTDSHT3(self):
        self.instr.write('VARIABLE:VALUE "sequencerState","Sequencing"')

    def saveWaveform(self,fname):
        #self.instr.write('SAVE:WAVEFORM:FILEFORMAT SPREADSHEETCsv')
        self.instr.write('SAve:WAVEform CH1 ' + ',' + '"' + str(fname) + '"')
        print "this is", str(fname)
        #self.instr.write('SAve:WAVEform Math1 ' + ',' + '"rene3.cvs"') #this code works
        
        #self.instr.write('SAve:WAVEform Math1, "rene.cvs"') This code works
        
    def Set_Chan1_Chan3_Math1(self, vterm, zoom='ON'):
        #self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
        #self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
        self.instr.write('MATH1:DEFINE "CH1-CH3"')   #sets up Math1  
        self.instr.write('SEL:CH1 OFF')  #Autosets scope measurements
        self.instr.write('SEL:CH3 OFF')  #Autosets scope measurements
        self.instr.write('SEL:MATH1 ON')
        self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
        self.instr.write('CH1:OFFSet ' + str(vterm))
        self.instr.write('CH2:OFFSet ' + str(vterm))
        self.instr.write('CH3:OFFSet ' + str(vterm))
        self.instr.write('CH4:OFFSet ' + str(vterm))
        self.instr.write('ZOOm:MODe ' + str(zoom))
        self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 10000')
        self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 2')
        self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 2')
        self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
        self.instr.write('CH1:POSition 0')
        self.instr.write('CH3:POSition 0')
        self.instr.write('TRIGger:A:EDGE:SOUrce CH1')  #sets trigger source
        #self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
        #wx.MilliSleep(5000) #
        self.instr.write('TRIGger:A SETLevel')  #sets trigger location
        
    def Get_Chan1_Chan3_Math1_Measurement(self, measure):
        self.instr.write('MEASU:IMM:TYPE ' + str(measure)) 
        return self.instr.ask('MEASU:IMM:VALUE?')   
    
    def Clear(self):
        self.instr.write('CLEAR ALL') 
          
'''
    def DpoJet_Recall_Mask(self,fpath,fname):
        self.instr.write('DPOJET:ADDM MASKHits')         # measurement 6 _ Plot 1
        self.instr.write('DPOJET:MEAS1:MASKF ' + '"' + fpath + fname  + '"')

       
    def getSummary(self):
        self.instr.write('VARIABLE:VALUE "reportSummary","Save"')
        
    def getReport(self):
        self.instr.write('VARIABLE:VALUE "reportDetails","Save"')
 '''       
    