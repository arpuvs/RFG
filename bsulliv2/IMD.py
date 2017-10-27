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

Analyzer.__SetSpan__(10e3)
for i in range(11):
    for freq in freqlist:
        Source1.__SetFreq__(freq-1e6)
        Source2.__SetFreq__(freq+1e6)
        Analyzer.__Setfc__(freq-3e6)
        Analyzer.__SetMarkerFreq__(1, freq-3e6)
        time.sleep(1)
        lowerPeak.append(float(Analyzer.__GetMarkerAmp__(1)))
        Analyzer.__Setfc__(freq+3e6)
        Analyzer.__SetMarkerFreq__(1, freq+3e6)
        time.sleep(1)
        higherPeak.append(float(Analyzer.__GetMarkerAmp__(1)))


    fh.write('Test %d' % i)
    fh.write('\n')
    fh.write(str(freqlist).strip('[]'))
    fh.write('\n')
    fh.write(str(lowerPeak).strip('[]'))
    fh.write('\n')
    fh.write(str(higherPeak).strip('[]'))
    fh.write('\n')

    print lowerPeak
    lowerPeak = []
    higherPeak = []

