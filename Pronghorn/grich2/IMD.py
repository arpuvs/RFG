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

def IMD3():
    Analyzer.__SetSpan__(10e3)
    Analyzer.__SetAverage__(100)
    lowerPeak = []
    higherPeak = []
    lowCarrier = []
    highCarrier = []
    higherSourceAmp = []
    lowerSourceAmp = []
    supplyI = []

    for freq in freqlist:
        # Set sources
        Source1.__SetState__(0)
        Source2.__SetState__(0)
        Source1.__SetFreq__(freq - 1e6)
        Source2.__SetFreq__(freq + 1e6)

        # Configure and measure low f Carrier
        Analyzer.__Setfc__(freq - 1e6)
        Analyzer.__SetMarkerFreq__(1, freq - 1e6)
        Source1.__SetState__(1)
        Analyzer.__ClearAverage__()
        time.sleep(2)
        carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        while abs(carrierMag - -8) >= 0.1:
            sourceAmp = float(Source1.__GetAmp__())
            Source1.__SetAmp__(sourceAmp + (-8 - carrierMag))
            Analyzer.__ClearAverage__()
            time.sleep(2)
            carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        # time.sleep(1)
        lowCarrier.append(float(Analyzer.__GetMarkerAmp__(1)))
        lowerSourceAmp.append(float(Source1.__GetAmp__()))

        # Repeat for high f carrier
        Source1.__SetState__(0)
        Analyzer.__Setfc__(freq + 1e6)
        Analyzer.__SetMarkerFreq__(1, freq + 1e6)
        Source2.__SetState__(1)
        Analyzer.__ClearAverage__()
        time.sleep(2)
        carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        while abs(carrierMag - -8) >= 0.1:
            sourceAmp = float(Source2.__GetAmp__())
            Source2.__SetAmp__(sourceAmp + (-8 - carrierMag))
            Analyzer.__ClearAverage__()
            time.sleep(2)
            carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        # time.sleep(1)
        highCarrier.append(float(Analyzer.__GetMarkerAmp__(1)))
        higherSourceAmp.append(float(Source2.__GetAmp__()))

        # raw_input('Waiting...')
        Source1.__SetState__(1)
        # Measure IMD
        Analyzer.__Setfc__(freq - 3e6)
        Analyzer.__SetMarkerFreq__(1, freq - 3e6)
        # raw_input('Waiting...')
        Analyzer.__ClearAverage__()
        time.sleep(2)
        lowerPeak.append(float(Analyzer.__GetMarkerAmp__(1)))
        Analyzer.__Setfc__(freq + 3e6)
        Analyzer.__SetMarkerFreq__(1, freq + 3e6)
        Analyzer.__ClearAverage__()
        time.sleep(2)
        higherPeak.append(float(Analyzer.__GetMarkerAmp__(1)))
        supplyI.append(float(Supply.__GetI__(1)))

        # raw_input('Waiting...')

        leftNormal = []
        rightNormal = []
    for j in range(len(lowerPeak)):
        leftNormal.append(-(float(lowCarrier[j]) - float(lowerPeak[j])))
        rightNormal.append(-(float(highCarrier[j]) - float(higherPeak[j])))



    fh.write('Test %d' % i)
    fh.write('\n')
    fh.write('Frequency:,')
    fh.write(str(freqlist).strip('[]'))
    fh.write('\n')
    fh.write('Supply Current:,')
    fh.write(str(supplyI).strip('[]'))
    fh.write('\n')
    fh.write('Low left:,')
    fh.write(str(lowerPeak).strip('[]'))
    fh.write('\n')
    fh.write('Low right:,')
    fh.write(str(higherPeak).strip('[]'))
    fh.write('\n')
    fh.write('High left:,')
    fh.write(str(highCarrier).strip('[]'))
    fh.write('\n')
    fh.write('High right:,')
    fh.write(str(lowCarrier).strip('[]'))
    fh.write('\n')
    fh.write('Left dBc:,')
    fh.write(str(leftNormal).strip('[]'))
    fh.write('\n')
    fh.write('Right dBc:,')
    fh.write(str(rightNormal).strip('[]'))
    fh.write('\n')
    print leftNormal

    # print lowerPeak

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
    channel = 'B'
    header = (dut, date, test, equipment, supplyV, supplyI, balun, channel)
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
    time.sleep(300)
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

Oven.__SetTemp__(25)
print (time.time()-startTime)
fh.write('Execution time (s) = %g' % (time.time() - startTime))

