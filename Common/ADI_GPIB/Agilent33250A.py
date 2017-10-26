#---------------------------------------------------------------------------------
# Name:        Agilent33250A.py
#
# Purpose:     Driver for the Agilent 33250A arbitrary waveform generator.
#              Functions are created primarily for pulse generation at this time.
#
# Author:      Dave Shoudy
#
# Created:     2007/10/08
#---------------------------------------------------------------------------------

from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class Agilent33250A(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        GPIBObjectBaseClass.__init__(self, 'Agilent Technologies,33250A', addr)
    
    def __SetupPulse__(self, width=100e-6, magnitude=3.3, offset=1.65):
        self.instr.write('OUTPUT OFF')                  # Output off
        self.instr.write('OUTP:LOAD 50')                # 50 Ohm output load
        self.instr.write('FUNC PULS')                   # Select pulse mode
        self.instr.write('VOLT %s' %str(magnitude))     # Set Vpp of the pulse
        self.instr.write('VOLT:OFFS %s' %str(offset))   # Set the offset voltage
        self.instr.write('VOLT:UNIT VPP')               # Voltage units of Vpp
        self.instr.write('OUTP:POL NORM')               # Normal output polarity
        self.instr.write('OUTP:SYNC OFF')               # Disable the SYNC connector
        self.instr.write('PULSE:PER MAX')               # Use maximum period of 2000s (another way to ensure only one pulse)
        self.instr.write('PULSE:TRAN MIN')              # Minimum edge transition time
        self.instr.write('PULSE:WIDTH %s' %str(width))  # Set pulse width
        self.instr.write('BURST:MODE TRIG')             # Set up triggering for burst mode
        self.instr.write('BURST:NCYC 1')                # Apply only 1 pulse
        self.instr.write('TRIG:SOUR BUS')               # Trigger from software (BUS)
        self.instr.write('TRIG:DELAY 0')                # No delay between trigger and output of pulse
        self.instr.write('BURS:STAT ON')                # Enable burst mode
        self.instr.write('OUTPUT ON')                   # Output on
        
    def __ApplyPulse__(self):
        self.instr.write('*TRG')        # Trigger the pulse in burst mode

    def __OutputOn__(self):
        self.instr.write('OUTPUT ON')

    def __OutputOff__(self):
        self.instr.write('OUTPUT OFF')

    def __SetVoltage__(self, magnitude = 3.3, offset = 0):
        self.instr.write('VOLT:UNIT VPP')
        self.instr.write('VOLT %s' % str(magnitude))
        self.instr.write('VOLT:OFFS %s' %str((offset)))

    def __SetFrequency__(self, frequency):
        self.instr.write('FREQuency %s' % str(frequency))
