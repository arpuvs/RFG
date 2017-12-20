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
    # VNA.__Preset__()
    # # VNA.__SetSweepType__(1, 'LOG')
    # VNA.__SetStartf__(1, startFreq)
    # VNA.__SetStopf__(1, endFreq)
    # VNA.__SetNumPoints__(1, numPoints)
    # VNA.__SetAvg__(1, avg)
    # VNA.__SetAutoTime__(1, True)
    # VNA.__SetTrigType__('MAN')
    # VNA.__SetContinuous__(1, False)
    # VNA.__EnableAvg__(1, True)
    # # VNA.__EnableTrigAvg__(True)
    # VNA.__SetTopology__(1, 'BBAL')
    # VNA.__SetPorts__(1, 1, 3, 2, 4)
    # VNA.__EnableBal__(1)
    # VNA.instr.write('SENS:CORR:CSET:ACT \"BS_Cal\", 1')

    VNA.__Preset__('full')
    # VNA.instr.write('SENS:CORR:CSET:ACT \"BS_Cal\", 1')
    VNA.__AddWindow__(1)
    # VNA.__AddMeas__(1, 'PwrMainHi', 'Swept IMD', 'PwrMainHi')
    trace = 1
    for meas in measlist:
        VNA.__AddMeas__(1, meas, 'Swept IMD', meas)
        VNA.__AddTrace__(1, trace, meas)
        trace = trace + 1
    VNA.__SetStopf__(1, 10.0105e9)
    VNA.__SetNumPoints__(1, 1e3)
    VNA.__SetAvg__(1, avg)
    VNA.__SetAutoTime__(1, True)
    # VNA.__SetTrigType__('MAN')
    # VNA.__SetContinuous__(1, False)
    VNA.__EnableAvg__(1, True)
    VNA.__IMDPowType__(1, 'OUTPUT')
    VNA.__IMDPower__(1, -8)
    # VNA.__EnableTrigAvg__(True)
    # VNA.__SetTopology__(2, 'BBAL')
    # VNA.__SetPorts__(2, 1, 3, 2, 4)
    # VNA.__EnableBal__(2)
    VNA.instr.write('SENS:CORR:CSET:ACT \"BS_IMD_Cal\", 1')
    VNA.instr.write('SENS:POW:ATT AREC,10')
    VNA.instr.write('SENS:POW:ATT BREC,10')
    VNA.__EnableAvg__(1, True)
    VNA.__SetAvg__(1, avg)


def setTemp(setpoint):
    # print 'Assuming same oven set up as on my bench'

    Oven.__SetTemp__(setpoint)
    current = float(Oven.__GetTemp__())
    while (abs(current - setpoint) > 2):
        time.sleep(1)
        current = float(Oven.__GetTemp__())
    print '@ Temp %d' % setpoint
    # if temp != 25:
    time.sleep(300)
    return True


# def setSupply():

def meas():
    VNA.__CheckStatus__(600)
    for run in range(avg):
        VNA.__InitMeas__(1)
        VNA.__CheckStatus__(600)
    # VNA.__SingleTrig__()  # ERROR: Unidentified header
    ans = VNA.__GetData__(1)
    ans = ans.split(',')
    for val in range(len(ans)):
        ans[val] = float(ans[val])
    # magans = []
    # imagans = []
    # for val in range(len(ans)):
    #     if (val % 2) == 0:
    #         magans.append(float(ans[val]))
    #     else:
    #         imagans.append(float(ans[val]))

    # compans = []
    # for val in range(len(magans)):
    #     compans.append(magans[val] + imagans[val] * 1j)

    # return compans
    # return magans, imagans
    return ans

def getData():
    readDict = {}
    VNA.__EnableAvg__(1, False)
    VNA.__EnableAvg__(1, True)
    time.sleep(60)
    print 'Done Sleeping'
    VNA.__FinishAvg__(1, 600)
    for meas in measlist:
        VNA.__SetActiveTrace__(1, meas)
        # VNA.__CheckStatus__(600)
        # for i in range(avg):
        #     VNA.__InitMeas__(1)
        #     VNA.__CheckStatus__(600)
        ans = VNA.__GetData__(1)
        ans = ans.split(',')
        for val in range(len(ans)):
            ans[val] = float(ans[val])
        readDict[meas] = ans

    freqlist = VNA.__GetFreq__(1)
    fh.write('Frequency,')
    fh.write(str(freqlist).strip('[]'))
    fh.write('\n')
    for meas in measlist:
        fh.write(meas)
        fh.write(',')
        fh.write(str(readDict[meas]).strip('[]'))
        fh.write('\n')
    #
    #
    # fh.write('Frequency,')
    # fh.write(str(freqlist).strip('[]'))
    # fh.write('\n')
    # fh.write('SCC21 MLOG,')
    # fh.write(str(scc21_mlog).strip('[]'))
    # fh.write('\n')
    # fh.write('SDC21 MLOG,')
    # fh.write(str(sdc21_mlog).strip('[]'))
    # fh.write('\n')
    # fh.write('SDD11 POL 1,')
    # fh.write(str(sdd11_pol[0]).strip('[]'))
    # fh.write('\n')
    # fh.write('SDD11 POL 2,')
    # fh.write(str(sdd11_pol[1]).strip('[]'))
    # fh.write('\n')
    # fh.write('SDD12 MLOG,')
    # fh.write(str(sdd12_mlog).strip('[]'))
    # fh.write('\n')
    # fh.write('SDD21 GDEL,')
    # fh.write(str(sdd21_gdel).strip('[]'))
    # fh.write('\n')
    # fh.write('SDD21 MLOG,')
    # fh.write(str(sdd21_mlog).strip('[]'))
    # fh.write('\n')
    # fh.write('SDD21 POL 1,')
    # fh.write(str(sdd21_pol[0]).strip('[]'))
    # fh.write('\n')
    # fh.write('SDD21 POL 2,')
    # fh.write(str(sdd21_pol[1]).strip('[]'))
    # fh.write('\n')
    # fh.write('SDD11 MLOG,')
    # fh.write(str(sdd11_mlog).strip('[]'))
    # fh.write('\n')
    # fh.write('SDD22 MLOG,')
    # fh.write(str(sdd22_mlog).strip('[]'))
    # fh.write('\n')
    # fh.write('AV, ')
    # fh.write(str(av).strip('[]'))
    # fh.write('\n')
    # fh.write('CMRR1, ')
    # fh.write(str(cmrr1).strip('[]'))
    # fh.write('\n')
    # fh.write('CMRR2, ')
    # fh.write(str(cmrr2).strip('[]'))
    # fh.write('\n')
    # fh.write('Group Delay,')
    # fh.write(str(group_delay).strip('[]'))
    # fh.write('\n')
    # fh.write('S12_V,')
    # fh.write(str(s12_v).strip('[]'))
    # fh.write('\n')

def header():
    dut = '3-5 ChB'
    test = 'PNA-X IMD'
    equipment = 'BAL0026 6dB in and out '
    # supplyV = Supply.__MeasP25V__()
    # supplyV = 'Temp'
    # print supplyV
    # supplyI = Supply.__MeasP25I__()
    # supplyI = 'Temp'
    # print supplyI
    # balun = 'INB: 0-VIN OUTB 0-VOP'
    header = (dut, date, test, equipment)
    header = str(header).strip('()')
    fh.write(header)
    fh.write('\n')







    # VNA.__SetBBalParam__(1, 1, 'SDD12')     # Doesn't seem to change to SDD12
    # VNA.__SetActiveFormat__(1, 'MLOG')
    # sdd12_mlog = meas()
    # print sdd12_mlog

startTime = time.time()

path = 'C:\\Users\\#RFW_Test01\\Desktop\\Pronghorn_Results\\VNA_Results\\IMD\\'

date = time.ctime(time.time())
date = date.replace(':', '-')
fh = open(path + 'VNA_IMD' + date + '.csv', 'w')

Zin_diff = 100
Zout_diff = 100
avg = 5

numPoints = 1000.0
startFreq = 10.5e6
endFreq = 10.0105e9

measlist = ['PwrMainHi', 'PwrMainLo', 'IM3HI', 'IM3LO', 'PwrMainIN', 'OIP3LO', 'OIP3HI']
templist = [25]
vcomlist = ['N\A']

header()
Supply.__SetEnable__(1)
VNAinit()
for temp in templist:
    # for balun in balunList:
    if templist != [25]:
        setTemp(temp)
    # fh.write('Balun config = %s' % balun)
    fh.write('Temp = %d' % temp)
    fh.write('\n')
    for vcom in vcomlist:
        fh.write('Vcom = %s\n' % vcom)
        # Supply.__SetV__(vcom, 3)  # Does nothing right now. Second supply not connected
        getData()
if templist != [25]:
    Oven.__SetTemp__(25)
Supply.__SetEnable__(0)
endTime = time.time() - startTime

print 'Program executed in %d seconds.' % endTime

fh.write('Execution Time = ,%d' % endTime)

fh.close()
# supplies = [5.0]
# temps = [25]
# currents = []
#
# VNAinit()
# for temp in temps:
#     # setTemp(temp)
#     for supply in supplies:
#         # setSupply()
#         supply.__SetP6V__(supply)
#         supply.__SetP25V__(3.3)
#         currents.append(float(supply.__MeasP6I__()))
#
#         getData()

