import sys, visa, time
sys.path.append('../Common')
from ADI_GPIB.AgilentN5181A import *
from ADI_GPIB.AgilentN9030A import *

# Supply = E3631A(23)
Source1 = AgilentN5181A(20)
Source2 = AgilentN5181A(11)
Analyzer = AgilentN9030A(18)

date = time.ctime(time.time())
date = date.replace(':', '.')
fh = open('Intermod_Dist_' + date + '.csv', 'w')

freqlist = [100e6, 250e6, 500e6, 1e9, 4e9]
lowerPeak = []
higherPeak = []
lowCarrier = []
highCarrier = []

Analyzer.__SetSpan__(10e3)
for i in range(1):
    for freq in freqlist:
        # Set sources
        Source1.__SetState__(0)
        Source2.__SetState__(0)
        Source1.__SetFreq__(freq-1e6)
        Source2.__SetFreq__(freq+1e6)

        # Configure and measure low f Carrier
        Analyzer.__Setfc__(freq-1e6)
        Analyzer.__SetMarkerFreq__(1, freq-1e6)
        Source1.__SetState__(1)
        time.sleep(1)
        carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        while abs(carrierMag - -8) >= 0.1:
            sourceAmp = float(Source1.__GetAmp__())
            Source1.__SetAmp__(sourceAmp + (-8 - carrierMag))
            time.sleep(1)
            carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        # time.sleep(1)
        lowCarrier.append(float(Analyzer.__GetMarkerAmp__(1)))

        # Repeat for high f carrier
        Source1.__SetState__(0)
        Analyzer.__Setfc__(freq+1e6)
        Analyzer.__SetMarkerFreq__(1, freq+1e6)
        Source2.__SetState__(1)
        time.sleep(1)
        carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        while abs(carrierMag - -8) >= 0.1:
            sourceAmp = float(Source2.__GetAmp__())
            Source2.__SetAmp__(sourceAmp + (-8 - carrierMag))
            time.sleep(1)
            carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        # time.sleep(1)
        highCarrier.append(float(Analyzer.__GetMarkerAmp__(1)))

        Source1.__SetState__(1)
        # Measure IMD
        Analyzer.__Setfc__(freq-3e6)
        Analyzer.__SetMarkerFreq__(1, freq-3e6)
        # raw_input('Waiting...')
        time.sleep(1)
        lowerPeak.append(float(Analyzer.__GetMarkerAmp__(1)))
        Analyzer.__Setfc__(freq+3e6)
        Analyzer.__SetMarkerFreq__(1, freq+3e6)
        time.sleep(1)
        higherPeak.append(float(Analyzer.__GetMarkerAmp__(1)))


        # raw_input('Waiting...')

        leftNormal = []
        rightNormal = []
    for j in range(len(lowerPeak)):
        leftNormal.append(float(lowCarrier[j]) - float(lowerPeak[j]))
        rightNormal.append(float(highCarrier[j]) - float(higherPeak[j]))

    fh.write('Test %d' % i)
    fh.write('\n')
    fh.write('Frequency:,')
    fh.write(str(freqlist).strip('[]'))
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

    # print lowerPeak
    lowerPeak = []
    higherPeak = []
    lowCarrier = []
    highCarrier = []

