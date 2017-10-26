#-----------------------------------------------------------------------------
# Name:        TEK_DG2020A.py
#
# Purpose:     Driver for the Tektronix DG2020A with P3420 output pod on port A. 
#              The functions contained here implement a SPI interface on the first
#              4 wires of POD A.  
#                   - A0 = internal high-impedance control (no-connect)
#                   - A1 = SCLK
#                   - A2 = CSB
#                   - A3 = SDI
#                   - A4 = PG_SEL, select line for Bacchus eval board circuit
#                          where low selects the pattern gen. SPI interface.
#
# Author:      Dave Shoudy
#
# Created:     2008/05/15
#              2008/09/19  Bug in SCLK generation for single transmissions fixed
#-----------------------------------------------------------------------------


from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time


class TEK_DG2020A(GPIBObjectBaseClass):
    
    
    def __init__(self, addr=-1):
        '''Initializes the GPIB interface'''
        GPIBObjectBaseClass.__init__(self, 'Tektronix,DG2020A', addr)
        self.instr.term_chars = ''  # No terminating characters to get GPIB to work ok
        
        # Internal class variables that are stored after initialization
        self.Vdd = 1.8
        self.SCLK_freq = 25e6
        self.writes = 100
        self.address_width = 16
        self.data_width = 8
        self.pause_width = 1
        self.total_bits = 100
        self.total_bits_digits = 3
    
    
    
    def __KilopassInitSPI__(self,Vdd=1.8,SCLK_freq=25e6,writes=100,address_width=16,data_width=8,pause_width=1):
        '''This function sets up the 3 wire SPI interface on the PG'''

        # Set internal variables
        self.Vdd = Vdd
        self.SCLK_freq = SCLK_freq
        self.writes = writes
        self.address_width = address_width
        self.data_width = data_width
        self.pause_width = pause_width
        
        # Stop operation
        self.instr.write('STOP')
        
        # Set data size based on the number of writes and the address, data, and pause bit lengths
        self.instr.write('DATA:MSIZE %s' %str(2*self.writes*(self.address_width+self.data_width+self.pause_width)+8))
        
        # Single trigger mode
        self.instr.write('MODE:STATE SINGLE')
        
        # Setup high impedance control through A0
        self.instr.write('OUTPUT:PODA:CH0:INH OFF')
        self.instr.write('OUTPUT:PODA:CH1:INH INT')
        self.instr.write('OUTPUT:PODA:CH2:INH INT')
        self.instr.write('OUTPUT:PODA:CH3:INH INT')
        self.instr.write('OUTPUT:PODA:CH4:INH OFF')
        
        # Assign bits to map to the POD A outputs
        self.instr.write('OUTPUT:PODA:CH0:ASSIGN 0')
        self.instr.write('OUTPUT:PODA:CH1:ASSIGN 1')
        self.instr.write('OUTPUT:PODA:CH2:ASSIGN 2')
        self.instr.write('OUTPUT:PODA:CH3:ASSIGN 3')
        self.instr.write('OUTPUT:PODA:CH4:ASSIGN 4')
        
        # Set logic high voltage
        self.instr.write('OUTPUT:PODA:CH0:HIGH %s' %str(self.Vdd))
        self.instr.write('OUTPUT:PODA:CH1:HIGH %s' %str(self.Vdd))
        self.instr.write('OUTPUT:PODA:CH2:HIGH %s' %str(self.Vdd))
        self.instr.write('OUTPUT:PODA:CH3:HIGH %s' %str(self.Vdd))
        self.instr.write('OUTPUT:PODA:CH4:HIGH %s' %str(self.Vdd))
        
        # Set logic low voltage
        self.instr.write('OUTPUT:PODA:CH0:LOW 0')
        self.instr.write('OUTPUT:PODA:CH1:LOW 0')
        self.instr.write('OUTPUT:PODA:CH2:LOW 0')
        self.instr.write('OUTPUT:PODA:CH3:LOW 0')
        self.instr.write('OUTPUT:PODA:CH4:LOW 0')
        
        # Setup data rate
        self.instr.write('SOURCE:OSC:INT:FREQ %s' %str(self.SCLK_freq*2))
        
        # Setup data lines
        self.__KilopassInitSPIpatterns__()
        
        # Start operation again
        self.instr.write('START')
        
        
        
    def __KilopassInitSPIpatterns__(self):    
        '''This function loads the sequence of default patterns into the PG before any data is loaded up.  SCLK, CSB, PG_SEL, and 
        the highZ Control signals are set here.  These signals won't change with varying data patterns'''
        
        # Get the total # of bits
        # 4 extra clocks on each end for PG_SEL and CSB room. Mult by 2 since 2bits needed for 2 clocks to make one data bit
        self.total_bits = 2*self.writes*(self.address_width+self.data_width+self.pause_width) + 8  
        
        # Get the total # of decimal digits in the # of bits
        if(self.total_bits > 10 and self.total_bits < 100):
            self.total_bits_digits = 2
        elif(self.total_bits > 100 and self.total_bits < 1000):
            self.total_bits_digits = 3
        elif(self.total_bits > 1000 and self.total_bits < 10000):
            self.total_bits_digits = 4
        elif(self.total_bits > 10000 and self.total_bits < 100000):
            self.total_bits_digits = 5
        #print 'total_bits =', self.total_bits
        #print 'total_bits_digits=', self.total_bits_digits
            
        # Stop operation
        self.instr.write('STOP')
        
        
        ## Create the highZ control signal
        highz_patt = ':DATA:PATT:BIT 0,0,' + str(self.total_bits) + ',#' + str(self.total_bits_digits) + str(self.total_bits) 
        highz_patt = highz_patt + '1'   # Leading 1
        i = 0
        while(i < self.total_bits-2):
            highz_patt = highz_patt + '0'
            i = i + 1
        highz_patt = highz_patt + '1'   # Trailing 1
        #print 'highz_patt =', highz_patt
        #print highz_patt.__len__()
        
        
        ## Create the SCLK signal
        sclk_patt = ':DATA:PATT:BIT 1,0,' + str(self.total_bits) + ',#' + str(self.total_bits_digits) + str(self.total_bits)
        sclk_patt = sclk_patt + '1111'  # 4 leading 1's
        sclk_base_patt = '01'
        i = 0
        while(i < self.total_bits-8): #-self.pause_width*2):    # Contruct signal
            sclk_patt = sclk_patt + sclk_base_patt
            i = i + 2
        i = 0
        #while(i < self.pause_width*2):
        #    sclk_patt = sclk_patt + '1'
        #    i = i + 1
        sclk_patt = sclk_patt + '1111'  # 4 trailing 1's
        #print 'sclk_patt =', sclk_patt
        #print sclk_patt.__len__()
        
        
        ## Create the CSB signal
        csb_patt = ':DATA:PATT:BIT 2,0,' + str(self.total_bits) + ',#' + str(self.total_bits_digits) + str(self.total_bits)
        csb_patt = csb_patt + '1110'  # 3 leading 1's and a 0
        csb_base_patt_bits = 2*(self.data_width+self.address_width+self.pause_width)
        csb_base_patt = ''
        i = 0
        while (i<csb_base_patt_bits-self.pause_width*2): # Zeros 
            csb_base_patt = csb_base_patt + '0'
            i = i+1
        i = 0
        while (i < self.pause_width*2):  # Add pausing 1's between writes
            csb_base_patt = csb_base_patt + '1'
            i = i+1
        i = 0
        while(i+csb_base_patt_bits <= self.total_bits-8):    # Contruct full signal
            csb_patt = csb_patt + csb_base_patt
            i = i + csb_base_patt_bits
        csb_patt = csb_patt + '1111'  # 4 trailing 1's
        #print 'csb_patt =', csb_patt
        #print csb_patt.__len__()
        
        
        ## Create the PG_SEL signal
        pgsel_patt = ':DATA:PATT:BIT 4,0,' + str(self.total_bits) + ',#' + str(self.total_bits_digits) + str(self.total_bits) 
        pgsel_patt = pgsel_patt + '11'   # Leading 1's
        i = 0
        while(i < self.total_bits-4):
            pgsel_patt = pgsel_patt + '0'
            i = i + 1
        pgsel_patt = pgsel_patt + '11'   # Trailing 1's
        #print 'pgsel_patt =', pgsel_patt
        #print pgsel_patt.__len__()
        
        
        ## Create the SDI signal
        sdi_patt = ':DATA:PATT:BIT 3,0,' + str(self.total_bits) + ',#' + str(self.total_bits_digits) + str(self.total_bits) 
        sdi_patt = sdi_patt + '11'   # Leading 1's
        i = 0
        while(i < self.total_bits-4):
            sdi_patt = sdi_patt + '0'
            i = i + 1
        sdi_patt = sdi_patt + '11'   # Trailing 1's
        #print 'sdi_patt =', sdi_patt
        #print sdi_patt.__len__()
        
        
        ## Write all patterns to the PG
        self.instr.write(highz_patt)
        self.instr.write(sclk_patt)
        self.instr.write(csb_patt)
        self.instr.write(pgsel_patt)
        self.instr.write(sdi_patt)
        
        # Start operation again
        self.instr.write('START')
        
    
    
    def __KilopassWriteSPI__(self,sdi_pairs=[[0x120,0x00],[0x120,0x00]]):
        '''Write to the SPI all [address,data] pairs in 'sdi_pairs'.  There should be 'writes' number of pairs provided to the 
        function, where 'writes' was defined in the Kilopass initialization'''
        self.__KilopassLoadSDI__(sdi_pairs)
        self.__Trigger__()
        
        
        
    def __KilopassLoadSDI__(self,sdi_pairs=[[0x120,0x00],[0x120,0x00]]):
        '''sdi_pairs should consist of "writes" number of [address,data] pairs with the correct address and data widths that were 
        set when initializing the kilopass.  All pairs will be put into a sinlge SDI pattern sequence to be sent sequentially over 
        the SPI'''
                
        # Stop operation
        self.instr.write('STOP')
        
        ## Create the SDI signal
        sdi_patt = ':DATA:PATT:BIT 3,0,' + str(self.total_bits) + ',#' + str(self.total_bits_digits) + str(self.total_bits) 
        sdi_patt = sdi_patt + '1111'   # Leading 1's
        bit_count = 0
        sdi_pair_bits = 2*(self.address_width+self.data_width+self.pause_width)   # bits per sdi address,data pair
        i = 0
        while(i < self.writes and (bit_count+sdi_pair_bits <= self.total_bits-8)):
            address_bin = self.dectobin_SDI(sdi_pairs[i][0],self.address_width)
            data_bin = self.dectobin_SDI(sdi_pairs[i][1],self.data_width)
            sdi_patt = sdi_patt + address_bin + data_bin
            j = 0
            while (j < self.pause_width*2):  # Add pausing 1's between writes
                sdi_patt = sdi_patt + sdi_patt[sdi_patt.__len__()-1]
                j = j+1
            bit_count = bit_count + sdi_pair_bits
            i = i + 1
        sdi_patt = sdi_patt + '1111'   # Trailing 1's
        #print 'sdi_patt =', sdi_patt
        #print sdi_patt.__len__()
        
        # Write SDI pattern 
        self.instr.write(sdi_patt)
        
        # Start operation again
        self.instr.write('START')
        
        
 
    def __NormalInitSPI__(self,Vdd=1.8,SCLK_freq=1e6):
        '''This function sets up the 3 wire SPI interface on the PG'''

        # Stop operation
        self.instr.write('STOP')
        
        # Set data size
        self.instr.write('DATA:MSIZE 64')
        
        # Single trigger mode
        self.instr.write('MODE:STATE SINGLE')
        
        # Setup high impedance control through A0
        self.instr.write('OUTPUT:PODA:CH0:INH OFF')
        self.instr.write('OUTPUT:PODA:CH1:INH INT')
        self.instr.write('OUTPUT:PODA:CH2:INH INT')
        self.instr.write('OUTPUT:PODA:CH3:INH INT')
        self.instr.write('OUTPUT:PODA:CH4:INH OFF')
        
        # Assign bits, may not need this
        self.instr.write('OUTPUT:PODA:CH0:ASSIGN 0')
        self.instr.write('OUTPUT:PODA:CH1:ASSIGN 1')
        self.instr.write('OUTPUT:PODA:CH2:ASSIGN 2')
        self.instr.write('OUTPUT:PODA:CH3:ASSIGN 3')
        self.instr.write('OUTPUT:PODA:CH4:ASSIGN 4')
        
        # Set logic high voltage
        self.instr.write('OUTPUT:PODA:CH0:HIGH %s' %str(Vdd))
        self.instr.write('OUTPUT:PODA:CH1:HIGH %s' %str(Vdd))
        self.instr.write('OUTPUT:PODA:CH2:HIGH %s' %str(Vdd))
        self.instr.write('OUTPUT:PODA:CH3:HIGH %s' %str(Vdd))
        self.instr.write('OUTPUT:PODA:CH4:HIGH %s' %str(Vdd))
        
        # Set logic low voltage
        self.instr.write('OUTPUT:PODA:CH0:LOW 0')
        self.instr.write('OUTPUT:PODA:CH1:LOW 0')
        self.instr.write('OUTPUT:PODA:CH2:LOW 0')
        self.instr.write('OUTPUT:PODA:CH3:LOW 0')
        self.instr.write('OUTPUT:PODA:CH4:LOW 0')
        
        # Setup data rate
        self.instr.write('SOURCE:OSC:INT:FREQ %s' %str(SCLK_freq*2))
        
        # Setup data lines 
        self.instr.write(':DATA:PATT:BIT 0,0,64,#2641000000000000000000000000000000000000000000000000000000000000001') # HighZ control
        self.instr.write(':DATA:PATT:BIT 1,0,64,#2641111010101010101010110101010101010101101010101010101011111111111') # SCLK
        self.instr.write(':DATA:PATT:BIT 2,0,64,#2641110000000000000000000000000000000000000000000000000001111111111') # CSB
        self.instr.write(':DATA:PATT:BIT 4,0,64,#2641100000000000000000000000000000000000000000000000000000111111111') # PG_SEL
        self.instr.write(':DATA:PATT:BIT 3,0,64,#2641111111111111111111111111111111111111111111111111111111111111111') # SDI
        
        # Start operation again
        self.instr.write('START')
        
        
        
    def __Trigger__(self):
        '''This function initiates a software trigger so that the PG sequence in memory will be sent'''
        self.instr.write('*TRG')
        
        
    
    def __NormalLoadSDI__(self,address=0x120,data=0x00):
        '''This function sets up the data on SDIO for a SPI transfer.  The SPI interface on the PG 
        should have already been setup.  A 16 bit address is setup, followed by 8 bits of data'''
        address_bin = self.dectobin_SDI(address,16)
        data_bin = self.dectobin_SDI(data,8)
        
        # Stop operation
        self.instr.write('STOP')
        
        # Create the data vector for SDI
        patt = ':DATA:PATT:BIT 3,0,64,#2641111'
        patt = patt + address_bin[0:16] + address_bin[15] + address_bin[16:32] + address_bin[31]
        patt = patt + data_bin + '1111111111'
        
        # Write the pattern to SDI
        self.instr.write(patt)
        # Start operation again
        self.instr.write('START')
        
        
        
    ## Internal only function
    def dectobin_SDI(self,dec=0,bits=8):
        '''This is a modified function of the written dectobin function to double each bit coming out, since each
        bit in the SDI vector needs to be repeated twice so that it is at the correct data rate'''
        i=0
        string = ''
        while (i<bits):
            bit = str(dec%2)
            string = bit + bit + string     # Modified this line to add the bit twice
            dec = dec >> 1
            i = i+1
        return string
    
    
            
    def __NormalWriteSPI__(self,address=0x120,data=0x00):
        '''This function writes 'data' to 'address' using SPI protocol.  'address' is a 16 bit address and 'data' is 8 bits'''
        self.__NormalLoadSDI__(address,data)
        self.__Trigger__()
        