
from CommonResources import PowerSupplySetting, MHz, M1FilterBoxGPIB_ADDR, GrabDataForFrequency, LevelSigGenToDesiredLevel
from CommonResources import BOTTOM_SIG_GEN_GPIB_ADDRESS, LEFT_POWER_SUPPLY_E3631A_ADDRESS, VOLTMETER_34401A_ADDRESS, SPEC_AN_FSP_ADDRESS, SPEC_AN_FSU_ADDRESS

# ------- Parameters ------- EDIT BELOW HERE!

# ------ Sig Gen Settings
SIG_GEN_ADDR_FOR_TEST = BOTTOM_SIG_GEN_GPIB_ADDRESS
SIG_GEN_POWER = -30 # Starting value in dBm

SIG_GEN_MAX_LEVEL = 20#dBm

DUT_POWER_LEVELS_AT_SPEC_AN = [-2.17, -4.67, -8.19] # dBm (Power output at spec An)  2Vpp/ 1.5Vpp / 1Vpp / 0.75Vpp / 0.5V for the 10-3700M 18dB Iso combiner
#DUT_POWER_LEVELS_AT_SPEC_AN = [-2.17] # dBm (Power output at spec An)  2Vpp/ 1.5Vpp / 1Vpp / 0.75Vpp / 0.5V for the 10-3700M 18dB Iso combiner

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
Filters = [2, 3, 4, 5, 6, 7, 9, 11, 13, 14, 15, 16, 1, 18] # Uncomment this line to use a different filter list
#Filters = [1] # Uncomment this line to use a different filter list

# ------

# ------ Power supply settings
POWER_SUPPLY_ADDR_FOR_TEST = LEFT_POWER_SUPPLY_E3631A_ADDRESS

POWER_SUPPLY_SETTINGS_TUPLE_LIST = [PowerSupplySetting(voltageOutputPort='P6V', voltage=5.0, currentLimit=0.5)]
# ------


# ------ Voltmeter and ammeter settings

# ------

# ------- SPEC AN SETTINGS
#SPEC_AN_FSUP_ADDRESS = SPEC_AN_FSU_ADDRESS # comment here
SPEC_AN_FSUP_ADDRESS = SPEC_AN_FSP_ADDRESS
SPEC_AN_SPAN = 200 # Hz
SPEC_AN_RES_BW = 10 # Hz
SPEC_AN_VID_BW_HZ = 30 # Hz cannot set lower for FSP (but can for FSU spec an)
SPEC_AN_ATTENUATION = 30 # dB
SPEC_AN_REFERENCE_LEVEL = 5 # dBm 
SPEC_AN_RANGE = 140 # dB
# -------

PRODUCT_NUMBER = 0

EVALUATION_BOARD_REVISION = 'LG38rA'
EVALUATION_BOARD_SERIAL_NUMBER = '1'

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
'''
AMP_REG_SETTINGS_TUPLE_LIST = [AmpRegSettingTuple(5, 1, 3, "3")]
'''
AMP_REG_SETTINGS_TUPLE_LIST = [AmpRegSettingTuple(0, 3, 3, "38"),
                        AmpRegSettingTuple(5, 3, 3, "33"),
                        AmpRegSettingTuple(10, 3, 3, "28"),
                        AmpRegSettingTuple(15, 3, 3, "23"),
                        AmpRegSettingTuple(0, 2, 3, "18"),
                        AmpRegSettingTuple(5, 2, 3, "13"),
                        AmpRegSettingTuple(0, 1, 3, "8"),
                        AmpRegSettingTuple(5, 1, 3, "3")]



# -------------------- DO NOT EDIT BELOW HERE! ---------------------------

from HD2_HD3_Test import Perform_HD2_HD3_Test

Perform_HD2_HD3_Test(SIG_GEN_ADDR_FOR_TEST=SIG_GEN_ADDR_FOR_TEST, AMP_REG_SETTINGS_TUPLE_LIST=AMP_REG_SETTINGS_TUPLE_LIST, PRODUCT_NUMBER=PRODUCT_NUMBER, EVALUATION_BOARD_REVISION=EVALUATION_BOARD_REVISION,
                    EVALUATION_BOARD_SERIAL_NUMBER=EVALUATION_BOARD_SERIAL_NUMBER, DIFFERNTIAL_MEASUREMENT=DIFFERNTIAL_MEASUREMENT, POWER_SUPPLY_ADDR_FOR_TEST=POWER_SUPPLY_ADDR_FOR_TEST,
                    POWER_SUPPLY_SETTINGS_TUPLE_LIST=POWER_SUPPLY_SETTINGS_TUPLE_LIST, SPEC_AN_FSUP_ADDRESS=SPEC_AN_FSUP_ADDRESS, VOLTMETER_34401A_ADDRESS=VOLTMETER_34401A_ADDRESS, AMMETER_34401A_ADDRESS = None, 
                    TEST_NAME=TEST_NAME, SIG_GEN_POWER=SIG_GEN_POWER, Filters = Filters, SIG_GEN_MAX_LEVEL=SIG_GEN_MAX_LEVEL, 
                    DUT_POWER_LEVELS_AT_SPEC_AN=DUT_POWER_LEVELS_AT_SPEC_AN, SPEC_AN_VID_BW_HZ=SPEC_AN_VID_BW_HZ,
                    SPEC_AN_SPAN = SPEC_AN_SPAN, SPEC_AN_RES_BW = SPEC_AN_RES_BW, SPEC_AN_ATTENUATION = SPEC_AN_ATTENUATION, SPEC_AN_REFERENCE_LEVEL = SPEC_AN_REFERENCE_LEVEL, SPEC_AN_RANGE = SPEC_AN_RANGE)
