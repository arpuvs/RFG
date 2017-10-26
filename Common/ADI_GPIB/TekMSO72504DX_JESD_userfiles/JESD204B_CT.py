# REVISION HISTORY: Aug 24, 2015 Leah Magaldi made edits

#from GPIBObjectList import *

import visa                     # imports GPIB VISA functions
import wx
import time
from itertools import count
from timeit import  Timer       # imports timer functions
from datetime import datetime   # basic date functions
import time
import csv
import os
import re
from ChkStatus  import wrtmsg,rdmsg,chkbusy,chkerr,chkDpoJetMeasureIfIdle
from GPIBObjectList import TekMSO72504DX

rm = visa.ResourceManager()
scope1=rm.get_instrument('GPIB0::15')

#scope1 = visa.instrument("GPIB0::15::INSTR")
#scope1 = TekMSO72504DX(15)

scope = TekMSO72504DX(15)
#scope.ClearGPIB()
scope1.clear()        # clear the PI interface
scope1.timeout = 10   # Set timeout to 10 seconds

#chkbusy(scope1)

def CT(channel,vterm,frequency,report_filename,BER_target,pattern_length,mask, displayplots):
    from DPOJet_functions import SaveReportToFile
    from DPOJet_functions import JESD204BMask11G
    from DPOJet_functions import JESD204BMask6G
    from DPOJet_functions import JESD204BMask11GRx
    from DPOJet_functions import JESD204BMask6GRx    

    ## Set up scope
    #scope.Scope_Factory() # "Default Setup" button ## Don't do this step. It closes DPOJet.
    #scope.Scope_AutoSet() # "Autoset" button
    #wx.MilliSleep(5000) # Scope autoset takes about 4 seconds
    scope.DpoJet_TurnOffChannels()
    scope.SetVscaleAll(.1)
    if (channel==00): scope.DpoJet_Set_LaneA(vterm)
    if (channel==00): scope.SetTriggerEdgeSource('CH1')
    if (channel==01): scope.DpoJet_Set_LaneB(vterm)
    if (channel==01): scope.SetTriggerEdgeSource('CH2')
    if (channel==10): scope.DpoJet_Set_DiffProbeCh1(vterm)
    if (channel==10): scope.SetTriggerEdgeSource('CH1')
    if (channel==11): scope.DpoJet_Set_DiffProbeCh3(vterm)
    if (channel==11): scope.SetTriggerEdgeSource('CH3')
    scope.SamplingModeRT()
    scope.TimeBase(20e-6) # sets horizontal time base
    scope.SampleRate(100E9) # sets the sample rate

    ##=====================================================
    ## Set up DPOJet
    ##=====================================================
    number_of_tests = 29
    #scope.DpoJet() # Starts DPOJet

    scope.DpoJet_Clear_All()
    
    ##=====================================================
    ## Mask setup
    ## there are 5 choices:
    ## '11GTx' '6GTx' '11GRx' '6GRx' 'NONE'
    ##=====================================================
    
    fpath ='C:\\TekApplications\\DPOJET\\Masks\\JESD204B\\Temp\\'
    fname = 'temp.msk'
    
    #offset for tests only needed if masks are not emabled
    offset = 0
    if mask=='11GTx':
        JESD204BMask11G(frequency) # Use this if you want 11G masks
        scope.DpoJet_Recall_Mask(fpath, fname) 
    elif mask=='6GTx':
        JESD204BMask6G(frequency) # Use this if you want 6G masks
        scope.DpoJet_Recall_Mask(fpath, fname) 
        print mask
    elif mask=='11GRx':
        JESD204BMask11GRx(frequency) # Use this if you want 11G Rx masks
        scope.DpoJet_Recall_Mask(fpath, fname) 
        print mask
    elif mask=='6GRx':
        JESD204BMask6GRx(frequency) # Use this if you want 6G Rx masks
        scope.DpoJet_Recall_Mask(fpath, fname) 
        print mask
    elif mask=='NONE':
        offset = 1
        print mask        

    scope.DpoJet_Load_Test("rise") # Select the Risetime test
    scope.DpoJet_Load_Test("fall") # Select the Falltime test    
    scope.DpoJet_Load_Test("com")  # 
    scope.DpoJet_Load_Test("highlow")  # 
    scope.DpoJet_Load_Test("high")  # 
    scope.DpoJet_Load_Test("low")  # 
    scope.DpoJet_Load_Test("freq") # Select the Frequency test
    scope.DpoJet_Load_Test("tie") # Select the TIE test
    scope.DpoJet_Load_Test("tj") # Select the Tj ber test
    scope.DpoJet_Load_Test("rj") # Select the Rj test
    scope.DpoJet_Load_Test("rjd") # Select the Rj-dd test
    scope.DpoJet_Load_Test("dj") # Select the Dj test
    scope.DpoJet_Load_Test("djd") # Select the Dj-dd test
    scope.DpoJet_Load_Test("pj") # Select the Pj test
    scope.DpoJet_Load_Test("dcd") # Select the DCD test
    scope.DpoJet_Load_Test("ddj")  # Select the DDj test 
    scope.DpoJet_Load_Test("width") # Select the Eye Opening Width test
    scope.DpoJet_Load_Test("height") # Select the Eye Opening Height test
    scope.DpoJet_Load_Test("widthb") # Select the Eye Opening Width @ BER test
    scope.DpoJet_Load_Test("heightb") # Select the Eye Opening Height @ BER test
    if (channel==0): scope.DpoJet_Intra_Pair1_3(5-offset) # Intra-pair skew Lane A
    if (channel==1): scope.DpoJet_Intra_Pair2_4(5-offset) # Intra-pair skew Lane B
    scope.DpoJet_RiseFall20_80(2) # Set Risefall thresholds to 20%/80% for testnum
    scope.DpoJet_RiseFall20_80(3) # Set Risefall thresholds to 20%/80% for testnum
    
    scope.DpoJet_Load_Test("pduty")#23 +dutycycle
    scope.DpoJet_Load_Test("nduty")#24-dutycycle
    scope.DpoJet_Load_Test("period")#25 period
    scope.DpoJet_Load_Test("undershoot")#26
    scope.DpoJet_Load_Test("overshoot")#27
    

    if displayplots =="All":
        ## Add plots (up to 4, there are 5 types (one already set as either eyemask unless user doesn't due that testing)
        if mask=='NONE':
            scope.DpoJet_AddEye(10-offset)
        scope.DpoJet_AddHistogram(9-offset) # Add the Bathtub plot to measurement #10 (TIE)
        scope.DpoJet_AddBathtub(10-offset) # Add the Bathtub plot to measurement #11 (TJ)
        scope.DpoJet_AddSpectrum(9-offset) # Add the Bathtub plot to measurement #10 (TIE)
        #scope.DpoJet_AddWaveform(22)
    elif displayplots =='Eye':
        if mask=='NONE':
            scope.DpoJet_AddEye(9-offset)
    
    
    ## Additional Test Configs
    scope.JESD204BCT_PLL_Setup(number_of_tests,frequency*1e9) # Select the recovery PLL
    scope.JESD204BCT_RJDJ_BER_Target(number_of_tests,BER_target) # Set the BER target to 1E-15 for all tests
    #scope.JESD204BCT_RJDJ_Pattern_Length(number_of_tests,pattern_length) # Set the BER target to 1E-15 for all tests
    scope.DpoJet_CM_Source(4,channel) # Set up the source for Common mode test
   
    ## don't know where below bug fix comes from
    ## Bug fix to properly display the Bathtub plot
##    scope.BathtubPlotBugFixSave()
##    wx.MilliSleep(10000)
##    chkbusy(scope1)
##    scope.BathtubPlotBugFixRecall()
##    wx.MilliSleep(10000)
##    chkbusy(scope1)
    
    
    ## Run the test
    scope.DpoJet_Single()
    chkDpoJetMeasureIfIdle(scope)   # if measure finished?
    SaveReportToFile(report_filename) # Save report to file
    
#     ## Get results from DPOJet
#     ####### Need to add commands to retrieve all the "mean" test results, then update the return list
    
    wx.MilliSleep(10000)
    if mask!='NONE':
        offset=0
        maskhits_seg1 = (scope.DpoJet_Indivdual_Measure(1,'seg1:hits')).rstrip()
        maskhits_seg2 = (scope.DpoJet_Indivdual_Measure(1,'seg2:hits')).rstrip()
        maskhits_seg3 = (scope.DpoJet_Indivdual_Measure(1,'seg3:hits')).rstrip()
        maskhits = (scope.DpoJet_Indivdual_Measure(1,'mean')).rstrip()

    else:
        offset=1
        maskhits_seg1 = 999
        maskhits_seg2 = 999
        maskhits_seg3 = 999
        maskhits = 999


    risetime = (scope.DpoJet_Indivdual_Measure(2-offset,'mean')).rstrip()
    falltime = (scope.DpoJet_Indivdual_Measure(3-offset,'mean')).rstrip()
    DC_CM= (scope.DpoJet_Indivdual_Measure(4-offset,'mean')).rstrip()
    Swing = (scope.DpoJet_Indivdual_Measure(5-offset,'mean')).rstrip()
    V_high = (scope.DpoJet_Indivdual_Measure(6-offset,'mean')).rstrip()
    V_low = (scope.DpoJet_Indivdual_Measure(7-offset,'mean')).rstrip()
    frequency = (scope.DpoJet_Indivdual_Measure(8-offset,'mean')).rstrip()
    #duty = (scope.DpoJet_Indivdual_Measure(9-offset,'mean')).rstrip()
    TIE = (scope.DpoJet_Indivdual_Measure(9-offset,'mean')).rstrip()
    TJBER = (scope.DpoJet_Indivdual_Measure(10-offset,'mean')).rstrip()
    Rj = (scope.DpoJet_Indivdual_Measure(11-offset,'mean')).rstrip()
    Rjdd = (scope.DpoJet_Indivdual_Measure(12-offset,'mean')).rstrip()
    Dj = (scope.DpoJet_Indivdual_Measure(13-offset,'mean')).rstrip()
    Djdd = (scope.DpoJet_Indivdual_Measure(14-offset,'mean')).rstrip()
    Pj = (scope.DpoJet_Indivdual_Measure(15-offset,'mean')).rstrip()
    DCD = (scope.DpoJet_Indivdual_Measure(16-offset,'mean')).rstrip()
    DDj = (scope.DpoJet_Indivdual_Measure(17-offset,'mean')).rstrip()
    width = (scope.DpoJet_Indivdual_Measure(18-offset,'mean')).rstrip()
    height = (scope.DpoJet_Indivdual_Measure(19-offset,'mean')).rstrip()
    widthBER = (scope.DpoJet_Indivdual_Measure(20-offset,'mean')).rstrip()
    heightBER = (scope.DpoJet_Indivdual_Measure(21-offset,'mean')).rstrip()
    IntraPairSkew = (scope.DpoJet_Indivdual_Measure(22-offset,'mean')).rstrip()
    PosDutyCycle = (scope.DpoJet_Indivdual_Measure(23-offset,'mean')).rstrip()
    NegDutyCycle = (scope.DpoJet_Indivdual_Measure(24-offset,'mean')).rstrip()
    period= (scope.DpoJet_Indivdual_Measure(25-offset,'mean')).rstrip()
    undershoot = (scope.DpoJet_Indivdual_Measure(26-offset,'mean')).rstrip()
    overshoot = (scope.DpoJet_Indivdual_Measure(27-offset,'mean')).rstrip()

    returnstring = maskhits,maskhits_seg1,maskhits_seg2,maskhits_seg3,risetime,falltime,DC_CM,Swing,V_high,V_low,frequency,TIE,TJBER,Rj,Rjdd,Dj,Djdd,Pj,DCD,DDj,width,height,widthBER,heightBER,IntraPairSkew, PosDutyCycle, NegDutyCycle, period, undershoot, overshoot
    print "maskhits,maskhits_seg1,maskhits_seg2,maskhits_seg3,risetime,falltime,DC_CM,Swing,V_high,V_low,frequency,duty,TIE,TJBER,Rj,Rjdd,Dj,Djdd,Pj,DCD,DDj,width,height,widthBER,heightBER,IntraPairSkew, PosDutyCycle, NegDutyCycle, period, undershoot, overshoot"

    print returnstring
    
    TekResultsdic={}
    TekResultsdic['maskhits']=maskhits
    TekResultsdic['maskhits_seg1']=float(maskhits_seg1)
    TekResultsdic['maskhits_seg2']=float(maskhits_seg2)
    TekResultsdic['maskhits_seg3']=float(maskhits_seg3)
    TekResultsdic['risetime']=float(risetime)
    TekResultsdic['falltime']=float(falltime)
    TekResultsdic['DC_CM']=float(DC_CM)
    TekResultsdic['Swing']=float(Swing)
    TekResultsdic['V_high']=float(V_high)
    TekResultsdic['V_low']=float(V_low)
    TekResultsdic['frequency']=float(frequency)
    TekResultsdic['TIE']=float(TIE)
    TekResultsdic['TJBER']=float(TJBER)
    TekResultsdic['Rj']=float(Rj)
    TekResultsdic['Rjdd']=float(Rjdd)
    TekResultsdic['Dj']=float(Dj)
    TekResultsdic['Djdd']=float(Djdd) 
    TekResultsdic['Pj']=float(Pj) 
    TekResultsdic['DCD']=float(DCD)
    TekResultsdic['DDj']=float(DDj)
    TekResultsdic['width']=float(width)
    TekResultsdic['height']=float(height)
    TekResultsdic['widthBER']=float(widthBER)
    TekResultsdic['heightBER']=float(heightBER)
    TekResultsdic['IntraPairSkew']=float(IntraPairSkew)
    TekResultsdic['PosDutyCycle']=float(PosDutyCycle)
    TekResultsdic['NegDutyCycle']=float(NegDutyCycle)  
    TekResultsdic['period']=float(period)
    TekResultsdic['undershoot']=float(undershoot)
    TekResultsdic['overshoot']=float(overshoot)

    print(TekResultsdic)
    return (TekResultsdic)