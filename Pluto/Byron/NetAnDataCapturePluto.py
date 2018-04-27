## Python script for control of PNA-X
# For MCP Lab Pluto
# Using this link: http://na.support.keysight.com/pna/help/latest/help.htm

# etup to make use of ADI_GPIB code
import ADI_GPIB.GPIBObject as GPIB
import time

# from CallSDP_Configure_FA_Range_DSA import Configure_FA_Range_DSA # For SDP interface
from PlutoV1 import PlutoV1


# Create the instance for the Network analyzer
NetAnAddr = 16 # Might change on a power cycle?

# DEVICE CS LINES
AMP_1_CS = "A"
AMP_2_CS = "B"
AMP_CS = AMP_2_CS

dutDevice = PlutoV1() # 100kHz SPI, 16 bit R/W (8 bit addr, 8 bit data)
dutDevice.connect(DUT1_Default = 0x00, DUT2_Default = 0x00) # Used same ID. Change later

# Test Options
SCREENSHOT = True
CSV = True
S4P = True

if __name__ == "__main__":

    NetAn = GPIB.GPIBObjectBaseClass(name="NetAn",addr=NetAnAddr,delay=0.25)

    raw_input("Manually calibrate the ports first and setup the measruements please! Then press enter...")

    # Make the directory for saving files
    filePath = "c:/Pluto_Att_Data/%s" % (time.ctime().replace(":","_"))
    filePath = filePath.replace(' ', '_')

    NetAn.Write("MMEM:MDIR '%s'" % filePath) # Create directory

    NetAn.Write("MMEMory:STORe:CSAR '%s/%s'" % (filePath, 'configSettings')) # Save the .csa file

    # AmpEnable one of {0, 1}
    dutDevice.Set_Amp_Enable(SPI_sel=AMP_CS, AmpEnable=True)
    # dutDevice.Set_Amp_Enable(SPI_sel = AMP_2_CS, AmpEnable = 1)

    # Bit of magic to get trace names for screenshotting things
    traceNames = NetAn.Query('CALC:PAR:CAT?')
    traceNames = traceNames.replace("\"", "")
    traceNames = traceNames.split(",") # Something like this now: ['CH1_S11_1', 'Sdd11', 'CH1_SDD22_2', 'Sdd22', 'CH1_SDD21_3', 'Sdd21', 'CH1_SDD12_4', 'Sdd12']
    traceNames = [traceNames[x] for x in range(0, len(traceNames), 2)]
    print traceNames

    NetAn.Write('CALC:PAR:SEL "%s"' % traceNames[0])  # Select the first trace --> required to avoid invalid parameters for the save S4P file

    # Run through and grab each dataset. Range generates an array of up to num - 1 (e.g. range(31) generates list with 0 to 31)
    pauseForAutoset=True
    for AttVal in range(11):  # 0-10

        # Set gain etc through SDP
        # Atten = Attenuation in dB (between 0 and 1 dB)
        Att_Val = AttVal * 0.1
        dutDevice.Set_Amp_Atten(SPI_sel=AMP_CS, AmpAtten=Att_Val)



        if (pauseForAutoset):
            raw_input("Please press autoset scale button to level everything onto the screen. Then press enter")
            pauseForAutoset = False
            # ConfiguredProperly = Configure_FA_Range_DSA(FA_Val = FAVal, Range_Val = RangeVal, DSA_Val = DSAVal)

        time.sleep(4)

        # Finally save off the data
        fileName = "DataFor_%.1f__dB" % (Att_Val) # Make sure to have everything 0 to 1dB
        fileName=fileName.replace('.', 'p')

        if(SCREENSHOT):
            # Save a screenshot of each trace
            for traceNum in range(len(traceNames)):
                fileNameTmp=fileName + "_Trace%d" % (traceNum + 1)
                print "Saving screenshot file as %s.png...\n" % fileNameTmp
                NetAn.Write('CALC:PAR:SEL "%s"' % traceNames[traceNum])
                NetAn.Write("HCOPY:FILE '%s/%s'" % (filePath, fileNameTmp + ".png"))

            NetAn.Write('CALC:PAR:SEL "%s"' % traceNames[0])  # Reselect the first trace

        if(S4P):
            print "Saving s4p file as %s.s4p...\n" % fileName
            NetAn.Query("CALC:DATA:SNP:PORTs:Save '1,2,3,4','%s/%s.s4p';*OPC?" % (filePath, fileName))
            time.sleep(2)

        if(CSV):
            print "Saving csv file as %s.csv...\n" % fileName
            # Save a .csv
            # Save all the displayed traces in the format that they are displayed in
            # -1 is used when the first arg after CSV formatted data is displayed
            NetAn.Write("MMEMory:STORe:DATA '%s/%s','CSV Formatted Data','displayed','displayed',-1" % (filePath, (fileName + ".csv")))
            time.sleep(2)

        #raw_input("press enter to go to next point...") # remove

    print "Thank You"
    dutDevice.Set_Amp_Enable(SPI_sel=AMP_CS, AmpEnable=False)
