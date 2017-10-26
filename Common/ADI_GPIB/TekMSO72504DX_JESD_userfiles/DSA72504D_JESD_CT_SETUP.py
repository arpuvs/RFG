## @package Tx Characterization
# (C) COPYRIGHT 2015 Brett Li
# Description
#    This PY file is used to enable Tx CT
# PROJECT: Tx Characterization
# FILENAME: DSA72504D_JESD_CT_Setup.py
# CREATED: 2015.03.28
# DESIGNER: Brett Li
# REVISION: 0x1.0
# REVISION HISTORY: Aug 24, 2015 Leah Magaldi made edits


##==========================================
## import modules
##==========================================


##==========================================
## Declaration of GPIB and USB equipment
##==========================================`
from GPIBObjectList import *

from JESD204B_CT import CT

##==========================================
## below variables should be changed for the tek scope.
##==========================================
channel = 0 #tek setup channel see TekMSO72504Dx
Datarate = 12.5
Lanenumber = 'A'
Part = 18
Serial_Rate = round((Datarate*1000),0)
temperature = '25'
current_voltage = '1'
vterm = 0 # This is the Rx termination voltage
BER_target = 15 # This is specified in 1E-(N)
pattern_length = 127# This should match the pattern length from the DUT
mask = '11GTx'  # 5 choices are: '11GTx' '6GTx' '11GRx' '6GRx' 'NONE'
displayplots = "Eye" # choices are 'All' (4 plots) or Eye (1 plot)
report_filename = 'Panda\\PN' +str(Part) + '_Lane' + str(Lanenumber) + '_' + str(Serial_Rate) + '_' + str(temperature) + '_' + str(current_voltage)

return_value = CT(channel,vterm,Datarate,str(report_filename),BER_target,pattern_length,mask,displayplots)
#SaveReportToFile(report_filename)
#channel,vterm,Datarate,report_filename,BER_target,pattern_length,scope,mask
#return report_filename 
                        
print return_value;                    

