import visa
import time


class PED13020(object):
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

    def autoAlign(self, abort=10):  #initiates the auto align process then queries the process status aborts after 10 sec
        Endtime=time.time()+abort
        #print Endtime
        self.instr.write(':SENS1:EYE:ALIG:AUTO ONCE')
        # print "AUTO ALIGN Sync In Progress...\n"
        while True:
            theTime= time.time()
            time.sleep(0.1)
            #print self.instr.query(':SENSe1:SYNC:STATe?')
            passFail =self.instr.query(":SENS1:EYE:ALIG:AUTO?")
            if theTime >= Endtime:
                self.instr.write(':SENS1:EYE:ALIG:AUTO ABORT')
                print "Auto Align Sync Aborted"
                break
            passFail= passFail.rstrip('\n')
            if passFail =='OK':
                # print "AUTO ALIGN SYNC STATUS: SYNCED\n"
                break
            elif passFail =='ERROR':
                print "AUTO ALIGN SYNC STATUS: ERROR"
                break

    def checkStatusAutoAlign(self):
        passFail = self.instr.query(":SENS1:EYE:ALIG:AUTO?")
        passFail = passFail.rstrip('\n')
        return passFail

    def centerDelay(self,abort=10):  #Initiates the CENTER DELAY process or queries the process status.
        Endtime = time.time() + abort
        self.instr.write(":SENS1:EYE:TCENT ONCE")
        print "CENTER DELAY Sync In Progress...\n"
        while True:
            theTime = time.time()
            try:
                passFail = self.instr.query(":SENSE1:EYE:TCEN?")
            except:
                if theTime >= Endtime:
                    self.instr.write('SENS1:EYE:TCEN ABORT')
                    print "Center Delay Sync Aborted"
                    break
                continue
            else:
                passFail = passFail.rstrip('\n')
                if passFail == 'OK':
                    print "CENTER DELAY SYNC STATUS: SYNCED\n"
                    break
                if passFail == 'ERROR':
                    print "CENTER DELAY SYNC STATUS: ERROR - Process has completed but was unable to successfully "\
                          "synchronize."
                    break

    def checkStatusCenterDelay(self):
        passFail = self.instr.query(":SENSE1:EYE:TCEN?")
        passFail = passFail.rstrip('\n')
        return passFail

    def abortAutoAlign(self):
        self.instr.write(':SENS1:EYE:ALIGn:AUTO ABORT')

    def abortCenterDelay(self):
        self.instr.write("SENS1:EYE:TCENT ONCE")

    def getEyeEdgeBER_Thr(self):
        print "EYE EDGE BER THRESHOLD: " + str(float(self.instr.query(':SENS1:EYE:THR?')))+"\n"
        return float(self.instr.query(':SENS1:EYE:THR?'))

    def setPatternType(self,type='PRBS'):
        type= type.upper()
        self.instr.write(':SENS1:PATT:TYPE '+str(type))
        print 'Pattern Type Set To: '+ str(type)

    def setPatternLength(self,length=8):
        if length in range(2,4194305):
            self.instr.write(':SENS1:PATT:LENG '+str(length))
            print 'Pattern Length: '+str(length)
        else:
            print 'ERROR: Pattern Length out of range. Valid Range is 2 to 4194304.'

    def setPatternPRBSLength(self,Plength):
        lengths =[7,9,11,15,23,31]
        if Plength in lengths:
            self.instr.write(':SENS1:PATT:PLEN '+str(Plength))
            print 'Pattern PRBS Length: '+str(Plength)
        else:
            print 'ERROR: Pattern PRBS Length "'+str(Plength)+'" is not an option. Valid lengths:'+str(lengths)

    def setSyncBER_thresh(self,thresh=1e-3):
        theThresh=[1e-1,1e-2,1e-3,1e-4,1e-5,1e-6,1e-7,1e-8]
        if thresh in theThresh:
            self.instr.write(':SENS1:SYNC:THR '+str(thresh))
            print 'SYNC BER THRESHOLD: '+str(thresh)
        else:
            print 'ERROR: THRESHOLD "'+str(thresh)+'" is not an option. Valid THRESHOLDS:'+str(theThresh)

    def getClockInputFreq(self):
        print str(self.instr.query(':SENS2:FREQ?'))+"Hz"
        return self.instr.query(':SENS2:FREQ?')

    def setSyncType(self,type='MANUAL'): #default is manual mode
        types=['MANUAL','AUTO']
        type= type.upper()
        if type in types:
            self.instr.write(':SENS1:SYNC:TYPE '+str(type))
            print "SYNC TYPE: "+ str(type)
        else:
            print "ERROR: Invalid type selection. Valid Selections: "+ str(types)

    def test(self):
        self.instr.write(':SENS1:EYE:ALIG:AUTO ONCE')

    def getBER(self):
        return self.instr.query('FETC:SENS1:ERAT?')

    def getErrCount(self):
        return self.instr.query('FETC:SENS1:ECO?')

    def getBitCount(self):
        return self.instr.query('FETC:SENS2:BCO?')

    def startAccumulation(self):
        self.instr.write(':SENS1:GATE:STAT ON')

    def stopAccumulation(self):
        self.instr.write(':SENS1:GATE:STAT OFF')

    def sync(self):
        self.instr.write(':SENS1:SYNC:EXEC ONCE')

    def syncStatus(self):
        return self.instr.ask(':SENS1:SYNC:EXEC?')

