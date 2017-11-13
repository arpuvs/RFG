# Incorporating structure from ADL5569_VNA_Automation Vee file
import sys, visa, time, math, cmath
sys.path.append('../../Common')

from ADI_GPIB.AgilentE5071C import *
from ADI_GPIB.E3631A import *
VNA = AgilentE5071C(17)
# Oven = WatlowF4(999999999)
Supply = E3631A(10)


def VNAinit():
    VNA.__SetSweepType(1, 'LOG')
    VNA.__SetStartf__(1, 10e06)
    VNA.__SetStopf__(1, 10.01e09)
    VNA.__SetNumPoints__(1, 1e3)
    VNA.__SetAvg__(1, 16)
    VNA.__SetAutoTime__(1, True)
    VNA.__SetTrigType__('MAN')
    VNA.__SetContinuous__(1, False)
    VNA.__EnableAvg(1, True)
    VNA.__EnableTrigAvg__(True)


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
    VNA.__InitMeas__(1)
    VNA.__SingleTrig__()
    status = 0
    while status == 0:
        status = VNA.__CheckStatus__()
        time.sleep(0.1)
    ans = VNA.__GetData__(1)
    ans = ans.split(',')
    magans = []
    imagans = []
    for val in range(len(ans)):
        if (val % 2) == 0:
            magans.append(float(ans[val]))
        else:
            imagans.append(float(ans[val]))

    compans = []
    for val in range(len(magans)):
        compans.append(magans[val] + imagans[val] * 1j)

    # return compans
    return magans, imagans


def build_av(mlog):
    ans = []
    for val in range(len(mlog)):
        ans.append(mlog[val] - 10.0*math.log10(Zout_diff/Zin_diff))
    return ans


def build_cmrr(sdd21, sdc21):
    ans = []
    for val in range(len(sdd21)):
        ans.append(sdd21[val] - sdc21[va])
    return ans


def build_gdel(phase, freq):
    ans = []
    ans[0] = 0
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
    # Scc21
    VNA.__SetActiveTrace__(1, 1)
    VNA.__SetBBalParam__(1, 1, 'SCC21')
    VNA.__SetActiveFormat__(1, 'MLOG')
    scc21_mlog = meas()

    VNA.__SetBBalParam__(1, 1, 'SDC21')
    sdc21_mlog = meas()

    VNA.__SetBBalParam__(1, 1, 'SDD11')
    VNA.__SetActiveFormat__(1, 'POL')
    sdd11_pol = meas()

    VNA.__SetBBalParam__(1, 1, 'SDD12')
    VNA.__SetActiveFormat__(1, 'MLOG')
    sdd12_mlog = meas()

    VNA.__SetBBalParam__(1, 1, 'SDD21')
    VNA.__SetActiveFormat__(1, 'GDEL')
    sdd21_gdel = meas()

    VNA.__SetBBalParam__(1, 1, 'SDD21')
    VNA.__SetActiveFormat__(1, 'MLOG')
    sdd21_mlog = meas()

    VNA.__SetBBalParam__(1, 1, 'SDD22')
    VNA.__SetActiveFormat__(1, 'POL')
    sdd21_pol = meas()

    av = build_av(sdd21_mlog[1])
    cmrr1 = build_cmrr(sdd21_mlog[1], sdc21_mlog[1])
    cmrr2 = build_cmrr(sdd21_mlog[1], scc21_mlog[1])
    group_delay = build_gdel(sdd21_pol[1], freqlist)
    s12_v = build_av(sdd12_mlog[1])
    zyIn = build_zy(sdd11_mlog)
    zyOut = build_zy(sdd22_mlog)




Zin_diff = 100
Zout_diff = 100

freqlist = []
freqlist.append(10e6)
for i in (range(1e3) -1):
    freqlist.append(freqlist[i] + 10e6)

getData()

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

