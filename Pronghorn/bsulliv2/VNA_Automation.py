# Incorporating structure from ADL5569_VNA_Automation Vee file
import sys, visa, time
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


def getData():
    # Scc21
    VNA.__SetActiveTrace__(1, 1)
    VNA.__SetBBalParam__(1, 1, 'SCC21')
    VNA.__SetActiveFormat__(1, 'MLOG')
    VNA.__InitMeas__(1)
    VNA.__SingleTrig__()
    status = 0
    while status == 0:
        status = VNA.__CheckStatus__()
        time.sleep(0.1)
    Scc21 = VNA.__GetData__(1)


supplies = [5.0]
temps = [25]
currents = []

VNAinit()
for temp in temps:
    # setTemp(temp)
    for supply in supplies:
        # setSupply()
        supply.__SetP6V__(supply)
        supply.__SetP25V__(3.3)
        currents.append(float(supply.__MeasP6I__()))

        getData()

