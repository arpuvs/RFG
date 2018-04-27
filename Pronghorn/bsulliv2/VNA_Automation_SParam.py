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
    VNA.__Preset__()
    VNA.__SetSweepType__(1, 'LOG')
    VNA.__SetStartf__(1, startFreq)
    VNA.__SetStopf__(1, endFreq)
    VNA.__SetNumPoints__(1, numPoints)
    VNA.__SetAutoTime__(1, True)
    VNA.__EnableAvg__(1, False)
    VNA.__SetTopology__(1, 'BBAL')
    VNA.__SetPorts__(1, 1, 3, 2, 4)
    VNA.__EnableBal__(1)
    VNA.__RemoveTrace__(1, 1)
    trace = 1

    # Adds measurements from supplied list
    for meas in measlist:
        VNA.__AddMeas__(1, meas, 'Standard', meas.split()[0])
        VNA.__AddTrace__(1, trace, meas)
        VNA.__SetActiveTrace__(1, meas)
        VNA.__SetActiveFormat__(1, meas.split()[1])
        trace = trace + 1

    VNA.__RecallCal__('BS_Cal')
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

# The following three functions are simple math operations taken from VNA Vee program
def build_av(mlog):
    ans = []
    for val in range(len(mlog)):
        ans.append(mlog[val] - 10.0*math.log10(Zin_diff/Zout_diff))
    return ans


def build_cmrr(sdd21, sdc21):
    ans = []
    for val in range(len(sdd21)):
        ans.append(sdd21[val] - sdc21[val])
    return ans


def build_gdel(phase, freq):
    ans = []
    ans.append(0)
    for val in range(len(phase) - 1):
        ans.append(((phase[val+1] - phase[val])*math.pi/180.0)/(freq[val+1]-freq[val]))
    return ans


# Retrieves measured data from VNA and prints to file
def getData():
    readDict = {}   # Dictionary for results to be stored in
    time.sleep(30)  # Necessary to let one sweep finish. Otherwise FinishAvg function does not work
    VNA.__FinishAvg__(1, 600)   # Pauses execution until VNA is finished averaging

    # Retrieve data from VNA
    for meas in measlist:
        VNA.__SetActiveTrace__(1, meas)
        ans = VNA.__GetData__(1)
        ans = ans.split(',')
        # Converts received data from unicode to numeric
        for val in range(len(ans)):
            ans[val] = float(ans[val])
        # Polar measurements return real and imaginary data that must be separated
        if meas.split()[1] == 'POL':
            readDict[meas + '1'] = []
            readDict[meas + '2'] = []
            for i in range(len(ans)):
                if i % 2:
                    readDict[meas + '1'].append(ans[i])
                else:
                    readDict[meas + '2'].append(ans[i])
        else:
            readDict[meas] = ans

    # Retrieves and converts swept frequency points
    freqlist = VNA.__GetFreq__(1)
    freqlist = freqlist.split(',')
    for val in range(len(freqlist)):
        freqlist[val] = float(freqlist[val])

    # Math functions from VNA Vee program
    av = build_av(readDict['SDD21 MLOG'])
    cmrr1 = build_cmrr(readDict['SDD21 MLOG'], readDict['SDC21 MLOG'])
    cmrr2 = build_cmrr(readDict['SDD21 MLOG'], readDict['SCC21 MLOG'])
    group_delay = build_gdel(readDict['SDD21 POL1'], freqlist)
    s12_v = build_av(readDict['SDD12 MLOG'])
    # zyIn = build_zy(sdd11_mlog)
    # zyOut = build_zy(sdd22_mlog)

    # Writes all data to file
    fh.write('Frequency,')
    fh.write(str(freqlist).strip('[]'))
    fh.write('\n')
    for meas in measlist:
        # Polar measurements need additional processing due to complex form
        if meas.split()[1] == 'POL':
            fh.write(meas + '1')
            fh.write(',')
            fh.write(str(readDict[meas + '1']).strip('[]'))
            fh.write('\n')
            fh.write(meas + '2')
            fh.write(',')
            fh.write(str(readDict[meas + '2']).strip('[]'))
            fh.write('\n')
        # All other measurements can be printed as is
        else:
            fh.write(meas)
            fh.write(',')
            fh.write(str(readDict[meas]).strip('[]'))
            fh.write('\n')
    fh.write('AV, ')
    fh.write(str(av).strip('[]'))
    fh.write('\n')
    fh.write('CMRR1, ')
    fh.write(str(cmrr1).strip('[]'))
    fh.write('\n')
    fh.write('CMRR2, ')
    fh.write(str(cmrr2).strip('[]'))
    fh.write('\n')
    fh.write('Group Delay,')
    fh.write(str(group_delay).strip('[]'))
    fh.write('\n')
    fh.write('S12_V,')
    fh.write(str(s12_v).strip('[]'))
    fh.write('\n')

# Prints first line of file
def header():
    test = 'P1dB'
    equipment = 'N5242A PNA-X BAL0026'
    header = (dut, date, test, equipment)
    header = str(header).strip('()')
    fh.write(header)
    fh.write('\n')


startTime = time.time()

path = 'C:\\Users\\#RFW_Test01\\Desktop\\Pronghorn_Results\\VNA_Results\\'

date = time.ctime(time.time())
date = date.replace(':', '-')
dut = '3-5 CHB'
fh = open(path + dut + ' SParam_' + date + '.csv', 'w')    # Creates csv file

# Impedance parameters
Zin_diff = 100
Zout_diff = 100
avg = 16

# Frequency sweep parameters
numPoints = 1000.0
startFreq = 10e6
endFreq = 10.01e9

# Measurements to be taken. See online VNA guide for more options
measlist = ['SCC21 MLOG', 'SDC21 MLOG', 'SDD11 POL', 'SDD12 MLOG', 'SDD21 GDEL',
            'SDD21 MLOG', 'SDD21 POL', 'SDD11 MLOG', 'SDD22 MLOG']

# Swept parameters
templist = [25]
vcomlist = ['N/A']

dut = '3-5 CHB'

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
