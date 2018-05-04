import sys, visa, time, math, cmath
sys.path.append('../../Common')

# Instrumnet imports and initialization
# from ADI_GPIB.WatlowF4 import *
# from ADI_GPIB.E3631A import *
# from ADI_GPIB.KeysightN5242A import *
from openpyxl import *
from BSTest import *
from PlutoV0 import PlutoV0


def NF():
    print 'Temp'


if __name__ == '__main__':
    path = 'C:\\Users\\bsulliv2\\Documents\\Results\\Pluto\\Raw\\Sparam\\'
    summaryPath = 'C:\\Users\\bsulliv2\\Documents\\Results\\Pluto\\PlutoSparamSummary.xlsx'

    Zin_diff = 100
    Zout_diff = 100
    avg = 16

    numPoints = 1000.0
    startFreq = 10e6
    endFreq = 10.01e9

    templist = [25]
    vcomlist = ['N/A']
    supplylist = [3.3]
    gainlist = ['12dB', '20dB']
    pwrmodelist = ['Low', 'Hi']
    Poutlist = [0, -8]
    dut = 'V1B3 B'
    channel = 'B'

    instDict = InstInit()

    pluto = PlutoV0()
    pluto.connect(DUT1_Default=0x00, DUT2_Default=0x00)
    pluto.Set_Amp_Gain(SPI_sel=channel, GainValue='12dB')
    pluto.Set_Amp_Coupling(SPI_sel=channel, Coupling='ON')
    pluto.Set_Amp_Pwr_Mod(SPI_sel=channel, PowerMode="Hi")
    pluto.Set_Amp_Enable(SPI_sel=channel, AmpEnable=True)
    pluto.Set_Amp_Trim(SPI_sel=channel, AmpTrimCode=15)

    NF()

    pluto.Set_Amp_Enable(SPI_sel=channel, AmpEnable=False)