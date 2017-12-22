# Incorporating structure from ADL5569_VNA_Automation Vee file
import sys, visa, time, math, cmath
sys.path.append('../../Common')

from ADI_GPIB.WatlowF4 import *
from ADI_GPIB.E3631A import *
from ADI_GPIB.KeysightN5242A import *

VNA = KeysightN5424A(17)
Oven = WatlowF4(4)
Supply = E3631A(23)


def VNAinit():
    VNA.__Preset__()
    VNA.__AddWindow__(1)
    VNA.__AddMeas__(1, 'P1dB', 'Gain Compression', 'CompOut21')
    VNA.__AddTrace__(1, 1, 'P1dB')
    VNA.__SetStartf__(1, 10.5e6)
    VNA.__SetStopf__(1, 10.0105e9)
    VNA.__SetNumPoints__(1, 1e3)
    VNA.__SetAvg__(1, avg)
    VNA.__SetSweepType__(1, 'LOG')
    VNA.__SetAutoTime__(1, True)
    VNA.__RecallCal__('BS_IMD_Cal')
    VNA.__GainCompMaxLevel__(2, 10)

def setTemp(setpoint):
    Oven.__SetTemp__(setpoint)
    current = float(Oven.__GetTemp__())
    while (abs(current - setpoint) > 2):
        time.sleep(1)
        current = float(Oven.__GetTemp__())
    print '@ Temp %d' % setpoint
    time.sleep(300)
    return True

def getData():
    VNA.__EnableAvg__(1, False)
    VNA.__EnableAvg__(1, True)
    time.sleep(60)
    print 'Done Sleeping'
    VNA.__FinishAvg__(1, 600)

    VNA.__SetActiveTrace__(1, 'P1dB')
    ans = VNA.__GetData__(1)
    ans = ans.split(',')
    for val in range(len(ans)):
        ans[val] = float(ans[val])
    P1dB = ans

    freqlist = VNA.__GetFreq__(1)
    fh.write('Frequency,')
    fh.write(str(freqlist).strip('[]'))
    fh.write('\n')
    fh.write('P1dB,')
    fh.write(str(P1dB).strip('[]'))
    fh.write('\n')

def header():
    dut = '3-5 ChA'
    test = 'PNA-X IMD'
    equipment = 'BAL0026 6dB in and out '
    header = (dut, date, test, equipment)
    header = str(header).strip('()')
    fh.write(header)
    fh.write('\n')

startTime = time.time()

path = 'C:\\Users\\#RFW_Test01\\Desktop\\Pronghorn_Results\\VNA_Results\\P1dB\\'

date = time.ctime(time.time())
date = date.replace(':', '-')
fh = open(path + 'P1dB' + date + '.csv', 'w')

Zin_diff = 100
Zout_diff = 100
avg = 5

numPoints = 1000.0
startFreq = 10.5e6
endFreq = 10.0105e9

measlist = ['PwrMainHi', 'PwrMainLo', 'IM3HI', 'IM3LO', 'PwrMainIN', 'OIP3LO', 'OIP3HI']
# templist = [25, -40, 80]
templist = [25]
vcomlist = ['N\A']

header()
Supply.__SetEnable(1)
VNAinit()
for temp in templist:
    if templist != [25]:
        setTemp(temp)
    fh.write('Temp = %d' % temp)
    fh.write('\n')
    for vcom in vcomlist:
        fh.write('Vcom = %s\n' % vcom)
        getData()
if templist != [25]:
    Oven.__SetTemp__(25)
Supply.__SetEnable__(0)
endTime = time.time() - startTime

print 'Program executed in %d seconds.' % endTime

fh.write('Execution Time = ,%d' % endTime)

fh.close()

