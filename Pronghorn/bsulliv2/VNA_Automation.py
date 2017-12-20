# Incorporating structure from ADL5569_VNA_Automation Vee file
import sys, visa, time, math, cmath
sys.path.append('../../Common')

from ADI_GPIB.WatlowF4 import *
from ADI_GPIB.E3631A import *
from ADI_GPIB.KeysightN5242A import *

VNA = KeysightN5424A(17)
Oven = WatlowF4(4)
# Supply = E3631A(23)


def VNAinit():
    VNA.__Preset__()
    VNA.__SetSweepType__(1, 'LOG')
    VNA.__SetStartf__(1, startFreq)
    VNA.__SetStopf__(1, endFreq)
    VNA.__SetNumPoints__(1, numPoints)
    VNA.__SetAutoTime__(1, True)
    # VNA.__SetTrigType__('MAN')
    # VNA.__SetContinuous__(1, False)
    VNA.__EnableAvg__(1, False)
    # VNA.__EnableTrigAvg__(True)
    VNA.__SetTopology__(1, 'BBAL')
    VNA.__SetPorts__(1, 1, 3, 2, 4)
    VNA.__EnableBal__(1)
    # VNA.instr.write('SENS:CORR:CSET:ACT \"BS_Cal\", 1')
    VNA.__RemoveTrace__(1, 1)
    trace = 1
    for meas in measlist:
        VNA.__AddMeas__(1, meas, 'Standard', meas.split()[0])
        VNA.__AddTrace__(1, trace, meas)
        VNA.__SetActiveTrace__(1, meas)
        VNA.__SetActiveFormat__(1, meas.split()[1])
        trace = trace + 1


    # VNA.__SetTopology__(1, 'BBAL')
    # VNA.__SetPorts__(1, 1, 3, 2, 4)
    # VNA.__EnableBal__(1)
    VNA.instr.write('SENS:CORR:CSET:ACT \"BS_Cal\", 1')
    VNA.__EnableAvg__(1, True)
    VNA.__SetAvg__(1, avg)


def setTemp(setpoint):
    print 'Assuming same oven set up as on my bench'

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
    # print len(phase)
    # print len(freq)
    for val in range(len(phase) - 1):
        ans.append(((phase[val+1] - phase[val])*math.pi/180.0)/(freq[val+1]-freq[val]))
    return ans

def lumped(mlog):
    val = []

    Zin_mag = []
    Zin_phase = []
    Zin_real = []
    Zin_imag = []
    Yin_real = []
    Yin_imag = []


    Rpin = []
    Rsin = []
    # Rpout = []
    # Rsout = []
    Cpin = []
    Csin = []
    # Cpout = []
    # Csout = []
    Lpin = []
    Lsin = []
    # Lpout = []
    # Lsout = []

    for num in range(len(mlog)):
        val.append(mlog[num] * (1+Zin_diff)/(1+Zin_diff))
        Zin_mag.append(abs(val[num]))
        Zin_phase.append(cmath.phase(val[num]))
        Zin_real.append(val[num].real)
        Zin_imag.append(val[num].imag)
        Yin_real.append((1.0/(val[num])).real)
        Yin_imag.append((1.0/(val[num])).imag)

        Rpin.append(1.0/Yin_real[num])
        Rsin.append(Zin_real[num])
        Cpin.append(Yin_imag[num]/(2.0*math.pi*freqlist[num]))
        Csin.append(1.0/(Zin_imag[num]*2.0*math.pi*freqlist[num]))
        Lpin.append(1.0/(Yin_imag*2.0*math.pi*freqlist[num]))
        Lsin.append(Zin_imag/(2.0*math.pi*freqlist[num]))

    # return [Zin_mag, Zin_phase, Zin_real, Zin_imag, Yin_real, Yin_imag]




def getData():
    readDict = {}
    time.sleep(30)
    VNA.__FinishAvg__(1,600)
    for meas in measlist:
        VNA.__SetActiveTrace__(1, meas)
        ans = VNA.__GetData__(1)
        ans = ans.split(',')
        for val in range(len(ans)):
            ans[val] = float(ans[val])

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

    freqlist = VNA.__GetFreq__(1)
    freqlist = freqlist.split(',')
    for val in range(len(freqlist)):
        freqlist[val] = float(freqlist[val])

    av = build_av(readDict['SDD21 MLOG'])
    cmrr1 = build_cmrr(readDict['SDD21 MLOG'], readDict['SDC21 MLOG'])
    cmrr2 = build_cmrr(readDict['SDD21 MLOG'], readDict['SCC21 MLOG'])
    group_delay = build_gdel(readDict['SDD21 POL1'], freqlist)
    s12_v = build_av(readDict['SDD12 MLOG'])
    # zyIn = build_zy(sdd11_mlog)
    # zyOut = build_zy(sdd22_mlog)

    fh.write('Frequency,')
    fh.write(str(freqlist).strip('[]'))
    fh.write('\n')
    for meas in measlist:
        if meas.split()[1] == 'POL':
            fh.write(meas + '1')
            fh.write(',')
            fh.write(str(readDict[meas + '1']).strip('[]'))
            fh.write('\n')
            fh.write(meas + '2')
            fh.write(',')
            fh.write(str(readDict[meas + '2']).strip('[]'))
            fh.write('\n')
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
    test = 'P1dB'
    equipment = 'N5242A PNA-X BAL0026'
    # supplyV = Supply.__MeasP25V__()
    # supplyI = Supply.__MeasP25I__()
    header = (dut, date, test, equipment)
    header = str(header).strip('()')
    fh.write(header)
    fh.write('\n')







    # VNA.__SetBBalParam__(1, 1, 'SDD12')     # Doesn't seem to change to SDD12
    # VNA.__SetActiveFormat__(1, 'MLOG')
    # sdd12_mlog = meas()
    # print sdd12_mlog

startTime = time.time()

path = 'C:\\Users\\bsulliv2\\Desktop\\Pronghorn_Results\\VNA_Results\\'

date = time.ctime(time.time())
date = date.replace(':', '-')
fh = open(path + 'SParam_' + date + '.csv', 'w')

Zin_diff = 100
Zout_diff = 100
avg = 16

numPoints = 1000.0
startFreq = 10e6
endFreq = 10.01e9

measlist = ['SCC21 MLOG', 'SDC21 MLOG', 'SDD11 POL', 'SDD12 MLOG', 'SDD21 GDEL',
            'SDD21 MLOG', 'SDD21 POL', 'SDD11 MLOG', 'SDD22 MLOG']

templist = [25]
vcomlist = ['N/A']
dut = '3-5 CHB'

header()

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
Oven.__SetTemp__(25)
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

