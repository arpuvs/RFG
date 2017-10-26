# Author: Kaushal Shrestha
# Date  : 08/24/2011
# Edit  :
#  - Wrapped the lines that need to execute only with 87206A around
#    if block in hw_initialize to avoid error (ATTN light blinking)
#  - L7206A does not support Disconnect (OPEN) fucntion. Instead use
#    Channel 7 or 8. For 87206 you have to use the (CLOSE) statement.
#  - Functions to Clear the error status and read the errors
#----------------------------------------------------
# Author: Tom MacLeod & Rodney Kranz
# Date: 02/23/2008
# Purpose: This module is a generic GPIB wrapper for:
# Agilent L7206A Coaxial Switch
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time

class AgilentL7206A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.25, sw_model_name='L7206A'):
        GPIBObjectBaseClass.__init__(self, 'Agilent Technologies,L4445A', addr)

        #Assign Delay
        self.__delay__ = delay

        #Reset
        self.Reset()

        #Default Bank Position
        self.bank_pos = '-1'

        #Default Pair Mode
        if (sw_model_name == 'L7206A'):
            self.pair_mode = 'OFF'
            self.str_disconnect = 'OPEN'
            self.str_connect = 'CLOSE'
        elif (sw_model_name == '87206A'):
            self.pair_mode = 'ON'
            self.str_disconnect = 'CLOSE'
            self.str_connect = 'OPEN'
        else:
            self.pair_mode = 'OFF'
            self.str_disconnect = 'OPEN'
            self.str_connect = 'CLOSE'

        #Initialize Hardware
        #self.__initialize_hw__()

    def __del__ ( self ):
        self.Reset()

    def Reset(self):
        '''This function resets the AgilentL7206A'''
        self.instr.write('*RST')
        self.currentChannel = 1

    def __initialize_hw__(self):
        '''Initializes hardware'''
        hw_id = self.__get_hw_id__()
        ch_range = '(@' + hw_id + '1:' + hw_id + '6)'
        bank_id = 'BANK' + str(self.__GetBank__())

        #print 'Ch Range: ' + ch_range
        #print 'Bank ID: ' + bank_id

        #These (3) commands are 87206A specific, and only requires when pair mode is on
        # However, we noticed that if the 87206A had been used in a bank, then it is safer
        # to have the code to turn off the pair mode. Saw weird behavior otherwise.
        # self.instr.write('ROUT:RMOD:DRIV:SOURCE OFF, (@1100)')
        # self.instr.write('ROUT:CHAN:DRIV:PAIR:MODE ' + self.pair_mode + ', ' + ch_range)
        # self.instr.write('ROUT:RMOD:BANK:DRIV:MODE OCOL, ' + bank_id + ', (@1100)') ## Don't even need this

        # Pair mode is force selected and written after turning the drive mode off.
        self.instr.write('ROUT:RMOD:DRIV:SOURCE OFF, (@1100)')
        self.instr.write('ROUT:CHAN:DRIV:PAIR:MODE ' + self.pair_mode + ', ' + ch_range)
        #Only the first 34945EXT is 'INT', all others are 'EXT'
        self.instr.write('ROUT:RMOD:DRIV:SOURCE INT, (@1100)')

        # Enable Channel Verification for L7206A (not for 87206A)
        if ( self.pair_mode == 'OFF' ) :
            self.instr.write('ROUT:CHANNEL:VERIFY:ENABLE ON, '+ ch_range)

        #Close all connections (CONNECT)
        self.instr.write('ROUT:' + self.str_connect + ' ' + ch_range)

    def __get_hw_id__(self):
        ''' Returns the hardware id, which accomodates for the
            34945EXT index and channel bank'''
        return '11' + self.bank_pos

    def __SetBank__(self, bank):
        '''This function sets the bank index'''
        #self.bank_pos = str((bank - 1) * 2)
        if ( bank != int( self.bank_pos ) ):
            if ( self.bank_pos != '-1' ) :
                print "Bank %s has already been previously assigned to this instance of switch object."  % self.bank_pos
                print "You might want to reinstantiate an object, especially if you are switching between L7206A and 87206A"
            self.bank_pos = str(bank)
            self.__initialize_hw__()

    def __GetBank__(self):
        '''This function returns the bank index'''
        #return int(self.bank_pos) / 2 + 1
        return int(self.bank_pos)

    def __SetChannel__(self, channel):
        '''This function selects the channel'''
        # You need to disconnect before connect only if PAIR mode is ON, else setting
        # to a different channel will suffice.
        if ( self.pair_mode == 'ON' ) :
            if ( self.currentChannel != int(channel) and self.currentChannel != 0 ):
                # For 87206A, it's a matter of executing the disconnect string
                self.instr.write('ROUT:' + self.str_disconnect + ' ' + self.__ChannelName__())

        self.currentChannel = int(channel)
        if ( self.currentChannel > 0 and self.currentChannel <=6 ):
            self.instr.write('ROUT:' + self.str_connect + ' ' + self.__ChannelName__())
        elif ( self.pair_mode == 'OFF' and self.currentChannel in [0,7,8] ) :
            tmp_channel = self.currentChannel
            # For L7206A, it's a matter of setting it to channel 7 or 8
            self.currentChannel = 8 # Change it to 8, and then revert back to 0
            self.instr.write('ROUT:' + self.str_connect + ' ' + self.__ChannelName__())
            self.currentChannel = tmp_channel
        else :
            if not ( self.currentChannel == 0 ) :
                print "%d is not supported" % self.currentChannel

        time.sleep(self.__delay__)

    def __GetChannel__(self):
        '''This function returns the current channel number'''
        return self.currentChannel

    def __ChannelName__(self):
        '''This function returns the a string representation for the currently
           selected channel'''
        hw_id = self.__get_hw_id__()
        ch_bank = '(@' + hw_id + str(self.currentChannel) + ')'

        return ch_bank

    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d

    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__

    def ClearErrors( self ):
        error = self.instr.write( '*CLS' )

    def ReadErrors( self ):
        errors=[]
        while ( True ) :
            error = self.instr.ask( 'SYST:ERR?' )
            if ( error == '+0,"No error"' ): break
            errors.append( error )
        return errors

    Bank    = property(__GetBank__, __SetBank__, None, "Selects the Bank")
    Channel = property(__GetChannel__, __SetChannel__, None, "Selects the Channel")
    Delay   = property(__GetDelay__, __SetDelay__, None, "Delay")

if __name__ == '__main__':
    #sw_ain_0  = AgilentL7206A( 9, sw_model_name='L7206A' )
    #sw_ain_1  = AgilentL7206A( 9, sw_model_name='L7206A' )
    #sw_ain_2  = AgilentL7206A( 9, sw_model_name='L7206A' )
    #sw_ain_3  = AgilentL7206A( 9, sw_model_name='L7206A')
    sw_ain_4  = AgilentL7206A( 9, sw_model_name='87206A')

    #sw_adc_ch = AgilentL7206A(9, sw_model_name='L7206A')

    #sw_ain_1.Bank  = 0 #Because this swtich is an 87206A, Bank 0 actually switches both Banks 0 & 1
    #sw_ain_0.Bank    = 0
    #sw_ain_1.Bank    = 1
    #sw_ain_2.Bank    = 2
    #sw_ain_3.Bank    = 3
    sw_ain_4.Bank    = 6
    #sw_adc_ch.Bank = 3

    for i in range( 0, 7 ) :
##        sw_ain_0.Channel = i % 7
##        sw_ain_1.Channel = i % 7
##        sw_ain_2.Channel = i % 7
##        sw_ain_3.Channel = i % 7
        sw_ain_4.Channel = i % 7

##    for adc_ch_index in range(4):
##        sw_adc_ch.Channel = adc_ch_index + 1
##        time.sleep(1)
##
##        for ain_index in range(4):
##            sw_ain_1.Channel = ain_index + 1
##            time.sleep(1)
##            sw_ain_2.Channel = ain_index + 1
##            time.sleep(2)
