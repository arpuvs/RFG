# Author: Ben Sullivan
# Date: 11/06/2017

# Necessary module and instrument imports
import sys, visa, time
sys.path.append('../../../Common')
sys.path.append('../../../Common/FMB_USB_Python_Files')
from ADI_GPIB.AgilentN5181A import *
from ADI_GPIB.AgilentN9030A import *
from ADI_GPIB.AgilentN6705B import *
from ADI_GPIB.WatlowF4 import *
from FMB import *

# Instrument initialization
Supply = AgilentN6705B(26)
# Source = AgilentN5181A(20)
Source = AgilentN5181A(11)
Analyzer = AgilentN9030A(18)
Oven = WatlowF4(4)
startTime = time.time()
# Filter = FMB('COM3', fmbDict)

# Main body of code, called by GUI
def HD23Main(path, freqlist, vcomlist, templist, dutNumber):

    def HD23():  # Main HD23 measurement function
        # Initializes analyzer
        Analyzer.__SetSpan__(10e3)
        Analyzer.__SetAverage__(100)

        # Initializes all measurement arrays
        fundamental = []
        second = []
        third = []
        Carrier = []
        SourceAmp = []
        secondNormal = []
        thirdNormal = []
        supplyI = []
        freqlistReal = []

        for freqindex in freqlist:
            # Converts fmb dict frequency to float
            freq = fmbDict[freqindex].split()
            if freq[1] == 'MHz':
                freq = float(freq[0]) * 1e6
            elif freq[1] == 'GHz':
                freq = float(freq[0]) * 1e9
            # print val
            freqlistReal.append(freq)

            # Sets up all equipment for given frequency
            Source.__SetFreq__(freq)
            Analyzer.__Setfc__(freq)
            Analyzer.__SetMarkerFreq__(1, freq)
            Source.__SetState__(1)
            Filter.select_filter(freqindex)
            time.sleep(0.1)
            Analyzer.__ClearAverage__()

            # Sets initial amplitude using measured output of dut
            Analyzer.__CheckStatus__(300)                     # Waits until averaging is complete
            carrierMag = float(Analyzer.__GetMarkerAmp__(1))  # Gets initial amplitude
            while abs(carrierMag - -2) >= 0.1:                # Adjusts amplitude until it is within 0.1 dBm of desired
                sourceAmp = float(Source.__GetAmp__())
                setAmp = sourceAmp + (-2 - carrierMag)
                if setAmp > 20:
                    raise Exception('Max source amplitude exceeded')
                Source.__SetAmp__(setAmp)
                Analyzer.__ClearAverage__()
                Analyzer.__CheckStatus__(300)
                carrierMag = float(Analyzer.__GetMarkerAmp__(1))

            # Gets final amplitude
            Carrier.append(float(Analyzer.__GetMarkerAmp__(1)))
            SourceAmp.append(float(Source.__GetAmp__()))

            # Makes fundamental, second and third harmonic measurements
            Analyzer.__Setfc__(freq)
            Analyzer.__SetMarkerFreq__(1, freq)
            Analyzer.__ClearAverage__()
            Analyzer.__CheckStatus__(300)
            fundamental.append(float(Analyzer.__GetMarkerAmp__(1)))
            Analyzer.__Setfc__(freq*2.0)
            Analyzer.__SetMarkerFreq__(1, freq*2.0)
            Analyzer.__ClearAverage__()
            Analyzer.__CheckStatus__(300)
            second.append(float(Analyzer.__GetMarkerAmp__(1)))
            Analyzer.__Setfc__(freq*3.0)
            Analyzer.__SetMarkerFreq__(1, freq*3.0)
            Analyzer.__ClearAverage__()
            Analyzer.__CheckStatus__(300)
            third.append(float(Analyzer.__GetMarkerAmp__(1)))
            supplyI.append(float(Supply.__GetI__(1)))

        # Converts dBm measurements to dBc
        for j in range(len(second)):
            secondNormal.append(-(float(Carrier[j]) - float(second[j])))
            thirdNormal.append(-(float(Carrier[j]) - float(third[j])))

        # Writes all measured parameters to file
        fh.write('Frequency:,')
        fh.write(str(freqlistReal).strip('[]'))
        fh.write('\n')
        fh.write('Supply Current:,')
        fh.write(str(supplyI).strip('[]'))
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

    # P3dB function. May remain unused if measurement is easier with the PNX.
    # Probably needs to be modified to actually use.
    def P3dB(freq):
        Analyzer.__SetSpan__(10e3)
        Analyzer.__SetAverage__(50)
        Analyzer.__Setfc__(freq)
        Analyzer.__SetMarkerFreq__(1, freq)
        Source.__SetFreq__(freq)
        sourceAmp = -20
        Source.__SetAmp__(sourceAmp)
        Source.__SetState__(1)
        # time.sleep(3)
        outAmp = float(Source.__GetAmp__())
        time.sleep(1)
        if freq > 4.0e9:
            time.sleep(4)
        Analyzer.__ClearAverage__()
        Analyzer.__CheckStatus__(300)
        dutAmp = float(Analyzer.__GetMarkerAmp__(1))
        gain = outAmp - dutAmp
        print outAmp
        print dutAmp
        print 'Initial gain = %g' % gain
        initGain = gain
        inc = 5
        print 'Inc = %d' % inc
        while abs(gain - initGain) <= 1.0:
            sourceAmp = sourceAmp + inc
            # Source.__SetFreq__(freq)
            # sourceAmp = -20
            Source.__SetAmp__(sourceAmp)
            # Source.__SetState__(1)
            time.sleep(1)
            amp = float(Source.__GetAmp__())
            Analyzer.__ClearAverage__()
            Analyzer.__CheckStatus__(300)
            dutAmp = float(Analyzer.__GetMarkerAmp__(1))
            gain = amp - dutAmp
            print 'Difference = %g' % abs(gain - initGain)
            print sourceAmp
            if sourceAmp >= 20:
                raise Exception('Amplitude too high, check configuration')

        sourceAmp = sourceAmp - (inc + 1)
        # print sourceAmp
        inc = 1
        gain = initGain
        print 'Inc = %d' % inc
        while abs(gain - initGain) <= 1.0:
            sourceAmp = sourceAmp + inc
            # Source.__SetFreq__(freq)
            # sourceAmp = -20
            Source.__SetAmp__(sourceAmp)
            # Source.__SetState__(1)
            time.sleep(1)
            amp = float(Source.__GetAmp__())
            Analyzer.__ClearAverage__()
            Analyzer.__CheckStatus__(300)
            dutAmp = float(Analyzer.__GetMarkerAmp__(1))
            gain = amp - dutAmp
            print 'Difference = %g' % abs(gain - initGain)
            print sourceAmp
            if sourceAmp >= 15:
                raise Exception('Amplitude too high, check configuration')

        sourceAmp = sourceAmp - (inc + 0.2)
        inc = 0.2
        print 'Inc = %g' % inc
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
            Analyzer.__CheckStatus__(300)
            dutAmp = float(Analyzer.__GetMarkerAmp__(1))
            gain = amp - dutAmp
            print 'Difference = %g' % abs(gain - initGain)
            print sourceAmp
            if sourceAmp >= 15:
                raise Exception('Amplitude too high, check configuration')

        # fh.write(amp)
        return amp

    # Prints first line of file
    def header(dut):
        test = 'HD23'
        equipment = 'N6705B N5181A N9030A BAL0026 6'
        # supplyV = Supply.__MeasP25V__()
        supplyV = float(Supply.__GetV__(1))
        print 'Supply V = %g' % supplyV
        # supplyI = Supply.__MeasP25I__()
        supplyI = float(Supply.__GetI__(1))
        print 'Supply I = %g' % supplyI
        balun = 'INB: 0-VIN OUTB 0-VOP'
        header = (dut, date, test, equipment, supplyV, supplyI, balun)
        header = str(header).strip('()')
        fh.write(header)
        fh.write('\n')

    # Sets oven to setpoint and soaks dut for allotted time
    def setTemp(setpoint):
        Oven.__SetTemp__(setpoint)
        current = float(Oven.__GetTemp__())
        while (abs(current - setpoint) > 2):
            time.sleep(1)
            current = float(Oven.__GetTemp__())
        print '@ Temp %d' % setpoint
        # if temp != 25:
        soak = 300
        time.sleep(soak)
        return True

    # Filter box frequency settings dictionary
    fmbDict = {1: "2.5 MHz", 2: "5 MHz", 3: "33 MHz", 4: "78 MHz",
              5: "120 MHz", 6: "225.3 MHz", 7: "350.3 MHz", 8: "500 MHz",
              9: "800.3 MHz", 10: "1 GHz", 11: "1.5 GHz", 12: "2 GHz",
              13: "2.5 GHz", 14: "3 GHz", 15: "3.5 GHz", 16: "4 GHz",
              17: "4.5 GHz", 18: "5 GHz", 19: "5.5 GHz", 20: "5.9 GHz",
              21: "Aux"}

    Filter = FMB('COM3', fmbDict)  # Initializes filter box

    # Creates and opens output file
    date = time.ctime(time.time())
    date = date.replace(':', '.')
    # fh = open('P3dB' + date + '.csv', 'w')
    fh = open(path + 'HD23' + date + '.csv', 'w')

    header(dutNumber)  # Prints header line

    # Sets up main supply
    # Vsupply = Ch1, Ven = Ch2, Vcom = Ch3
    Supply.__SetV__(5, 1)
    Supply.__SetI__(0.25, 1)


    # balunList = ('standard', 'input flipped', 'both flipped', 'output flipped')
    # balunList = ('S')
    for temp in templist:
        setTemp(temp)                       # Sets DUT to temperature
        fh.write('Temp = %d' % temp)
        fh.write('\n')
        for vcom in vcomlist:
            Supply.__SetV__(vcom, 3)        # Sets DUT to common mode voltage
            print 'Vcom = %g' % vcom
            fh.write('Vcom = %g\n' % vcom)
            HD23()                          # Runs main HD23 measurement

    # Returns oven to ambient temp, finds execution time and closes file
    setTemp(25)
    print time.time()-startTime
    fh.write('Execution time (s) = %g' % (time.time() - startTime))
    fh.close()


# Called if program run by itself
if __name__ == '__main__':
    # Sets all necessary variables
    path = 'C:\\Users\\bsulliv2\\Desktop\\Pronghorn_Results\\HD23\\'
    # freqlist = [100e6, 250e6, 500e6, 1.0e9, 1.5e9, 2.0e9, 2.5e9, 3.0e9, 3.5e9, 4.0e9]
    # freqs = [5, 6, 8, 10, 11, 12, 13, 14, 15, 16]
    freqs = [12]
    # vcoms = []
    # for i in range(20, 31):
    #     vcoms.append(i/10.0)
    # vcoms = [2.0, 2.5, 3.0]
    vcoms = [2.5]
    # temps = [25, 85, -40]
    temps = [25]
    dut = 0

    HD23Main(path, freqs, vcoms, temps, dut)  # Calls main program