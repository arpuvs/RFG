# Author: Ben Sullivan
# Date: 12/19/2017

import sys, visa, time, math, cmath
sys.path.append('../../Common')

# Instrumnet imports and initialization
from ADI_GPIB.WatlowF4 import *
from ADI_GPIB.E3631A import *
from ADI_GPIB.KeysightN5242A import *

VNA = KeysightN5424A(17)
Oven = WatlowF4(4)
Supply = E3631A(23)

# Sets all necessary VNA parameters and adds all specified measurements
def VNAinit():
    VNA.__Preset__('full')
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
    VNA.__GainCompMaxLevel__(1, 10)

# Sets oven to specified temperature and soaks
def setTemp(setpoint):
    Oven.__SetTemp__(setpoint)
    current = float(Oven.__GetTemp__())
    while (abs(current - setpoint) > 2):
        time.sleep(1)
        current = float(Oven.__GetTemp__())
    print '@ Temp %d' % setpoint
    time.sleep(300)
    return True

# Retrieves measured data from VNA and prints to file
def getData():
    VNA.__EnableAvg__(1, False)
    VNA.__EnableAvg__(1, True)

    time.sleep(60)  # Necessary to let one sweep finish. Otherwise FinishAvg function does not work
    print 'Done Sleeping'
    VNA.__FinishAvg__(1, 600)  # Pauses execution until VNA is finished averaging

    # Retrieve data from VNA
    VNA.__SetActiveTrace__(1, 'P1dB')
    ans = VNA.__GetData__(1)
    ans = ans.split(',')
    # Converts received data from unicode to numeric
    for val in range(len(ans)):
        ans[val] = float(ans[val])
    P1dB = ans

    # Retrieves swept frequency points
    freqlist = VNA.__GetFreq__(1)

    # Writes all data to file
    fh.write('Frequency,')
    fh.write(str(freqlist).strip('[]'))
    fh.write('\n')
    fh.write('P1dB,')
    fh.write(str(P1dB).strip('[]'))
    fh.write('\n')


# Prints first line of file
def header():
    dut = '3-5 ChA'
    test = 'PNA-X IMD'
    equipment = 'BAL0026 6dB in and out '
    header = (dut, date, test, equipment)
    header = str(header).strip('()')
    fh.write(header)
    fh.write('\n')


startTime = time.time()

path = 'C:\\Users\\bsulliv2\\Desktop\\Pronghorn_Results\\VNA_Results\\P1dB\\'

date = time.ctime(time.time())
date = date.replace(':', '-')
fh = open(path + 'P1dB' + date + '.csv', 'w')

# Impedance parameters
Zin_diff = 100
Zout_diff = 100
avg = 5

# Frequency sweep parameters
numPoints = 1000.0
startFreq = 10.5e6
endFreq = 10.0105e9

# Swept parameters
# templist = [25, -40, 80]
templist = [25]
vcomlist = ['N\A']

header()
Supply.__SetEnable__(1)
VNAinit()

# Main loop structure
for temp in templist:
    if templist != [25]:
        setTemp(temp)
    fh.write('Temp = %d' % temp)
    fh.write('\n')
    for vcom in vcomlist:
        fh.write('Vcom = %s\n' % vcom)
        getData()

# Final actions: return to temperature, get execution time and close file
if templist != [25]:
    Oven.__SetTemp__(25)
Supply.__SetEnable__(0)
endTime = time.time() - startTime

print 'Program executed in %d seconds.' % endTime

fh.write('Execution Time = ,%d' % endTime)

fh.close()
