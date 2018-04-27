def GrabDataForFrequency(specAnObj, startingFreq, startingSpan, startingResBW, startingVideoBW=30, correctionFactorOutputDict=None, freqDwellTime=None, numAvgsAfter50=2, numAvgsAfter70=5):
    import time

    specAnObj.CenterFrequency = startingFreq

    specAnObj.Span = startingSpan

    specAnObj.ResBand = startingResBW

    specAnObj.instr.write("BAND:VID %f Hz" % startingVideoBW) # Set video BW

    specAnObj.marker = startingFreq

    if(freqDwellTime == None):
        time.sleep(float(specAnObj.instr.ask("SWE:TIME?"))*1.5) # Wait 1.5 times the sweep time normally
    else:
        time.sleep(freqDwellTime) # Otherwise wait for the user specified amount of time

    [measFreq, measAmplitude] = specAnObj.marker

    print "Freq: %f Hz Pow: %f dBm" % (measFreq, measAmplitude)

    if(measAmplitude <= -50.0 and measAmplitude > - 70.0): # If measured ampltitude is between -50 and -70 then average it numAvgsAfter50 times
        avgAmpl = 0
        for avg in range(numAvgsAfter50):
            [measFreq, measAmplitude] = specAnObj.marker
            avgAmpl +=  measAmplitude

            if(freqDwellTime == None):
                time.sleep(float(specAnObj.instr.ask("SWE:TIME?"))*1.1) # Wait 1.1 times the sweep time normally
            else:
                time.sleep(freqDwellTime) # Otherwise wait for the user specified amount of time

            
        avgAmpl /= float(numAvgsAfter50)
        measAmplitude = avgAmpl # set the amplitude equal to the final average
        
    elif(measAmplitude <= -70.0): # If measured ampltitude is below -70 then average it numAvgsAfter70 times
        avgAmpl = 0
        for avg in range(numAvgsAfter70):
            [measFreq, measAmplitude] = specAnObj.marker
            avgAmpl +=  measAmplitude

            if(freqDwellTime == None):
                time.sleep(float(specAnObj.instr.ask("SWE:TIME?"))*1.1) # Wait 1.1 times the sweep time normally
            else:
                time.sleep(freqDwellTime) # Otherwise wait for the user specified amount of time
                
        avgAmpl /= float(numAvgsAfter70)
        measAmplitude = avgAmpl # set the amplitude equal to the final average
        
    # Apply correction factor for output cable/balun
    if(correctionFactorOutputDict is not None):
        # Get factor from lookup
        correctionFactorOutputCable = -14 # dBm --> Found using lookup table with frequency for balun
        measFreqPowCorrected = measAmplitude - correctionFactorOutputCable # Correction factor is negative
        print "Corrected pow: %s dBm" % str(measFreqPowCorrected)
    else:
        measFreqPowCorrected = measAmplitude
        print "Meas pow specAn: %s dBm" % str(measFreqPowCorrected)
    
    return (measFreq, measFreqPowCorrected)

def GetTonePower(specAnObj, startingFreq, numAvgs, startingSpan_Hz=200, startingResBW_Hz=10, startingVidBW_Hz=30, outputCorrectionDict=None, freqDwellTime=None, numAvgsAfter50=2, numAvgsAfter70=5):
    ''' A wrapper to make the getting of fundamental power data easier '''
    avgTonePower = 0
    avgFreq = 0
    for avg in range(numAvgs):        
        (freq, power) = GrabDataForFrequency(specAnObj, startingFreq, startingSpan=startingSpan_Hz, startingResBW=startingResBW_Hz, startingVideoBW = startingVidBW_Hz, numAvgsAfter50=numAvgsAfter50, numAvgsAfter70=numAvgsAfter70)
        avgTonePower += power
        avgFreq += freq

    return (avgFreq/float(numAvgs), avgTonePower/float(numAvgs))
  
def LevelSigGenToDesiredLevel(SigGen, SpecAnObj, Frequency, DesiredSpecAnLevel_dBm = -13, SIG_GEN_MAX_LEVEL = 15, numAvgs=4, RF_driveStarting = -35):
    import time
    MAX_TRIES = 10
    
    SigGen.Level = RF_driveStarting   # Set sig gen level
    New_Fund = float(SigGen.Level)
    #print "Sig Gen Level"
    #print New_Fund

    (avgFreq, avgPow) = GetTonePower(specAnObj=SpecAnObj, startingFreq=Frequency, numAvgs=numAvgs)
        
    Difference = abs(DesiredSpecAnLevel_dBm - avgPow)
    #print Difference
    # keep adjusting until the difference between measured fund power and desired level is +-0.1
    # and until you have tried MAX_TRIES times 
    #   * this is necessary because sometimes it gets stuck and bounces back and forth between two numbers
    #   * and can't get any closer ( you might hear a clicking noise from the SMA, that is what's happening )
    numRuns = 0
    while (abs(Difference) > 0.1 and numRuns < MAX_TRIES):  
        (avgFreq, avgPow) = GetTonePower(specAnObj=SpecAnObj, startingFreq=Frequency, numAvgs=numAvgs)
    
        Difference = DesiredSpecAnLevel_dBm - avgPow
        #print Difference
        # adjust the New_Fund based on the difference
        New_Fund += Difference
        #print New_Fund
        
        if (New_Fund < SIG_GEN_MAX_LEVEL):
            SigGen.Level = New_Fund
        else:
            SigGen.Level = SIG_GEN_MAX_LEVEL
            numRuns = MAX_TRIES
            
        # increase the try count by 1
        numRuns += 1
        time.sleep(0.3)
    
    return SigGen.Level 
    
    
class PowerSupplySetting:
    '''Useful for interacting with the E3631A. Just say "PowerSupplySetting("P6V",5.0, 2.0)" to set to 6V supply with 5.0V @ 2.0 A limit'''
    def __init__(self, voltageOutputPort, voltage, currentLimit):
        if(voltageOutputPort not in ["P6V", "P25V", "N25V"]):
           raise Exception("Did not define output correctly! Use P6V, P25V or N25V")
        self.voltageOutputPort = voltageOutputPort
        self.currentOutputPort = voltageOutputPort[:-1]+"I"
        self.voltage = voltage
        self.currentLimit = currentLimit
    
    def __GetVoltage__(self):
        return self.voltage
        
    def __GetCurrentLimit__(self):
        return self.currentLimit

    def __GetVoltageOutputPort__(self):
        return self.voltageOutputPort

    def __GetCurrentOutputPort__(self):
        return self.currentOutputPort

    voltageOutputPort    = property(__GetVoltageOutputPort__,  None, None, "Gets the output voltage port")
    currentOutputPort    = property(__GetCurrentOutputPort__,  None, None, "Gets the output current port")
    voltage              = property(__GetVoltage__,      None, None, "Gets the voltage setting")
    currentLimit         = property(__GetCurrentLimit__,      None, None, "Gets the current limit setting")


# ------ MHz definition
MHz = 1e6
	
# ------ GPIB Addresses
TOP_SIG_GEN_GPIB_ADDRESS = 12 # Top SMA100
MID_SIG_GEN_GPIB_ADDRESS = 13 # Mid SMA100
BOTTOM_SIG_GEN_GPIB_ADDRESS = 14 # Bottom SMA100
    

LEFT_POWER_SUPPLY_E3631A_ADDRESS = 6 
RIGHT_POWER_SUPPLY_E3631A_ADDRESS = 7 # NOT ON GPIB YET

AMMETER_34401A_ADDRESS = 25 # Ammeter DMM function
VOLTMETER_34401A_ADDRESS = 24 # Voltmeter DMM function

SPEC_AN_FSP_ADDRESS = 20
SPEC_AN_FSU_ADDRESS = 21

M1FilterBoxGPIB_ADDR = 11 # Filter box prototype
# ------ 
