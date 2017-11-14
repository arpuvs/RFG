import sys, visa, time
sys.path.append('../Common')
from ADI_GPIB.AgilentN5181A import *
from ADI_GPIB.AgilentN9030A import *
from ADI_GPIB.AgilentN6705B import *
from ADI_GPIB.WatlowF4 import *

Supply = AgilentN6705B(26)
# Source1 = AgilentN5181A(20)
Source = AgilentN5181A(11)
Analyzer = AgilentN9030A(18)
Oven = WatlowF4(4)
startTime = time.time()




def HD23():
    Analyzer.__SetSpan__(10e3)
    Analyzer.__SetAverage__(100)
    fundamental = []
    second = []
    third = []
    Carrier = []
    SourceAmp = []
    secondNormal = []
    thirdNormal = []
    supplyI = []


    for freq in freqlist:
        Source.__SetFreq__(freq)
        Analyzer.__Setfc__(freq)
        Analyzer.__SetMarkerFreq__(1, freq)
        Source.__SetState__(1)
        Analyzer.__ClearAverage__()
        time.sleep(2)
        carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        while abs(carrierMag - -4) >= 0.1:
            sourceAmp = float(Source.__GetAmp__())
            Source.__SetAmp__(sourceAmp + (-4 - carrierMag))
            Analyzer.__ClearAverage__()
            time.sleep(2)
            carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        # time.sleep(1)
        Carrier.append(float(Analyzer.__GetMarkerAmp__(1)))
        SourceAmp.append(float(Source.__GetAmp__()))

        Analyzer.__Setfc__(freq)
        Analyzer.__SetMarkerFreq__(1, freq)
        Analyzer.__ClearAverage__()
        time.sleep(2)
        fundamental.append(float(Analyzer.__GetMarkerAmp__(1)))
        Analyzer.__Setfc__(freq*2.0)
        Analyzer.__SetMarkerFreq__(1, freq*2.0)
        Analyzer.__ClearAverage__()
        time.sleep(2)
        second.append(float(Analyzer.__GetMarkerAmp__(1)))
        Analyzer.__Setfc__(freq*3.0)
        Analyzer.__SetMarkerFreq__(1, freq*3.0)
        Analyzer.__ClearAverage__()
        time.sleep(2)
        third.append(float(Analyzer.__GetMarkerAmp__(1)))
        supplyI.append(float(Supply.__GetI__(1)))

    for j in range(len(second)):
        secondNormal.append(-(float(Carrier[j]) - float(second[j])))
        thirdNormal.append(-(float(Carrier[j]) - float(third[j])))

    fh.write('Test %d' % i)
    fh.write('\n')
    fh.write('Frequency:,')
    fh.write(str(freqlist).strip('[]'))
    fh.write('\n')
    fh.write('Supply Current:,')
    fh.write(str(freqlist).strip('[]'))
    fh.write('\n')
    fh.write('Carrier:,')
    fh.write(str(Carrier).strip('[]'))
    fh.write('\n')
    fh.write('Second:,')
    fh.write(str(second).strip('[]'))
    fh.write('\n')
    fh.write('Third:,')
    fh.write(str(third).strip('[]'))
    fh.write('\n')
    fh.write('Second dBc:,')
    fh.write(str(secondNormal).strip('[]'))
    fh.write('\n')
    fh.write('Third dBc:,')
    fh.write(str(thirdNormal).strip('[]'))
    fh.write('\n')

def P3dB(freq):
    Analyzer.__SetSpan__(10e3)
    Analyzer.__SetAverage__(100)
    Analyzer.__Setfc__(freq)
    Analyzer.__SetMarkerFreq__(1, freq)
    Source.__SetFreq__(freq)
    sourceAmp = -20
    Source.__SetAmp__(sourceAmp)
    Source.__SetState__(1)
    # time.sleep(3)
    outAmp = float(Source.__GetAmp__())
    Analyzer.__ClearAverage__()
    time.sleep(2)
    dutAmp = float(Analyzer.__GetMarkerAmp__(1))
    gain = outAmp - dutAmp
    print 'Initial gain = %g' % gain
    initGain = gain
    inc = 5
    print inc
    while abs(gain - initGain) <= 1.0:
        sourceAmp = sourceAmp + inc
        # Source.__SetFreq__(freq)
        # sourceAmp = -20
        Source.__SetAmp__(sourceAmp)
        # Source.__SetState__(1)
        time.sleep(1)
        amp = float(Source.__GetAmp__())
        Analyzer.__ClearAverage__()
        time.sleep(2)
        dutAmp = float(Analyzer.__GetMarkerAmp__(1))
        gain = amp - dutAmp
        print 'Difference = %g' % abs(gain - initGain)
        print sourceAmp
        if sourceAmp >= 15:
            raise Exception('Amplitude too high, check configuration')

    sourceAmp = sourceAmp - (2*inc + 1)
    print sourceAmp
    inc = 1
    gain = initGain
    print inc
    while abs(gain - initGain) <= 1.0:
        sourceAmp = sourceAmp + inc
        # Source.__SetFreq__(freq)
        # sourceAmp = -20
        Source.__SetAmp__(sourceAmp)
        # Source.__SetState__(1)
        time.sleep(1)
        amp = float(Source.__GetAmp__())
        Analyzer.__ClearAverage__()
        time.sleep(2)
        dutAmp = float(Analyzer.__GetMarkerAmp__(1))
        gain = amp - dutAmp
        print 'Difference = %g' % abs(gain - initGain)
        if sourceAmp >= 15:
            raise Exception('Amplitude too high, check configuration')

    sourceAmp = sourceAmp - (inc + 0.2)
    inc = 0.2
    print inc
    gain = initGain
    while abs(gain - initGain) <= 1.0:
        sourceAmp = sourceAmp + inc
        # Source.__SetFreq__(freq)
        # sourceAmp = -20
        Source.__SetAmp__(sourceAmp)
        # Source.__SetState__(1)
        time.sleep(1)
        amp = float(Source.__GetAmp__())
        Analyzer.__ClearAverage__()
        time.sleep(2)
        dutAmp = float(Analyzer.__GetMarkerAmp__(1))
        gain = amp - dutAmp
        print 'Difference = %g' % abs(gain - initGain)
        if sourceAmp >= 15:
            raise Exception('Amplitude too high, check configuration')

    # fh.write(amp)
    return amp


def header():
    dut = '3-4'
    test = 'P3dB'
    equipment = 'N6705B N5181A N9030A BAL0026 6'
    # supplyV = Supply.__MeasP25V__()
    supplyV = float(Supply.__GetV__(1))
    print supplyV
    # supplyI = Supply.__MeasP25I__()
    supplyI = float(Supply.__GetI__(1))
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
fh = open('P3dB' + date + '.csv', 'w')
header()
freqlist = [100e6, 250e6, 500e6, 1e9, 1.5e9, 2e9, 2.5e9, 3e9, 3.5e9, 4e9]
templist = [25, 85, -40]



# Vsupply = Ch1, Ven = Ch2, Vcom = Ch3
Supply.__SetV__(5, 1)
Supply.__SetI__(0.25, 1)


# balunList = ('standard', 'input flipped', 'both flipped', 'output flipped')
# balunList = ('S')
# for temp in templist:
# for balun in balunList:
#     setTemp(temp)
#     fh.write('Balun config = %s' % balun)
# fh.write('Temp = %d' % temp)
# fh.write('\n')
# raw_input('Configure Bal uns to : %s' % balun)
for i in range(3):
    fh.write('Test %d\n' % i)
    for freq in freqlist:
    # HD23()
        val = float(P3dB(freq))
        fh.write('%g, %g, \n' % (freq, val))
# setTemp(25)
print time.time()-startTime
fh.write('Execution time (s) = %g' % (time.time() - startTime))

