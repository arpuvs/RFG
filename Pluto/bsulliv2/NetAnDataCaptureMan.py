## Python script for control of PNA-X
# For MCP Lab Pluto

# Using this link: http://na.support.keysight.com/pna/help/latest/help.htm

# Setup to make use of ADI_GPIB code
# import sys
# sys.path.append("C:\\test\\PyTest\\USB") # Brings in the drivers from the network drive
import ADI_GPIB.GPIBObject as GPIB
import time


# Create the instance for the Network analyzer
NetAnAddr = 16 # Might change on a power cycle?
NetAn = GPIB.GPIBObjectBaseClass(name="NetAn",addr=NetAnAddr,delay=0.25)

raw_input("Manually calibrate the ports first and setup the measruements please! Then press enter...")


# Make the directory for saving files
filePath =  "c:/Pluto_Att_Data/%s" % (time.ctime().replace(":","_"))
filePath = filePath.replace(' ', '_')

# Finally save off the data
fileName="DataFor_Pluto-Man"   # Make sure to have everything 0 to 1dB

NetAn.Write("MMEM:MDIR '%s'" % filePath) # Create directory

NetAn.Write("MMEMory:STORe:CSAR '%s/%s'" % (filePath, fileName)) # Save the .csa file

# Finally save off the data

NetAn.Write("CALC:DATA:SNP:PORTs:Save '1,2,3,4','%s/%s.s4p';*OPC?" % (filePath, fileName))

time.sleep(2)

# Save a .csv
# Save all the displayed traces in the format that they are displayed in
# -1 is used when the first arg after CSV formatted data is displayed
NetAn.Write("MMEMory:STORe:DATA '%s/%s','CSV Formatted Data','displayed','displayed',-1" % (filePath, (fileName + ".csv")))

time.sleep(2)
            
# Save a screenshot
NetAn.Write("HCOPY:FILE '%s/%s'" % (filePath, fileName + ".png"))

# Change leopard gain etc and retake data
