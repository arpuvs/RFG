from CommonResources import MID_SIG_GEN_GPIB_ADDRESS, TOP_SIG_GEN_GPIB_ADDRESS, LEFT_POWER_SUPPLY_E3631A_ADDRESS, VOLTMETER_34401A_ADDRESS, SPEC_AN_FSP_ADDRESS, SPEC_AN_FSU_ADDRESS
from CommonResources import MHz, PowerSupplySetting

# ------- Parameters ------- EDIT BELOW HERE! ----------
# Test 1 of 6
# ------ Sig Gen Settings ------------------------------
SIG_GEN_1_ADDR_FOR_TEST = TOP_SIG_GEN_GPIB_ADDRESS
SIG_GEN_2_ADDR_FOR_TEST = MID_SIG_GEN_GPIB_ADDRESS
SIG_GEN_POWER = -20
# Starting value in dBm
CENTER_FREQUENCIES_LIST = [100*MHz, 200*MHz, 500*MHz, 1000*MHz, 1500*MHz, 2000*MHz, 2500*MHz, 3000*MHz, 3500*MHz, 4000*MHz] # All these are in Hz! 

# ------ Settings for frequency sweep 


# ------------------------------------

SIG_GEN_MAX_LEVEL = 28 # dBm --> Maximum power the signal generator can go to before it gives up trying to level the spec an power 
SIG_GEN2_IMD3_OFFSET = 2*MHz # Offset for other generator (e.g. 100MHz SigGen1 --> 2 MHz offset --> 98MHz SigGen2)
DUT_POWER_LEVELS_AT_SPEC_AN = [-5.25, -7.75, -11.27] # dBm (Power output at spec An)  1V for the 10-3700M 18dB Iso combiner

# ------------------------------------------------------

# Have to load cal data

# ------ Power supply settings -------------------------
POWER_SUPPLY_ADDR_FOR_TEST = LEFT_POWER_SUPPLY_E3631A_ADDRESS

POWER_SUPPLY_SETTINGS_TUPLE_LIST = [PowerSupplySetting(voltageOutputPort='P6V', voltage=5.09, currentLimit=0.5)] # Leopard is higher current
# ------------------------------------------------------

# ------ Voltmeter and ammeter settings ----------------
VOLTMETER_34401A_ADDRESS = VOLTMETER_34401A_ADDRESS
# ------------------------------------------------------

# ------- SPEC AN SETTINGS -----------------------------
#SPEC_AN_FSUP_ADDRESS = SPEC_AN_FSU_ADDRESS
SPEC_AN_FSUP_ADDRESS = SPEC_AN_FSP_ADDRESS
SPEC_AN_SPAN = 200 # Hz
SPEC_AN_RES_BW = 10 # Hz
SPEC_AN_VID_BW_HZ = 30 # Hz cannot set lower for FSP (but can for FSU spec an)
SPEC_AN_ATTENUATION = 30 # dB to see spurs on noise floor
SPEC_AN_REFERENCE_LEVEL = 0 # dBm
SPEC_AN_RANGE = 140 # dB
# ------------------------------------------------------

PRODUCT_NUMBER = 'Leopard'

EVALUATION_BOARD_REVISION = 'RevA'

EVALUATION_BOARD_SERIAL_NUMBER = '3'

TEST_NAME = 'IMD3'
   
DIFFERNTIAL_MEASUREMENT = True # Change to True for differential measurement or False for single ended measurement

# Settings for the SDP/Amp
''' Each setting is (DSA, Range, FA, Test Amp Gain Str) FA is not used unless HW pin is enabled though
    Range   DSA     FA      Test Amp Gain
    3       0       3       38dB
    3       5       3       33dB
    3       10      3       28dB
    3       15      3       23dB
    3       20      3       18dB
    2       0       3       18dB
    2       5       3       13dB
    2       10      3       8dB
    1       0       3       8dB
    1       5       3       3dB
    1       10      3       -2dB

'''
from AmpRegSettingClass import AmpRegSettingTuple
AMP_REG_SETTINGS_TUPLE_LIST = [AmpRegSettingTuple(0, 1, 3, "10"),
                        AmpRegSettingTuple(4, 1, 3, "6"),
                        AmpRegSettingTuple(8, 1, 3, "2"),
                        AmpRegSettingTuple(0, 2, 3, "20"),
                        AmpRegSettingTuple(4, 2, 3, "16"),
			AmpRegSettingTuple(8, 2, 3, "12"),
			AmpRegSettingTuple(12, 2, 3, "8"),
                        AmpRegSettingTuple(16, 2, 3, "4"),
                        AmpRegSettingTuple(0, 3, 3, "40"),
                        AmpRegSettingTuple(4, 3, 3, "36"),
			AmpRegSettingTuple(8, 3, 3, "32"),
			AmpRegSettingTuple(12, 3, 3, "28"),
                        AmpRegSettingTuple(16, 3, 3, "24"),
			AmpRegSettingTuple(20, 3, 3, "20")] 

# -------------------- DO NOT EDIT BELOW HERE! ---------------------------

from IMD3_LEOPARD_ONLY import PerformIMD3Test

PerformIMD3Test(SIG_GEN_1_ADDR_FOR_TEST=SIG_GEN_1_ADDR_FOR_TEST, AMP_REG_SETTINGS_TUPLE_LIST=AMP_REG_SETTINGS_TUPLE_LIST, SIG_GEN_2_ADDR_FOR_TEST=SIG_GEN_2_ADDR_FOR_TEST, PRODUCT_NUMBER=PRODUCT_NUMBER, EVALUATION_BOARD_REVISION=EVALUATION_BOARD_REVISION,
                EVALUATION_BOARD_SERIAL_NUMBER=EVALUATION_BOARD_SERIAL_NUMBER, DIFFERNTIAL_MEASUREMENT=DIFFERNTIAL_MEASUREMENT, POWER_SUPPLY_ADDR_FOR_TEST=POWER_SUPPLY_ADDR_FOR_TEST,
                POWER_SUPPLY_SETTINGS_TUPLE_LIST=POWER_SUPPLY_SETTINGS_TUPLE_LIST, SPEC_AN_FSUP_ADDRESS=SPEC_AN_FSUP_ADDRESS, VOLTMETER_34401A_ADDRESS=VOLTMETER_34401A_ADDRESS, AMMETER_34401A_ADDRESS = None, 
                TEST_NAME=TEST_NAME, SIG_GEN_POWER=SIG_GEN_POWER, CENTER_FREQUENCIES_LIST=CENTER_FREQUENCIES_LIST, SIG_GEN_MAX_LEVEL=SIG_GEN_MAX_LEVEL, 
                SIG_GEN2_IMD3_OFFSET=SIG_GEN2_IMD3_OFFSET, DUT_POWER_LEVELS_AT_SPEC_AN=DUT_POWER_LEVELS_AT_SPEC_AN, SPEC_AN_VID_BW_HZ = SPEC_AN_VID_BW_HZ,
                SPEC_AN_SPAN = SPEC_AN_SPAN, SPEC_AN_RES_BW = SPEC_AN_RES_BW, SPEC_AN_ATTENUATION = SPEC_AN_ATTENUATION, SPEC_AN_REFERENCE_LEVEL = SPEC_AN_REFERENCE_LEVEL, SPEC_AN_RANGE = SPEC_AN_RANGE)

