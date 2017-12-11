# Author: Ben Sullivan
# Date: 10/27/2017

# Module and instrument imports
import sys, visa, time
sys.path.append('../../Common')
from ADI_GPIB.AgilentN5181A import *
from ADI_GPIB.AgilentN9030A import *
from ADI_GPIB.AgilentN6705B import *
from ADI_GPIB.WatlowF4 import *

# Instrument initialization
Supply = AgilentN6705B(26)
Source1 = AgilentN5181A(20)
Source2 = AgilentN5181A(11)
Analyzer = AgilentN9030A(18)
Oven = WatlowF4(4)
startTime = time.time()

def IMD3main(path, freqlist, vcomlist, templist, dut, attnList):
    # Main IMD measurement program
    def IMD3(freq):
        # Initializes spectrum analyzer for measurements
        Analyzer.__SetSpan__(10e3)
        Analyzer.__SetAverage__(50)
        Analyzer.__SetAutoAtten__(0)
        Analyzer.__SetAtten__(6)

        # Initializes arrays
        lowerPeak = []
        higherPeak = []
        lowCarrier = []
        highCarrier = []
        higherSourceAmp = []
        lowerSourceAmp = []
        supplyI = []


        # for freq in freqList:
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
        Analyzer.__CheckStatus__(300)   # Waits for averaging
        carrierMag = float(Analyzer.__GetMarkerAmp__(1))  # Measures initial amplitude
        while abs(carrierMag - -8) >= 0.1:  # Adjusts until carrier mag is within 0.1dBm of desired amplitude
            sourceAmp = float(Source1.__GetAmp__())     # Gets amplitude
            setAmp = sourceAmp + (-8 - carrierMag)      # Adjusts amplitude
            if setAmp >= 15:    # Raises flag if max amplitude exceeded
                raise Exception('Amplitude too high, check configuration')
            Source1.__SetAmp__(setAmp)      # Sets new amplitude
            Analyzer.__ClearAverage__()
            Analyzer.__CheckStatus__(300)
            carrierMag = float(Analyzer.__GetMarkerAmp__(1))    # Gets new amplitude

        # Records measured source and carrier values
        lowCarrier.append(float(Analyzer.__GetMarkerAmp__(1)))
        lowerSourceAmp.append(float(Source1.__GetAmp__()))

        # Repeat for high f carrier - same process as above
        Source1.__SetState__(0)
        Analyzer.__Setfc__(freq + 1e6)
        Analyzer.__SetMarkerFreq__(1, freq + 1e6)
        Source2.__SetState__(1)
        Analyzer.__ClearAverage__()
        Analyzer.__CheckStatus__(300)
        carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        while abs(carrierMag - -8) >= 0.1:
            sourceAmp = float(Source2.__GetAmp__())
            setAmp = sourceAmp + (-8 - carrierMag)
            if setAmp >= 15:
                raise Exception('Amplitude too high, check configuration')
            Source2.__SetAmp__(setAmp)
            Analyzer.__ClearAverage__()
            Analyzer.__CheckStatus__(300)
            carrierMag = float(Analyzer.__GetMarkerAmp__(1))
        highCarrier.append(float(Analyzer.__GetMarkerAmp__(1)))
        higherSourceAmp.append(float(Source2.__GetAmp__()))

        for attn in attnList:
            Analyzer.__SetAtten__(attn)
            # Measure lower IMD3
            Source1.__SetState__(1)
            Analyzer.__Setfc__(freq - 3e6)
            Analyzer.__SetMarkerFreq__(1, freq - 3e6)
            # raw_input('Waiting...')
            Analyzer.__ClearAverage__()
            Analyzer.__CheckStatus__(300)
            lowerPeak.append(float(Analyzer.__GetMarkerAmp__(1)))

            # Measure higher IMD3
            Analyzer.__Setfc__(freq + 3e6)
            Analyzer.__SetMarkerFreq__(1, freq + 3e6)
            Analyzer.__ClearAverage__()
            Analyzer.__CheckStatus__(300)
            higherPeak.append(float(Analyzer.__GetMarkerAmp__(1)))
            supplyI.append(float(Supply.__GetI__(1)))

        leftNormal = []
        rightNormal = []
        # Converts dBm measurements to dBc
        for j in range(len(lowerPeak)):
            leftNormal.append(-(float(lowCarrier[0]) - float(lowerPeak[j])))
            rightNormal.append(-(float(highCarrier[0]) - float(higherPeak[j])))


        # Writes all results to output file
        # fh.write('Test %d' % i)
        # fh.write('\n')
        fh.write('Frequency:,')
        fh.write(str(freq).strip('[]'))
        fh.write('\n')
        fh.write('Attenuation Setting:,')
        fh.write(str(attnList).strip('[]'))   # Only thing added so far - printing out all attn readings at all freqs
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

        # Print first line of file
    def header():
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

    # Sets oven temperature to setpoint and soaks DUT
    def setTemp(setpoint):
        Oven.__SetTemp__(setpoint)
        current = float(Oven.__GetTemp__())
        while (abs(current - setpoint) > 2):
            time.sleep(1)
            current = float(Oven.__GetTemp__())
        print '@ Temp %d' % setpoint
        soak = 300
        time.sleep(soak)
        return True

    # Initializes and opens output file
    date = time.ctime(time.time())
    date = date.replace(':', '-')
    fh = open(path + 'Intermod_Dist_' + date + '.csv', 'w')

    header()    # Prints first line of file

    # Configure supplies
    # Vsupply = Ch1, Ven = Ch2, Vcom = Ch3
    Supply.__SetV__(5, 1)
    Supply.__SetI__(0.25, 1)


    # balunList = ('standard', 'input flipped', 'both flipped', 'output flipped')
    # balunList = ('S')
    for temp in templist:
    # for balun in balunList:
        if templist != [25]:
            setTemp(temp)
        # fh.write('Balun config = %s' % balun)
        fh.write('Temp = %d' % temp)
        fh.write('\n')
        for vcom in vcomlist:
            Supply.__SetV__(vcom, 3)  # Sets DUT to common mode voltage

            Source1.__SetState__(0)
            Source2.__SetState__(0)
            print 'Aligning...'
            Analyzer.__CheckStatus__(300)
            Analyzer.__Align__()  # Aligns device with no input
            Analyzer.__CheckStatus__(300)
            print 'Done'

            print 'Vcom = %g' % vcom
            fh.write('Vcom = %g\n' % vcom)
            # raw_input('Configure Bal uns to : %s' % balun)
            #     for i in range(1):
            for freq in freqlist:
                IMD3(freq)  # Runs main IMD measurements

    # Final clean up actions
    if templist != [25]:
        Oven.__SetTemp__(25)
    print (time.time()-startTime)
    fh.write('Execution time (s) = %g' % (time.time() - startTime))

if __name__ == '__main__':
    path = 'C:\\Users\\bsulliv2\\Desktop\\Pronghorn_Results\\IMD3\\'
    freqs = [100e6, 250e6, 500e6, 1.0e9, 1.5e9, 2.0e9, 2.5e9, 3.0e9, 3.5e9, 4.0e9, 4.5e9, 5.0e9, 5.5e9, 5.9e9]
    attns = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26]
    # freqs = [6e9]
    # vcoms = []
    # for i in range(20, 31):
    #     vcoms.append(i/10.0)
    # vcoms = [2.0, 2.5, 3.0]
    vcoms = [2.5]
    # temps = [25, 85, -40]
    temps = [25]
    dut = '4-3'

    IMD3main(path, freqs, vcoms, temps, dut, attns)  # Calls main program

