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


from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

# print "this is the file for the TekDSA scope"
#class Tek_Prac(GPIBObjectBaseClass):
class TekDSA72504D_alt(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        GPIBObjectBaseClass.__init__(self, 'TEKTRONIX,DSA72504D', addr)
        self.instr.write('AUTOSET EXEC')
    # This function takes in a list of channels to be turned on or off
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------- CHANNEL CONTROL-------------------------------------------------------------------------------------------------------
    def ChanCtrlOnOff(self,chansOn=[]):
        #Turn all channels off
        self.instr.write('SEL:CH1 OFF;CH2 OFF;CH3 OFF; CH4 OFF')
        for i in chansOn:
            self.instr.write('SEL:CH' + str(i) + ' ON')
        #self.instr.write('AUTOSET EXEC')
    def TurnOFFALL(self):
        self.instr.write('SEL:CH1 OFF;CH2 OFF;CH3 OFF; CH4 OFF')
        print "\nAll Channels OFF"
    def TurnONALL(self):
        self.instr.write('SEL:CH1 ON;CH2 ON;CH3 ON; CH4 ON')
        print "\nAll Channels ON"
        self.instr.write('AUTOSET EXEC')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------- SET MEASURMENT TYPE SOURCE NUM AND TYPE OF SOURCE ----------------------------------------------------------------------------------------------
    def SetAllMeasureVAL_Type_Source_ChanNEW(self,annotation,typeOfmeas=[],sourceNumForMeas=[],typeOfSource=[]): #USE THIS FUNCTION
        #self.instr.write('AUTOSET EXEC')  # Autosets the scope
        # self.instr.write('CLEAR ALL')  # Clears the scope
        for i in range(1, len(typeOfmeas) + 1):  # variable 'i' will increment within range 1 to the value of number +1
            num = typeOfmeas[i - 1]  # sets variable num to each item in the type list starting at type[0]
            self.instr.write('*WAI')  # make sure the scope is ready for another command
            self.instr.write('MEASU:MEAS' + str(i) + ':TYP ' + num)  # sets up the meas number and type
            self.instr.write('*WAI')
        j = 0  #
        k=0
        for i in range(1,len(typeOfmeas)+1):
            for j in sourceNumForMeas:
                self.instr.write('*WAI')
                self.instr.write('MEASU:MEAS' + str(i) + ':SOURCE'+str(j)+' '+typeOfSource[i-1])
                self.instr.write('MEASUREMENT:MEAS' + str(i) + ':STATE ON')  # enables calculation and display of the specified measurement found on pg 596 in manual  "MEASUrement:MEAS<x>:STATE"
                self.instr.write('*WAI')
        j = 0
        if annotation==None:
            self.instr.write('MEASUrement:ANNOTation:STATE OFF')
        else:
            self.instr.write('MEASUrement:ANNOTation:STATE MEAS' + str(annotation))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------DISPLAY MEASURMENT VALUES----------------------------------------------------------------------------------------------
    def displayMeas(self,tim): #This function displays the measurement stats and also stores them in and returns it to where this function was called.
        typeOfMeasare=[]
        for i in range(1,9):
            nameMeas= self.instr.ask('MEASU:MEAS'+str(i)+':TYPE?')
            nameMeas= nameMeas.strip("\n")
            if nameMeas == 'UNDEFINED':
                continue
            else:
                typeOfMeasare.append(nameMeas)

        otherDiction={}
        theMeasurements={}
        if tim>0:
            print "Please wait. Selected delay:",str(tim)+"s"
        time.sleep(tim)
        theVALUE_MEAN_MIN_MAX_STD_CNT = ['VALUE', 'MEAN', 'MINIMUM', 'MAXIMUM', 'STDdev', 'COUNT']
        for i in range(1, len(typeOfMeasare)+ 1):
            measNames = {}
            for j in range(0, len(theVALUE_MEAN_MIN_MAX_STD_CNT)):
                try:
                    value= self.instr.ask('MEASU:MEAS' + str(i) + ':' + theVALUE_MEAN_MIN_MAX_STD_CNT[j] + '?')
                    measNames[theVALUE_MEAN_MIN_MAX_STD_CNT[j] + str(i)] = value
                except ValueError:
                    measNames[theVALUE_MEAN_MIN_MAX_STD_CNT[j] + str(i)] = 'ERROR: Press "Default Setup"  '
                    pass
                self.instr.write('*WAI')
                try:
                    otherDiction[theVALUE_MEAN_MIN_MAX_STD_CNT[j] + str(i)]= value
                except:
                    otherDiction[theVALUE_MEAN_MIN_MAX_STD_CNT[j] + str(i)] = 'ERROR: Press "Default Setup" '
                    pass
                self.instr.write('*WAI')
                num = typeOfMeasare[i - 1]
                theMeasurements['Measurement ' + str(i) + ' ' + num.capitalize()] = dict(measNames.items())  # stores the measurements in a dictionary called theMeasurements
        #print otherDiction
        for i in range(1, len(typeOfMeasare) + 1):
            print ".........................."
            num = typeOfMeasare[i - 1]
            print 'Measurement ' + str(i) + ' ' + num.capitalize()
            print "--------------------------"
            for j in range(0, len(theVALUE_MEAN_MIN_MAX_STD_CNT)):
                print theVALUE_MEAN_MIN_MAX_STD_CNT[j], str(i), '=', otherDiction[theVALUE_MEAN_MIN_MAX_STD_CNT[j] + str(i)]
        return sorted(theMeasurements.items()) #returns the dictionary
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------- MATH Setup -------------------------------------------------------------------------------------------------------------
    def setupMath(self,MathNumandExpre={},mathOn=[]): #This functiion takes takes a dictionary of the Math name (MATH1,MATH2,MATH3,MATH4) as the key and expression as value. The second argument is optional, but can display a list of math waveforms on the scope(1-4)
        self.instr.write('SEL:MATH1 OFF;MATH2 OFF;MATH3 OFF;MATH4 OFF')
        theList = MathNumandExpre.items()
        theList=sorted(theList)

        for i in range(0,len(MathNumandExpre.items())):
            self.instr.write(theList[i][0]+':DEFINE '+'"'+theList[i][1]+'"')  # sets up Math functions in the list
        theList = dict(theList)
        for i in mathOn:
            compareVar = 'MATH' + str(i)
            if compareVar not in theList:
                print "ERROR:", compareVar + " expression not found. Can't display"
            else:
                self.instr.write('SEL:' + compareVar + ' ON')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------Reference Levels Setup----------------------------------------------------------------------------------------------

    def setMethodforRefLev(self,methodMode=[],MeasNum=[]): #specifies or queries the method used to calculate the 0% and 100% reference level. First argument: list of methods(HIStogram|MINMax|MEAN), Second argument: list of measurement numbers you want to set the methods to.
        for i in range(0, len(MeasNum)):
            self.instr.write('MEASUrement:MEAS'+str(MeasNum[i])+':METHod '+(methodMode[i]))
    def setMethodUnitsRevLev(self,methodUni=[],MeasNum=[]):#specifies or queries the reference level units used for measurement calculations. first arg: list of units (ABSOLUTE|PERCENT) sec arg: list of measrement numbers to set the units to.
        for i in range(0,len(methodUni)):
            self.instr.write('MEASUrement:MEAS'+str(MeasNum[i])+':REFLevel:METHod '+methodUni[i])
    def setHi_Low_MiVal(self,Hi_LowORMid=[],MeasNum=[],refVal=[]): #This command will set the reference levels for HIGH LOW MID(1) OR MID2. This function should always be called after the the method and the units are set to function correctly. First argument: select HIGH LOW or MID, Second argument: select the measurement # and the value
        for i in range(0,len(Hi_LowORMid)):
            theUnits = self.instr.ask('MEASUrement:MEAS' + str(MeasNum[i]) + ':REFLevel:METHod?')
            theUnits=theUnits.rstrip() #removes last character / used to take the newline character out
            self.instr.write('MEASUrement:MEAS'+str(MeasNum[i])+':REFLevel:'+theUnits+':'+Hi_LowORMid[i]+' '+str(refVal[i]))
    def setSigTypSrcMeas(self,type=[],source=[],meas=[]): #sets a list signal types and sources for list of measurements
        for i in range (0,len(type)):
            self.instr.write('MEASUrement:MEAS'+str(meas[i])+':SOUrce'+str(source[i])+':SIGType '+type[i])
    def measNoise(self,measNum=[],noiseMeas=[]): # to use this function make sure the signal type is set to EYE  first using the setSigTypeSrcMeas function.
        for i in range(0,len(measNum)):
            self.instr.write('MEASUrement:MEAS'+str(measNum[i])+':NOISe '+noiseMeas[i])

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------TRIGGER SETUP--------------------------------------------------------------------------------------

    def setTrigA_EdgeTypSrcCoupSlope(self, source=[],typeCoup=[],typeLevel=[],typeSlope=[]):
        for i in range(0,len(source)):

            self.instr.write('TRIGger:A:EDGE:Source ' +source[i])
            self.instr.write('TRIGger:A:EDGE:COUPling:'+source[i]+' ' +typeCoup[i])
            self.instr.write('TRIGger:A:LEVEL:'+source[i]+' '+str(typeLevel[i]))
            self.instr.write('TRIGger:A:EDGE:SLOpe:'+source[i]+' '+typeSlope[i])

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def setTermination(self,chan=[],termVoltage=[]):
        for i in range(0,len(chan)):
            self.instr.write('CH'+str(chan[i])+':VTERm:BIAS '+str(termVoltage[i]))

    def WRITE(self,write):
        self.instr.write(write)
    def ASK(self,name):
        return self.instr.ask(name)
    # def default_Autoset(self):
    #     self.instr.write('FACTORY')
    #     self.instr.write('AUTOSET EXEC')









#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------




    # def setTrigEdgeSource_Slope_Coupling(self,typeOfTrig,type=[], location=[]):#Haven't tested this function yet
    #     typeOfTrig.upper()
    #     if len(type) != len(location):
    #         print "# of Types not equal to # Locations selected"
    #         return
    #     elif typeOfTrig=='A':
    #         for i in range(0,len(type)):
    #             self.instr.write('TRIGger:A:EDGE:'+type[i]+' ' + str(location[i]))  # sets horizontal trigger location
    #     elif typeOfTrig == 'B':
    #         for i in range(0, len(type)):
    #             self.instr.write('TRIGger:B:EDGE:' + type[i] + ' ' + str(location[i]))  # sets horizontal trigger location
    #     else:
    #         print "Trigger type selected is not an option"
    #         return
    #
    # def SetTriggerPos(self, x):
    #     self.instr.write('HORizontal:TRIGger:POSition ' + str(x))  # sets horizontal trigger location

































#     def GetAcqPar(self):
#         return self.instr.ask('ACQ?')
#
#     def GetFreq(self):
#         self.instr.write('MEASU:IMM:TYP FREQ')
#         return float(self.instr.ask('MEASU:IMM:VAL?'))
#
#     def MeasFreq(self, source):
#         self.instr.write('MEASU:MEAS1:TYP FREQ')
#         self.instr.write('MEASU:MEAS1:SOURCE CH' + str(source))
#         return self.instr.ask('MEASU:MEAS1:MEAN?')
#
#     def GetSRC1(self):
#         print "test"
#         self.instr.write('MEASU:IMM:SOURCE[10000]?')
#         return float(self.instr.ask('MEASU:IMM:VAL?'))
#
#     def GetSRC2(self):
#         self.instr.write('MEASU:IMM:SOURCE2?')
#         # return float(self.instr.ask('MEASU:IMM:VAL?'))
#
#     def GetDely(self):
#         self.instr.write('MEASU:IMM:TYP DEL')
#         return float(self.instr.ask('MEASU:IMM:VAL?'))
#
#     def GetUnits(self):
#         self.instr.write('MEASU:IMM:TYP UNI?')
#         return float(self.instr.ask('MEASU:IMM:VAL?'))
#
#     def FastAcqOn(self):
#         self.instr.write(':FastAcq:state 1')
#
#     def FastAcqOff(self):
#         self.instr.write(':FastAcq:state 0')
#
#     def SetJitter(self, Source):
#         self.instr.write('HIS:SOU ' + Source)
#
#     def GetJitterPKPK(self, MEAS):
#         # self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:' + MEAS + ':VAL?'))
#
#     def GetJitterRMS(self, MEAS):
#         # self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:' + MEAS + ':VAL?'))
#
#     def GetMeasuredValue(self, MEAS):
#         # self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:' + MEAS + ':VAL?'))
#
#     def GetMeasuredMax(self, MEAS):
#         # self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:' + MEAS + ':MAX?'))
#
#     def GetMeasuredMin(self, MEAS):
#         # self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:' + MEAS + ':MINI?'))
#
#     def GetMeasuredSTD(self, MEAS):
#         # self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:' + MEAS + ':STD?'))
#
#     def GetMeasuredMean(self, MEAS):
#         # self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:' + MEAS + ':MEAN?'))
#
#     def SetSingle(self):
#         self.instr.write('ACQuire:STOPAFTER SEQUENCE')  # sets the single button
#
#     def SetAcqON(self):
#         print "test1"
#         self.instr.write('ACQuire:STATE RUN')  # sets the single button
#
#     def SetAcqOFF(self):
#         self.instr.write('ACQuire:STATE STOP')  # sets the single button
#
#         # def SetSEQ(self):
#         # self.instr.write('ACQuire:STOPAFTER SEQUENCE') #sets the single button
#
#     def SetTriggerEdgeSource(self, x):
#         self.instr.write('TRIGger:A:EDGE:SOUrce ' + str(x))  # sets horizontal trigger location
#
#     def GetTriggerEdgeSource(self):
#         return self.instr.ask('TRIGger:A:EDGE:SOUrce?')  # sets horizontal trigger location
#
#     def SetTriggerEdgeSlope(self, x):
#         self.instr.write('TRIGger:A:EDGE:SLOpe ' + str(x))  # sets horizontal trigger location
#
#     def GetTriggerEdgeSlope(self):
#         return self.instr.ask('TRIGger:A:EDGE:SLOpe?')
#
#     def SetTriggerEdgeCoupling(self, x):
#         self.instr.write('TRIGger:A:EDGE:COUPling ' + str(x))
#
#     def GetTriggerEdgeCoupling(self):
#         return self.instr.ask('TRIGger:A:EDGE:COUPling?')
#
#     def AcqState(self):
#         return self.instr.ask('ACQ:STATE?')
#
#     def SetRun(self):
#         self.instr.write('ACQuire:STOPAFTER RUNSTOP')  # sets run/stop
#
#     def HorizontalMode(self, x):
#         self.instr.write('HORizontal:MODE ' + str(x))  # the modes are AUTO, CONSTANT, MANUAL
#
#     def SampleRate(self, x):
#         self.instr.write('HORizontal:MODE:SAMPLERATE ' + str(x))  # sets the sample rate
#
#     def TimeBase(self, y):
#         self.instr.write('HORizontal:MAIn:SCAle ' + str(y))  # sets horizontal time base
#
#     def SetVertTriggerPos1(self, x):
#         self.instr.write('TRIGger:A:Level:CH1 ' + str(x))  # sets vertical trigger position on CH1
#
#     def SetVertTriggerPos2(self, x):
#         self.instr.write('TRIGger:A:Level:CH2 ' + str(x))  # ssets vertical trigger position on CH2
#
#     def SetVertTriggerPos3(self, x):
#         self.instr.write('TRIGger:A:Level:CH3 ' + str(x))  # sets vertical trigger position on CH3
#
#     def SetVertTriggerPos4(self, x):
#         self.instr.write('TRIGger:A:Level:CH4 ' + str(x))  # sets vertical trigger position on CH4
#
#     def SetTriggerPos(self, x):
#         self.instr.write('HORizontal:TRIGger:POSition ' + str(x))  # sets horizontal trigger location
#
#     def GetTriggerPos(self):
#         return float(self.instr.ask('HORizontal:TRIGger:POSition?'))  # gets horizontal trigger location
#
#     def SetTrigger50(self):
#         self.instr.write('TRIGger:A: SETLevel')  # sets horizontal trigger location
#
#     def DelayTime(self, x):
#         self.instr.write('HORizontal[:MAIn]:DELay:TIMe ' + str(x))
#
#     def DelayPosition(self, x):
#         self.instr.write('HORizontal[:MAIn]:DELay:POSition ' + str(x))
#
#     # .....DPOJET Functions....................................................................................
#
#     def DpoJet(self):
#         self.instr.write('DPOJET:Ver?')  # starts DPOJET automatically
#
#     def DpoJet_Clear_All(self):
#         self.instr.write('DPOJET:CLEARALLMeas')  # clears DPOJET measurements
#
#     def DpoJet_Clear_Meas(self):
#         self.instr.write('DPOJET:CLEAR Meas')  # clears DPOJET measurements
#
#     def DpoJet_Stop(self):
#         self.instr.write('DPOJET:STATE STOP')  # STOP DPOJET measurements
#
#     def DpoJet_Single(self):
#         # self.instr.write('DPOJET:STATE START')  #START DPOJET measurements
#         self.instr.write('DPOJET:STATE SINGLE')  # START DPOJET measurements
#
#     def DpoJet_Run(self):
#         self.instr.write('DPOJET:STATE RUN')  # START DPOJET measurements
#
#     def Scope_Factory(self):
#         self.instr.write('FACTORY')  # Resets scope to factory setup
#
#     def Scope_AutoSet(self):
#         self.instr.write('AUTOSET EXEC')  # Autosets scope measurements
#
#     def Scope_DPO_AutoSet(self):
#         self.instr.write('DPOJET:SourceA Both')  # Autosets Horizontal and Veritacal scaling
#
#     def Scope_DPO_Resolution(self, resolution):
#         self.instr.write("HOR:MODE:RECO " + str(resolution))
#
#     def Scope_DPO_SouMeas(self, meascount, math_a):
#         self.instr.write("DPOJET:MEAS" + str(
#             meascount) + ":SOU " + math_a)  # meascount is line number in tests and math_a is Math1, Math2...
#
#     def Scope_CH1_ON(self):
#         self.instr.write('SEL:CH1 ON')  # Autosets scope measurements
#
#     def Scope_CH2_ON(self):
#         self.instr.write('SEL:CH2 ON')  # Autosets scope measurements
#
#     def Scope_CH3_ON(self):
#         self.instr.write('SEL:CH3 ON')  # Autosets scope measurements
#
#     def Scope_CH4_ON(self):
#         self.instr.write('SEL:CH4 ON')  # Autosets scope measurements
#
#     def Scope_CH1_OFF(self):
#         self.instr.write('SEL:CH1 OFF')  # Autosets scope measurements
#
#     def Scope_CH2_OFF(self):
#         self.instr.write('SEL:CH2 OFF')  # Autosets scope measurements
#
#     def Scope_CH3_OFF(self):
#         self.instr.write('SEL:CH3 OFF')  # Autosets scope measurements
#
#     def Scope_CH4_OFF(self):
#         self.instr.write('SEL:CH4 OFF')  # Autosets scope measurements
#
#     def Scope_CHANNEL_CONTROL(self, stat1, stat2, stat3, stat4):
#         # self.instr.write('SEL:CH1 ' + '"' + stat1 + ';' + '"')# + 'CH2' + stat2; + '"' + 'CH3' + stat3; + '"' + 'CH4' + stat4 + '"')  #Autosets scope measurements
#         # self.instr.write('SEL:CH1 ' + '"' + stat1 + ';' + 'CH2' + stat2 + ';' + 'CH3' + stat3 + ';' + 'CH4' + stat4 + '"')  #Autosets scope measurements
#         self.instr.write('SEL:CH1 ' + stat1)
#         self.instr.write('SEL:CH2 ' + stat2)
#         self.instr.write('SEL:CH3 ' + stat3)
#         self.instr.write('SEL:CH4 ' + stat4)
#
#     def Scope_CH_OFF_CONTROL(self):
#         self.instr.write('SEL:CH1 OFF;CH2 OFF;CH3 OFF; CH4 OFF')  # Autosets scope measurements
#
#     def SamplingModeRT(self):
#         self.instr.write('ACQuire:SAMPlingmode RT')
#         self.instr.write('CH1:BANdwidth:ENHanced:FORCe ON')
#
#     def ZoomON(self):
#         self.instr.write('ZOOm:MODe ON')
#         self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 200')
#         self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 1')
#
#     def DpoJet_Recall_Setup(self):
#         self.instr.write('RECALL:SETUP ' + '"' + "c:\File Path .set" + '"')  # Recall Setup
#
#     def DpoJet_Recall_Mask(self, fpath, fname):
#         self.instr.write('DPOJET:ADDM MASKHits')  # measurement 6 _ Plot 1
#         self.instr.write('DPOJET:MEAS1:MASKF ' + '"' + fpath + fname + '"')
#         # fpath = C:/TekApplications/DPOJET/Masks/JESDB/
#         # wrtmsg(scope,'DPOJET:MEAS6:MASKF ' + '"' + fpath + fname + '"')   # mask file location
#
#     def DpoJet_PLL_Setup(self, frequency):
#         self.instr.write('DPOJET:MEAS1:BITTYPE ALLBITS')
#         self.instr.write('DPOJET:MEAS1:CLOCKRECOVERY:METHOD CUSTOM')  # SET TO WHATEVER METHOD USER WANTS
#         self.instr.write('DPOJET:MEAS1:CLOCKRECOVERY:MODEL ONE')  # CAN BE EITHER ONE OR TWO -  FILTER ROLLOFF
#         self.instr.write('DPOJET:MEAS1:CLOCKRECOVERY:LoopBandwidth ' + str((frequency) / 1667))
#         # scope1.write("DPOJET:MEAS1:CLOCKRECOVERY:LoopBandwidth " + str(datarate(variable)/1667)
#         # scope1.write("DPOJET:MEAS1:CLOCKRECOVERY:LoopBandwidth " + str(6.144e9/1667))
#
#     def JESD204BCT_PLL_Setup(self, test_number, frequency):
#         i = 1
#         while (i < test_number + 1):
#             if (i <> 4):
#                 self.instr.write('DPOJET:MEAS' + str(i) + ':BITTYPE ALLBITS')
#                 self.instr.write(
#                     'DPOJET:MEAS' + str(i) + ':CLOCKRECOVERY:METHOD CUSTOM')  # SET TO WHATEVER METHOD USER WANTS
#                 self.instr.write(
#                     'DPOJET:MEAS' + str(i) + ':CLOCKRECOVERY:MODEL ONE')  # CAN BE EITHER ONE OR TWO -  FILTER ROLLOFF
#                 self.instr.write('DPOJET:MEAS' + str(i) + ':CLOCKRECOVERY:LoopBandwidth ' + str((frequency) / 1667))
#                 i += 1
#             if (i == 4):
#                 i += 1
#
#     def JESD204BCT_RJDJ_BER_Target(self, test_number, ber):
#         i = 1
#         while (i < test_number + 1):
#             self.instr.write('DPOJET:MEAS' + str(i) + ':RJDJ:BER ' + str(ber))
#             self.instr.write('DPOJET:MEAS' + str(i) + ':BER:TARGETBER ' + str(ber))
#             i += 1
#
#     def JESD204BCT_RJDJ_Pattern_Length(self, test_number, pattern):
#         i = 1
#         while (i < test_number + 1):
#             self.instr.write('DPOJET:MEAS' + str(i) + ':RJDJ:PATL ' + str(pattern))
#             i += 1
#
#     def DpoJet_Load_Test(self, test_name):
#         self.instr.write('DPOJET:ADDM ' + str(test_name))
#
#     def DpoJet_Set_Math1(self, CH_A, CH_B, Operand):
#         self.instr.write('MATH1:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  # sets up Math1
#         self.instr.write('SEL:MATH1 ON')
#
#     def DpoJet_Set_Math2(self, CH_A, CH_B, Operand):
#         self.instr.write('MATH2:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  # sets up Math2
#         self.instr.write('SEL:MATH2 ON')
#
#     def DpoJet_Set_Math3(self, CH_A, CH_B, Operand):
#         self.instr.write('MATH3:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  # sets up Math3
#         self.instr.write('SEL:MATH3 ON')
#
#     def DpoJet_Set_Math4(self, CH_A, CH_B, Operand):
#         self.instr.write('MATH4:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  # sets up Math4
#         self.instr.write('SEL:MATH4 ON')
#
#     def DpoJet_TurnOffChannels(self):
#         self.instr.write('SEL:CH1 OFF')  # Autosets scope measurements
#         self.instr.write('SEL:CH2 OFF')  # Autosets scope measurements
#         self.instr.write('SEL:CH3 OFF')  # Autosets scope measurements
#         self.instr.write('SEL:CH4 OFF')  # Autosets scope measurements
#         self.instr.write('SEL:MATH1 OFF')  # Autosets scope measurements
#         self.instr.write('SEL:MATH2 OFF')  # Autosets scope measurements
#
#     def DpoJet_Set_LaneA(self, vterm, zoom='ON'):
#         # self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
#         # self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
#         self.instr.write('MATH1:DEFINE "CH1-CH3"')  # sets up Math1
#         self.instr.write('SEL:CH1 ON')  # Autosets scope measurements
#         self.instr.write('SEL:CH3 ON')  # Autosets scope measurements
#         self.instr.write('SEL:MATH1 ON')
#         self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH1:OFFSet ' + str(1.5 * vterm))
#         self.instr.write('CH2:OFFSet ' + str(1.5 * vterm))
#         self.instr.write('CH3:OFFSet ' + str(1.5 * vterm))
#         self.instr.write('CH4:OFFSet ' + str(1.5 * vterm))
#         self.instr.write('ZOOm:MODe ' + str(zoom))
#         self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 10000')
#         self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 2')
#         self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 2')
#         self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
#         self.instr.write('CH1:POSition 0')
#         self.instr.write('CH3:POSition 0')
#         self.instr.write('TRIGger:A:EDGE:SOUrce:CH1')  # sets trigger source
#         # self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
#         # wx.MilliSleep(5000) #
#         self.instr.write('TRIGger:A SETLevel')  # sets trigger location
#
#     def DpoJet_Set_LaneB(self, vterm, zoom='ON'):
#         # self.instr.write('SEL:CH2 ON')  #Autosets scope measurements
#         # self.instr.write('SEL:CH4 ON')  #Autosets scope measurementsself.instr.write('MATH2:DEFINE "CH2-CH4"')  #sets up Math1
#         self.instr.write('MATH2:DEFINE "CH2-CH4"')  # sets up Math1
#         self.instr.write('SEL:CH2 ON')  # Autosets scope measurements
#         self.instr.write('SEL:CH4 ON')  # Autosets scope measurements
#         self.instr.write('SEL:MATH2 ON')
#         self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH1:OFFSet ' + str(1.5 * vterm))
#         self.instr.write('CH2:OFFSet ' + str(1.5 * vterm))
#         self.instr.write('CH3:OFFSet ' + str(1.5 * vterm))
#         self.instr.write('CH4:OFFSet ' + str(1.5 * vterm))
#         self.instr.write('ZOOm:MODe ' + str(zoom))
#         self.instr.write('ZOOm:ZOOM1:CH2:HORizontal:SCAle 10000')
#         self.instr.write('ZOOm:ZOOM1:CH2:VERtical:SCAle 2')
#         self.instr.write('ZOOm:ZOOM1:CH4:VERtical:SCAle 2')
#         # self.instr.write('ZOOm:ZOOM1:Math2:DISplay OFF')
#         self.instr.write('CH2:POSition 0')
#         self.instr.write('CH4:POSition 0')
#         self.instr.write('TRIGger:A:EDGE:SOUrce:CH2')  # sets trigger source
#         # self.instr.write('TRIGger:A:LEVel:CH3 ' + str((vterm+1)/2))
#         # wx.MilliSleep(5000) #
#         self.instr.write('TRIGger:A SETLevel')  # sets trigger location
#
#     def DpoJet_Set_DiffProbeCh1(self, vterm, zoom='ON'):
#         # self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
#         # self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
#         # self.instr.write('MATH1:DEFINE "CH1-CH3"')   #sets up Math1
#         self.instr.write('SEL:CH1 ON')  # Autosets scope measurements
#         self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH1:OFFSet ' + str(vterm))
#         self.instr.write('CH2:OFFSet ' + str(vterm))
#         self.instr.write('CH3:OFFSet ' + str(vterm))
#         self.instr.write('CH4:OFFSet ' + str(vterm))
#         self.instr.write('ZOOm:MODe ' + str(zoom))
#         self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 10000')
#         self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 1')
#         # self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 1')
#         # self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
#         self.instr.write('CH1:POSition 0')
#         self.instr.write('TRIGger:A:EDGE:SOUrce:CH1')  # sets trigger source
#         # self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
#         # wx.MilliSleep(5000) #
#         self.instr.write('TRIGger:A SETLevel')  # sets trigger location
#
#     def DpoJet_Set_DiffProbeCh3(self, vterm, zoom='ON'):
#         # self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
#         # self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
#         # self.instr.write('MATH1:DEFINE "CH1-CH3"')   #sets up Math1
#         self.instr.write('SEL:CH3 ON')  # Autosets scope measurements
#         self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH1:OFFSet ' + str(vterm))
#         self.instr.write('CH2:OFFSet ' + str(vterm))
#         self.instr.write('CH3:OFFSet ' + str(vterm))
#         self.instr.write('CH4:OFFSet ' + str(vterm))
#         self.instr.write('ZOOm:MODe ' + str(zoom))
#         self.instr.write('ZOOm:ZOOM1:CH3:HORizontal:SCAle 10000')
#         # self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 1')
#         self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 1')
#         # self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
#         self.instr.write('CH3:POSition 0')
#         self.instr.write('TRIGger:A:EDGE:SOUrce:CH3')  # sets trigger source
#         # self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
#         # wx.MilliSleep(5000) #
#         self.instr.write('TRIGger:A SETLevel')  # sets trigger location
#
#     def DpoJet_Measure(self, channel, measure):
#         self.instr.write('MEASU:IMM:SOU ' + channel)
#         self.instr.write('MEASU:IMM:TYPE ' + measure)
#         return self.instr.ask('MEASU:IMM:VALUE?')
#         # wrtmsg(scope,"SAVE:SETUP 10")
#         # wrtmsg(scope,"RECALL:SETUP 10")
#
#     def DpoJet_Indivdual_Measure(self, meascount, measure):
#         return self.instr.ask('DPOJET:MEAS' + str(meascount) + ':RESULts:ALLAcqs:' + str(measure) + '?')
#
#     def DpoJet_Intra_Pair(self):
#         # Measure Intra pair Skew
#         self.instr.write("DPOJET:ADDM SKEW")  # measurement 14
#         self.instr.write("DPOJET:MEAS1:CUST 'Intra-pair skew'")  # sets name of test on screen(Custom measurement Name)
#         self.instr.write("DPOJET:MEAS1:SOU1 CH1")
#         self.instr.write("DPOJET:MEAS1:SOU2 CH3")
#         self.instr.write("DPOJET:MEAS1:EDGE1 RISE")
#         self.instr.write("DPOJET:MEAS1:EDGE2 FALL")
#
#     def DpoJet_Intra_Pair1_3(self, testnum):
#         # Measure Intra pair Skew
#         self.instr.write("DPOJET:ADDM SKEW")  # measurement 14
#         self.instr.write("DPOJET:MEAS" + str(
#             testnum) + ":CUST 'Intra-pair skew'")  # sets name of test on screen(Custom measurement Name)
#         self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU1 CH1")
#         self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU2 CH3")
#         self.instr.write("DPOJET:MEAS" + str(testnum) + ":EDGE1 BOTH")
#         self.instr.write("DPOJET:MEAS" + str(testnum) + ":TOE OPP")  # To Edge opposite of from edge
#
#     def DpoJet_Intra_Pair2_4(self, testnum):
#         # Measure Intra pair Skew
#         self.instr.write("DPOJET:ADDM SKEW")  # measurement 14
#         self.instr.write("DPOJET:MEAS" + str(
#             testnum) + ":CUST 'Intra-pair skew'")  # sets name of test on screen(Custom measurement Name)
#         self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU1 CH2")
#         self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU2 CH4")
#         self.instr.write("DPOJET:MEAS" + str(testnum) + ":EDGE1 BOTH")
#         self.instr.write("DPOJET:MEAS" + str(testnum) + ":TOE OPP")  # To Edge opposite of from edge
#
#     def DpoJet_CM_Source(self, testnum, lane):
#         if (lane == 00):
#             self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU1 CH1")
#             self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU2 CH3")
#         if (lane == 01):
#             self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU1 CH2")
#             self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU2 CH4")
#         if (lane == 10):
#             self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU1 CH1")
#             self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU2 CH1")
#         if (lane == 11):
#             self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU1 CH3")
#             self.instr.write("DPOJET:MEAS" + str(testnum) + ":SOU2 CH3")
#
#     def DpoJet_AddBathtub(self, testnum):
#         self.instr.write("DPOJET:ADDP BATH, MEAS" + str(testnum))
#         self.instr.write("DPOJET:PLOT3:BATH:BER 16")
#
#     def DpoJet_AddHistogram(self, testnum):
#         self.instr.write("DPOJET:ADDP HISTO, MEAS" + str(testnum))
#
#     def DpoJet_AddSpectrum(self, testnum):
#         self.instr.write("DPOJET:ADDP SPECtrum, MEAS" + str(testnum))
#
#     def DpoJet_RiseFall20_80(self, testnum):
#         self.instr.write('DPOJET:REFLevels:CH1:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH2:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH3:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH4:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:Math1:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:Math2:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH1:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:CH2:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:CH3:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:CH4:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:Math1:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:Math2:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:CH1:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH2:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH3:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH4:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:Math1:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:Math2:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH1:PERcent:RISELow 20')
#         self.instr.write('DPOJET:REFLevels:CH2:PERcent:RISELow 20')
#         self.instr.write('DPOJET:REFLevels:CH3:PERcent:RISELow 20')
#         self.instr.write('DPOJET:REFLevels:CH4:PERcent:RISELow 20')
#         self.instr.write('DPOJET:REFLevels:Math1:PERcent:RISELow 20')
#         self.instr.write('DPOJET:REFLevels:Math2:PERcent:RISELow 20')
#
#     def BathtubPlotBugFixSave(self):
#         self.instr.write('SAVE:SETUP 10')
#
#     def BathtubPlotBugFixRecall(self):
#         self.instr.write('RECALL:SETUP 10')
#
#     # def DpoJet_Intra_Pair(self):
#     #   wrtmsg(scope,"DPOJET:ADDP HISTO, MEAS5")
#
#     # ........End DPOJET Functions......................................................................................
#
#     def HistogramBox(self, a, b, c, d):
#         self.instr.write(
#             'HIStogram:Box ' + str(a) + ', ' + str(b) + ', ' + str(c) + ', ' + str(d))  # sets histogram box parameters
#
#     def HistogramModeHor(self):  # sets the histogram mode: horizaontal or vertical
#         self.instr.write('HIStogram:MODe Horizontal')
#
#     def HistogramModeVer(self):  # sets the histogram mode: horizaontal or vertical
#         self.instr.write('HIStogram:MODe VERTICAL')
#
#     def HistogramSource(self, Source):
#         self.instr.write('HIStogram:SOU ' + Source)
#
#     def DelayMeasureDirection(self, direction):
#         self.instr.write(
#             'MEASUrement:IMMed:DELay:DIREction ' + direction)  # sets search direction for delay measurement
#
#     def DelayMeasureTo(self, Source2):
#         self.instr.write('MEASUrement:IMMed:SOURCE2 ' + Source2)  # sets to edge in delay measurement
#
#     def DelayMeasureFrom(self, Source1):
#         self.instr.write('MEASUrement:IMMed:SOURCE[1] ' + Source1)  # sets from edge in delay measurement
#
#     def ImmediateMeasureDelay(self):
#         self.instr.write('MEASUrement:IMMed:TYPe DEL')  # sets immediate measurement type
#
#     def ImmediateMeasureHits(self):
#         self.instr.write('MEASUrement:IMMed:TYPe HITS')  # sets immediate measurement type
#
#     def ImmediateMeasurePhase(self):
#         self.instr.write('MEASUrement:IMMed:TYPe PHAse')  # sets immediate measurement type
#
#     def ImmediateMeasurementValue(self):
#         return float(self.instr.ask('MEASUrement:IMMed:VALue?'))  # returns measurement value
#
#     def Resolution(self, Resolution):
#         self.instr.write('HOR:RESO ' + str(Resolution))
#
#     # Olie's inputs
#     def GetTriggerPosition(self):
#         return float(self.instr.ask('WFMOutpre:PT_Off?'))  # find trigger position in samples
#
#     def Xinc(self):
#         return float(self.instr.ask('WFMOutpre:XINcr?'))  # time increment per sample
#
#     def GetHscale(self):
#         return float(self.instr.ask('HORizontal:MAIn:SCAle?'))  # get time/div
#
#     def SetHscale(self, hscale):
#         self.instr.write('HORizontal:MAIn:SCAle ' + str(hscale))
#
#     def GetVscale(self, Source2):
#         return float(self.instr.ask(Source2 + ":SCALe?"))
#
#     def SetVscale(self, ch, vscale):
#         self.instr.write(str(ch) + ':SCAle ' + str(vscale))
#
#     def SetVscaleAll(self, vscale):
#         self.instr.write('CH1:SCAle ' + str(vscale))
#         self.instr.write('CH2:SCAle ' + str(vscale))
#         self.instr.write('CH3:SCAle ' + str(vscale))
#         self.instr.write('CH4:SCAle ' + str(vscale))
#         self.instr.write('Math1:SCAle ' + str(vscale * 2))
#         self.instr.write('Math2:SCAle ' + str(vscale * 2))
#
#     def SetVterm(self, ch, vterm):
#         self.instr.write(str(ch) + ':VTERm:BIAS ' + str(vterm))
#
#     def SetPosition(self, ch, position):
#         self.instr.write(str(ch) + ':POSition ' + str(position))
#
#     def SetOffset(self, ch, offset):
#         self.instr.write(str(ch) + ':OFFSet ' + str(offset))
#
#     def SetSRC2(self, Source2):
#         self.instr.write('MEASUrement:IMMed:SOURCE2 ' + Source2)  # sets to edge in delay measurement
#
#     def SetSRC1(self, Source1):
#         self.instr.write('MEASUrement:IMMed:SOURCE[1] ' + Source1)  #
#
#     # def SetSrc1(self, Source1):
#     #    self.instr.write('MEASUrement:IMMed:SOURCE[1] ' + Source1)  #sets from edge in delay measurement
#     # def Set1Src1(self):
#     #    return str(self.instr.ask('MEASUrement:IMMed:SOURCE[1]?'))
#
#     def SetChanDelay(self, Chan, Delay):
#         self.instr.write(Chan + ':DESKew ' + Delay)  # sets from edge in delay measurement
#
#     def GetChanDelay(self, Chan):
#         return float(self.instr.ask(Chan + ':DESKew?'))  # sets from edge in delay measurement
#
#     def SetDelay(self):
#         self.instr.write('MEASUrement:IMMed:TYPe DELay')  # sets from edge in delay measurement
#
#     def SetFreq(self):
#         self.instr.write('MEASUrement:IMMed:TYPe FREQuency')  # sets from edge in delay measurement
#
#     def SetPeriod(self):
#         self.instr.write('MEASUrement:IMMed:TYPe PERIOD')  # sets from edge in delay measurement
#
#     def SetDuty(self):
#         self.instr.write('MEASUrement:IMMed:TYPe PDUty')  # sets from edge in delay measurement
#
#     def Edge1(self):
#         self.instr.write('MEASUrement:IMMed:DELay:EDGE1 RISE')  # sets from edge in delay measurement
#
#     def DelayMeasureEdge1(self, edge):
#         self.instr.write('MEASUrement:IMMed:DELay:EDGE1 ' + edge)
#
#     def Edge2(self):
#         self.instr.write('MEASUrement:IMMed:DELay:EDGE2 RISE')  # sets from edge in delay measurement
#
#     def DelayMeasureEdge2(self, edge):
#         self.instr.write('MEASUrement:IMMed:DELay:EDGE2 ' + edge)
#
#     def DirectBackards(self):
#         self.instr.write(':MEASUREMENT:IMMED:DELAY:DIRECTION BACKWARDS')  # sets from edge in delay measurement
#
#     def DirectForward(self):
#         self.instr.write(':MEASUREMENT:IMMED:DELAY:DIRECTION FORWARDs')  # sets from edge in delay measurement
#
#     def GetValue(self):
#         return float(self.instr.ask('MEASUrement:IMMed:VALue?'))  # gets efined value
#
#     def DefineTrig(self, Source1):
#         self.instr.write('DATA:SOURCE ' + Source1)  # sets from edge in delay measurement
#
#     def DefineTrig1(self, Source1):
#         self.instr.write('TRIGger:A:EDGE:SOUrce ' + Source1)
#
#     def SetHigh(self):
#         self.instr.write('MEASUrement:IMMed:TYPe HIGH')  # sets from edge in delay measurement
#
#     def SetMax(self):
#         self.instr.write('MEASUrement:IMMed:TYPe MAX')  # sets from edge in delay measurement
#
#     def SetMin(self):
#         self.instr.write('MEASUrement:IMMed:TYPe MINI')  # sets from edge in delay measurement
#
#     def SetMeaSRC2(self, number, Source2):
#         self.instr.write('MEASUrement:MEAS' + str(number) + ':SOURCE[2] ' + Source2)  #
#
#     def SetMeasSRC1(self, number, Source1):
#         self.instr.write('MEASUrement:MEAS' + str(number) + ':SOURCE[1] ' + Source1)  #
#
#     def SetMeasureMax(self, number):
#         self.instr.write('MEASUrement:MEAS' + str(number) + ':TYPe MAX')  # sets from edge in delay measurement
#
#     def SetMeasureMin(self, number):
#         self.instr.write('MEASUrement:MEAS' + str(number) + ':TYPe MINI')
#
#     def MeasureMax(self, number):
#         return float(self.instr.ask('MEASUrement:MEAS' + str(number) + ':MAX?'))  # sets from edge in delay measurement
#
#     def MeasureMin(self, number):
#         return float(self.instr.ask('MEASUrement:MEAS' + str(number) + ':MINI?'))
#
#     def MeasureMean(self, number):
#         return float(self.instr.ask('MEASUrement:MEAS' + str(number) + ':MEAN?'))
#
#     def SetLow(self):
#         self.instr.write('MEASUrement:IMMed:TYPe LOW')  # sets from edge in delay measurement
#
#     def SetAmplitude(self):
#         self.instr.write('MEASUrement:IMMed:TYPe AMP')  # sets from edge in delay measurement
#
#     def SetHist(self, Source2):
#         self.instr.write('HIStogram:SOUrce ' + Source2)  # sets from edge in delay measurement
#
#     def SetHistStateON(self):
#         self.instr.write('HIStogram:STATE ON')  # sets from edge in delay measurement
#
#     def SetHistBox(self, leftp, topp, rightp, bottomp):
#         self.instr.write('HIStogram:Box ' + str(leftp) + "," + str(topp) + "," + str(rightp) + "," + str(
#             bottomp))  # sets from edge in delay measurement
#
#     def HeaderOFF(self):
#         self.instr.write('HEADer OFF')
#
#     def runTDSHT3(self):
#         self.instr.write('VARIABLE:VALUE "sequencerState","Sequencing"')
#
#     def saveWaveform(self, fname):
#         # self.instr.write('SAVE:WAVEFORM:FILEFORMAT SPREADSHEETCsv')
#         self.instr.write('SAve:WAVEform CH1 ' + ',' + '"' + str(fname) + '"')
#         print "this is", str(fname)
#         # self.instr.write('SAve:WAVEform Math1 ' + ',' + '"rene3.cvs"') #this code works
#
#         # self.instr.write('SAve:WAVEform Math1, "rene.cvs"') This code works
#
#     def Set_Chan1_Chan3_Math1(self, vterm, zoom='ON'):
#         # self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
#         # self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
#         self.instr.write('MATH1:DEFINE "CH1-CH3"')  # sets up Math1
#         self.instr.write('SEL:CH1 OFF')  # Autosets scope measurements
#         self.instr.write('SEL:CH3 OFF')  # Autosets scope measurements
#         self.instr.write('SEL:MATH1 ON')
#         self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH1:OFFSet ' + str(vterm))
#         self.instr.write('CH2:OFFSet ' + str(vterm))
#         self.instr.write('CH3:OFFSet ' + str(vterm))
#         self.instr.write('CH4:OFFSet ' + str(vterm))
#         self.instr.write('ZOOm:MODe ' + str(zoom))
#         self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 10000')
#         self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 2')
#         self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 2')
#         self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
#         self.instr.write('CH1:POSition 0')
#         self.instr.write('CH3:POSition 0')
#         self.instr.write('TRIGger:A:EDGE:SOUrce CH1')  # sets trigger source
#         # self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
#         # wx.MilliSleep(5000) #
#         self.instr.write('TRIGger:A SETLevel')  # sets trigger location
#
#     def Get_Chan1_Chan3_Math1_Measurement(self, measure):
#         self.instr.write# Predefined variables and functions
# # evalapp - the eval app XML object
# # topwin - the main frame class
# # readAll - read all interfaces of all chips
# # writeAll - write all settings to all chips
# # getSavePath - ask the user for a path to save a file
# # getOpenPath - ask the user for a path to open a file
# # unloadBoards - unload the currently loaded boards
# # loadBoard - load a new board from XML
# # ProgressDialog - a class for showing progress of your script
# from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
#
# # print "this is the file for the TekDSA scope"
# class TekDSA72504D(GPIBObjectBaseClass):
#     def __init__(self, addr=-1):
#         GPIBObjectBaseClass.__init__(self, 'TEKTRONIX,DSA72504D',addr)
#
#     def GetAcqPar(self):
#         return self.instr.ask('ACQ?')
#
#     def GetFreq(self):
#         self.instr.write('MEASU:IMM:TYP FREQ')
#         return float(self.instr.ask('MEASU:IMM:VAL?'))
#
#     def MeasFreq(self, source):
#         self.instr.write('MEASU:MEAS1:TYP FREQ')
#         self.instr.write('MEASU:MEAS1:SOURCE CH' + str(source))
#         return self.instr.ask('MEASU:MEAS1:MEAN?')
#
#
#     def GetSRC1(self):
#         print "test"
#         self.instr.write('MEASU:IMM:SOURCE[10000]?')
#         return float(self.instr.ask('MEASU:IMM:VAL?'))
#
#     def GetSRC2(self):
#         self.instr.write('MEASU:IMM:SOURCE2?')
#         #return float(self.instr.ask('MEASU:IMM:VAL?'))
#
#     def GetDely(self):
#         self.instr.write('MEASU:IMM:TYP DEL')
#         return float(self.instr.ask('MEASU:IMM:VAL?'))
#
#     def GetUnits(self):
#         self.instr.write('MEASU:IMM:TYP UNI?')
#         return float(self.instr.ask('MEASU:IMM:VAL?'))
#
#     def FastAcqOn(self):
#         self.instr.write(':FastAcq:state 1')
#
#     def FastAcqOff(self):
#         self.instr.write(':FastAcq:state 0')
#
#     def SetJitter(self, Source):
#         self.instr.write('HIS:SOU '+Source)
#
#     def GetJitterPKPK(self,MEAS):
#         #self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:'+MEAS+':VAL?'))
#
#     def GetJitterRMS(self,MEAS):
#         #self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:'+MEAS+':VAL?'))
#     def GetMeasuredValue(self,MEAS):
#         #self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:'+MEAS+':VAL?'))
#
#     def GetMeasuredMax(self,MEAS):
#         #self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:'+MEAS+':MAX?'))
#
#     def GetMeasuredMin(self,MEAS):
#         #self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:'+MEAS+':MINI?'))
#
#     def GetMeasuredSTD(self,MEAS):
#         #self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:'+MEAS+':STD?'))
#
#     def GetMeasuredMean(self,MEAS):
#         #self.instr.write('MEASU:MEAS1:PKPKJitter')
#         return float(self.instr.ask('MEASU:'+MEAS+':MEAN?'))
#
#     def SetSingle(self):
#         self.instr.write('ACQuire:STOPAFTER SEQUENCE') #sets the single button
#
#     def SetAcqON(self):
#         print "test1"
#         self.instr.write('ACQuire:STATE RUN') #sets the single button
#
#     def SetAcqOFF(self):
#         self.instr.write('ACQuire:STATE STOP') #sets the single button
#
#     #def SetSEQ(self):
#         #self.instr.write('ACQuire:STOPAFTER SEQUENCE') #sets the single button
#
#     def SetTriggerEdgeSource(self,x):
#         self.instr.write('TRIGger:A:EDGE:SOUrce '+str(x))  #sets horizontal trigger location
#
#     def GetTriggerEdgeSource(self):
#         return self.instr.ask('TRIGger:A:EDGE:SOUrce?')  #sets horizontal trigger location
#
#     def SetTriggerEdgeSlope(self,x):
#         self.instr.write('TRIGger:A:EDGE:SLOpe '+str(x))  #sets horizontal trigger location
#
#     def GetTriggerEdgeSlope(self):
#         return self.instr.ask('TRIGger:A:EDGE:SLOpe?')
#
#     def SetTriggerEdgeCoupling(self,x):
#         self.instr.write('TRIGger:A:EDGE:COUPling '+str(x))
#
#     def GetTriggerEdgeCoupling(self):
#         return self.instr.ask('TRIGger:A:EDGE:COUPling?')
#
#     def AcqState(self):
#         return self.instr.ask('ACQ:STATE?')
#
#     def SetRun(self):
#         self.instr.write('ACQuire:STOPAFTER RUNSTOP') #sets run/stop
#
#     def HorizontalMode(self,x):
#         self.instr.write('HORizontal:MODE ' +str(x)) # the modes are AUTO, CONSTANT, MANUAL
#     def SampleRate(self,x):
#         self.instr.write('HORizontal:MODE:SAMPLERATE ' +str(x)) # sets the sample rate
#
#     def TimeBase(self,y):
#         self.instr.write('HORizontal:MAIn:SCAle '+str(y)) #sets horizontal time base
#
#     def SetVertTriggerPos1(self,x):
#         self.instr.write('TRIGger:A:Level:CH1 '+str(x))  #sets vertical trigger position on CH1
#
#     def SetVertTriggerPos2(self,x):
#         self.instr.write('TRIGger:A:Level:CH2 '+str(x))  #ssets vertical trigger position on CH2
#
#     def SetVertTriggerPos3(self,x):
#         self.instr.write('TRIGger:A:Level:CH3 '+str(x))  #sets vertical trigger position on CH3
#
#     def SetVertTriggerPos4(self,x):
#         self.instr.write('TRIGger:A:Level:CH4 '+str(x))  #sets vertical trigger position on CH4
#
#     def SetTriggerPos(self,x):
#         self.instr.write('HORizontal:TRIGger:POSition '+str(x))  #sets horizontal trigger location
#
#     def GetTriggerPos(self):
#         return float(self.instr.ask('HORizontal:TRIGger:POSition?'))  #gets horizontal trigger location
#
#     def SetTrigger50(self):
#         self.instr.write('TRIGger:A: SETLevel')  #sets horizontal trigger location
#
#     def DelayTime(self,x):
#         self.instr.write('HORizontal[:MAIn]:DELay:TIMe '+str(x))
#
#     def DelayPosition(self,x):
#         self.instr.write('HORizontal[:MAIn]:DELay:POSition '+str(x))
#
#     #.....DPOJET Functions....................................................................................
#
#     def DpoJet(self):
#         self.instr.write('DPOJET:Ver?')  #starts DPOJET automatically
#
#     def DpoJet_Clear_All(self):
#         self.instr.write('DPOJET:CLEARALLMeas')  #clears DPOJET measurements
#
#     def DpoJet_Clear_Meas(self):
#         self.instr.write('DPOJET:CLEAR Meas')  #clears DPOJET measurements
#
#     def DpoJet_Stop(self):
#         self.instr.write('DPOJET:STATE STOP')  #STOP DPOJET measurements
#
#     def DpoJet_Single(self):
#         #self.instr.write('DPOJET:STATE START')  #START DPOJET measurements
#         self.instr.write('DPOJET:STATE SINGLE')  #START DPOJET measurements
#
#     def DpoJet_Run(self):
#         self.instr.write('DPOJET:STATE RUN')  #START DPOJET measurements
#
#     def Scope_Factory(self):
#         self.instr.write('FACTORY')  #Resets scope to factory setup
#
#     def Scope_AutoSet(self):
#         self.instr.write('AUTOSET EXEC')  #Autosets scope measurements
#
#     def Scope_DPO_AutoSet(self):
#         self.instr.write('DPOJET:SourceA Both')  #Autosets Horizontal and Veritacal scaling
#
#     def Scope_DPO_Resolution(self,resolution):
#         self.instr.write("HOR:MODE:RECO "+ str(resolution))
#
#     def Scope_DPO_SouMeas(self,meascount,math_a):
#         self.instr.write("DPOJET:MEAS" + str(meascount)+ ":SOU " + math_a)   #meascount is line number in tests and math_a is Math1, Math2...
#
#
#     def Scope_CHANNEL_CONTROL(self,stat1,stat2,stat3,stat4):
#         #self.instr.write('SEL:CH1 ' + '"' + stat1 + ';' + '"')# + 'CH2' + stat2; + '"' + 'CH3' + stat3; + '"' + 'CH4' + stat4 + '"')  #Autosets scope measurements
#         #self.instr.write('SEL:CH1 ' + '"' + stat1 + ';' + 'CH2' + stat2 + ';' + 'CH3' + stat3 + ';' + 'CH4' + stat4 + '"')  #Autosets scope measurements
#         self.instr.write('SEL:CH1 ' + stat1)
#         self.instr.write('SEL:CH2 ' + stat2)
#         self.instr.write('SEL:CH3 ' + stat3)
#         self.instr.write('SEL:CH4 ' + stat4)
#
#     def Scope_CH_OFF_CONTROL(self):
#         self.instr.write('SEL:CH1 OFF;CH2 OFF;CH3 OFF; CH4 OFF')  #Autosets scope measurements
#
#     def SamplingModeRT(self):
#         self.instr.write('ACQuire:SAMPlingmode RT')
#         self.instr.write('CH1:BANdwidth:ENHanced:FORCe ON')
#
#     def ZoomON(self):
#         self.instr.write('ZOOm:MODe ON')
#         self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 200')
#         self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 1')
#
#
#     def DpoJet_Recall_Setup(self):
#         self.instr.write('RECALL:SETUP ' + '"' + "c:\File Path .set" + '"')  #Recall Setup
#
#     def DpoJet_Recall_Mask(self,fpath,fname):
#         self.instr.write('DPOJET:ADDM MASKHits')         # measurement 6 _ Plot 1
#         self.instr.write('DPOJET:MEAS1:MASKF ' + '"' + fpath + fname  + '"')
#         #fpath = C:/TekApplications/DPOJET/Masks/JESDB/
#         #wrtmsg(scope,'DPOJET:MEAS6:MASKF ' + '"' + fpath + fname + '"')   # mask file location
#
#     def DpoJet_PLL_Setup(self,frequency):
#         self.instr.write('DPOJET:MEAS1:BITTYPE ALLBITS')
#         self.instr.write('DPOJET:MEAS1:CLOCKRECOVERY:METHOD CUSTOM') #SET TO WHATEVER METHOD USER WANTS
#         self.instr.write('DPOJET:MEAS1:CLOCKRECOVERY:MODEL ONE') #CAN BE EITHER ONE OR TWO -  FILTER ROLLOFF
#         self.instr.write('DPOJET:MEAS1:CLOCKRECOVERY:LoopBandwidth ' + str((frequency)/1667))
#         #scope1.write("DPOJET:MEAS1:CLOCKRECOVERY:LoopBandwidth " + str(datarate(variable)/1667)
#         #scope1.write("DPOJET:MEAS1:CLOCKRECOVERY:LoopBandwidth " + str(6.144e9/1667))
#
#     def JESD204BCT_PLL_Setup(self,test_number,frequency):
#         i=1
#         while (i<test_number+1):
#             if(i<>4):
#                 self.instr.write('DPOJET:MEAS'+str(i)+':BITTYPE ALLBITS')
#                 self.instr.write('DPOJET:MEAS'+str(i)+':CLOCKRECOVERY:METHOD CUSTOM') #SET TO WHATEVER METHOD USER WANTS
#                 self.instr.write('DPOJET:MEAS'+str(i)+':CLOCKRECOVERY:MODEL ONE') #CAN BE EITHER ONE OR TWO -  FILTER ROLLOFF
#                 self.instr.write('DPOJET:MEAS'+str(i)+':CLOCKRECOVERY:LoopBandwidth ' + str((frequency)/1667))
#                 i += 1
#             if(i==4):
#                 i += 1
#
#     def JESD204BCT_RJDJ_BER_Target(self,test_number,ber):
#         i=1
#         while (i<test_number+1):
#             self.instr.write('DPOJET:MEAS'+str(i)+':RJDJ:BER '+ str(ber))
#             self.instr.write('DPOJET:MEAS'+str(i)+':BER:TARGETBER '+ str(ber))
#             i += 1
#
#     def JESD204BCT_RJDJ_Pattern_Length(self,test_number,pattern):
#         i=1
#         while (i<test_number+1):
#             self.instr.write('DPOJET:MEAS'+str(i)+':RJDJ:PATL '+ str(pattern))
#             i += 1
#
#     def DpoJet_Load_Test(self,test_name):
#         self.instr.write('DPOJET:ADDM ' + str(test_name))
#
#     def DpoJet_Set_Math1(self,CH_A,CH_B,Operand):
#         self.instr.write('MATH1:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  #sets up Math1
#         self.instr.write('SEL:MATH1 ON')
#
#     def DpoJet_Set_Math2(self,CH_A,CH_B,Operand):
#         self.instr.write('MATH2:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  #sets up Math2
#         self.instr.write('SEL:MATH2 ON')
#
#     def DpoJet_Set_Math3(self,CH_A,CH_B,Operand):
#         self.instr.write('MATH3:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  #sets up Math3
#         self.instr.write('SEL:MATH3 ON')
#
#     def DpoJet_Set_Math4(self,CH_A,CH_B,Operand):
#         self.instr.write('MATH4:DEFINE ' + '"' + CH_A + Operand + CH_B + '"')  #sets up Math4
#         self.instr.write('SEL:MATH4 ON')
#
#     def DpoJet_TurnOffChannels(self):
#         self.instr.write('SEL:CH1 OFF')  #Autosets scope measurements
#         self.instr.write('SEL:CH2 OFF')  #Autosets scope measurements
#         self.instr.write('SEL:CH3 OFF')  #Autosets scope measurements
#         self.instr.write('SEL:CH4 OFF')  #Autosets scope measurements
#         self.instr.write('SEL:MATH1 OFF')  #Autosets scope measurements
#         self.instr.write('SEL:MATH2 OFF')  #Autosets scope measurements
#
#
#     def DpoJet_Set_LaneA(self, vterm, zoom='ON'):
#         #self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
#         #self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
#         self.instr.write('MATH1:DEFINE "CH1-CH3"')   #sets up Math1
#         self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
#         self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
#         self.instr.write('SEL:MATH1 ON')
#         self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH1:OFFSet ' + str(1.5*vterm))
#         self.instr.write('CH2:OFFSet ' + str(1.5*vterm))
#         self.instr.write('CH3:OFFSet ' + str(1.5*vterm))
#         self.instr.write('CH4:OFFSet ' + str(1.5*vterm))
#         self.instr.write('ZOOm:MODe ' + str(zoom))
#         self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 10000')
#         self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 2')
#         self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 2')
#         self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
#         self.instr.write('CH1:POSition 0')
#         self.instr.write('CH3:POSition 0')
#         self.instr.write('TRIGger:A:EDGE:SOUrce:CH1')  #sets trigger source
#         #self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
#         #wx.MilliSleep(5000) #
#         self.instr.write('TRIGger:A SETLevel')  #sets trigger location
#
#     def DpoJet_Set_LaneB(self, vterm, zoom='ON'):
#         #self.instr.write('SEL:CH2 ON')  #Autosets scope measurements
#         #self.instr.write('SEL:CH4 ON')  #Autosets scope measurementsself.instr.write('MATH2:DEFINE "CH2-CH4"')  #sets up Math1
#         self.instr.write('MATH2:DEFINE "CH2-CH4"')   #sets up Math1
#         self.instr.write('SEL:CH2 ON')  #Autosets scope measurements
#         self.instr.write('SEL:CH4 ON')  #Autosets scope measurements
#         self.instr.write('SEL:MATH2 ON')
#         self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH1:OFFSet ' + str(1.5*vterm))
#         self.instr.write('CH2:OFFSet ' + str(1.5*vterm))
#         self.instr.write('CH3:OFFSet ' + str(1.5*vterm))
#         self.instr.write('CH4:OFFSet ' + str(1.5*vterm))
#         self.instr.write('ZOOm:MODe ' + str(zoom))
#         self.instr.write('ZOOm:ZOOM1:CH2:HORizontal:SCAle 10000')
#         self.instr.write('ZOOm:ZOOM1:CH2:VERtical:SCAle 2')
#         self.instr.write('ZOOm:ZOOM1:CH4:VERtical:SCAle 2')
#         #self.instr.write('ZOOm:ZOOM1:Math2:DISplay OFF')
#         self.instr.write('CH2:POSition 0')
#         self.instr.write('CH4:POSition 0')
#         self.instr.write('TRIGger:A:EDGE:SOUrce:CH2')  #sets trigger source
#         #self.instr.write('TRIGger:A:LEVel:CH3 ' + str((vterm+1)/2))
#         #wx.MilliSleep(5000) #
#         self.instr.write('TRIGger:A SETLevel')  #sets trigger location
#
#     def DpoJet_Set_DiffProbeCh1(self, vterm, zoom='ON'):
#         #self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
#         #self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
#         #self.instr.write('MATH1:DEFINE "CH1-CH3"')   #sets up Math1
#         self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
#         self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH1:OFFSet ' + str(vterm))
#         self.instr.write('CH2:OFFSet ' + str(vterm))
#         self.instr.write('CH3:OFFSet ' + str(vterm))
#         self.instr.write('CH4:OFFSet ' + str(vterm))
#         self.instr.write('ZOOm:MODe ' + str(zoom))
#         self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 10000')
#         self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 1')
#         #self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 1')
#         #self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
#         self.instr.write('CH1:POSition 0')
#         self.instr.write('TRIGger:A:EDGE:SOUrce:CH1')  #sets trigger source
#         #self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
#         #wx.MilliSleep(5000) #
#         self.instr.write('TRIGger:A SETLevel')  #sets trigger location
#
#     def DpoJet_Set_DiffProbeCh3(self, vterm, zoom='ON'):
#         #self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
#         #self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
#         #self.instr.write('MATH1:DEFINE "CH1-CH3"')   #sets up Math1
#         self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
#         self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH1:OFFSet ' + str(vterm))
#         self.instr.write('CH2:OFFSet ' + str(vterm))
#         self.instr.write('CH3:OFFSet ' + str(vterm))
#         self.instr.write('CH4:OFFSet ' + str(vterm))
#         self.instr.write('ZOOm:MODe ' + str(zoom))
#         self.instr.write('ZOOm:ZOOM1:CH3:HORizontal:SCAle 10000')
#         #self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 1')
#         self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 1')
#         #self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
#         self.instr.write('CH3:POSition 0')
#         self.instr.write('TRIGger:A:EDGE:SOUrce:CH3')  #sets trigger source
#         #self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
#         #wx.MilliSleep(5000) #
#         self.instr.write('TRIGger:A SETLevel')  #sets trigger location
#
#     def DpoJet_Measure(self,channel,measure):
#         self.instr.write('MEASU:IMM:SOU ' + channel)
#         self.instr.write('MEASU:IMM:TYPE ' + measure)
#         return self.instr.ask('MEASU:IMM:VALUE?')
#         #wrtmsg(scope,"SAVE:SETUP 10")
#         #wrtmsg(scope,"RECALL:SETUP 10")
#
#     def DpoJet_Indivdual_Measure(self,meascount,measure):
#         return self.instr.ask('DPOJET:MEAS' +  str(meascount) + ':RESULts:ALLAcqs:' + str(measure) + '?')
#
#
#     def DpoJet_Intra_Pair(self):
#         # Measure Intra pair Skew
#         self.instr.write("DPOJET:ADDM SKEW")             # measurement 14
#         self.instr.write("DPOJET:MEAS1:CUST 'Intra-pair skew'") #sets name of test on screen(Custom measurement Name)
#         self.instr.write("DPOJET:MEAS1:SOU1 CH1")
#         self.instr.write("DPOJET:MEAS1:SOU2 CH3")
#         self.instr.write("DPOJET:MEAS1:EDGE1 RISE")
#         self.instr.write("DPOJET:MEAS1:EDGE2 FALL")
#
#     def DpoJet_Intra_Pair1_3(self,testnum):
#         # Measure Intra pair Skew
#         self.instr.write("DPOJET:ADDM SKEW")             # measurement 14
#         self.instr.write("DPOJET:MEAS"+str(testnum)+":CUST 'Intra-pair skew'") #sets name of test on screen(Custom measurement Name)
#         self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH1")
#         self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH3")
#         self.instr.write("DPOJET:MEAS"+str(testnum)+":EDGE1 BOTH")
#         self.instr.write("DPOJET:MEAS"+str(testnum)+":TOE OPP") # To Edge opposite of from edge
#
#     def DpoJet_Intra_Pair2_4(self,testnum):
#         # Measure Intra pair Skew
#         self.instr.write("DPOJET:ADDM SKEW")             # measurement 14
#         self.instr.write("DPOJET:MEAS"+str(testnum)+":CUST 'Intra-pair skew'") #sets name of test on screen(Custom measurement Name)
#         self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH2")
#         self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH4")
#         self.instr.write("DPOJET:MEAS"+str(testnum)+":EDGE1 BOTH")
#         self.instr.write("DPOJET:MEAS"+str(testnum)+":TOE OPP") # To Edge opposite of from edge
#
#     def DpoJet_CM_Source(self,testnum,lane):
#         if (lane==00):
#             self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH1")
#             self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH3")
#         if (lane==01):
#             self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH2")
#             self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH4")
#         if (lane==10):
#             self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH1")
#             self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH1")
#         if (lane==11):
#             self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU1 CH3")
#             self.instr.write("DPOJET:MEAS"+str(testnum)+":SOU2 CH3")
#
#     def DpoJet_AddBathtub(self,testnum):
#         self.instr.write("DPOJET:ADDP BATH, MEAS" + str(testnum))
#         self.instr.write("DPOJET:PLOT3:BATH:BER 16")
#
#     def DpoJet_AddHistogram(self,testnum):
#         self.instr.write("DPOJET:ADDP HISTO, MEAS" + str(testnum))
#
#     def DpoJet_AddSpectrum(self,testnum):
#         self.instr.write("DPOJET:ADDP SPECtrum, MEAS" + str(testnum))
#
#     def DpoJet_RiseFall20_80(self,testnum):
#         self.instr.write('DPOJET:REFLevels:CH1:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH2:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH3:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH4:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:Math1:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:Math2:PERcent:FALLHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH1:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:CH2:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:CH3:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:CH4:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:Math1:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:Math2:PERcent:FALLLow 20')
#         self.instr.write('DPOJET:REFLevels:CH1:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH2:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH3:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH4:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:Math1:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:Math2:PERcent:RISEHigh 80')
#         self.instr.write('DPOJET:REFLevels:CH1:PERcent:RISELow 20')
#         self.instr.write('DPOJET:REFLevels:CH2:PERcent:RISELow 20')
#         self.instr.write('DPOJET:REFLevels:CH3:PERcent:RISELow 20')
#         self.instr.write('DPOJET:REFLevels:CH4:PERcent:RISELow 20')
#         self.instr.write('DPOJET:REFLevels:Math1:PERcent:RISELow 20')
#         self.instr.write('DPOJET:REFLevels:Math2:PERcent:RISELow 20')
#
#     def BathtubPlotBugFixSave(self):
#         self.instr.write('SAVE:SETUP 10')
#
#     def BathtubPlotBugFixRecall(self):
#         self.instr.write('RECALL:SETUP 10')
#
#
#
#     #def DpoJet_Intra_Pair(self):
#     #   wrtmsg(scope,"DPOJET:ADDP HISTO, MEAS5")
#
#     #........End DPOJET Functions......................................................................................
#
#     def HistogramBox(self, a, b, c, d):
#         self.instr.write('HIStogram:Box '+str(a)+', '+str(b)+', '+str(c)+', '+str(d))  #sets histogram box parameters
#
#     def HistogramModeHor(self):#sets the histogram mode: horizaontal or vertical
#         self.instr.write('HIStogram:MODe Horizontal')
#
#     def HistogramModeVer(self):#sets the histogram mode: horizaontal or vertical
#         self.instr.write('HIStogram:MODe VERTICAL')
#
#     def HistogramSource(self,Source):
#         self.instr.write('HIStogram:SOU '+Source)
#
#     def DelayMeasureDirection(self,direction):
#         self.instr.write('MEASUrement:IMMed:DELay:DIREction '+direction)  #sets search direction for delay measurement
#
#     def DelayMeasureTo(self, Source2):
#         self.instr.write('MEASUrement:IMMed:SOURCE2 ' + Source2)  #sets to edge in delay measurement
#
#     def DelayMeasureFrom(self, Source1):
#         self.instr.write('MEASUrement:IMMed:SOURCE[1] ' + Source1)  #sets from edge in delay measurement
#
#     def ImmediateMeasureDelay(self):
#         self.instr.write('MEASUrement:IMMed:TYPe DEL')  #sets immediate measurement type
#
#     def ImmediateMeasureHits(self):
#         self.instr.write('MEASUrement:IMMed:TYPe HITS')  #sets immediate measurement type
#
#     def ImmediateMeasurePhase(self):
#         self.instr.write('MEASUrement:IMMed:TYPe PHAse')  #sets immediate measurement type
#
#     def ImmediateMeasurementValue(self):
#         return float(self.instr.ask('MEASUrement:IMMed:VALue?'))  #returns measurement value
#
#     def Resolution(self,Resolution):
#         self.instr.write('HOR:RESO ' + str(Resolution))
#
#     #Olie's inputs
#     def GetTriggerPosition(self):
#         return float(self.instr.ask('WFMOutpre:PT_Off?'))  #find trigger position in samples
#
#     def Xinc(self):
#         return float(self.instr.ask('WFMOutpre:XINcr?'))  #time increment per sample
#
#     def GetHscale(self):
#         return float(self.instr.ask('HORizontal:MAIn:SCAle?'))  #get time/div
#
#     def SetHscale(self, hscale):
#         self.instr.write('HORizontal:MAIn:SCAle ' + str(hscale))
#
#     def GetVscale(self, Source2):
#         return float(self.instr.ask(Source2 + ":SCALe?"))
#
#     def SetVscale(self, ch, vscale):
#         self.instr.write(str(ch) + ':SCAle ' + str(vscale))
#
#     def SetVscaleAll(self, vscale):
#         self.instr.write('CH1:SCAle ' + str(vscale))
#         self.instr.write('CH2:SCAle ' + str(vscale))
#         self.instr.write('CH3:SCAle ' + str(vscale))
#         self.instr.write('CH4:SCAle ' + str(vscale))
#         self.instr.write('Math1:SCAle ' + str(vscale*2))
#         self.instr.write('Math2:SCAle ' + str(vscale*2))
#
#     def SetVterm(self, ch, vterm):
#         self.instr.write(str(ch) + ':VTERm:BIAS ' + str(vterm))
#
#     def SetPosition(self, ch, position):
#         self.instr.write(str(ch) + ':POSition ' + str(position))
#
#     def SetOffset(self, ch, offset):
#         self.instr.write(str(ch) + ':OFFSet ' + str(offset))
#
#     def SetSRC2(self, Source2):
#         self.instr.write('MEASUrement:IMMed:SOURCE2 ' + Source2)  #sets to edge in delay measurement
#
#     def SetSRC1(self, Source1):
#         self.instr.write('MEASUrement:IMMed:SOURCE[1] ' + Source1)  #
#
#     #def SetSrc1(self, Source1):
#     #    self.instr.write('MEASUrement:IMMed:SOURCE[1] ' + Source1)  #sets from edge in delay measurement
#     #def Set1Src1(self):
#     #    return str(self.instr.ask('MEASUrement:IMMed:SOURCE[1]?'))
#
#     def SetChanDelay(self,Chan,Delay):
#         self.instr.write(Chan+':DESKew '+Delay)  #sets from edge in delay measurement
#
#     def GetChanDelay(self,Chan):
#         return float(self.instr.ask(Chan+':DESKew?'))  #sets from edge in delay measurement
#
#     def SetDelay(self):
#         self.instr.write('MEASUrement:IMMed:TYPe DELay')  #sets from edge in delay measurement
#
#     def SetFreq(self):
#         self.instr.write('MEASUrement:IMMed:TYPe FREQuency')  #sets from edge in delay measurement
#
#     def SetPeriod(self):
#         self.instr.write('MEASUrement:IMMed:TYPe PERIOD')  #sets from edge in delay measurement
#
#     def SetDuty(self):
#         self.instr.write('MEASUrement:IMMed:TYPe PDUty')  #sets from edge in delay measurement
#
#     def Edge1(self):
#         self.instr.write('MEASUrement:IMMed:DELay:EDGE1 RISE')  #sets from edge in delay measurement
#
#     def DelayMeasureEdge1(self,edge):
#         self.instr.write('MEASUrement:IMMed:DELay:EDGE1 '+edge)
#
#     def Edge2(self):
#         self.instr.write('MEASUrement:IMMed:DELay:EDGE2 RISE')  #sets from edge in delay measurement
#
#     def DelayMeasureEdge2(self,edge):
#         self.instr.write('MEASUrement:IMMed:DELay:EDGE2 '+edge)
#
#     def DirectBackards(self):
#         self.instr.write(':MEASUREMENT:IMMED:DELAY:DIRECTION BACKWARDS')  #sets from edge in delay measurement
#
#     def DirectForward(self):
#         self.instr.write(':MEASUREMENT:IMMED:DELAY:DIRECTION FORWARDs')  #sets from edge in delay measurement
#
#     def GetValue(self):
#         return float(self.instr.ask('MEASUrement:IMMed:VALue?'))  #gets efined value
#
#     def DefineTrig(self, Source1):
#         self.instr.write('DATA:SOURCE ' + Source1)  #sets from edge in delay measurement
#
#     def DefineTrig1(self, Source1):
#         self.instr.write('TRIGger:A:EDGE:SOUrce ' + Source1)
#
#     def SetHigh(self):
#         self.instr.write('MEASUrement:IMMed:TYPe HIGH')  #sets from edge in delay measurement
#
#     def SetMax(self):
#         self.instr.write('MEASUrement:IMMed:TYPe MAX')  #sets from edge in delay measurement
#
#     def SetMin(self):
#         self.instr.write('MEASUrement:IMMed:TYPe MINI')  #sets from edge in delay measurement
#
#
#     def SetMeaSRC2(self, number, Source2):
#         self.instr.write('MEASUrement:MEAS'+str(number)+':SOURCE[2] ' + Source2)  #
#
#     def SetMeasSRC1(self, number, Source1):
#         self.instr.write('MEASUrement:MEAS'+str(number)+':SOURCE[1] ' + Source1)  #
#
#     def SetMeasureMax(self,number):
#         self.instr.write('MEASUrement:MEAS'+str(number)+':TYPe MAX')  #sets from edge in delay measurement
#
#     def SetMeasureMin(self,number):
#         self.instr.write('MEASUrement:MEAS'+str(number)+':TYPe MINI')
#
#     def MeasureMax(self,number):
#         return float(self.instr.ask('MEASUrement:MEAS'+str(number)+':MAX?'))  #sets from edge in delay measurement
#
#     def MeasureMin(self,number):
#         return float(self.instr.ask('MEASUrement:MEAS'+str(number)+':MINI?'))
#
#     def MeasureMean(self,number):
#         return float(self.instr.ask('MEASUrement:MEAS'+str(number)+':MEAN?'))
#
#     def SetLow(self):
#         self.instr.write('MEASUrement:IMMed:TYPe LOW')  #sets from edge in delay measurement
#
#     def SetAmplitude(self):
#         self.instr.write('MEASUrement:IMMed:TYPe AMP')  #sets from edge in delay measurement
#
#     def SetHist(self, Source2):
#         self.instr.write('HIStogram:SOUrce ' + Source2)  #sets from edge in delay measurement
#
#     def SetHistStateON(self):
#         self.instr.write('HIStogram:STATE ON')  #sets from edge in delay measurement
#
#     def SetHistBox(self, leftp, topp, rightp, bottomp):
#         self.instr.write('HIStogram:Box ' + str(leftp) + "," + str(topp) + "," + str(rightp) + "," + str(bottomp))  #sets from edge in delay measurement
#
#     def HeaderOFF(self):
#         self.instr.write('HEADer OFF')
#
#     def runTDSHT3(self):
#         self.instr.write('VARIABLE:VALUE "sequencerState","Sequencing"')
#
#     def saveWaveform(self,fname):
#         #self.instr.write('SAVE:WAVEFORM:FILEFORMAT SPREADSHEETCsv')
#         self.instr.write('SAve:WAVEform CH1 ' + ',' + '"' + str(fname) + '"')
#         print "this is", str(fname)
#         #self.instr.write('SAve:WAVEform Math1 ' + ',' + '"rene3.cvs"') #this code works
#
#         #self.instr.write('SAve:WAVEform Math1, "rene.cvs"') This code works
#
#     def Set_Chan1_Chan3_Math1(self, vterm, zoom='ON'):
#         #self.instr.write('SEL:CH1 ON')  #Autosets scope measurements
#         #self.instr.write('SEL:CH3 ON')  #Autosets scope measurements
#         self.instr.write('MATH1:DEFINE "CH1-CH3"')   #sets up Math1
#         self.instr.write('SEL:CH1 OFF')  #Autosets scope measurements
#         self.instr.write('SEL:CH3 OFF')  #Autosets scope measurements
#         self.instr.write('SEL:MATH1 ON')
#         self.instr.write('CH1:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH2:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH3:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH4:VTERm:BIAS ' + str(vterm))
#         self.instr.write('CH1:OFFSet ' + str(vterm))
#         self.instr.write('CH2:OFFSet ' + str(vterm))
#         self.instr.write('CH3:OFFSet ' + str(vterm))
#         self.instr.write('CH4:OFFSet ' + str(vterm))
#         self.instr.write('ZOOm:MODe ' + str(zoom))
#         self.instr.write('ZOOm:ZOOM1:CH1:HORizontal:SCAle 10000')
#         self.instr.write('ZOOm:ZOOM1:CH1:VERtical:SCAle 2')
#         self.instr.write('ZOOm:ZOOM1:CH3:VERtical:SCAle 2')
#         self.instr.write('ZOOm:ZOOM1:Math1:DISplay OFF')
#         self.instr.write('CH1:POSition 0')
#         self.instr.write('CH3:POSition 0')
#         self.instr.write('TRIGger:A:EDGE:SOUrce CH1')  #sets trigger source
#         #self.instr.write('TRIGger:A:LEVel:CH1 ' + str((vterm+1)/2))
#         #wx.MilliSleep(5000) #
#         self.instr.write('TRIGger:A SETLevel')  #sets trigger location
#
#     def Get_Chan1_Chan3_Math1_Measurement(self, measure):
#         self.instr.write('MEASU:IMM:TYPE ' + str(measure))
#         return self.instr.ask('MEASU:IMM:VALUE?')
#
#     def Clear(self):
#         self.instr.write('CLEAR ALL')
#
# '''
#     def DpoJet_Recall_Mask(self,fpath,fname):
#         self.instr.write('DPOJET:ADDM MASKHits')         # measurement 6 _ Plot 1
#         self.instr.write('DPOJET:MEAS1:MASKF ' + '"' + fpath + fname  + '"')
#
#
#     def getSummary(self):
#         self.instr.write('VARIABLE:VALUE "reportSummary","Save"')
#
#     def getReport(self):
#         self.instr.write('VARIABLE:VALUE "reportDetails","Save"')
#  '''
#     ('MEASU:IMM:TYPE ' + str(measure))
#         return self.instr.ask('MEASU:IMM:VALUE?')
#
#     def Clear(self):
#         self.instr.write('CLEAR ALL')
#
#
# '''
#     def DpoJet_Recall_Mask(self,fpath,fname):
#         self.instr.write('DPOJET:ADDM MASKHits')         # measurement 6 _ Plot 1
#         self.instr.write('DPOJET:MEAS1:MASKF ' + '"' + fpath + fname  + '"')
#
#
#     def getSummary(self):
#         self.instr.write('VARIABLE:VALUE "reportSummary","Save"')
#
#     def getReport(self):
#         self.instr.write('VARIABLE:VALUE "reportDetails","Save"')
#  '''


#     #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#     #DO NOT USE THIS FUNCTION BELOW
#     # this function takes in the number of measurements, the channels you want the measurements on, and the type of measurements then prints the value
#     def SetAllMeasureVAL_Type_Source_Chan(self, number ,Chan=[],type=[]): #number (number of measurements) - Chan (takes list of channels need to set) - type ( takes a list of measurement types the the instrument understands  # DO NOT USE THIS
#         global numforlater  # used in displayMeas function
#         global chans  # made as global for use in other function
#         global types  # made as global for use in other function
#         global bye
#         bye=1
#         numforlater = number  # set this global variable equal to the value of number from user input
#         types = type  # set this global variable equal to type list from user input
#         chans = Chan  # set this global variable equal to Chan list from user input
#         if len(Chan) > 8 or len(type) > 8 or number > 8 or len(Chan) < 1 or len(type) < 1 or number < 1:
#             print "ERROR: The amount of measurements requested is not an option. Must be in range (1-8). Check arguments and try again. "
#             return
#         elif len(Chan) != number or len(type) != number:
#             print "ERROR: The amount of channels or types not equal to number of measurements requested. Check arguments and try again. "
#             return
#         for k in Chan:
#             while k>4 or k <1:
#                 if k>4:
#                     print "ERROR:",str(k)+" is not an option for a channel. (1-4)"
#                     bye=bye-1
#                     break
#                 elif k<1:
#                     print "ERROR:" , str(k) + " is not an option for a channel. (1-4)"
#                     bye = bye-1
#                     break
#         if bye<=0:
#             return''
#         self.instr.write('AUTOSET EXEC') #Autosets the scope
#         #self.instr.write('CLEAR ALL')  # Clears the scope
#         for i in range(1,number+1): # variable 'i' will increment within range 1 to the value of number +1
#             num= type[i-1] # sets variable num to each item in the type list starting at type[0]
#             self.instr.write('*WAI') #make sure the scope is ready for another command
#             self.instr.write('MEASU:MEAS'+str(i)+':TYP '+ num)    #sets up the meas number and type
#             self.instr.write('*WAI')
#         j=0 #
#         for i in Chan:
#             j= j+1
#             self.instr.write('*WAI')
#             self.instr.write('MEASU:MEAS'+str(j)+':SOURCE CH' +str(i))
#             self.instr.write('MEASUREMENT:MEAS' + str(j) + ':STATE ON') #enables calculation and display of the specified measurement found on pg 596 in manual  "MEASUrement:MEAS<x>:STATE"
#             self.instr.write('*WAI')
#         j=0

        # if len(chans) != numforlater or len(types) != numforlater:
        #     return ''
        # elif len(chans) > 8 or len(types) > 8 or numforlater  > 8 or len(chans) < 1 or len(types) < 1 or numforlater < 1:
        #     return ''
        # elif bye<=0:
        #     return ''
        # otherDiction={}
        # theMeasurements = {}
        # if tim>0:
        #     print "Please wait. Selected delay:",str(tim)+"s"
        # time.sleep(tim)
        # theVALUE_MEAN_MIN_MAX_STD_CNT = ['VALUE', 'MEAN', 'MINIMUM', 'MAXIMUM', 'STDdev', 'COUNT']
        # for i in range(1, numforlater+ 1):
        #     measNames = {}
        #     for j in range(0, len(theVALUE_MEAN_MIN_MAX_STD_CNT)):
        #         measNames[theVALUE_MEAN_MIN_MAX_STD_CNT[j] + str(i)] = float(self.instr.ask( 'MEASU:MEAS' + str(i) + ':' + theVALUE_MEAN_MIN_MAX_STD_CNT[j] + '?')) # ,'MEAN':float(self.instr.ask('MEASU:MEAS' +str(i) + ':MEAN?')),'MINIMUM':float(self.instr.ask('MEASU:MEAS' +str(i) + ':VAL?')),'MAX':float(self.instr.ask('MEASU:MEAS' +str(i) + ':VAL?'))}
        #         self.instr.write('*WAI')
        #         otherDiction[theVALUE_MEAN_MIN_MAX_STD_CNT[j] + str(i)]= float(self.instr.ask( 'MEASU:MEAS' + str(i) + ':' + theVALUE_MEAN_MIN_MAX_STD_CNT[j] + '?'))
        #         self.instr.write('*WAI')
        #         num = types[i - 1]
        #         theMeasurements['Measurement ' + str(i) + ' ' + num.capitalize()] = dict(measNames.items())  # stores the measurements in a dictionary called theMeasurements
        # print otherDiction
        # for i in range(1, numforlater + 1):
        #     print ".........................."
        #     num = types[i - 1]
        #     print 'Measurement ' + str(i) + ' ' + num.capitalize()
        #     print "--------------------------"
        #     for j in range(0, len(theVALUE_MEAN_MIN_MAX_STD_CNT)):
        #         print theVALUE_MEAN_MIN_MAX_STD_CNT[j], str(i), '=', otherDiction[theVALUE_MEAN_MIN_MAX_STD_CNT[j] + str(i)]
        # return sorted(theMeasurements.items()) #returns the dictionary
