import visa
import time

class SDG12060(object):
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

    def set_pattern_length(self, length):
        '''
        Sets pattern length, valid from 2 to 4194304.
        '''
        assert(length > 1 or length <= 4194304)
        self.instr.write(":DIGital:PATTern:LENGth " + str(length))

    def get_pattern_length(self):
        '''
        Returns the set pattern length for a given channel.
        '''
        return int(self.instr.query(":DIGital:PATTern:LENGth?"))

    def set_pattern_type(self, pattern):
        '''
        Sets the pattern type for a given channel.
        Pattern options are 'PRBS' or 'DATA'
        '''
        pattern = pattern.upper()
        assert((pattern == "PRBS") or (pattern == "DATA"))
        self.instr.write(":DIGital:PATTern:TYPE " + pattern)

    def get_pattern_type(self):
        '''
        Returns current pattern type for a given channel.
        Return options: 'PRBS' or 'DATA'.
        '''
        return self.instr.query(":DIGital:PATTern:TYPE?").strip("\n")

    def set_prbs_pattern_length(self, length):
        '''
        Sets PRBS pattern lenght for a given channel.
        Options: 7, 9, 11, 15, 23, 31
        '''
        assert(length == 7 or length == 15 or length == 23 or length == 31)
        self.instr.write(":DIGital:PATTern:PLENgth " + str(length))

    def get_prbs_pattern_length(self):
        return int(self.instr.query(":DIGital:PATTern:PLENgth?"))

    #Add :DIGital[1|2|3|4]:PATTern:DATA
    #Add :DIGital[1|2|3|4]:PATTern:HDATa

    def insert_error(self, num_of_errors=1):
        assert(num_of_errors > 0)
        self.instr.write(":DIGital:PATTern:SERRor")

    #Add :DIGital[1|2|3|4]:PATTern:ERATe
    #Add :DIGital[1|2|3|4]:PATTern:ERATe:STATe
    #Add :DIGital[1|2|3|4]:PATTern:BSHift
    #Add :DIGital[1|2|3|4]:SIGNal[:POS|:NEG]:CROSsover:[VALue]
    #Add :OUTPut0:SOURce
    #Add :OUTPut0:DIVider

    def set_output_state(self, state):
        '''
        Set output state for a given channel.
        Options 'ON' or 'OFF'
        '''
        #Add error check to state
        self.instr.write(":OUTPut:STATe " + state)
        pass #:OUTPut[1|2|3|4][:STATe]

    def get_output_state(self):
        return self.instr.query(":OUTPut:STATe?").strip("\n")

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

    def setTrigOutEvent(self, event='PERiodic'):
        event = event.upper()
        self.instr.write(':OUTP0:SOUR ' + event)



    #Add [:SOURce]:SKEW[1|2|3|4]
    #Add [:SOURce]:VOLTage[1|2|3|4][:POS|:NEG][:LEVel][:IMMediate]:[:AMPLitude]
    #Add [:SOURce]:VOLTage[1|2|3|4][:POS|:NEG][:LEVel][:IMMediate]:OFFSet
    #Add [:SOURce]:VOLTage[1|2|3|4][:POS|:NEG][:LEVel][:IMMediate]:TERMination
    #Add [:SOURce]:VOLTage[1|2|3|4][:LEVel][:IMMediate]:LINK
    #Add :MMEMory stuff.....
    #Add :SYSTem:ERRor[:NEXT]?
    #Add :TRIGger:SOURce
    #Add :TRIGger:LOCK
