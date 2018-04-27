'''

Lab Automation tailored to helping David Brandon in Building 1

Description:


Chas Frick

February 2017
UPDATED: MArch 2017 -- SDP wrapper created for Leopard ONLY!

Requires:
Rohde SMA100 Sig Gen (at GPIB Address XXX) 
E3631A Power supply (at GPIB Address XX)
Rohde FSP Spectrum Analyzer (at GPIB Address XX)
34401A DMM configured as ammeter (at GPIB Address XXX)
34401A DMM configured as voltmeter (at GPIB Address XXX)
SDP box with ID #105 connected to USB
Filter matrix (at GPIB address 11) (M1 Prototype box)

Outputs:


'''



'''

TO DO:
- Filter matrix
- Determine why dictionary not keeping order
- Split equipment into different categories instead of a long string
- Set range on spec an to go from 0 to -120 (Need a custom command for this)

'''



from CommonResources import PowerSupplySetting, MHz, M1FilterBoxGPIB_ADDR, GrabDataForFrequency, LevelSigGenToDesiredLevel
from CommonResources import BOTTOM_SIG_GEN_GPIB_ADDRESS, LEFT_POWER_SUPPLY_E3631A_ADDRESS, VOLTMETER_34401A_ADDRESS, SPEC_AN_FSP_ADDRESS, SPEC_AN_FSU_ADDRESS

# ------- Parameters ------- EDIT BELOW HERE!

# ------ Sig Gen Settings
SIG_GEN_ADDR_FOR_TEST = BOTTOM_SIG_GEN_GPIB_ADDRESS
SIG_GEN_POWER = -30 # Starting value in dBm

SIG_GEN_MAX_LEVEL = 5 #dBm

#DUT_POWER_LEVELS = [-7, -9, -13, -19] # dBm (Power output from sig Gen)
DUT_POWER_LEVELS_AT_SPEC_AN = [-7]#, -9.5, -13, -15.5, -19] # dBm (Power output at spec An)  2Vpp/ 1.5Vpp / 1Vpp / 0.75Vpp / 0.5V for the 10-3700M 18dB Iso combiner

# ------

# ------ Filter box settings
####################################################################################################
# Installed on 2/28/17 by Chas Frick for David Brandon's Lab                                    ####
#### 1=Auxiliary        2=2.3MHz        3=10.3M         4=70M   5=100.3M        6=200M          ####
#### 7=300M             8=400M          9=500M          10=700M 11=1G           12=1.5G         ####
#### 13=2G              14=2.5G         15=3.1G         16=3.7G 17=4.1G         18=4.5G         ####
#### 19=5G              20=5.5G         21=5.95G                                                ####
####################################################################################################
from FilterBox import FilterBox
Filters = FilterBox.InstalledFilters #This list is all the filters
#Filters = InstalledFilters_2_28_17 # [2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15,  16,  17] This list is all the filters
#Filters = [17] # Uncomment this line to use a different filter list
# ------

# ------ Power supply settings
POWER_SUPPLY_ADDR_FOR_TEST = LEFT_POWER_SUPPLY_E3631A_ADDRESS

POWER_SUPPLY_SETTINGS_TUPLE_LIST = [PowerSupplySetting(voltageOutputPort='P6V', voltage=5.0, currentLimit=0.2)]
# ------


# ------ Voltmeter and ammeter settings

# ------

# ------- SPEC AN SETTINGS
SPEC_AN_FSUP_ADDRESS = SPEC_AN_FSP_ADDRESS
#SPEC_AN_FSUP_ADDRESS = SPEC_AN_FSU_ADDRESS
SPEC_AN_SPAN = 200 # Hz
SPEC_AN_RES_BW = 10 # Hz
SPEC_AN_VID_BW_HZ = 30 # Hz cannot set lower for FSP (but can for FSU spec an)
SPEC_AN_ATTENUATION = 30 # dB
SPEC_AN_REFERENCE_LEVEL = 0 # dBm
SPEC_AN_RANGE = 120 # dB
# -------

PRODUCT_NUMBER = 0

EVALUATION_BOARD_REVISION = 'A'
EVALUATION_BOARD_SERIAL_NUMBER = '12'

TEST_NAME = 'HarmonicDistortion'
   

DIFFERNTIAL_MEASUREMENT = True # Change to True for differential measurement or False for single ended measurement

# Settings for the SDP/Amp
''' Each setting is (DSA, Range, FA, Test Amp Gain Str) FA is not used unless HW pin is enabled though
    Range   DSA     FA      Test Amp Gain
    3       0       3       38dB
    3       5       3       33dB
    3       10      3       28dB
    3       15      3       23dB
    2       0       3       18dB
    2       5       3       13dB
    1       0       3       8dB
    1       5       3       3dB
'''

from AmpRegSettingClass import AmpRegSettingTuple
AMP_REG_SETTINGS_TUPLE_LIST = [AmpRegSettingTuple(0, 3, 3, "38"),
                        AmpRegSettingTuple(5, 3, 3, "33"),
                        AmpRegSettingTuple(10, 3, 3, "28"),
                        AmpRegSettingTuple(15, 3, 3, "23"),
                        AmpRegSettingTuple(0, 2, 3, "18"),
                        AmpRegSettingTuple(5, 2, 3, "13"),
                        AmpRegSettingTuple(0, 1, 3, "8"),
                        AmpRegSettingTuple(5, 1, 3, "3")]


#-------------------------- DO NOT EDIT BELOW HERE!

def Perform_HD2_HD3_Test(SIG_GEN_ADDR_FOR_TEST, PRODUCT_NUMBER, AMP_REG_SETTINGS_TUPLE_LIST, EVALUATION_BOARD_REVISION, EVALUATION_BOARD_SERIAL_NUMBER, DIFFERNTIAL_MEASUREMENT, POWER_SUPPLY_ADDR_FOR_TEST,
                        POWER_SUPPLY_SETTINGS_TUPLE_LIST, SPEC_AN_FSUP_ADDRESS, VOLTMETER_34401A_ADDRESS, AMMETER_34401A_ADDRESS = None, 
                        TEST_NAME='HarmonicDistortion', SIG_GEN_POWER=-10, Filters = Filters, SIG_GEN_MAX_LEVEL=5, SPEC_AN_VID_BW_HZ=30,
                        DUT_POWER_LEVELS_AT_SPEC_AN = [-7], SPEC_AN_SPAN = 200, SPEC_AN_RES_BW = 10, SPEC_AN_ATTENUATION = 30, SPEC_AN_REFERENCE_LEVEL = 0, SPEC_AN_RANGE = 120):
    
    import sys
    sys.path.append("T:\USB") # Brings in the drivers from the network drive

    import CSV

    import time
    import math
    import collections
    import ADI_GPIB
    import FilterBox

    sigGenForTest = ADI_GPIB.SMA(SIG_GEN_ADDR_FOR_TEST)
    #print sigGenForTest

    # Filter matrix setup
    M1FilterBox = FilterBox.FilterBox(M1FilterBoxGPIB_ADDR)
    

    voltmeter = ADI_GPIB.HP34401A(VOLTMETER_34401A_ADDRESS)
    #print voltmeter
    #ammeter = ADI_GPIB.HP34401A(AMMETER_34401A_ADDRESS)
    #print ammeter
    
    specAnFSUPSeries = ADI_GPIB.FSUP(SPEC_AN_FSUP_ADDRESS)
    #print specAnFSUPSeries
    
    powerSupplyForTest = ADI_GPIB.E3631A(POWER_SUPPLY_ADDR_FOR_TEST)
    #print powerSupplyForTest

    EquipmentUsedList = [sigGenForTest, voltmeter, specAnFSUPSeries, powerSupplyForTest]

    equipNameList = []
    for equip in EquipmentUsedList:
        equipNameList.append(equip.instr.ask("*IDN?"))

    inputBalun = None #Balun('Name')
    outputBalun = "5310 Picosecond Balun"

    if(DIFFERNTIAL_MEASUREMENT):
        EquipmentUsedList.append(outputBalun)
        equipNameList.append(outputBalun)

    EquipListStr = (";".join(equipNameList)).replace(",","_")
    #print EquipListStr
    
    # Turn off sig gens and power supply
    sigGenForTest.Enabled = 0
    powerSupplyForTest.Enabled = 0
    
    # Set spec an settings
    specAnFSUPSeries.AttLevel = SPEC_AN_ATTENUATION
    specAnFSUPSeries.ReferenceLevel = SPEC_AN_REFERENCE_LEVEL
    specAnFSUPSeries.instr.write("DISP:WIND:TRAC:Y:SPAC LOG") # Set vertical spacing to manual log scale
    specAnFSUPSeries.instr.write("DISP:WIND:TRAC:Y %ddB" % SPEC_AN_RANGE) # Set vertical to SPEC_AN_RANGE dB from the reference level
    specAnFSUPSeries.ResBand = 20*1e3 # 20 kHz
    specAnFSUPSeries.instr.write("BAND:VID %f Hz" % (SPEC_AN_VID_BW_HZ)) #Set video bw
    specAnFSUPSeries.Span = 20 * MHz # 20 MHz
    
    specAnFSUPSeries.instr.write("FREQ:SPAN:FULL") # Set to full span for a sec
    SPEC_AN_FULL_SPAN_MHZ_str = specAnFSUPSeries.instr.ask("FREQ:SPAN?") # Get the limits of the instrument
    SPEC_AN_FULL_SPAN_MHZ = float(SPEC_AN_FULL_SPAN_MHZ_str)

    # File naming
    fileNamesDict = {}
    for DUTPowerAtSpecAn in DUT_POWER_LEVELS_AT_SPEC_AN:
        currentTime = time.localtime() # returns timestruct
        timeStr = '__Date_%d_%d_%d__Time_%d_%d_%d' % (currentTime.tm_mon, currentTime.tm_mday, currentTime.tm_year, currentTime.tm_hour, currentTime.tm_min, currentTime.tm_sec)

        fileNameStart = 'TestName_%s__ProductNum_%s__BoardRev_%s__BoardSN_%s' % (TEST_NAME, str(PRODUCT_NUMBER), str(EVALUATION_BOARD_REVISION), str(EVALUATION_BOARD_SERIAL_NUMBER))

        fileExtension = '.csv'
        
        powerAtSpecAnStr = "_PowerAtSpecAn_M%f" % abs(DUTPowerAtSpecAn)
        
        powerAtSpecAnStr = powerAtSpecAnStr.replace(".", "P") # Replace the floatingPoint period
        
        fullFileName = fileNameStart + timeStr + powerAtSpecAnStr +fileExtension

        #print fullFileName
        
        fileNamesDict["%f" % DUTPowerAtSpecAn] = fullFileName

    for powerSupplySetting in POWER_SUPPLY_SETTINGS_TUPLE_LIST:
        print "Setting power supply to %s and %f A\n" % (powerSupplySetting.voltage, powerSupplySetting.currentLimit)
        # Set power supply levels
        sigGenForTest.Enabled = 0
        powerSupplyForTest.Enabled = 0
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

            time.sleep(0.25) # Wait 0.25 seconds
    
            for DUTPowerAtSpecAn in DUT_POWER_LEVELS_AT_SPEC_AN:
                print "*" * 40
                print "Setting DUT power to %f dBm\n" % DUTPowerAtSpecAn

                sigGenForTest.Enabled = 0

                sigGenForTest.Level = SIG_GEN_POWER # So have some room to start moving up with sig gen
                
                csvf = CSV.Results_File(fileNamesDict["%f" % DUTPowerAtSpecAn])

                for filterNum in Filters: # Run through each selected filter

                    # Set filter settings
                    M1FilterBox.SetFilterNum(sigGenForTest, filterNum) # Configures the sig gen frequency
                    
                    print "Sig Gen freq: %f" % sigGenForTest.Frequency
                    print "FilterBox filter: %d %s" % (M1FilterBox.CF, M1FilterBox.CFF)

                    print "*" * 40
                    print "Starting test with frequency: %f Hz\n" % sigGenForTest.Frequency
                    sigGenForTest.Level = SIG_GEN_POWER

                    time.sleep(1.0) # Wait 1 second

                    
                    sigGenForTest.Enabled = 1

                    # Level the sig gens out to the desired DUT output power
                    centerFreq = sigGenForTest.Frequency
                    LevelSigGenToDesiredLevel(SigGen=sigGenForTest, SpecAnObj=specAnFSUPSeries, Frequency=centerFreq, DesiredSpecAnLevel_dBm = DUTPowerAtSpecAn, SIG_GEN_MAX_LEVEL = SIG_GEN_MAX_LEVEL, numAvgs=1, RF_driveStarting = SIG_GEN_POWER)

                    # Zoom into and capture data for center frequency
                    print "\nCapturing data for center freq..."
                    (centerFreq, centerPow) = GrabDataForFrequency(specAnObj=specAnFSUPSeries, startingFreq=centerFreq, startingSpan=SPEC_AN_SPAN, startingResBW=SPEC_AN_RES_BW, startingVideoBW=SPEC_AN_VID_BW_HZ)

                    if(2*centerFreq < SPEC_AN_FULL_SPAN_MHZ):
                        # Zoom into and capture data for 2nd harmonic
                        print "\nCapturing data for 2nd harmonic..."
                        (secondFreq, secondPow) = GrabDataForFrequency(specAnObj=specAnFSUPSeries, startingFreq=2*centerFreq, startingSpan=SPEC_AN_SPAN, startingResBW=SPEC_AN_RES_BW, startingVideoBW=SPEC_AN_VID_BW_HZ)
                    else:
                        (secondFreq, secondPow) = ("N/A", "N/A")

                    if(3*centerFreq < SPEC_AN_FULL_SPAN_MHZ):
                        # Zoom into and capture data for 3rd harmonic
                        print "\nCapturing data for 3rd harmonic..."
                        (thirdFreq, thirdPow) = GrabDataForFrequency(specAnObj=specAnFSUPSeries, startingFreq=3*centerFreq, startingSpan=SPEC_AN_SPAN, startingResBW=SPEC_AN_RES_BW, startingVideoBW=SPEC_AN_VID_BW_HZ)
                    else:
                        (thirdFreq, thirdPow) = ("N/A", "N/A")
                        
                    # Measure current
                    measPowSupplyVoltage = getattr(powerSupplyForTest,powerSupplySetting.voltageOutputPort)
                    measPowSupplyCurrent = getattr(powerSupplyForTest,powerSupplySetting.currentOutputPort)
                    measVoltDMM = voltmeter.Voltage
                    measCurrDMM = 0 #ammeter.current
                    print "Measured voltage (E3631A): %f V\tWith DMM: %f V" % (float(measPowSupplyVoltage), float(measVoltDMM))
                    print "Measured current (E3631A): %f A\tWith DMM: %f A" % (float(measPowSupplyCurrent), float(measCurrDMM))
                                    
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

                    results_dict["Notes"] = equipNameList[equipNum].replace(",",";")
                    #results_dict["Notes"] = EquipListStr   
                    #results_dict["Notes %s" % equipStr] = equipNameList[equipNum].replace(",",";")
                    
		    results_dict["DSA Setting [Decimal]"] = AmpRegSetting.DSA
                    results_dict["Range Setting [Decimal]"] = AmpRegSetting.Range
                    results_dict["FA Setting [Decimal]"] = AmpRegSetting.FA
                    results_dict["Approx Amp Gain [dB]"] = AmpRegSetting.TestGainStr
                    
                    results_dict["f1 [Hz]"] = centerFreq
                    results_dict["p1 [dBm]"] = centerPow

                    results_dict["f2 [Hz]"] = secondFreq
                    if(secondPow != "N/A"):
                        results_dict["p2 [dBm]"] = secondPow
                    else:
                        results_dict["p2 [dBm]"] = "N/A"
                        
                    results_dict["f3 [Hz]"] = thirdFreq
                    if(thirdPow != "N/A"):
                        results_dict["p3 [dBm]"] = thirdPow
                    else:
                        results_dict["p3 [dBm]"] = "N/A"
                    
                    results_dict["Sig Gen Pow Lvl [dBm]"] = sigGenForTest.Level
                    results_dict["Set Power Supply Voltage [V]"] = powerSupplySetting.voltage
                    results_dict["Meas. Power Supply Voltage [V]"] = measPowSupplyVoltage
                    results_dict["Set Power Supply Current [A]"] = powerSupplySetting.currentLimit
                    results_dict["Meas. Power Supply Current [A]"] = measPowSupplyCurrent
                    results_dict["Measured DUT current [A]"] = measCurrDMM
                    results_dict["Measured DUT voltage [V]"] = measVoltDMM

                    
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

    sigGenForTest.Enabled = 0
    powerSupplyForTest.Enabled = 0
    
    print "-" * 40
    print "\nScript has completed after %f seconds!" % numSecondsForTest
    print "Check \"%s....csv\" for data!" % (TEST_NAME)

if __name__ == '__main__':
    
    Perform_HD2_HD3_Test(SIG_GEN_ADDR_FOR_TEST=SIG_GEN_ADDR_FOR_TEST, AMP_REG_SETTINGS_TUPLE_LIST=AMP_REG_SETTINGS_TUPLE_LIST, PRODUCT_NUMBER=PRODUCT_NUMBER, EVALUATION_BOARD_REVISION=EVALUATION_BOARD_REVISION,
                    EVALUATION_BOARD_SERIAL_NUMBER=EVALUATION_BOARD_SERIAL_NUMBER, DIFFERNTIAL_MEASUREMENT=DIFFERNTIAL_MEASUREMENT, POWER_SUPPLY_ADDR_FOR_TEST=POWER_SUPPLY_ADDR_FOR_TEST,
                    POWER_SUPPLY_SETTINGS_TUPLE_LIST=POWER_SUPPLY_SETTINGS_TUPLE_LIST, SPEC_AN_FSUP_ADDRESS=SPEC_AN_FSUP_ADDRESS, VOLTMETER_34401A_ADDRESS=VOLTMETER_34401A_ADDRESS, AMMETER_34401A_ADDRESS = None, 
                    TEST_NAME=TEST_NAME, SIG_GEN_POWER=SIG_GEN_POWER, Filters = Filters, SIG_GEN_MAX_LEVEL=SIG_GEN_MAX_LEVEL, 
                    DUT_POWER_LEVELS_AT_SPEC_AN=DUT_POWER_LEVELS_AT_SPEC_AN, SPEC_AN_VID_BW_HZ=SPEC_AN_VID_BW_HZ,
                    SPEC_AN_SPAN = SPEC_AN_SPAN, SPEC_AN_RES_BW = SPEC_AN_RES_BW, SPEC_AN_ATTENUATION = SPEC_AN_ATTENUATION, SPEC_AN_REFERENCE_LEVEL = SPEC_AN_REFERENCE_LEVEL, SPEC_AN_RANGE = SPEC_AN_RANGE)

    '''
    import sys
    sys.path.append("T:\USB") # Brings in the drivers from the network drive

    import CSV

    import time
    import math
    import collections
    import ADI_GPIB
    import FilterBox

    sigGenForTest = ADI_GPIB.SMA(SIG_GEN_ADDR_FOR_TEST)
    #print sigGenForTest

    # Filter matrix setup
    M1FilterBox = FilterBox.FilterBox(M1FilterBoxGPIB_ADDR)
    

    voltmeter = ADI_GPIB.HP34401A(VOLTMETER_34401A_ADDRESS)
    #print voltmeter
    #ammeter = ADI_GPIB.HP34401A(AMMETER_34401A_ADDRESS)
    #print ammeter
    
    #specAnFSU = ADI_GPIB.FSUP(SPEC_AN_FSU_ADDRESS)
    specAnFSP = ADI_GPIB.FSUP(SPEC_AN_FSP_ADDRESS)
    #print specAnFSP
    
    powerSupplyForTest = ADI_GPIB.E3631A(POWER_SUPPLY_ADDR_FOR_TEST)
    #print powerSupplyForTest

    EquipmentUsedList = [sigGenForTest, voltmeter, specAnFSP, powerSupplyForTest]

    equipNameList = []
    for equip in EquipmentUsedList:
        equipNameList.append(equip.instr.ask("*IDN?"))

    inputBalun = None #Balun('Name')
    outputBalun = "5310 Picosecond Balun"

    if(DIFFERNTIAL_MEASUREMENT):
        EquipmentUsedList.append(outputBalun)
    equipNameList.append(outputBalun)

    EquipListStr = (";".join(equipNameList)).replace(",","_")
    print EquipListStr
    
    # Turn off sig gens and power supply
    sigGenForTest.Enabled = 0
    powerSupplyForTest.Enabled = 0
    
    # Set spec an settings
    specAnFSP.AttLevel = SPEC_AN_ATTENUATION
    specAnFSP.ReferenceLevel = SPEC_AN_REFERENCE_LEVEL
    specAnFSP.instr.write("DISP:WIND:TRAC:Y:SPAC LOG") # Set vertical spacing to manual log scale
    specAnFSP.instr.write("DISP:WIND:TRAC:Y 120dB") # Set vertical to 120 dB from the reference level
    specAnFSP.ResBand = 20*1e3 # 20 kHz
    specAnFSP.Span = 20 * MHz # 20 MHz
    
    specAnFSP.instr.write("FREQ:SPAN:FULL") # Set to full span for a sec
    SPEC_AN_FULL_SPAN_MHZ_str = specAnFSP.instr.ask("FREQ:SPAN?") # Get the limits of the instrument
    SPEC_AN_FULL_SPAN_MHZ = float(SPEC_AN_FULL_SPAN_MHZ_str)
    
    for DUTPowerAtSpecAn in DUT_POWER_LEVELS_AT_SPEC_AN:
        print "*" * 40
        print "Setting DUT power to %f dBm\n" % DUTPowerAtSpecAn

        sigGenForTest.Enabled = 0

        sigGenForTest.Level = DUTPowerAtSpecAn + 5 # So have some room to start moving up with sig gen
        
        # File naming
        currentTime = time.localtime() # returns timestruct
        timeStr = '__Date_%d_%d_%d__Time_%d_%d_%d' % (currentTime.tm_mon, currentTime.tm_mday, currentTime.tm_year, currentTime.tm_hour, currentTime.tm_min, currentTime.tm_sec)

        fileNameStart = 'TestName_%s__ProductNum_%s__BoardRev_%s__BoardSN_%s' % (TEST_NAME, str(PRODUCT_NUMBER), str(EVALUATION_BOARD_REVISION), str(EVALUATION_BOARD_SERIAL_NUMBER))

        fileExtension = '.csv'
        
        powerAtSpecAnStr = "_PowerAtSpecAn_M%f" % abs(DUTPowerAtSpecAn)
        
        powerAtSpecAnStr = powerAtSpecAnStr.replace(".", "P") # Replace the floatingPoint period
        
        fullFileName = fileNameStart + timeStr + powerAtSpecAnStr +fileExtension
        
        csvf = CSV.Results_File(fullFileName)

        for filterNum in Filters: # Run through each selected filter

            # Set filter settings
            M1FilterBox.SetFilterNum(sigGenForTest, filterNum) # Configures the sig gen frequency
            
            print "Sig Gen freq: %f" % sigGenForTest.Frequency
            print "FilterBox filter: %d %s" % (M1FilterBox.CF, M1FilterBox.CFF)

            print "*" * 40
            print "Starting test with frequency: %f Hz\n" % sigGenForTest.Frequency
            sigGenForTest.Level = SIG_GEN_POWER

            time.sleep(1.0) # Wait 1 second

            for powerSupplySetting in POWER_SUPPLY_SETTINGS_TUPLE_LIST:
                print "Setting power supply to %s and %f A\n" % (powerSupplySetting.voltage, powerSupplySetting.currentLimit)
                # Set power supply levels
                sigGenForTest.Enabled = 0
                powerSupplyForTest.Enabled = 0
                setattr(powerSupplyForTest,powerSupplySetting.voltageOutputPort, powerSupplySetting.voltage)
                setattr(powerSupplyForTest,powerSupplySetting.currentOutputPort, powerSupplySetting.currentLimit)

                # Confirm settings
                #raw_input("Press enter to turn the power supply on...")
                print ("Turning on the power supply")
                powerSupplyForTest.Enabled = 1

                time.sleep(2.0) # Wait 2 seconds
                sigGenForTest.Enabled = 1

                # Level the sig gens out to the desired DUT output power
                centerFreq = sigGenForTest.Frequency
                LevelSigGenToDesiredLevel(SigGen=sigGenForTest, SpecAnObj=specAnFSP, Frequency=centerFreq, DesiredSpecAnLevel_dBm = DUTPowerAtSpecAn, SIG_GEN_MAX_LEVEL = 12, numAvgs=1, RF_driveStarting = -15)

                # Zoom into and capture data for center frequency
                print "\nCapturing data for center freq..."
                (centerFreq, centerPow) = GrabDataForFrequency(specAnObj=specAnFSP, startingFreq=centerFreq, startingSpan=SPEC_AN_SPAN, startingResBW=SPEC_AN_RES_BW)

                if(2*centerFreq < SPEC_AN_FULL_SPAN_MHZ):
                    # Zoom into and capture data for 2nd harmonic
                    print "\nCapturing data for 2nd harmonic..."
                    (secondFreq, secondPow) = GrabDataForFrequency(specAnObj=specAnFSP, startingFreq=2*centerFreq, startingSpan=SPEC_AN_SPAN, startingResBW=SPEC_AN_RES_BW)
                else:
                    (secondFreq, secondPow) = ("N/A", "N/A")

                if(3*centerFreq < SPEC_AN_FULL_SPAN_MHZ):
                    # Zoom into and capture data for 3rd harmonic
                    print "\nCapturing data for 3rd harmonic..."
                    (thirdFreq, thirdPow) = GrabDataForFrequency(specAnObj=specAnFSP, startingFreq=3*centerFreq, startingSpan=SPEC_AN_SPAN, startingResBW=SPEC_AN_RES_BW)
                else:
                    (thirdFreq, thirdPow) = ("N/A", "N/A")
                    
                # Measure current
                measPowSupplyVoltage = getattr(powerSupplyForTest,powerSupplySetting.voltageOutputPort)
                measPowSupplyCurrent = getattr(powerSupplyForTest,powerSupplySetting.currentOutputPort)
                measVoltDMM = voltmeter.voltage
                measCurrDMM = 0 #ammeter.current
                print "Measured voltage (E3631A): %f V\tWith DMM: %f V" % (float(measPowSupplyVoltage), float(measVoltDMM))
                print "Measured current (E3631A): %f A\tWith DMM: %f A" % (float(measPowSupplyCurrent), float(measCurrDMM))
                                
                # Record data 
                results_dict = collections.OrderedDict() # Remembers the order the keys are added and will output in this order!
                
                curTime = time.localtime()
                results_dict["Time"] = '%d:%d:%d' % (curTime.tm_hour % 12, curTime.tm_min, curTime.tm_sec)
                
                #results_dict["Equipment used"] = EquipListStr
                for equipNum in range(len(EquipmentUsedList)):
                
                        equipStr = str(EquipmentUsedList[equipNum]) # Looks like <ADI_GPIB.ObjType.ObjType at 0xXXXX>
                        
                        if("balun" not in equipStr and "Balun" not in equipStr):
                            equipStr = equipStr.split(".")
                            equipStr = equipStr[1] # Grab the Obj type
                            
                results_dict["EQUIPMENT %s" % equipStr] = equipNameList[equipNum].replace(",",";")
                
                
                results_dict["Center Freq [Hz]"] = centerFreq
                results_dict["Center Pow [dBc]"] = centerPow
                results_dict["2nd Freq [Hz]"] = secondFreq
                
                if(secondPow != "N/A"):
                    results_dict["2nd Pow [dBc]"] = centerPow - float(secondPow)
                else:
                    results_dict["2nd Pow [dBc]"] = "N/A"
                    
                results_dict["3rd Freq [Hz]"] = thirdFreq
                
                if(thirdPow != "N/A"):
                    results_dict["3rd Pow [dBc]"] = centerPow - float(thirdPow)
                else:
                    results_dict["3rd Pow [dBc]"] = "N/A"
                
                results_dict["Sig Gen Pow Lvl [dBm]"] = sigGenForTest.Level
                results_dict["Set Power Supply Voltage [V]"] = powerSupplySetting.voltage
                results_dict["Meas. Power Supply Voltage [V]"] = measPowSupplyVoltage
                results_dict["Set Power Supply Current [A]"] = powerSupplySetting.currentLimit
                results_dict["Meas. Power Supply Current [A]"] = measPowSupplyCurrent
                results_dict["Measured DUT current [A]"] = measCurrDMM
                results_dict["Measured DUT voltage [V]"] = measVoltDMM

                results_dict["Differential"] = DIFFERNTIAL_MEASUREMENT
                
                
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

    sigGenForTest.Enabled = 0
    powerSupplyForTest.Enabled = 0
    
    print "-" * 40
    print "\nScript has completed after %f seconds!" % numSecondsForTest
    print "Check \"%s\" for data!" % (fullFileName)  
    '''
