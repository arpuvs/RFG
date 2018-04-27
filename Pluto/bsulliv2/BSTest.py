import sys
import time
from PlutoV1 import PlutoV1
# sys.path.append('E:/bsulliv2/hcg_wireline/common')
# from ADI_GPIB.E3633A import *
# from ADI_GPIB.TekDSA72504D import *
# from SMAUSB import *

def Main():
    # instDict['Supply3p3'].__SetEnable__(1)
    dutDevice = PlutoV1()
    dutDevice.connect(DUT1_Default = 0x00, DUT2_Default = 0x00)
    dutDevice.Set_Amp_Enable(SPI_sel='A', AmpEnable=True)
    dutDevice.Set_Amp_Atten(SPI_sel='A', AmpAtten=0.0)
    raw_input('Waiting...')
    dutDevice.Set_Amp_Atten(SPI_sel='A', AmpAtten=0.9)
    raw_input('Waiting...')
    dutDevice.Set_Amp_Enable(SPI_sel='A', AmpEnable=False)

def InstInit():
    instDict = {}
    # instDict['source'] = AgilentE8257D(1)
    # instDict['source'] = SDG12070('USB0::0x1857::0x2F26::4129339::INSTR')
    # instDict['errorDet'] = PED13020('USB0::0x1857::0x32DC::2133327::INSTR')
    # instDict['Supply2'] = Keithley2230('0x05E6::0x2230::9200245')
    # instDict['Supply1'] = Keithley2230('0x05E6::0x2230::9200268')
    # instDict['Supply3'] = Keithley2230('0x05E6::0x2230::9200526')
    instDict['Supply3p3'] = E3633A(8)
    instDict['clkSource'] = SMAUSB('USB0::0x0AAD::0x0048::104063::INSTR')
    # instDict['thermo'] = Thermo4300(29, 1, 140, -60)
    instDict['scope'] = TekDSA72504D(15)
    return instDict

if __name__ == '__main__':
    # InstInit()
    Main()
