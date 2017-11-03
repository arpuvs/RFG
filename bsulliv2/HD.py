import sys, visa, time
sys.path.append('../Common')
from ADI_GPIB.AgilentN5181A import *
from ADI_GPIB.AgilentN9030A import *
from ADI_GPIB.AgilentN6705B import *
from ADI_GPIB.WatlowF4 import *

Supply = AgilentN6705B(26)
Source1 = AgilentN5181A(20)
Source2 = AgilentN5181A(11)
Analyzer = AgilentN9030A(18)
Oven = WatlowF4(4)
startTime = time.time()




def HD23():
    

def header():
    dut = '3-4'
    test = 'IMD3'
    equipment = 'N5181A N9030A BAL0026 BAL006'
    # supplyV = Supply.__MeasP25V__()
    supplyV = 'Temp'
    print supplyV
    # supplyI = Supply.__MeasP25I__()
    supplyI = 'Temp'
    print supplyI
    balun = 'INB: 0-VIN OUTB 0-VOP'
    header = (dut, date, test, equipment, supplyV, supplyI, balun)
    header = str(header).strip('()')
    fh.write(header)
    fh.write('\n')


def setTemp(setpoint):
    Oven.__SetTemp__(setpoint)
    current = float(Oven.__GetTemp__())
    while (abs(current - setpoint) > 2):
        time.sleep(1)
        current = float(Oven.__GetTemp__())
    print '@ Temp %d' % setpoint
    # if temp != 25:
    time.sleep(330)
    return True


date = time.ctime(time.time())
date = date.replace(':', '.')
fh = open('Intermod_Dist_' + date + '.csv', 'w')
header()
freqlist = [100e6, 250e6, 500e6, 1e9, 1.5e9, 2e9, 2.5e9, 3e9, 3.5e9, 4e9]
templist = [25, 85, -40]
lowerPeak = []
higherPeak = []
lowCarrier = []
highCarrier = []
higherSourceAmp = []
lowerSourceAmp = []


# Vsupply = Ch1, Ven = Ch2, Vcom = Ch3
Supply.__SetV__(5,1)
Supply.__SetI__(0.25,1)


# balunList = ('standard', 'input flipped', 'both flipped', 'output flipped')
# balunList = ('S')
for temp in templist:
# for balun in balunList:
    setTemp(temp)
    # fh.write('Balun config = %s' % balun)
    fh.write('Temp = %d' % temp)
    fh.write('\n')
    # raw_input('Configure Bal uns to : %s' % balun)
    for i in range(1):
        IMD3()

setTemp(25)
print time.time()-startTime()
fh.write('Execution time (s) = %g' % (time.time() - startTime))

