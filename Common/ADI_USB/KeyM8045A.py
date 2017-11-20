# Predefined variables and functions
# evalapp - the eval app XML object
# topwin - the main frame class
# readAll - read all interfaces of all chips
# writeAll - write all settings to all chips
# getSavePath - ask the user for a path to save a file
# getOpenPath - ask the user for a path to open a file
# unloadBoards - unload the currently loaded boards
# loadBoard - load a new board from XML
# ProgressDialog - a class for showing progress of your script
import visa


class KeyM8045A():
    def __init__(self, addr=-3):
        rm = visa.ResourceManager()
        self.instr = rm.open_resource("TCPIP0::localhost::hislip0::INSTR")
        myStr = self.instr.query("*IDN?")
        print myStr

    # ###======================= Global Commands ================================####
    def Global_Jitter_Enable(self, status):
        '''
        This command enables or disables global jitter. It is a global SCPI; working for all modules.
        status: ON/OFF
        '''
        self.instr.write(":JITT:STAT 'M1.System', " + status)

    # ###======================= Jitter ================================####
    def Jitter_External(self, source, status):
        '''
        Enable/disable the external jitter input connector for Data Out1, Data Out2 and Clock Out.
        The name of the connectors are DATA MOD IN and CLK MOD IN.
        source: DataOut1/ClkOut
        status: ON/OFF
        '''
        self.instr.write(":JITT:HFR:EXT:STAT 'M1." + source + "', " + status)

    def Jitter_Delay(self, delay):
        '''
        Sets the delay of the jitter profile of the corresponding output.
        '''
        self.instr.write(":JITT:CONF:DEL 'M1.DataOut2', " + str(delay))

    def Hifreq_Jitter_Unit(self, unit):
        '''
        Specifies whether the jitter parameters are to be specified/returned in seconds (TIME) or unit intervals (UINTerval).
        unit: UINT|TIME
        '''
        self.instr.write(":SOURce:JITTer:HFRequency:UNIT 'M1.DataOut1', " + unit)

    def Peri_Hifreq_Jitter_Enable(self, source, status):
        '''
        This command is used to enable/disable periodic jitter high frequency output at the given location.
        status: ON/OFF
        source: DataOut1/ClkOut
        '''
        self.instr.write(":JITT:HFR:PER 'M1." + source + "', " + status)

    def Peri_Hifreq_Jitter_Amp(self, amp):
        '''
        This command sets the amplitude of the periodic jitter in seconds or unit intervals for the specified output.
        The units are set using the [:SOURce]:JITTer:HFRequency:UNIT command.
        Range: 0mUI to 1.102UI
        '''
        self.instr.write(":JITT:HFR:PER:AMPL 'M1.DataOut1', " + str(amp))

    def Peri_Hifreq_Jitter_Freq(self, freq):
        '''
        This command sets the frequency of the periodic jitter for the specified output.
        Range: 1 kHz to 500 MHz
        '''
        self.instr.write(":JITT:HFR:PER:FREQ 'M1.DataOut1', " + str(freq))

    def BUJ_Enable(self, source, status):
        '''
        Enables/disables the generation of bounded uncorrelated jitter at the specified output.
        source: DataOut1/ClkOut
        status: ON/OFF
        '''
        self.instr.write(":JITT:HFR:BUNC 'M1." + source + "', " + status)  # 1 = Enable 0 =  Disalbed

    def BUJ_Hifreq_Jitter_Amp(self, Datarate, Amp):
        '''
        This command sets the bounded uncorrelated jitter amplitude in seconds (TIME) or unit intervals (UINTerval).
        The units are set using the [:SOURce]:JITTer:HFRequency:UNIT command.
        This command also sets the bounded uncorrelated PRBS data rate to 625MBps, 1250 MBps, or 2500 MBps.
        Datarate: RATE625|RATE1250|RATE2500
        '''
        self.instr.write(":JITT:HFR:BUNC:DRAT 'M1.DataOut1', " + Datarate)
        self.instr.write(":JITT:HFR:BUNC:AMPL 'M1.DataOut1', " + str(Amp))

    def BUJ_Hifreq_Jitter_Filter(self, bandwidth):
        '''
        This command selects the low-pass filter for bounded uncorrelated jitter (50, 100, or 200 MHz).
        bandwidth: LP50|LP100|LP200
        '''
        self.instr.write(":JITT:HFR:BUNC:FILT 'M1.DataOut1', " + bandwidth)

    def BUJ_Hifreq_Jitter_Pattern(self, pattern):
        '''
        This command selects polynomial of the PRBS for bounded uncorrelated jitter source.
        pattern: PRBS7|PRBS8|PRBS9|PRBS10|PRBS11|PRBS15|PRBS23|PRBS31
        '''
        self.instr.write(":JITT:HFR:BUNC:FILT 'M1.DataOut1', " + pattern)

    def BUJ_Hifreq_Jitter_Pattern2(self, pattern):  #this one works, the string needed :PRBS instead of :FILT
        '''
        This command selects polynomial of the PRBS for bounded uncorrelated jitter source.
        pattern: PRBS7|PRBS8|PRBS9|PRBS10|PRBS11|PRBS15|PRBS23|PRBS31
        '''
        self.instr.write(":JITT:HFR:BUNC:PRBS 'M1.DataOut1', " + pattern)

    def Rj_Hifreq_Jitter_Enable(self, source, status):
        '''
        This command enables/disables the generation of random jitter.
        status: ON/OFF
        source: DataOut1/ClkOut
        '''
        self.instr.write(":JITT:HFR:RAND 'M1." + source + "', " + status)

    def Rj_Hifreq_Jitter_Amp(self, amp):
        '''
        This command sets the root mean square (rms) RJ amplitude in seconds or unit intervals based
        on the selected amplitude unit. The units are set using the [:SOURce]:JITTer:HFRequency:UNIT command.
        amp: 0 uUI to 13.08 mUI or 0 ps to 78.57 ps
        '''
        self.instr.write(":JITT:HFR:RAND:AMPL 'M1.DataOut1', " + str(amp))

    def Rj_Hifreq_Jitter_Filter_Low(self, filt):
        '''
        This command enables/disables the low-pass filter for random jitter. LP100 enables a 100 MHz
        low-pass filter; LP500 enables a 500 MHz low-pass filter.
        filter: OFF|LP100|LP500
        '''
        self.instr.write(":JITT:HFR:RAND:FILT 'M1.DataOut1', " + str(filt))

    def Rj_Hifreq_Jitter_Filter_Low2(self, filt): # this one works, the string needed :LPAss
        '''
        This command enables/disables the low-pass filter for random jitter. LP100 enables a 100 MHz
        low-pass filter; LP500 enables a 500 MHz low-pass filter.
        filter: OFF|LP100|LP500
        '''
        self.instr.write(":JITT:HFR:RAND:FILT:LPAss 'M1.DataOut1', " + str(filt))

    def Rj_Hifreq_Jitter_Filter_Hi(self, filt):
        '''
        This command enables/disables the high-pass filter for random jitter. HP10 enables a 10 MHz high-pass filter.
        filter: OFF|HP10
        '''
        self.instr.write(":JITT:HFR:RAND:FILT:HPAS 'M1.DataOut1', " + str(filt))

    def Lowfreq_Jitter_Unit(self, source, unit):
        '''
        Specifies whether the jitter parameters are to be specified/returned in seconds (TIME) or unit intervals (UINTerval).
        unit: UINT|TIME
        source: DataOut1/ClkOut
        '''
        self.instr.write(":JITT:LFR:UNIT 'M1." + source + "', " + unit)

    def Peri_Lowfreq_Jitter_Enable(self, source, status):
        '''
        This command enables/disables the low frequency periodic jitter source.
        status: ON/OFF
        source: DataOut1/ClkOut
        '''
        self.instr.write(":JITT:LFR:PER 'M1." + source + "', " + status)

    def Peri_Lowfreq_Jitter_Amp(self, source, freq, amp):
        '''
        This command sets the amplitude of the periodic low frequency jitter in unit intervals or time
        for the specified output. The units are set using the [:SOURce]:JITTer:LFRequency:UNIT command.
        This command also sets the frequency of the periodic jitter. Acceptable units include Hz, kHz,
        MHz and exponents (for example, 1E3 is the same as 1,000 Hz).
        source: DataOut1/ClkOut
        '''
        self.instr.write(":JITT:LFR:PER:FREQ 'M1." + source + "', " + str(freq))
        self.instr.write(":JITT:LFR:PER:AMPL 'M1." + source + "', " + str(amp))

    def Peri_Lowfreq_Jitter_Amp_freq(self, source, freq):
        '''
        this just does the freq set
        '''
        self.instr.write(":JITT:LFR:PER:FREQ 'M1." + source + "', " + str(freq))

    def Peri_Lowfreq_Jitter_Amp_Amp(self, source, amp):
        '''
        this just does the amp set
        '''
        self.instr.write(":JITT:LFR:PER:AMPL 'M1." + source + "', " + str(amp))

    def F2_jitter(self, jitter):
        '''
        This command sets the f/2 jitter at the output in seconds. Acceptable units include ps and exponents (for example, -10e-12 is the same as -10 ps).
        Range -20 ps to +20 ps
        Example :OUTP:DATA:F2J 'M1.DataOut2', -10e-12
        '''
        self.instr.write(":OUTP:DATA:F2J 'M1.DataOut1', " + jitter)

    def Jitter_Sweep_Enable(self, status):
        '''
        This command enables/disables the jitter sweep.
        status: ON/OFF
        '''
        self.instr.write(":JITT:SWE 'M1.DataOut1', " + status)

    def Jitter_Sweep_Freq_Range(self, start, stop):
        '''
        This command defines the start frequency of the jitter sweep. The start frequency must be lower than the stop frequency and the range should be
        in accordance with the waveform. Acceptable units include Hz, kHz, MHz, GHz and exponents (for example, 1E3 is the same as 1,000 Hz).
        start: 1 kHz to 500 MHz
        stop: 1 kHz to 500 MHz
        '''
        self.instr.write(":JITT:SWE:FREQ:STAR 'M1.DataOut1', " + start)
        self.instr.write(":JITT:SWE:FREQ:STOP 'M1.DataOut1', " + stop)

    def ClearStatus(self):
        '''
        Description This command clears all status register structures in a device. These registers include:
        OPERation Status Register structure
        QUEStionable Status Register structure
        The corresponding enable registers are unaffected.
        '''
        self.instr.write("*CLS")  # clear all status

    def Operation_Pending_flag(self):
        '''The *OPC? query returns the ASCII character "1" in the Output Queue when the No\
        Operation Pending flag is TRUE. At the same time, it also sets the Message Available\
        (MAV) bit in the Status Byte Register. The *OPC? will not allow further execution of commands or\
        queries until the No Operation Pending flag is true, or receipt of a Device Clear (dcas) message, or a power on.\
        '''
        self.instr.write("*OPC?")  # clear all status

    def Global_Output_Enable(self, status):
        '''
        This command sets global output state to ON or OFF.
        This command works for all modules, as it is a Global command.
        Status: ON/OFF
        '''
        self.instr.write(":OUTP:GLOB 'M1.System', " + status)

    def Data_Disable(self):
        '''
        This command switches an output on or off.
        <ON|OFF|1|0>: Switch an output on or off.
        '''
        self.instr.write(":OUTP 'M1.DataOut1', 0")  # Turn oFF Data

    def Data_Enable(self):
        '''
        This command switches an output on or off.
        <ON|OFF|1|0>: Switch an output on or off.
        '''
        self.instr.write(":OUTP 'M1.DataOut1', 1")  # Turn on Data

    def Output_Offset(self, source, offset, ):
        '''
        This command sets the offset value of an output signal in Volts addressed by an identifier.
        Acceptable units include mV, V and exponents (for example, 500E-3 is the same as 500 mV).
        source: DataOut1/ClkOut
        '''
        self.instr.write(":SOURce:VOLTage:OFFSet 'M1." + source + "', " + str(offset))  # mV Offset for ClockP

    def Data_Amplitude(self, damp):
        '''Description: Set peak to peak voltage amplitude
        set channel 1(DataOut1) of module 1 (M1) output to damp(V)
        The location identifier consists of two parts: the first part specifies the module, the second part addresses,
        If a SCPI command is to be sent to a specific module only and not a specific channel, simply use M1+/- or M2+/- as the location identifier.
        If you want to set a value that acts on all components of a modular instrument (for example, set all jitter sources to off), omit the location identifier.
        100 mV to 1.8 Vpp differential
        damp range: 0.05 ~ 0.9
        '''
        self.instr.write("SOUR:VOLT:AMPL 'M1.DataOut1', " + str(damp))  # mV  Amplitude for Data

    def Output_High(self, source, high):
        '''
        This command sets the upper voltage level of an output signal in Volts addressed by an identifier.
        Acceptable units include mV, V and exponents (for example, 500E-3 is the same as 500 mV).
        source: DataOut1/ClkOut
        '''
        self.instr.write(":VOLT:HIGH 'M1." + source + "', " + str(high))

    def Output_Low(self, source, low):
        '''
        This command sets the lower voltage level of an output signal in Volts
        source: DataOut1/ClkOut
        '''
        self.instr.write(":VOLT:LOW 'M1." + source + "', " + str(low))

    def Output_Range(self, range1):
        '''
        Amplitude ranges guarantee a glitch free change of the amplitude value within a specified range. The upper and lower limits of these ranges are
        specified in the data sheet. Ranges are only specified for the DataOut channel.
        range: R1|R2|R3|R4|R5|R6|R7|R8
        '''
        self.instr.write(":VOLT:RANG 'M1.DataOut1', " + str(range1))

    def Data_Coupling_mode(self, mode):
        '''
        This command selects DC or AC output coupling.
        <AC|DC>: Select output coupling.
        '''
        self.instr.write(":OUTPut:COUPling 'M1.DataOut1', " + mode)

    def Data_Polarity(self, polarity):
        '''
        This command sets the output polarity to either normal or inverted.
        <NORmal|INVerted>: Set output polarity to normal or inverted.
        '''
        self.instr.write(":OUTPut:POLarity 'M1.DataOut1', " + polarity)

    def Clock_Disable(self):
        '''
        This command switches an output on or off.
        <ON|OFF|1|0>: Switch an output on or off.
        '''
        self.instr.write(":OUTP 'M1.ClkOut', 0")  # Turn oFF CLK

    def Clock_Enable(self):
        '''
        This command switches an output on or off.
        <ON|OFF|1|0>: Switch an output on or off.
        '''
        self.instr.write(":OUTP 'M1.ClkOut', 1")  # Turn ON CLK

    def Clock_Amplitude(self, camp):
        '''
        This command sets the peak to peak value of an output signal in Volts
        Differential: 0.2 to 2.0 V, 10 mV steps
        '''
        self.instr.write("SOUR:VOLT:AMPL 'M1.ClkOut', " + str(camp))  # mV  Amplitude for ClockP

    def Synth_Bit_Rate(self, synthBitRate):
        '''
        Sets the frequency of the synthesizer in the M8020A/M8030A. Acceptable units include kHz, MHz, GHz and exponents (for example, 10E9 is the
        same as 10 GHz).
        For M8041A: 256 MHz to 16.207 GHz
        For M8195A: 256 MHz to 32.5 GHz
        '''
        self.instr.write(
            "SOUR:FREQ 'M1.ClkGen'," + str(synthBitRate))  # Sets internal synthesizer to 9.953GHz

    def Trig_Mode(self, mode):
        '''
        Selects the different trigger modes.
        mode: INT|REF|DIR|CMUL
        INTernal 100 MHz reference clock or AXIe 100 MHz (M9505A AXIe Chassis)
        REFerence 10 MHz / 100 MHz external reference clock
        DIRect 8.1 GHz to 16.207 GHz clock used as the system frequency directly in the M8041A
        CMULtiplier Multiplied/divided clock used to specify system frequency
        '''
        self.instr.write(":TRIGger:SOURce 'M1.ClkGen', " + str(mode))
        # self.instr.write(":TRIGger:REFerence:FREQuency 'M1.ClkGen', " + str(mode))

    def Trig_Ref_Freq(self, mode):
        '''
        Selects the refernce frequency set to REF10 or REF100
        '''

        self.instr.write(":TRIGger:REFerence:FREQuency 'M1.ClkGen', " + str(mode))

    def Divider(self, divider):
        '''
        This command selects a specific clock divider from DIV1 through DIV80.
        divider: 1 to 80
        '''
        self.instr.write(":OUTPut:DIVider 'M1.ClkOut',DIV" + str(divider))  # Set value of clock Divider

    def Deemph_Unit(self, unit):
        '''
        This command defines the tap value unit: dB or PCT (PerCenT).
        the unit should be set before sending the values with the above de-emphasis commands:PRESet/PRECursor/POSTcursor
        unit: DB|PCT
        '''
        self.instr.write(":OUTP:DEEM:UNIT 'M1.DataOut1', " + unit)

    def Set_Deemph_cursor_magnitude(self, cursor, magn): # expects cursor 0, 1 or 3 and magn from -0.4 to +0.4
        '''
        This command defines the tap value unit: dB or PCT (PerCenT).
        the unit should be set before sending the values with the above de-emphasis commands:PRESet/PRECursor/POSTcursor
        unit: DB|PCT
        '''
        if cursor==0: self.instr.write(":OUTP:DEEM:CURS:MAGN0 'M1.DataOut1',"+str(magn))
        if cursor==1: self.instr.write(":OUTP:DEEM:CURS:MAGN1 'M1.DataOut1',"+str(magn))
        if cursor==3: self.instr.write(":OUTP:DEEM:CURS:MAGN3 'M1.DataOut1',"+str(magn))



    def Data_Sequence_Creat(self, name):
        '''
        This command is used to create a new sequence.
        '''
        self.instr.write(":DATA:SEQ:NEW '" + name + "'")

    def Data_Sequence_Bind(self, name):
        '''
        This command binds the identifiers to a specified sequence. The identifier is either a location or a group name identifier. If locations are already used
        in another sequence, they get re-assigned to this sequence.
        '''
        self.instr.write(":DATA:SEQ:BIND 'my','M1.DataOut1'")

    #         self.instr.write(":DATA:SEQ:BIND '" + name + "','M1.DataOut1'")

    def Data_Sequence_Value(self):
        '''
        This command is used to enter a sequence string consisting of the pattern sequence parameters for the specified sequence name and download it to
        the hardware. A definite length block must be entered indicating the length of the string to download.
        <sequence-name>: Specify sequence name.
        <sequence-string>: Enter definite length block and pattern sequence XML string.
        Note: It is recommended to edit the sequence string in the Sequence Editor in either "UI" or "<Xml>" mode and then copy/paste the xml sequence string.
        '''
        self.instr.write(":DATA:SEQuence:VALue 'Analyzer',#3342<?xml version=\"1.0\" \
                            encoding=\"utf-16\"?><sequenceDefinition \
                            xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" \
                            xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" \
                            xmlns=\"http://www.agilent.com/schemas/M8000/DataSequence\"><descr \
                            iption /><sequence><loop><block length=\"128\"><prbs \
                            polynomial=\"2^7-1\" \
                            /></block></loop></sequence></sequenceDefinition>")

    def Load_M8040_setupFile(self, setup_file):
        setup_file = 'setup_ctle_prbs7_sweep'
        setup_file = str(setup_file) + "'"
        instr = ':MMEM:WORK:SETT:REC '
        combo = str(instr) + "'" + str(setup_file) + ""
        #print combo
        self.instr.write(combo)

    def SubRate(self, subrate):
        self.instr.write("GEN:SUBR " + str(subrate))
        # sets sub rate clock output divider for Generator internal clock synth
        # 1,2,4,8,16,32,64,128.  1 is full rate

    def Link_Data_Disable(self):
        self.instr.write("GEN:DOUT:LPNS 0")  # Generator Data +\- outputs are not linked

    def Link_Data_Enable(self):
        self.instr.write("GEN:DOUT:LPNS 1")  # Generator Data +\- outputs are linked

    def Link_Clock_Disable(self):
        self.instr.write("GEN:COUT:LPNS 0")  # Clock Data +\- outputs are not linked

    def Link_Clock_Enable(self):
        self.instr.write("GEN:COUT:LPNS 1")  # Clock Data +\- outputs are linked

    def Data_DOP_Clip(self):
        return self.instr.query("GEN:DOP:CLIP")  # Retrieve whether the Generator Data+ output setting is clipped

    def Data_DON_Clip(self):
        return self.instr.query("GEN:dON:CLIP")

    def Data_Output_Impedance(self, value):
        self.instr.write("GEN:DOP:IMP" + str(value))  # output impedance in Ohms. Range[30 to 100,000]
        self.instr.write("GEN:DON:IMP" + str(value))

    ##Set the data_output logic family.PECL is not available on the BERTScope.
    def Data_Output_Logic(self, family1):
        self.instr.write("GEN:DON:LFAM" + family1)
        self.instr.write("GEN:DOP:LFAM" + family1)

    def Generator_Ref_Enable(self):
        self.instr.write("GEN:REFIN:ENABLE 1")  # Enable the Generator Reference In

    def Generator_Ref_Freq(self, frequency):
        self.instr.write("GEN:REFIN:FREQ " + str(frequency))

    ##Set or retrieve the termination voltage of the Generator Data+ output. May require some delay to complete.
    '''
    numeric: Generator Data+ output termination voltage in mV.

    Range [-2,000 to +2,000]. Input out of range will be clipped and recorded in the status queue.
    '''

    def Data_Termination_GEN(self, dpterm, dnterm):
        self.instr.write("GEN:DOP:TVOL " + str(dpterm))  # mV Termination for DataP
        self.instr.write("GEN:DON:TVOL " + str(dnterm))  # mV Termination for DataN

    def Data_Termination_DET(self, dpterm):
        self.instr.write("DET:DOP:TVOL " + str(dpterm))  # mV Termination for DataP
        self.instr.write("DET:DON:TVOL " + str(dpterm))  # mV Termination for DataN

    def Clock_Termination(self, cpterm, cnterm):
        self.instr.write("GEN:COP:TVOL " + str(cpterm))  # mV Termination for ClockP
        self.instr.write("GEN:CON:TVOL " + str(cnterm))  # mV Termination for ClockN

    def Clock_Offset(self, cpoffset, cnoffset):
        self.instr.write("GEN:COP:SLOF " + str(cpoffset))  # mV Offset for DataP
        self.instr.write("GEN:CON:SLOF " + str(cnoffset))  # mV Offset for DataN

    ##Restores a pre-saved configuration from a file representing the entire state of the instrument.
    def Restore_ConfigButton(self, fpath, fname):
        self.instr.write('RCONfiguration "' + fpath + fname + '"')  # restores configuration

    def Save_ConfigButton(self, fpath, fname):
        self.instr.write('SCONFiguration "' + fpath + fname + '"')  # saves configuration

    def Sine_Jitter_Enable(self):
        self.instr.write("GSM:SJitter:Enable 1")  # 1 = Enable 0 =  Disalbed

    def Sine_Jitter_Disable(self):
        self.instr.write("GSM:SJitter:Enable 0")  # 1 = Enable 0 =  Disable

    '''
    Set or retrieve the sinusoidal jitter frequency in Hz.

    Range [20,000 to 80,000,000]
    '''

    def Sine_Freq_Amp(self, sineFreq, sineAmp):
        self.instr.write("GSM:SJitter:FREQ " + str(sineFreq))  # sets adjust frequency
        self.instr.write(
            "GSM:SJitter:AMPU " + str(sineAmp))  # sets amplitude of frequency based on percentage of UI

    def SineLF_Jitter_Enable(self):
        self.instr.write("GSM:LFSJ:ENABLE 1")  # 1 = Enable 0 =  Disalbed

    def SineLF_Jitter_Disable(self):
        self.instr.write("GSM:LFSJ:ENABLE 0")  # 1 = Enable 0 =  Disable

    def SineLF_Freq_Amp(self, sineFreq, sineAmp):
        self.instr.write("GSM:LFSJ:FREQ " + str(sineFreq))  # sets adjust frequency
        self.instr.write(
            "GSM:LFSJ:AMPPS " + str(sineAmp))  # sets amplitude of frequency based on percentage of UI

    def Sinusodial_Interference(self, interFreq, interAmp):
        self.instr.write("GSM:SInterference:AMPL " + str(
            interAmp))  # Sinusoidal interference amplitude 100,000,000 to  2,5000,000,000
        self.instr.write(
            "GSM:SInterference:FREQ " + str(interFreq))  # Sinusoidal interference amplitude 10 to  400

    def Random_Jitter_Enable(self):
        self.instr.write("GSM:RJitter:Enable 1")  # 1 = Enable 0 =  Disalbed

    def Random_Jitter_Disable(self):
        self.instr.write("GSM:RJitter:Enable 0")  # 1 = Enable 0 =  Disable

    def Random_Jitter_Freq(self, randomFreq, randomAmp):
        self.instr.write("GSM:RJitter:FREQ " + str(randomFreq))  # sets adjust frequency
        self.instr.write("GSM:RJitter:AMPU " + str(randomAmp))  # sets amplitude of frequency

    def Global_Stress_Disable(self):
        self.instr.write("GSM:Stress:Enable 0")  # global stress disabled

    def Global_Stress_Enable(self):
        self.instr.write("GSM:Stress:Enable 1")  # global stress enabled

    ##Set or retrieve the internal clock synthesizer frequency of the Generator.
    '''
    BERTScope BSA175C: Range [500,000,000 to 17,500,000,000]

    Input out of range will be clipped and recorded in the status queue.
    '''

    def Error_Inject_Manual(self, event):
        self.instr.write("GENerator:EIMode MANual")  # Manual Mode

    def Error_Inject_Continuous(self, event):
        self.instr.write("GENerator:EIMode CONT")  # Continuous Mode

    def Error_Inject_Mode(self, event):
        self.instr.write("GEN:EIM" + event)  # Set or retrieve the Generator Error Inject mode
        # event can be set as:CONTinuous | MANual | EXTernal | OFF

    def Error_Inject_enable(self,event): #0= off , 1= on
        if event: self.instr.write(":OUTPut:EINSertion 'M1.DataOut1', 1")
        else:     self.instr.write(":OUTPut:EINSertion 'M1.DataOut1', 0")

    def Retr_Inject_BER(self):
        return float(self.instr.query("GEN:IBER"))  # Retrieve the injected BER of the Generator

    def LoadMquery(self, fpath, fname):
        # fpath ='D:\\BitAlyzer\\Mask\\JESD204B\\'
        # fname = 'OIF-CEI-26G-C.msk'
        self.instr.write('MASK:MFName ' + '"' + fpath + fname + '"')  # Loads Mask file remotely

    def SaveMask(self, fpath, fname):
        # fpath ='D:\\BitAlyzer\\Mask\\JESD204B\\'
        # fname = 'OIF-CEI-26G-C.msk'
        self.instr.write('MASK:SMW ' + '"' + fpath + fname + '"')  # Saves Mask File remotely

    ##Auto center the Eye
    def EyeAutoScale(self):
        self.instr.write("EYE:ASCale")  # Autoscales Eye Mask Screen on Bert Scope

    '''
    Perform Data Centering. This command is equivalent to the Auto Align function
    on the local control interface. Action only. May require some delay to complete.
    '''

    def Det_AutoAlign(self):
        self.instr.write('DET:PDC')

    ##Retrieve whether Detector Data Centering (Auto Align) succeeds or not. Query only.
    ## Returns: < 1 > Data centering is successful < 0 > Data centering is not successful
    def Det_AutoAlign_done(self):
        return float(self.instr.query('DET:DCS?'))

    # Retrieve whether the Detector is in sync.
    def Det_AutoAlign_sync(self):
        return float(self.instr.query('DET:ISYNC?'))

    ##Set or retrieve the Full Rate Clock property of the Detector.
    ##1 Detector is Full Rate Clock Mode  -  0 Detector is Half Rate Clock Mode
    def DetectorClkDiv(self, value=1):
        self.instr.write("DETector:FULLRateclock " + str(value))

    def Jitter_units_perUI(self):
        self.instr.write("JMAP:JUNITS PERCENTUI")  # sets units for jitter map to percent UI

    def Jitter_P_P(self):
        return float(self.instr.query("EYE:MVALue:JITTer?"))  # Returns the Jitter P-P Query Only.

    def Jitter_RMS(self):
        return float(self.instr.query("EYE:MVALue:JRMS?"))  # Returns the Eye Jitter RMS Query Only.

    def Jitter_BUJ(self):
        return float(self.instr.query("JMAP:BUJ?"))  # Returns the BUJ Query Only.

    def Jitter_BUJ_Locked(self):
        return float(self.instr.query("JMAP:BUJLOCKED?"))  # Returns the BUJ Locked Query Only.

    def Jitter_DDJ(self):
        return float(self.instr.query("JMAP:DDJ?"))  # Returns the Data-Dependent Jitter Query Only.

    def Jitter_DJ(self):
        return float(self.instr.query("JMAP:DJ?"))  # Returns the Deterministic Jitter Query Only.

    def Jitter_EJ(self):
        return float(self.instr.query("JMAP:EJ?"))  # Returns the EJ Locked Jitter Query Only.

    def Jitter_EJTROF(self):
        return float(self.instr.query("JMAP:EJTROF"))  # Returns the Emphasis Jitter Transition Offset Query Only.

    def Jitter_RJ(self):
        return float(self.instr.query("JMAP:RJ?"))  # Returns the Random Jitter Query Only.

    def Jitter_TJ(self):
        return float(self.instr.query("JMAP:TJ?"))  # Returns the TJ Jitter Query Only.

    def Jitter_ISI(self):
        return float(self.instr.query("JMAP:ISI?"))  # Returns the TJ Jitter Query Only.

    def Jitter_DJIT(self):
        return float(self.instr.query("JMAP:DJIT?"))  # Returns the Deterministic Jitter Query Only.

    def Jitter_Clear(self):
        self.instr.write("JITTer:CLEar")  # Clear Jitter

    ##Set or retrieve the Generator data type.
    def Gen_Pattern(self, type1):
        self.instr.write("GEN:PATT " + str(type1))  # set pattern PN15 or PN7 and so on

    ##Set or retrieve the data type of the Detector. PN11 pattern is available only on BERTScope Analyzers.
    '''
    PN7 | PN11 | PN15 | PN15 | PN20 | PN23 | PN31: Pseudo-random data types: PRBS-7, PRBS-11 1, PRBS-15, PRBS-20, PRBS-23, PRBS-31

    USTart: User pattern
    UGRab:  Grab and Go
    USHift: Shift and Sync
    AUTomatic: Automatic detection
    ALLZERO: All-zeros pattern
    '''

    def Det_Pattern(self, type1):
        self.instr.write("DET:PATT " + str(type1))  # set pattern PN15 or PN7 and so on

    def Jitter_BER(self, BER):
        self.instr.write("JMAP:PPBEr " + str(BER))  # sets jitter map BER

    def DET_Run(self):
        self.instr.write("DET:RUIN 20")  # Sets Run state to 20 seconds
        self.instr.write("RSTATE 1")  # 1 Starts Jitter; 0 Stops Jitter

    def Jitter_Run(self):
        self.instr.write("DET:RUIN 20")  # Sets Run state to 20 seconds
        self.instr.write("MASK:RSTATE 1")  # 1 Starts Jitter; 0 Stops Jitter

    def RUN(self):
        self.instr.write("MASK:RSTATE 1")  # 1 Starts

    def STOP(self):
        self.instr.write("MASK:RSTATE 0")  # 1 Starts

    def JMAP_Run(self):
        self.instr.write("JMAP:RUNMODE NORMAL")  # Run IN Normal Mode

    def Detector_Bits(self):
        return float(self.instr.query("DET:BITS?"))  # Returns number of bits passed from duration run

    def Detector_Errors(self):
        return float(self.instr.query("DET:ERR?"))  # Returns number of error bits from duration run

    def Detector_DataCenter_Amplitude(self):
        return float(self.instr.query("DETector:DCAMv?"))  # Retrieve the data center amplitude in mV. Query only.

    ##Set or retrieve the Detector Data Input Attenuation Factor.
    ##Valid ranges: 0.001:1 to 1000:1 or -60 dB to +60 dB
    def Detector_Data_Attenuation(self, factor):
        self.instr.write("DET:ATTENF" + str(factor))

    def View_Eye(self):
        self.instr.write("View Eye")  # view eye diagram

    def View_Det(self):
        self.instr.write("View Detector")  # view detector

    def View_Generator(self):
        self.instr.write("View Generator")  # view detector

    def View_JitterMap(self):
        self.instr.write("View JMAP_MAP")  # view detector

    def View_StressedEye(self):
        self.instr.write("View STRESSedeye")  # view detector

    def View_Mask(self):
        self.instr.write("View MASK")  # view detector

    def Detector_DataCenterUnit_Int(self):
        return float(self.instr.query("DETector:DCUinterval?"))  # Retrieve the data center unit interval. Query only.

    def Mask_Center_Errors(self):
        return float(self.instr.query("MASK:CPERrors?"))  # Retrieve Mask Test Center Polygon Errors. Query only.

    def Mask_Lower_Errors(self):
        return float(self.instr.query("MASK:LPERrors?"))  # Retrieve Mask Test Lower Polygon Errors. Query only.

    def Mask_Upper_Errors(self):
        return float(self.instr.query("MASK:UPERrors??"))  # Retrieve Mask Test Upper Polygon Errors. Query only.

    def Eye_Time_Offset(self, time_offset):
        self.instr.write("EYE:TOOFfset " + str(time_offset))  # Set the time offset of the Eye view.

    def ISI_Primary_SET(self, mode):
        self.instr.write("STRCmb:PRIIsi " + str(mode))  # Set ISI on primary channel BSAITS125.

    def ISI_Secondary_SET(self, mode):
        self.instr.write("STRCmb:SECIsi " + str(mode))  # Set ISI on secondary channel BSAITS125.

    def ISI_PRIM_SEC_SET(self, mode):
        self.instr.write("STRCmb:CMBIsi " + str(mode))  # Set ISI when primary and secondary channels are linked

    def EXT_Loss_SET(self, mode):
        self.instr.write("STRCmb:EXT1 " + str(mode))  # Set EXT loss BSAITS125.

    def CABLE_LOSS_SET(self, mode):
        self.instr.write("STRCmb:CABLoss " + str(mode))  # Set cable loss BSAITS125.

    def LINK_PRIM_SEC(self, mode):
        self.instr.write("STRCmb:LINKprisec " + str(mode))  # to link primary and secondary set to 1

    def REF_FREQ_SET(self, mode):
        self.instr.write("STRCmb:DATAhzauto " + str(mode))  # Set reference frequency BSAITS125.

    def ISI_Primary_Get(self, mode):
        return float(self.instr.query("STRCmb:PRIIsi?"))  # Get ISI on primary channel BSAITS125.

    def ISI_Secondary_GET(self, mode):
        return float(self.instr.query("STRCmb:SECIsi?"))  # Get ISI on secondary channel BSAITS125.

    def EXT_Loss_GET(self, mode):
        return float(self.instr.query("STRCmb:EXT1?"))  # Get EXT loss BSAITS125.

    def CABLE_LOSS_GET(self, mode):
        return float(self.instr.query("STRCmb:CABLoss?"))  # Get cable loss BSAITS125.

    def REF_FREQ_GET(self, mode):
        return float(self.instr.query("STRCmb:DATAhzauto?"))  # Get reference frequency BSAITS125.

    def Num_CRs(self):
        return self.instr.query("CRService:AttachDevCounT?")
        # Retrieves the number of BERTScope CRs that are currently
        # communicating with the Clock Recovery Service

    def CR_Close(self):
        self.instr.write("CRS:CLOSE")  # Close the communication connection to the current BERTScope CR

    def CR_Open(self, name):
        self.instr.write("CRS:OPEN" + name)  # Selects or Returns the device name of the current BERTScope CR

    def Setup_Auto_Save(self, statues):
        self.instr.write("CRControl:AUTOSconfigDEVice" + str(
            statues))  # determines whether CR restores its shutdown state at power-on
        # o:off, 1:on

    def Statues_of_CR(self):
        return self.instr.query("CRC:BUSY?")
        # 0  Device is for available for communication
        # 1  Device is temporarily unavailable for communication

    def CR_Clock_Output(self, statues):
        self.instr.write("CRControl:CLocKOUTput" + str(statues))
        # 0  Clock output disabled
        # 1  Clock output enabled

    def CR_Clock_Amp(self, amplitude):
        self.instr.write("CRC:CLKAMPL" + str(amplitude))
        # Sets or retrieves the clock output amplitude in mV.
        # Range [250 mV to 900 mV]

    def CR_Duty_CycDist(self):
        return float(self.instr.query(
            "CRControl:DutyCycleDistortion?"))  # Retrieves the Duty Cycle Distortion measurement in % Unit Interval

    def CR_Lock_Mode(self, mode):
        self.instr.write("CRC:LOCKMODE" + mode)  # MANUAL | AUTOMATIC | NARROW

    def CR_Lock_Range(self, range1):
        self.instr.write("CRC:RANGE" + str(range1))  # Range [10E6. Hz to 500E6. Hz]

    def CR_Loop_Band(self, bandwidth):
        self.instr.write("CRC:LOOPBW" + str(bandwidth))  # Range is 100E3 Hz to 12E6 Hz

    def CR_Edge_Density(self, percent):
        self.instr.write(
            "CRC:NOMEDGED" + str(percent))  # Sets or retrieves the nominal edge density in percent,Range [10% to 100%]

    def CR_Nominal_Frequency(self, frequency):
        self.instr.write("CRC:NOMFREQ" + str(
            frequency))  # Sets or retrieves the nominal frequency in Hz.Range is 150E6 Hz to 12.5E9 Hz

    def CR_Peak(self, peak_db):
        self.instr.write("CRC:PEAKING" + str(peak_db))  # Range is to 0 dB to 6 dB

    def CR_PHerror_Lim(self, limit):
        self.instr.write("CRC:PHERRLMT" + str(
            limit))  # Sets the the phase error limit in percent unit interval.Range is 10 %UI to 90 %UI

    """
    The following instructions will be used to control EYE Diagram.

    """

    ##Set or retrieve the Auto Center optical power format.
    ## format:UW|DBM
    def Power_Formate(self, formate):
        self.instr.write("EYE:AMPP" + formate)

    ##Set or retrieve the Auto Center mode of the Eye view.
    ##mode:EOPening | TRANsition
    def Eye_Mode(self, mode):
        self.insyr.write("EYE:ASM" + mode)

    ##Set or retrieve Optical Mode Average Power format.
    ##format:UW|DBM
    def Avg_Power_Foermate(self, formate):
        self.instr.write("EYE:AWGPP" + formate)

    ##Set or retrieve the cursor mode of the Eye view.
    ##mode:NONE | TIME | VOLT | TVOL | SINGle
    '''
    NONE   No cursor is displayed
    TIME   Only two time cursors are displayed
    VOLT   Only two voltage cursors are displayed
    TVOL   Two time cursors and two voltage cursors are displayed
    SINGle Single cursor is displayed

    '''

    def Cursor_Mode(self, mode):
        self.instr.write("EYE:CMOD" + mode)

    ##Set or retrieve Cross Noise 0 and 1 optical power format.
    ## format:UW|DBM
    def Noise_Pwer_mode(self, formate):
        self.instr.write("EYE:CN0P" + formate)
        self.instr.write("EYE:CN1P" + formate)

    ##Set or retrieve Crossing Voltage power format.
    ##MV Value displayed in mV |  % Value displayed in %UI
    def Cross_Vol_Form(self, formate):
        self.instr.write("EYE:CVFO" + formate)

    ##Set or retrieve the edge mode of the Eye view.
    ##8020 Use 80%-20% edge  | 9010  Use 90%-10% edge
    def Edge_Mode(self, mode):
        self.instr.write("EYE:EMOD" + mode)

    ##Save Eye diagram matrix data to a CSV file. Full path name should be given.
    def Save_Eye_Digram(self, filename):
        self.instr.write("EYE:ESAV" + filename)

    '''
    Set or retrieve the threshold level (in mV or uW, depending on the mode) for the Rising or Falling Level Crossing measurement.

    The threshold value in mV or uW that defines the level at which the 80/20 or
    90/10 rising or falling edge crosses to set the Rising or Falling Level Crossing in ps.
    Limits vary depending on the signal, and must be between the 80/20 or 90/10
    points on the rising or falling edges, depending on the edge mode configuration.
    '''

    def Threshold_Level(self, value):
        self.instr.write("EYE:LCRTH" + str(value))

    ##Enable/disable display of Eye measurements.
    def Display_able(self, boolen):
        self.instr.write("EYE:MDEN" + str(boolen))

    ##Set or retrieve the Eye Overshoot0 or 1 measurement format.
    ##format: MV | %
    def Eye_Overshoot(self, formate):
        self.instr.write("EYE:OVSH0FO" + formate)
        self.instr.write("EYE:OVSH1FO" + formate)

    ##Set or retrieve the persistence of the Eye view.
    '''
    Eye persistence as a number of images being persisted.

    Range [0 to 5]. Input out of range will be clipped and recorded in the status queue.
    A value of -1 runs the Eye diagram with infinite persistence.
    '''

    def Persistence(self, value):
        self.instr.write("EYE:PERS" + str(value))

    ##Set or retrieve the Eye Sample Depth in bits.
    '''
    Range [2,000 to 10,000,000]. Input out of range will be clipped and recorded in the status queue.

    A value of -1 runs the Eye diagram in the 'Auto' mode with a sample depth of
    10,000 bits.
    '''

    def Sample_Depth(self, number):
        self.instr.write("EYE:SDEP" + str(number))

    ##Save Single Value Eye diagram data to a CSV file. Full path name should be given. Action only.
    def Save_Single_val(self, filename):
        self.instr.write("EYE:SSAV" + filename)

    ##Set or retrieve the Eye center time offset of the Eye view.
    '''
    Eye center time offset in ps.

    The range of the input is the same as described in the numeric keypad if you
    click the volt Center button in the Eye view. Range [0 to 33,000]
    '''

    def Eye_Time_Center_Offset(self, time_offset):
        self.instr.write("EYE:TCOFfset " + str(time_offset))  # Set the Eye center time offset of the Eye view.

    ##Set or retrieve the time extent of the Eye view.
    '''
    Eye time extent in ps. Range [200 to 33,000].

    Input out of range will be clipped and recorded in the status queue.
    '''

    def Eye_Extent(self, value):
        self.instr.write("EYE:TEXT" + str(value))

    ##Set or retrieve the time offset of the Eye view.
    '''
    Eye time offset in ps. Range [-16,500 to +16,500].

    Input out of range will be clipped and recorded in the status queue.
    '''

    def Time_Offset(self, offset):
        self.instr.write("EYE:TOFF" + str(offset))

    ##Set or retrieve the Eye center voltage offset of the Eye view.
    '''
    Eye center voltage offset in mV.

    The range of the input is the same as described in the numeric keypad if you click the time Center button
    in the Eye view. Range [-2000 to +4000]
    '''

    def Center_Voltage_Offset(self, offset):
        self.instr.write("EYE:VCOF" + str(offset))

    ##Set or retrieve the voltage extent of the Eye view.
    ##Eye voltage extent in mV. Range [160 to 6,000].
    def Eye_Extent_Vol(self, voltage):
        self.instr.write("EYE:VEXT" + str(voltage))

    ##Set or retrieve Maximum and minimum voltage power format.UW|DBM
    def Vol_Power_Format(self, formate):
        self.instr.write("EYE:VMAP" + formate)
        self.instr.write("EYE:VMIP" + formate)

    ##Set or retrieve the voltage offset of the Eye view, and Voltage Offset power format:UW | DBM
    '''
    Eye voltage offset in mV. Range [-2000 to 4000].
    '''

    def Vol_Offset(self, formate, value):
        self.instr.write("EYE:VOFP" + formate)
        self.instr.write("EYE:VOFF" + str(value))

    """
    The following instructions will be used as: Clean EYE
    """

    ##Retrieve configuration data of the CleanEye Amplitude measurement.
    '''
    The data is returned in the following format (in one line, shown here as multi-line for clarity):

    Max point: <from>%UI-<to>%UI(<method>),
    Min point: <from>%UI-<to>%UI(<method>)
    Example:
    Max point: 30%UI-70%UI(Average), Min point:40%UI-55%UI(Min)
    '''

    def CleanEye_Amp(self):
        return self.instr.query("EYE:AMPL:CE:CONFIG?")

    ##Set or retrieve whether CleanEye amplitude measurement is enabled.
    def CleanEye_Able(self, boolen):
        self.instr.write("EYE:AMPL:CE:ENAB" + str(boolen))

    ##Set an individual point for CleanEye Amplitude measurement.
    '''
    <0 | 1> Point Number (0 for Max point, 1 for Min point)
    <numeric> From: (integer value in %UI)
    <numeric> To: (integer value in %UI)
    <method> AVERAGE, MODE, or MAX for Max point AVERAGE, MODE, or MIN for Min point
    '''

    def Indiv_CleanEye_Amp(self, boolen, num1, num2, method):
        self.instr.write("EYE:AMPL:CE:POINT" + str(boolen) + "," + str(num1) + "," + str(num2) + "," + method)

    ##Set a protocol preset for CleanEye Amplitude measurement.
    ##If no protocol was set, returns "None"
    '''
    <protocol>   PCIE
                 SATA_minamp
                 SATA_maxamp
                 SAS
                 DPORT10
                 DPORT11
                 USB3
                 None
    '''

    def Protocol_Preset(self, protocol):
        self.instr.write("EYE:AMPL:CE:PROTOCOL" + protocol)

    ##Set or retrieve CleanEye sample depth.Range [2,000 to 1,000,000].
    def Clean_Sample_Depth(self, depth):
        self.instr.write("EYE:CLRS" + str(depth))

    ##Set or retrieve CleanEye Pattern length in bits.
    '''
    Range [64 to 1,048,576].

    A value of -1 calculates pattern length automatically based on input detector pattern.
    '''

    def Clean_Length(self, length):
        self.instr.write("EYE:CLRP" + str(length))

    ##Set or retrieve whether CleanEye Rise Time measurement is enabled.
    def Clean_Rise_Enable(self, boolen):
        self.instr.write("EYE:RTIM:CE:ENAB" + str(boolen))

    ##Set or retrieve whether CleanEye Fall Time measurement is enabled.
    def Clean_Fall_Enable(self, boolen):
        self.instr.write("EYE:FTIM:CE:ENAB" + str(boolen))

    ##Set an individual point for CleanEye Rise Time measurement.
    '''
    <0 | 1> Point Number 0: Max point 1: Min point
    <from> From: (integer value in %UI)
    <to> To: (integer value in %UI)
    <method> AVERAGE MODE, or MAX for Max point AVERAGE, MODE, or MIN for Min point
    '''

    def Clean_Eye_Rise(self, boolen, num1, num2, method):
        self.instr.write("EYE:RTIM:CE:POINT" + str(boolen) + "," + str(num1) + "," + str(num2) + "," + method)

    ##Set an individual point for CleanEye Fall Time measurement.
    def Clean_Eye_Fall(self, boolen, num1, num2, method):
        self.instr.write("EYE:FTIM:CE:POINT" + str(boolen) + "," + str(num1) + "," + str(num2) + "," + method)

    def Detector_EYE_Amplitude(self):
        return float(self.instr.query("EYE:MVAL:AMPL?"))  # Retrieve the eye amplitude

    def Detector_EYE_Voffset(self):
        return float(self.instr.query("EYE:MVAL:VOFS?"))  # Retrieve the eye amplitud

