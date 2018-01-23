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
vcomSupply = E3631A(15)

# Sets all necessary VNA parameters and adds all specified measurements
def VNAinit():
    VNA.__Preset__('full')
    VNA.__AddWindow__(1)
    trace = 1

    # Adds measurements from supplied list
    for meas in measlist:
        VNA.__AddMeas__(1, meas, 'Swept IMD', meas)
        VNA.__AddTrace__(1, trace, meas)
        trace = trace + 1

    VNA.__SetStopf__(1, 10.0105e9)
    VNA.__SetNumPoints__(1, 1e3)
    VNA.__SetAvg__(1, avg)
    VNA.__SetAutoTime__(1, True)
    VNA.__EnableAvg__(1, True)
    VNA.__IMDPowType__(1, 'OUTPUT')
    VNA.__IMDPower__(1, -8)
    VNA.__RecallCal__('BS_IMD_Cal')
    VNA.__SetAttenuation__(10)
    VNA.__SetSourceAttenuation__(1, 2, 0)
    VNA.__EnableAvg__(1, True)
    VNA.__SetAvg__(1, avg)

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
    readDict = {}   # Dictionary for results to be stored in
    VNA.__EnableAvg__(1, False)
    VNA.__EnableAvg__(1, True)

    time.sleep(60)  # Necessary to let one sweep finish. Otherwise FinishAvg function does not work
    print 'Done Sleeping'
    VNA.__FinishAvg__(1, 600)   # Pauses execution until VNA is finished averaging

    # Retrieve data from VNA
    for meas in measlist:
        VNA.__SetActiveTrace__(1, meas)
        ans = VNA.__GetData__(1)
        ans = ans.split(',')
        # Converts received data from unicode to numeric
        for val in range(len(ans)):
            ans[val] = float(ans[val])
        readDict[meas] = ans

    # Retrieves swept frequency points
    freqlist = VNA.__GetFreq__(1)

    # Writes all data to file
    fh.write('Frequency,')
    fh.write(str(freqlist).strip('[]'))
    fh.write('\n')
    for meas in measlist:
        fh.write(meas)
        fh.write(',')
        fh.write(str(readDict[meas]).strip('[]'))
        fh.write('\n')

# Prints first line of file
def header():
    dut = '3-4 ChA'
    test = 'PNA-X IMD'
    equipment = 'BAL0026 6dB in and out '
    header = (dut, date, test, equipment)
    header = str(header).strip('()')
    fh.write(header)
    fh.write('\n')


startTime = time.time()

path = 'C:\\Users\\bsulliv2\\Desktop\\Pronghorn_Results\\VNA_Results\\IMD'

date = time.ctime(time.time())
date = date.replace(':', '-')
fh = open(path + 'VNA_IMD' + date + '.csv', 'w')    # Creates csv file

# Impedance parameters
Zin_diff = 100
Zout_diff = 100
avg = 5

# Frequency sweep parameters
numPoints = 1000.0
startFreq = 10.5e6
endFreq = 10.0105e9

# Measurements to be taken. See online VNA guide for more options
measlist = ['PwrMainHi', 'PwrMainLo', 'IM3HI', 'IM3LO', 'PwrMainIN', 'OIP3LO', 'OIP3HI']

# Swept parameters
templist = [25, -40, 85]
vcomlist = [2.0, 2.5, 3.0]
supplylist = [4.5, 5.0, 5.5]

header()
Supply.__SetEnable__(1)
VNAinit()

# Main loop structure
for temp in templist:
    if templist != [25]:
        setTemp(temp)
    fh.write('Temp = %d' % temp)
    fh.write('\n')
    for supply in supplylist:
        Supply.__SetP25V__(supply)
        fh.write('Supply = %g\n' % supply)
        for vcom in vcomlist:
            vcomSupply.__SetP25V__(vcom)
            fh.write('Vcom = %g\n' % vcom)
            time.sleep(0.2)
            getData()

# Final actions: return to temperature, get execution time and close file
if templist != [25]:
    Oven.__SetTemp__(25)
Supply.__SetEnable__(0)
endTime = time.time() - startTime

print 'Program executed in %d seconds.' % endTime

fh.write('Execution Time = ,%d' % endTime)

fh.close()
