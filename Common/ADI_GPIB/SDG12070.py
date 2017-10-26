import visa
import time
import os
class SDG12070(object):
    def __init__(self, addr, delay=0):
        self.__delay_time = 0
        visaObj = visa.ResourceManager()
        self.instr = visaObj.open_resource(addr)
        self.set_delay(delay)

    def __del__(self):
        self.instr.close()

    def set_delay(self, delay):
        self.__delay_time = delay

    def ident(self):
        '''
        Returns a tuple with the following:
            0) Manufacturer
            1) Inst Model
            2) Inst Serial Number
            3) Inst Firmware
        '''
        return tuple(self.instr.query("*IDN?").split(','))

    def reset(self):
        '''
        Resets the instrument to default settings.
        '''
        self.instr.write("*RST")

    def set_pattern_length(self, length, channel=1):
        '''
        Sets pattern length, valid from 2 to 2,097,152.
        '''
        assert(channel > 0 or channel < 3)
        assert(length > 1 or length <= 2097152)
        self.instr.write(":DIGital" + str(channel) + ":PATTern:LENGth " + str(length))

    def get_pattern_length(self, channel=1):
        '''
        Returns the set pattern length for a given channel.
        '''
        return int(self.instr.query(":DIGital" + str(channel) + ":PATTern:LENGth?"))

    def set_pattern_type(self, pattern, channel=1):
        '''
        Sets the pattern type for a given channel.
        Pattern options are 'PRBS' or 'DATA'
        '''
        pattern = pattern.upper()
        assert(channel > 0 or channel < 3)
        assert((pattern == "PRBS") or (pattern == "DATA"))
        self.instr.write(":DIGital" + str(channel) + ":PATTern:TYPE " + pattern)

    def get_pattern_type(self, channel=1):
        '''
        Returns current pattern type for a given channel.
        Return options: 'PRBS' or 'DATA'.
        '''
        assert(channel > 0 or channel < 3)
        return self.instr.query(":DIGital" + str(channel) + ":PATTern:TYPE?").strip("\n")

    def set_prbs_pattern_length(self, length, channel=1):
        '''
        Sets PRBS pattern lenght for a given channel.
        Options: 7, 9, 11, 15, 23, 31
        '''
        assert(channel > 0 or channel < 3)
        assert(length == 7 or length == 9 or length == 11 or length == 15 or length == 23 or length == 31)
        self.instr.write(":DIGital" + str(channel) + ":PATTern:PLENgth " + str(length))

    def get_prbs_pattern_length(self, channel=1):
        assert(channel > 0 or channel < 3)
        return int(self.instr.query(":DIGital" + str(channel) + ":PATTern:PLENgth?"))

    #Add :DIGital[1|2|3|4]:PATTern:DATA
    #Add :DIGital[1|2|3|4]:PATTern:HDATa

    def insert_error(self, num_of_errors=1, channel=1):
        assert(num_of_errors > 0)
        assert(channel > 0 or channel < 3)
        self.instr.write(":DIGital" + str(channel) + ":PATTern:SERRor")

    #Add :DIGital[1|2|3|4]:PATTern:ERATe
    #Add :DIGital[1|2|3|4]:PATTern:ERATe:STATe
    #Add :DIGital[1|2|3|4]:PATTern:BSHift
    #Add :DIGital[1|2|3|4]:SIGNal[:POS|:NEG]:CROSsover:[VALue]
    #Add :OUTPut0:SOURce
    #Add :OUTPut0:DIVider

    def set_output_state(self, state, channel=1):
        '''
        Set output state for a given channel.
        Options 'ON' or 'OFF'
        '''
        assert(channel > 0 or channel < 3)
        #Add error check to state
        self.instr.write(":OUTPut" + str(channel) + ":STATe " + state)
        pass #:OUTPut[1|2|3|4][:STATe]

    def get_output_state(self, channel=1):
        return self.instr.query(":OUTPut" + str(channel) + ":STATe?").strip("\n")

    #Add :OUTPut:CLOCk:DIVider
    #Add :SENSe:ROSCillator:SOURce

    #Add [:SOURce]:FREQuency[:CW|:FIXed]
    def set_data_rate(self, rate_in_Mbps):
        assert(rate_in_Mbps > 30)
        assert(rate_in_Mbps <= 30000)

        if rate_in_Mbps < 1000:
            freqStr = "{:.4f}e6".format(rate_in_Mbps)
        else:
            freqStr = "{:.5f}e6".format(rate_in_Mbps)

        self.instr.write(":SOURce:FREQuency " + freqStr)

    def get_data_rate(self):
        return int(float(self.instr.query(":SOURce:FREQuency?")) / 1E6)

    #Add [:SOURce]:SKEW[1|2|3|4]
    #Add [:SOURce]:VOLTage[1|2|3|4][:POS|:NEG][:LEVel][:IMMediate]:[:AMPLitude]

    def set_voltage(self, level, setting='BOTH', channel=1):
        '''
            level in mV
            valid setting: POS, NEG, BOTH
        '''
        if setting == 'POS' or setting == 'BOTH':
            self.instr.write(":SOURce:VOLTage" + str(channel) + ":POS " + str(level) + "E-3")

        if setting == 'NEG' or setting == 'BOTH':
            self.instr.write(":SOURce:VOLTage" + str(channel) + ":NEG " + str(level) + "E-3")

    def get_voltage(self, setting='POS', channel=1):
        '''
        returns level in mV
        valid setting: POS, NEG
        '''
        assert (setting == 'POS' or setting == 'NEG')
        readback = self.instr.query(":SOURce:VOLTage" + str(channel) + ":" + setting + "?")
        return float(readback)*1000


    #Add [:SOURce]:VOLTage[1|2|3|4][:POS|:NEG][:LEVel][:IMMediate]:OFFSet
    #Add [:SOURce]:VOLTage[1|2|3|4][:POS|:NEG][:LEVel][:IMMediate]:TERMination
    #Add [:SOURce]:VOLTage[1|2|3|4][:LEVel][:IMMediate]:LINK - added
    #Add :MMEMory stuff..... - added
    #Add :SYSTem:ERRor[:NEXT]? - added
    #Add :TRIGger:SOURce - added
    #Add :TRIGger:LOCK   - added
#-------------------------------------New Functions (8/10/17)-------------------------------------------------------------------
    def setClkOutputDiv(self,cod=1): #Programs the clock output divider
        dividers=[1,2,4,8,16]
        if cod in dividers:
            self.instr.write(':OUTP:CLOC:DIV '+str(cod))
        else:
            raise Exception(str(cod)+' is not an option for Output Clock Dividers')
    def getClkOutputDiv(self):        #Queries the clock output divider and returns the value
        return self.instr.query(':OUTP:CLOC:DIV?')
    def setTrigClockSrc(self,source='IMMediate'):
        assert(source == 'IMMediate' or source == 'IMM' or source == 'EXTernal' or source == 'EXT')
        self.instr.write(':TRIG:SOUR '+str(source))
    def getTrigClockSrc(self):
        return str(self.instr.query(':TRIG:SOUR?'))
    def getSystemErr(self):
        return self.instr.query(':SYST:ERR?')
    def setTrigLock(self):
        self.instr.write(':TRIG:LOCK')
    def set10MHzRefSrc(self,source= 'INTERNAL'):
        source= source.upper()
        if source != 'INT' or source!= 'INTERNAL' or source!= 'EXT' or source!= 'EXTERNAL':
            print '"'+str(source)+'" is not an option'
        else:
            self.instr.write(':SENSE:ROSCILLATOR:SOURCE '+str(source))
    def getRefSource(self):
        return self.instr.query(':SENSE:ROSCILLATOR:SOURCE?')
    def setInternalClkFreq(self,freq= 30e9):
        self.instr.write(':FREQ '+str(freq))
    def getIntClkFreq(self):
        return self.instr.query(':FREQ?')
    # def setPatternDataMemASCII(self,filename,dataLength=2,strtAddr=1,chan=1):
    #     try:
    #         filename2= str(filename)+".txt"
    #         f= open(filename2)
    #     except IOError:
    #         print "Could not find file: "+filename2
    #     else:
    #         theLetter= f.read()
    #         theLetter = list(theLetter)
    #         print theLetter
    #         for i in range(0,len(theLetter)+1):
    #             try:
    #                 theNum=theLetter.index('\n')
    #             except:
    #                 break
    #             else:
    #                 theLetter.remove(theLetter[theNum])
    #             #theLetter.remove(theLetter[theLetter.index('\n')])
    #         for i in range(0,len(theLetter)):
    #             theLetter[i] = theLetter[i].rstrip('\n')
    #         print theLetter
    #         #return
    #         binaryList =[]
    #         for i in theLetter :
    #             print i
    #             binary=''.join(format(ord(x), 'b') for x in i)
    #             while len(binary) !=8:
    #                 binary= '0'+binary
    #             print binary
    #             binaryList.append(binary)
    #         binaryList=''.join(binaryList)
    #         if len(binaryList) not in range(1,1025):
    #             print "ERROR: Bit Count not in range (1-1024)"
    #         else:
    #             if chan ==1:
    #                 print 'Channel Selected: '+str(chan)+' (Default)'
    #             else:
    #                 print 'Channel Selected: '+str(chan)
    #             if chan ==1:
    #                 print 'Start Address Bit Location: '+str(strtAddr)+' (Default)'
    #             else:
    #                 print 'Start Address Bit Location: '+str(strtAddr)
    #             print 'Bit Count: '+str(len(binaryList))
    #             print 'Bytes: '+str(len(theLetter))
    #             if dataLength== 2:
    #                 print 'Data Length: '+str(dataLength)+' (Default)'
    #             else:
    #                 print 'Data Length: ' + str(dataLength)
    #             #print binaryList
    #             print ':DIG1:PATT:DATA '+str(strtAddr)+','+str(len(binaryList))+',#'+str(dataLength)+str(len(binaryList))+str(binaryList)
    #         self.instr.write(':DIG1:PATT:DATA '+str(strtAddr)+','+str(len(binaryList))+',#'+str(dataLength)+str(len(binaryList))+str(binaryList))
    #         print self.instr.query(':DIG1:PATT:DATA? 1,8')
    #         f.close()
    # def setOffset(self,offset=0,setting='BOTH',chan=1):
    #     if setting == 'BOTH':
    #         self.instr.write(':VOLT'+str(chan)+':NEG:OFFS '+str(offset)+'V')
    def setPatternDataMemHex(self, filename,chan=1,strtAdd=1): # first line in the file should be the pattern length
        if chan not in range(1,3) or strtAdd not in range(1,2097153):
            raise ValueError('Channel selected/Start Start address not in range.')
        hexList=['0','1','2','3','4','5','6','7',
                     '8','9','A','B','C','D','E',
                     'F','a','b','c','d','e','f']
        try:
            patLengthFile = open(filename)
        except IOError:
            print "Could not find file: " + filename
        else:
            patLength = patLengthFile.readline()[0:].rstrip('\n')
            patLengthFile.close()
            #print patLength
            if int(patLength) not in range(2,2097143):
                raise Exception('Pattern Length must be in range 2-2097142')
        try:
            hexFile = open(filename)
        except IOError:
            print "Could not find file: " + filename
        else:
            theLetter = hexFile.read()[len(patLength):]
            theLetter = list(theLetter)
            countfornewLine = theLetter.count('\n')
            countforSpaces = theLetter.count(' ')
            hexToBin=[]
            if countfornewLine!=0:
                for i in range(0,countfornewLine):
                    theLetter.remove('\n')
            print theLetter
            if countforSpaces!=0:
                for i in range(0,countforSpaces):
                    theLetter.remove(' ')
            for i in range(0, len(theLetter)):
                try:
                    hexToBin.append('{:0b}'.format(int(theLetter[i],16)))
                except:
                    raise ValueError('Error: Use Hexadecimal')
                else:
                    while len(hexToBin[i]) != 4:
                        hexToBin[i]= '0'+hexToBin[i]
            hexToBin=''.join(hexToBin)
            theLetter=''.join(theLetter)
            numbits=len(hexToBin)
            if numbits not in range(1,4097):
                raise ValueError('Number of bits not in range')
            print 'Number of bits: '+str(numbits)
            if numbits % 4 !=0:
                raise ValueError('Error: Check Bits')
            strtandBits= strtAdd + numbits
            if strtandBits > 2097153:
                raise ValueError('(<start address> + <bit count>) must be <= 2097153')
            else:
                self.instr.write(":DIGital" + str(chan) + ":PATTern:LENGth " + str(patLength))
                print 'Pattern Length Set To: '+self.instr.query(":DIGital" + str(chan) + ":PATTern:LENGth?").rstrip('\n')
                if numbits>32:
                    self.instr.write(':DIG'+str(chan)+':PATT:HDAT '+str(strtAdd)+','+str(numbits)+',#'+str(2)+str(len(theLetter))+ theLetter)
                    print ':DIG' + str(chan) + ':PATT:HDAT ' + str(strtAdd) + ',' + str(numbits) + ',#' + str(2) + str(len(theLetter)) + theLetter
                else:
                    self.instr.write(':DIG' + str(chan) + ':PATT:HDAT ' + str(strtAdd) + ',' + str(numbits) + ',#' + str(1) + str(len(theLetter)) + theLetter)
                    print ':DIG' + str(chan) + ':PATT:HDAT ' + str(strtAdd) + ',' + str(numbits) + ',#' + str(1) + str(len(theLetter)) + theLetter
            print 'Pattern Data: '+str(theLetter)
            print 'Length of pattern: '+str(len(theLetter))
            print 'Binary: '+ hexToBin
            hexFile.close()
    def getPatternDataMem(self,address,numBits,chan=1):
        '''
        queries the num bits from selected
        channel pattern data at selected address
        '''
        addBit= address+ numBits
        if address in range(1,2097153) and numBits in range(1,1025) and chan in range(1,3) and addBit <= 2097153:
            self.instr.query(':DIG'+str(chan)+':PATT:DATA? '+str(address)+','+str(numBits))
        else:
            raise ValueError()
    def setErrorInsertion(self, chan=1):
        self.instr.write(':DIG'+str(chan)+':PATT:SERROR')
    def setErrorRateInsertion(self,chan=1,rate=1e-3):
        self.instr.write(':DIG'+str(chan)+':PATT:ERAT '+str(rate))
    def getErrorRateInsertion(self,chan=1):
        return self.instr.query(':DIG'+str(chan)+':PATT:ERAT?')
    def enableInsertionErr(self,chan=1,state='OFF'):
        state= state.upper()
        self.instr.write(':DIG'+str(chan)+':PATT:ERAT:STAT '+state)
    def getStateErrorEnable(self,chan=1):
        return self.instr.query(':DIG' + str(chan) + ':PATT:ERAT:STAT?')
    def setBitShift(self,chan=1,shift=0):
        self.instr.write(':DIG'+str(chan)+':PATT:BSH '+str(int(shift)))
    def getBitShift(self,chan=1):
        return self.instr.query(':DIG'+str(chan)+':PATT:BSH?')
    def setTrigOutEvent(self,event='PERiodic'):
        event= event.upper()
        self.instr.write(':OUTP0:SOUR '+event)
    def getTrigOutputDiv(self):
        return self.instr.query(':OUTP0:DIV?')
    def getTrigOutEvent(self):
        return self.instr.query(':OUTP0:SOUR?')
    def setTrigDivider(self,divider=64):
        trigOut= self.instr.query(':OUTP0:SOUR?')
        trigOut= trigOut.rstrip('\n')
        if trigOut== 'PER':
            self.instr.write(':OUTP0:DIV ' + str(divider))
        else:
            print 'Set Trig Out to Periodic'
    def getListInstrSettingsfileMem(self):
        return self.instr.query(':MMEM:CAT:STAT?')
    def getListPatternDatafileMem(self):
        return self.instr.query(':MMEM:CAT:PDAT?')
    def delExistInstrSetFilesMem(self,filename):
        filename = filename.upper()
        if len(filename) not in range(1,9):
            print 'Length of file name must be in range 1-8 characters'
        else:
            self.instr.write(':MMEM:DEL:STAT "'+str(filename)+'"')
            print 'Deleted File: '+str(filename)
    def delPatternDataFile(self,filename):
        filename=filename.upper()
        if len(filename) not in range(1,9):
            print 'Length of file name must be in range 1-8 characters'
        else:
            self.instr.write(':MMEM:DEL:PDAT "' + str(filename) + '"')
            print 'Deleted File: ' + str(filename)
    def renameInstrSetFileMem(self,filename,newFilename):
        filename = filename.upper()
        newFilename=newFilename.upper()
        if len(filename) not in range(1, 9) or len(newFilename)not in range(1,9):
            print 'Length of file name(s) must be in range 1-8 characters'
        else:
            self.instr.write(':MMEM:MOVE:STAT "' + str(filename) + '","'+str(newFilename)+'"')
            print 'Old File Name: ' + str(filename) +'\n'\
                  'New File Name: ' + str(newFilename)+'\n'
    def renamePatternDataFileMem(self,filename,newFilename):
        filename = filename.upper()
        newFilename = newFilename.upper()
        if len(filename) not in range(1, 9) or len(newFilename) not in range(1, 9):
            print 'Length of file name(s) must be in range 1-8 characters'
        else:
            self.instr.write(':MMEM:MOVE:PDAT "' + str(filename) + '","' + str(newFilename) + '"')
            print 'Old File Name: ' + str(filename) + '\n' \
                  'New File Name: ' + str(newFilename) + '\n'
    def recallInstrSettingSaved(self,savedFilename):
        savedFilename= savedFilename.upper()
        if len(savedFilename) not in range(1,9):
            print 'Length of file name must be in range 1-8 characters'
        else:
            self.instr.write(':MMEM:LOAD:STAT "' + str(savedFilename) + '"')
            print 'Recalled Instrument Setting: ' + str(savedFilename)
    def recallPatternDataSaved(self,savedFilename):
        savedFilename = savedFilename.upper()
        if len(savedFilename) not in range(1, 9):
            print 'Length of file name must be in range 1-8 characters'
        else:
            self.instr.write(':MMEM:LOAD:PDAT "' + str(savedFilename) + '"')
            print 'Recalled Pattern Data: ' + str(savedFilename)
    def storeInstrSetting(self,filename):
        filename= filename.upper()
        if len(filename) not in range(1,9):
            print 'Length of file name must be in range 1-8 characters'
        else:
            self.instr.write(':MMEM:STOR:STAT "' + str(filename) + '"')
            print 'Stored File: ' + str(filename)
    def storePatternData(self,filename):
        if len(filename) not in range(1, 9):
            print 'Length of file name must be in range 1-8 characters'
        else:
            self.instr.write(':MMEM:STOR:PDAT "' + str(filename) + '"')
            print 'Stored File: ' + str(filename)
    def setLinkOnOFF(self,selVoltageNum=1,mode='OFF'):
        mode=mode.upper()
        if selVoltageNum in range(1,5) and mode=='OFF' or mode== 'ON':
            self.instr.write(':VOLT'+str(selVoltageNum)+':LINK '+str(mode))
        else:
            raise Exception()
    def setTerminationVolt(self,selVoltNum=1, valVolt=0):
        if valVolt in range(-2,3.4) and selVoltNum in range(1,3):
            self.instr.write(':VOLT'+str(selVoltNum)+':POS:TERM '+str(valVolt)+'V')
        else:
            raise Exception()
    def setNRZsigCrossPointCmplmnt(self,percentage=50,chan=1):
        self.instr.write(':DIG'+str(chan)+':SIGN:POS:CROS '+str(percentage))
        self.instr.write(':DIG'+str(chan)+':SIGN:NEG:CROS ' + str(100-percentage))
    def setNRZsigCrossPointPOS(self,percentage=50,chan=1):
        self.instr.write(':DIG'+str(chan)+':SIGN:POS:CROS ' + str(percentage))
    def setNRZsigCrossPointNEG(self,percentage=50,chan=1):
        self.instr.write(':DIG'+str(chan)+':SIGN:NEG:CROS ' + str(percentage))
    def getNRZsigCrossPointPosNEG(self,chan=1):
        pos= self.instr.query(':DIG' + str(chan) + ':SIGN:POS:CROS?').rstrip('\n')
        neg= self.instr.query(':DIG' + str(chan) + ':SIGN:NEG:CROS?').rstrip('\n')
        print 'POS: '+ pos
        print 'NEG: '+ neg
        # posNeg=[]
        # posNeg.append(pos)
        # posNeg.append(neg)
        # return posNeg
    def getNRZsigCrossPointPOS(self, chan=1):
        print 'POS: '+self.instr.query(':DIG' + str(chan) + ':SIGN:POS:CROS?').rstrip('\n')
        return self.instr.query(':DIG' + str(chan) + ':SIGN:POS:CROS?').rstrip('\n')
    def getNRZsigCrossPointNEG(self, chan=1):
        print 'NEG: ' + self.instr.query(':DIG' + str(chan) + ':SIGN:NEG:CROS?').rstrip('\n')
        return self.instr.query(':DIG' + str(chan) + ':SIGN:NEG:CROS?').rstrip('\n')
    def setChanSkew(self,skew= 0e-12,chan=1):
        self.instr.write(':SKEW'+str(chan)+' '+str(skew))
    def getChanSkew(self,chan=1):
        return self.instr.query(':SKEW'+str(chan)+'?')
    def enableChanJitInsertion(self,chan=1,state='OFF'):
        state=state.upper()
        if chan in range(1,3) and state == 'OFF' or state== 'ON':
            self.instr.write(':PM'+str(chan)+' '+str(state))
        else:
            raise Exception()
    def getChanJitInsertion(self,chan=1):
        return self.instr.query(':PM'+str(chan)+'?')
    def setPk2pkAmpChnIntSinJitSrce(self,chan=1,amplitude= 0):
        self.instr.write('PM'+str(chan)+':INT1 '+str(amplitude)+'ps')
    def getPk2pkAmpChnIntSinJitSrce(self,chan=1):
        return self.instr.query('PM'+str(chan)+':INT1?')
    def setFreqInternalsineJitSrc(self,chan=1,freq= 1):
        self.instr.write(':PM'+str(chan)+':INT1:FREQ '+str(freq)+'MHz')
    def getFreqInternalsineJitSrc(self,chan=1):
        return self.instr.query(':PM' + str(chan) + ':INT1:FREQ?')
    def setChanInternalSineJitStatus(self,chan=1, state='OFF'):
        state= state.upper()
        if chan in range(1, 3) and state == 'OFF' or state == 'ON':
            self.instr.write(':PM'+str(chan)+':INTERNAL1:STATE '+str(state))
        else:
            raise Exception()
    def getChanInternalSineJitStatus(self, chan=1):
        return self.instr.write(':PM' + str(chan) + ':INTERNAL1:STATE?')
    def setRMSampOfRanJitSrc(self,chan=1,rms= 0):
        self.instr.write(':PM'+str(chan)+':INT2 '+str(rms)+'ps')
    def getRMSampOfRanJitSrc(self,chan=1):
        return self.instr.query(':PM' + str(chan) + ':INT2?')
    def setRandomJitStaus(self,chan=1, state= 'OFF'):
        state=state.upper()
        if chan in range(1, 3) and state == 'OFF' or state == 'ON':
            self.instr.write(':PM'+str(chan)+':INTERNAL2:STATE '+str(state))
        else:
            raise Exception()
    def getRandomJitStatus(self,chan=1):
        return self.instr.query(':PM' + str(chan) + ':INTERNAL2:STATE?')
    def setOffsetPOS(self,chan=1,offset=0): #in volts, can be changed
        self.instr.write(':VOLT'+str(chan)+':POS:OFFS '+str(offset)+'V')
    def setOffsetNEG(self,chan=1,offset=0):
        self.instr.write(':VOLT' + str(chan) + ':NEG:OFFS ' + str(offset) + 'V')
    def setOffsetPOS_NEG(self,chan=1, pos=0, neg=0):
        self.instr.write(':VOLT' + str(chan) + ':POS:OFFS ' + str(pos) + 'V')
        self.instr.write(':VOLT' + str(chan) + ':NEG:OFFS ' + str(neg) + 'V')
    def getOffsetPOS(self,chan=1): #in volts, can be changed
        return self.instr.query(':VOLT'+str(chan)+':POS:OFFS?')
    def getOffsetNEG(self,chan=1):
        return self.instr.query(':VOLT' + str(chan) + ':NEG:OFFS?')




#-----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    gen = SDG12070(addr='USB0::0x1857::0x2F26::4129339::INSTR')
    for volt in xrange(250, 500, 50):
        gen.set_voltage(volt)
        print "POS: ", str(gen.get_voltage('POS')), "NEG:", str(gen.get_voltage('NEG'))
        time.sleep(2)
