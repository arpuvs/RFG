'''

Lab Automation tailored to helping David Brandon in Building 1

Description:
IMD3 for Leopard only!

Chas Frick

March 2017

Requires:
Rohde SMA100 Sig Gen (at GPIB Address XXX) 
E3631A Power supply (at GPIB Address XX)
Rohde FSP Spectrum Analyzer (at GPIB Address XX)
34401A DMM configured as Ammeter (at GPIB Address XXX)
34401A DMM configured as voltmeter (at GPIB Address XXX)
SDP box with ID #105 connected to USB

Outputs:


'''



'''

TO DO:
- Split equipment into different categories instead of a long string  --> Maybe improve with parsing of gpib thing

'''

MHz = 1e6

from CommonResources import PowerSupplySetting, GrabDataForFrequency, LevelSigGenToDesiredLevel

from CommonResources import MID_SIG_GEN_GPIB_ADDRESS, TOP_SIG_GEN_GPIB_ADDRESS, LEFT_POWER_SUPPLY_E3631A_ADDRESS, VOLTMETER_34401A_ADDRESS, AMMETER_34401A_ADDRESS, SPEC_AN_FSP_ADDRESS, SPEC_AN_FSU_ADDRESS

# ------- Parameters ------- EDIT BELOW HERE! ----------

# ------ Sig Gen Settings ------------------------------
SIG_GEN_1_ADDR_FOR_TEST = TOP_SIG_GEN_GPIB_ADDRESS
SIG_GEN_2_ADDR_FOR_TEST = MID_SIG_GEN_GPIB_ADDRESS
SIG_GEN_POWER = -35 # Starting value in dBm

# ------ Settings for frequency sweep
# SPEC_AN_FSUP_ADDRESS = SPEC_AN_FSU_ADDRESS # Uncomment this for using the FSU spec an (SPAN: 20 Hz to 8GHz)
SPEC_AN_FSUP_ADDRESS = SPEC_AN_FSP_ADDRESS # Uncomment this for using the FSP spec an (SPAN: 9 kHz to 13.6GHz)

STARTING_FREQ_MHZ = 100 # MHz
STEP_SIZE_MHZ = 100 # MHz
STOP_FREQ_DIV_100_IN_MHZ = 37 # Stop freq is 37 * 100 MHz = 3.7GHz
#CENTER_FREQUENCIES_LIST = [x*STEP_SIZE_MHZ*MHz + STARTING_FREQ_MHZ*MHz for x in range(STOP_FREQ_DIV_100_IN_MHZ)] # Comment this line and uncomment the next for the normal sweep
# It takes ~ 40 minutes to run data for the whole span 100 to 3.7G for 1 power
#CENTER_FREQUENCIES_LIST = [100*MHz, 200*MHz]
CENTER_FREQUENCIES_LIST = [100*MHz, 200*MHz, 500*MHz, 1000*MHz, 2000*MHz, 3000*MHz, 3500*MHz, 4000*MHz] # All these are in Hz!
# ------------------------------------

SIG_GEN_MAX_LEVEL = 20 # dBm --> Maximum power the signal generator can go to before it gives up trying to level the spec an power 
SIG_GEN2_IMD3_OFFSET = 2*MHz # Offset for other generator (e.g. 100MHz SigGen1 --> 2 MHz offset --> 98MHz SigGen2)
#DUT_POWER_LEVELS_AT_SPEC_AN = [-13, -15.5, -19] # dBm (Power output at spec An)  1V / 0.75Vpp / 0.5V for the 10-3700M 18dB Iso combiner
DUT_POWER_LEVELS_AT_SPEC_AN = [-13] # dBm (Power output at spec An)  1V for the 10-3700M 18dB Iso combiner
# ------------------------------------------------------

# Have to load cal data

# ------ Power supply settings -------------------------
POWER_SUPPLY_ADDR_FOR_TEST = LEFT_POWER_SUPPLY_E3631A_ADDRESS

POWER_SUPPLY_SETTINGS_TUPLE_LIST = [PowerSupplySetting(voltageOutputPort='P6V', voltage=5.05, currentLimit=0.4)]
# ------------------------------------------------------


# ------ Voltmeter and Ammeter settings ----------------

# ------------------------------------------------------

# ------- SPEC AN SETTINGS -----------------------------
SPEC_AN_SPAN = 200 # Hz
SPEC_AN_RES_BW = 10 # Hz
SPEC_AN_VID_BW_HZ = 19 # Hz cannot set lower for FSP (but can for FSU spec an)
SPEC_AN_ATTENUATION = 30 # dB to see spurs on noise floor
SPEC_AN_REFERENCE_LEVEL = 0 # dBm
SPEC_AN_RANGE = 130 # dB
# ------------------------------------------------------

PRODUCT_NUMBER = 0

EVALUATION_BOARD_REVISION = 'Test'
EVALUATION_BOARD_SERIAL_NUMBER = '1'

TEST_NAME = 'IMD3'
   

DIFFERNTIAL_MEASUREMENT = True # Change to True for differential measurement or False for single ended measurement


# Settings for the SDP/Amp
''' Each setting is (DSA, Range, FA, Test Amp Gain Str) FA is not used unless HW pin is enabled though
    Range   DSA     FA      Test Amp Gain
    3       0       3       40dB
    3       5       3       35dB
    3       10      3       30dB
    3       15      3       25dB
    3       20      3       20dB
    2       0       3       20dB
    2       5       3       15dB
    2       10      3       10dB
    2       15      3       5dB
    2       20      3       0dB
    1       0       3       10dB
    1       5       3       5dB
    1       10      3       0dB
    1       15       3      -5dB
    1       20       3      -10dB
'''

from AmpRegSettingClass import AmpRegSettingTuple
AMP_REG_SETTINGS_TUPLE_LIST = [AmpRegSettingTuple(0, 3, 3, "40r3"),
                        AmpRegSettingTuple(5, 3, 3, "35r3"),
                        AmpRegSettingTuple(10, 3, 3, "30r3"),
                        AmpRegSettingTuple(15, 3, 3, "25r3"),
                        AmpRegSettingTuple(20, 3, 3, "20r3"),
                        AmpRegSettingTuple(0, 2, 3, "15r2"),
                        AmpRegSettingTuple(5, 2, 3, "10r2"),
                        AmpRegSettingTuple(10, 2, 3, "5r2"),
                        AmpRegSettingTuple(0, 1, 3, "0r2"),
                        AmpRegSettingTuple(5, 1, 3, "5r1"),
                        AmpRegSettingTuple(10, 1, 3, "0r1")]
#                        AmpRegSettingTuple(15, 1, 3, "n5r1"),
#                        AmpRegSettingTuple(20, 1, 3, "n10r1")]



#-------------------------- DO NOT EDIT BELOW HERE! -----

def PerformIMD3Test(SIG_GEN_1_ADDR_FOR_TEST, SIG_GEN_2_ADDR_FOR_TEST, PRODUCT_NUMBER, EVALUATION_BOARD_REVISION, EVALUATION_BOARD_SERIAL_NUMBER, DIFFERNTIAL_MEASUREMENT, 
                    POWER_SUPPLY_ADDR_FOR_TEST, AMP_REG_SETTINGS_TUPLE_LIST, POWER_SUPPLY_SETTINGS_TUPLE_LIST, SPEC_AN_FSUP_ADDRESS, VOLTMETER_34401A_ADDRESS, AMMETER_34401A_ADDRESS, 
                    TEST_NAME='IMD3', SIG_GEN_POWER=-30, CENTER_FREQUENCIES_LIST=[100*MHz, 200*MHz, 500*MHz, 1000*MHz, 2000*MHz, 3000*MHz, 3700*MHz], 
                    SIG_GEN_MAX_LEVEL=-5, SIG_GEN2_IMD3_OFFSET=2*MHz, DUT_POWER_LEVELS_AT_SPEC_AN=[-13], SPEC_AN_VID_BW_HZ = 30, 
                    SPEC_AN_SPAN = 200, SPEC_AN_RES_BW = 10, SPEC_AN_ATTENUATION = 30, SPEC_AN_REFERENCE_LEVEL = 0, SPEC_AN_RANGE = 120):
                    
    #import sys
    #sys.path.append("T:\USB") # Brings in the drivers from the network drive

    import CSV
    import time
    import math
    import collections
    import ADI_GPIB

    sigGen1ForTest = ADI_GPIB.SMA(SIG_GEN_1_ADDR_FOR_TEST)
    sigGen2ForTest = ADI_GPIB.SMA(SIG_GEN_2_ADDR_FOR_TEST)
    #print sigGenForTest
    
    voltmeter = ADI_GPIB.HP34401A(VOLTMETER_34401A_ADDRESS)
    #print voltmeter
    
    if(AMMETER_34401A_ADDRESS is not None):
        ammeter = ADI_GPIB.HP34401A(AMMETER_34401A_ADDRESS)
        #print ammeter
    
    specAnFSUPSeries = ADI_GPIB.FSUP(SPEC_AN_FSUP_ADDRESS)
    #print specAnFSUPSeries
    
    powerSupplyForTest = ADI_GPIB.E3631A(POWER_SUPPLY_ADDR_FOR_TEST)
    #print powerSupplyForTest

    if(AMMETER_34401A_ADDRESS is not None):
        ammeter.Write('SENS:FUNC "CURRENT:DC"') # Set the ammeter to actually measure current
        ammeter.Write('SENS:CURR:DC:RANG 3E-1') # Set the range to be in 0.3A
        EquipmentUsedList = [sigGen1ForTest, sigGen2ForTest, voltmeter, ammeter, specAnFSUPSeries, powerSupplyForTest]
    else:
        EquipmentUsedList = [sigGen1ForTest, sigGen2ForTest, voltmeter, specAnFSUPSeries, powerSupplyForTest]

    equipNameList = []
    for equip in EquipmentUsedList:
        equipNameList.append(equip.instr.ask("*IDN?"))

    inputBalun = "Balun"
    outputBalun = "Balun"
    
    if(DIFFERNTIAL_MEASUREMENT):
        EquipmentUsedList.append(outputBalun)
        equipNameList.append(outputBalun)
     

    fileNamesDict = {}
    for DUTPowerAtSpecAn in DUT_POWER_LEVELS_AT_SPEC_AN:
        currentTime = time.localtime() # returns timestruct
        timeStr = '__Date_%d_%d_%d__Time_%d_%d_%d' % (currentTime.tm_mon, currentTime.tm_mday, currentTime.tm_year, currentTime.tm_hour, currentTime.tm_min, currentTime.tm_sec)
        fileNameStart = 'TestName_%s__ProductNum_%s__BoardRev_%s__BoardSN_%s' % (TEST_NAME, str(PRODUCT_NUMBER), str(EVALUATION_BOARD_REVISION), str(EVALUATION_BOARD_SERIAL_NUMBER))
        fileExtension = '.csv'
        fileDir = '.\\Data\\'
        powerAtSpecAnStr = "_PowerAtSpecAn_M%f" % abs(DUTPowerAtSpecAn)
        powerAtSpecAnStr = powerAtSpecAnStr.replace(".", "P") # Replace the floatingPoint period
        fullFileName = fileDir + fileNameStart + timeStr + powerAtSpecAnStr +fileExtension
        #print fullFileName
        fileNamesDict["%f" % DUTPowerAtSpecAn] = fullFileName
        

    # Turn off sig gens and power supply
    sigGen1ForTest.Enabled = 0
    sigGen2ForTest.Enabled = 0
    powerSupplyForTest.Enabled = 0
    
    # Set spec an settings
    specAnFSUPSeries.AttLevel = SPEC_AN_ATTENUATION
    specAnFSUPSeries.ReferenceLevel = SPEC_AN_REFERENCE_LEVEL
    specAnFSUPSeries.instr.write("DISP:WIND:TRAC:Y:SPAC LOG") # Set vertical spacing to manual log scale
    specAnFSUPSeries.instr.write("DISP:WIND:TRAC:Y %fdB" % SPEC_AN_RANGE) # Set vertical to SPEC_AN_RANGE dB from the reference level
    specAnFSUPSeries.ResBand = 20*1e3 # 20 kHz
    specAnFSUPSeries.instr.write("BAND:VID %f Hz" % (SPEC_AN_VID_BW_HZ)) #Set video bw
    specAnFSUPSeries.Span = 20 * MHz # 20 MHz

    # ------------------------------------------
    # Actual test starts now

    for powerSupplySetting in POWER_SUPPLY_SETTINGS_TUPLE_LIST:
        print "Setting power supply to %s and %f A\n" % (powerSupplySetting.voltage, powerSupplySetting.currentLimit)
        # Set power supply levels

        powerSupplyForTest.Enabled = 0
        sigGen1ForTest.Enabled = 0
        sigGen2ForTest.Enabled = 0

        setattr(powerSupplyForTest,powerSupplySetting.voltageOutputPort, powerSupplySetting.voltage)
        setattr(powerSupplyForTest,powerSupplySetting.currentOutputPort, powerSupplySetting.currentLimit)

        # Confirm settings
        #raw_input("Press enter to turn the power supply on...")
        print ("Turning on the power supply")
        powerSupplyForTest.Enabled = 1

        from CallSDP_Configure_FA_Range_DSA import Configure_FA_Range_DSA
        # Configure SDP with FS, Range and DSA
        for AmpRegSetting in AMP_REG_SETTINGS_TUPLE_LIST:
            ConfiguredProperly = Configure_FA_Range_DSA(FA_Val = AmpRegSetting.FA, Range_Val = AmpRegSetting.Range, DSA_Val = AmpRegSetting.DSA)

            if(ConfiguredProperly):
                print "Good to start testing!"
            else:
                print "ERROR with SDP!"
                    
            for DUTPowerAtSpecAn in DUT_POWER_LEVELS_AT_SPEC_AN:
            
                print "*" * 40
                print "Setting Sig Gen powers to %f dBm\n" % DUTPowerAtSpecAn
                # Set sig gen power = DUT power
                sigGen1ForTest.Enabled = 0
                sigGen2ForTest.Enabled = 0

                sigGen1ForTest.Level = SIG_GEN_POWER # Start sig gens at desired starting point! in dBm 
                sigGen2ForTest.Level = SIG_GEN_POWER # Start sig gens at desired starting point! in dBm 
                
                csvf = CSV.Results_File(fileNamesDict ["%f" % DUTPowerAtSpecAn])
                
                for centerFreq in CENTER_FREQUENCIES_LIST:
                
                    print "*" * 40
                    print "Starting test with frequency: %f Hz\n" % centerFreq
                    
                    sigGen1ForTest.Frequency = centerFreq
                    sigGen2ForTest.Frequency = centerFreq - SIG_GEN2_IMD3_OFFSET
                        
                    time.sleep(0.5) # Wait 0.5 seconds

                    sigGen1ForTest.Enabled = 1
                    sigGen2ForTest.Enabled = 1

                    time.sleep(1.5) # Wait 1.5 seconds

                    # Level the sig gens out to the desired DUT output power
                    LevelSigGenToDesiredLevel(SigGen=sigGen1ForTest, SpecAnObj=specAnFSUPSeries, Frequency=centerFreq , DesiredSpecAnLevel_dBm = DUTPowerAtSpecAn, SIG_GEN_MAX_LEVEL = SIG_GEN_MAX_LEVEL, numAvgs=1, RF_driveStarting = SIG_GEN_POWER)
                    LevelSigGenToDesiredLevel(SigGen=sigGen2ForTest, SpecAnObj=specAnFSUPSeries, Frequency=centerFreq - SIG_GEN2_IMD3_OFFSET, DesiredSpecAnLevel_dBm = DUTPowerAtSpecAn, SIG_GEN_MAX_LEVEL = SIG_GEN_MAX_LEVEL, numAvgs=1, RF_driveStarting = SIG_GEN_POWER)
                    
                    time.sleep(1.0)

                    # Zoom into and capture data for first spur frequency
                    print "Capturing data for left lowest spur..."
                    (leftLowSpurFreq, leftLowSpurPow) = GrabDataForFrequency(specAnObj=specAnFSUPSeries, startingFreq=centerFreq - 2*SIG_GEN2_IMD3_OFFSET, startingSpan=SPEC_AN_SPAN, startingResBW=SPEC_AN_RES_BW, startingVideoBW=SPEC_AN_VID_BW_HZ)
                    
                    # Zoom into and capture data for left high frequency
                    print "Capturing data for left high freq..."
                    (leftHighFreq, leftHighPow) = GrabDataForFrequency(specAnObj=specAnFSUPSeries, startingFreq=centerFreq - SIG_GEN2_IMD3_OFFSET, startingSpan=SPEC_AN_SPAN, startingResBW=SPEC_AN_RES_BW, startingVideoBW=SPEC_AN_VID_BW_HZ)
                    
                    # Zoom into and capture data for right high frequency
                    print "Capturing data for right high freq..."
                    (rightHighFreq, rightHighPow) = GrabDataForFrequency(specAnObj=specAnFSUPSeries, startingFreq=centerFreq, startingSpan=SPEC_AN_SPAN, startingResBW=SPEC_AN_RES_BW, startingVideoBW=SPEC_AN_VID_BW_HZ)
                    
                    # Zoom into and capture data for first spur frequency
                    print "Capturing data for right lowest spur..."
                    (rightLowSpurFreq, rightLowSpurPow) = GrabDataForFrequency(specAnObj=specAnFSUPSeries, startingFreq=centerFreq + SIG_GEN2_IMD3_OFFSET, startingSpan=SPEC_AN_SPAN, startingResBW=SPEC_AN_RES_BW, startingVideoBW=SPEC_AN_VID_BW_HZ)
                    time.sleep(1.0) # Wait 1 second
                    
                    # Measure current
                    measPowSupplyVoltage = getattr(powerSupplyForTest,powerSupplySetting.voltageOutputPort)
                    measPowSupplyCurrent = getattr(powerSupplyForTest,powerSupplySetting.currentOutputPort)
                    measPowSupplyVoltage = float(measPowSupplyVoltage)
                    measPowSupplyCurrent = float(measPowSupplyCurrent)                    
                    measVoltDMM = voltmeter.Voltage
                    measVoltDMM = float(measVoltDMM)             
                    if(AMMETER_34401A_ADDRESS is not None):
                        measCurrDMM = ammeter.Current
                        measCurrDMM = float(measCurrDMM) 
                    else:
                        measCurrDMM = 0
                    print "Measured voltage (E3631A): %f V\tWith DMM: %f V" % (measPowSupplyVoltage, measVoltDMM)
                    print "Measured current (E3631A): %f A\tWith DMM: %f A" % (measPowSupplyCurrent, measCurrDMM)


                    # Record data 
                    results_dict = collections.OrderedDict() # Remembers the order the keys are added and will output in this order!
                    
                    curTime = time.localtime()
                    results_dict["Time"] = '%d:%d:%d' % (curTime.tm_hour % 12, curTime.tm_min, curTime.tm_sec)

                    results_dict["SN#"] = EVALUATION_BOARD_SERIAL_NUMBER
                    
                    results_dict["Differential"] = DIFFERNTIAL_MEASUREMENT
			
                    #results_dict["Notes"] = EquipListStr
                    for equipNum in range(len(EquipmentUsedList)):
                    
                        equipStr = str(EquipmentUsedList[equipNum]) # Looks like <ADI_GPIB.ObjType.ObjType at 0xXXXX>
                        
                        if("balun" not in equipStr and "Balun" not in equipStr):
                            equipStr = equipStr.split(".")
                            equipStr = equipStr[1] # Grab the Obj type

                    results_dict["Notes %s" % equipStr] = equipNameList[equipNum].replace(",",";")
                    results_dict["DSA Setting [Decimal]"] = AmpRegSetting.DSA
                    results_dict["Range Setting [Decimal]"] = AmpRegSetting.Range
                    results_dict["FA Setting [Decimal]"] = AmpRegSetting.FA
                    results_dict["Approx Amp Gain [dB]"] = AmpRegSetting.TestGainStr                    
                    results_dict["2f1-f2 [Hz]"] = leftLowSpurFreq
                    results_dict["2f1-f2 IM [dBm]"] = leftLowSpurPow
                    results_dict["f1 IMD3 [dBc]"] = leftLowSpurPow - leftHighPow
                    results_dict["f1 [Hz]"] = leftHighFreq
                    results_dict["p1 [dBm]"] = leftHighPow
                    results_dict["f2 [Hz]"] = rightHighFreq
                    results_dict["p2 [dBm]"] = rightHighPow
                    results_dict["2f2-f1 [Hz]"] = rightLowSpurFreq
                    results_dict["2f2-f1 IM [dBm]"] = rightLowSpurPow
                    results_dict["f2 IMD3 [dBc]"] = rightLowSpurPow - rightHighPow
                    results_dict["Sig Gen 1 Pow Lvl [dBm]"] = sigGen1ForTest.Level
                    results_dict["Sig Gen 2 Pow Lvl [dBm]"] = sigGen2ForTest.Level
                    results_dict["Power Level specified at SpecAn [dBm]"] = DUTPowerAtSpecAn
                    results_dict["Set Power Supply Voltage [V]"] = powerSupplySetting.voltage
                    results_dict["Meas. Power Supply Voltage [V]"] = measPowSupplyVoltage 
                    results_dict["Set Power Supply Current [A]"] = powerSupplySetting.currentLimit
                    results_dict["Meas. Power Supply Current [A]"] = measPowSupplyCurrent
                    results_dict["Measured DUT voltage [V]"] = measVoltDMM
                    results_dict["Measured DUT current [A]"] = measCurrDMM
                    
                    
                    
                    # Save results dictionary to file
                    # results_dict = collections.OrderedDict(sorted(results_dict.items()))
                    
                    #print results_dict
                    csvf.ManualCreateHeader(results_dict) 
                    csvf.WriteDictionary(results_dict)
                    print "-" * 40
                print "-" * 40

    curTime = time.localtime()
    curTimeSec = (curTime.tm_hour)*3600 + (curTime.tm_min) * 60 + (curTime.tm_sec)
    startTimeSec = (currentTime.tm_hour)*3600 + (currentTime.tm_min) * 60 + (currentTime.tm_sec)
    numSecondsForTest = curTimeSec - startTimeSec

    sigGen1ForTest.Enabled = 0
    sigGen2ForTest.Enabled = 0
    powerSupplyForTest.Enabled = 0
    
    print "-" * 40
    print "\nScript has completed after %f seconds!" % numSecondsForTest
    print "Check \"%s....csv\" files for data!" % (TEST_NAME)  


if __name__ == '__main__':

    PerformIMD3Test(SIG_GEN_1_ADDR_FOR_TEST=SIG_GEN_1_ADDR_FOR_TEST, AMP_REG_SETTINGS_TUPLE_LIST=AMP_REG_SETTINGS_TUPLE_LIST, SIG_GEN_2_ADDR_FOR_TEST=SIG_GEN_2_ADDR_FOR_TEST, PRODUCT_NUMBER=PRODUCT_NUMBER, EVALUATION_BOARD_REVISION=EVALUATION_BOARD_REVISION,
                        EVALUATION_BOARD_SERIAL_NUMBER=EVALUATION_BOARD_SERIAL_NUMBER, DIFFERNTIAL_MEASUREMENT=DIFFERNTIAL_MEASUREMENT, POWER_SUPPLY_ADDR_FOR_TEST=POWER_SUPPLY_ADDR_FOR_TEST,
                        POWER_SUPPLY_SETTINGS_TUPLE_LIST=POWER_SUPPLY_SETTINGS_TUPLE_LIST, SPEC_AN_FSUP_ADDRESS=SPEC_AN_FSUP_ADDRESS, VOLTMETER_34401A_ADDRESS=VOLTMETER_34401A_ADDRESS, AMMETER_34401A_ADDRESS = AMMETER_34401A_ADDRESS, 
                        TEST_NAME=TEST_NAME, SIG_GEN_POWER=SIG_GEN_POWER, CENTER_FREQUENCIES_LIST=CENTER_FREQUENCIES_LIST, SIG_GEN_MAX_LEVEL=SIG_GEN_MAX_LEVEL, 
                        SIG_GEN2_IMD3_OFFSET=SIG_GEN2_IMD3_OFFSET, DUT_POWER_LEVELS_AT_SPEC_AN=DUT_POWER_LEVELS_AT_SPEC_AN, SPEC_AN_VID_BW_HZ = SPEC_AN_VID_BW_HZ,
                        SPEC_AN_SPAN = SPEC_AN_SPAN, SPEC_AN_RES_BW = SPEC_AN_RES_BW, SPEC_AN_ATTENUATION = SPEC_AN_ATTENUATION, SPEC_AN_REFERENCE_LEVEL = SPEC_AN_REFERENCE_LEVEL, SPEC_AN_RANGE = SPEC_AN_RANGE)


