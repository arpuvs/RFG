#-----------------------------------------------------------------------------
# Name:        TEK_HFS9003.py
# Purpose:     Driver for the Tektronix HFS9003 pattern generator.
#
# Author:      Dave Shoudy
#
# Created:     2007/11/20
#-----------------------------------------------------------------------------

from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class TEK_HFS9003(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        '''Initializes the GPIB interface'''
        GPIBObjectBaseClass.__init__(self, 'Tektronix,HFS9003', addr)
 
    # Internal only function
    def dectobin_SDIO(self,dec=0,bits=8):
        '''This is a modified function of the written dectobin function to double each bit coming out, since each
        bit in the SDIO vector needs to be repeated twice so that it is at the correct data rate'''
        i=0
        string = ''
        while (i<bits):
            bit = str(dec%2)
            string = bit + bit + string     # Modified this line to add the bit twice
            dec = dec >> 1
            i = i+1
        return string
    
 
    def __EnableOutputs__(self):
        '''This function enables all outputs on the HFS 9DG2 channel (bank B)'''
        self.instr.write('PGENB:CH1:OUTPUT ON')
        self.instr.write('PGENB:CH2:OUTPUT ON')
        self.instr.write('PGENB:CH3:OUTPUT ON')                


    def __DisableOutputs__(self):
        '''This function disables all outputs on the HFS 9DG2 channel (bank B)'''
        self.instr.write('PGENB:CH1:OUTPUT OFF')
        self.instr.write('PGENB:CH2:OUTPUT OFF')
        self.instr.write('PGENB:CH3:OUTPUT OFF')

        
    def __Trigger__(self):
        '''This function initiates a software trigger so that the PG sequence will be sent'''
        self.instr.write('*TRG')

    
    def __SetupSPI__(self,Vdd=3.3,SCLK_freq=1e6):
        '''This function sets up the 3 wire SPI interface on the PG with CHB1=SCLK, CHB2=SDIO, and CHB3=CSB'''
        
        # Disable outputs
        self.__DisableOutputs__()
        
        # Use NRZ pulses
        self.instr.write('PGENB:CH1:TYPE NRZ')
        self.instr.write('PGENB:CH2:TYPE NRZ')
        self.instr.write('PGENB:CH3:TYPE NRZ')
        
        # Use min edge transition time
        self.instr.write('PGENB:CH1:TRAN MIN')
        self.instr.write('PGENB:CH2:TRAN MIN')
        self.instr.write('PGENB:CH3:TRAN MIN')
        
        # 0V low logic level
        self.instr.write('PGENB:CH1:LOW 0')
        self.instr.write('PGENB:CH2:LOW 0')
        self.instr.write('PGENB:CH3:LOW 0')
        
        # High logic level of Vdd
        self.instr.write('PGENB:CH1:HIGH %s' %str(Vdd))
        self.instr.write('PGENB:CH2:HIGH %s' %str(Vdd))
        self.instr.write('PGENB:CH3:HIGH %s' %str(Vdd))
        
        # Normal polarity
        self.instr.write('PGENB:CH1:POL NORM')
        self.instr.write('PGENB:CH2:POL NORM')
        self.instr.write('PGENB:CH3:POL NORM')
        
        # Normal pulse rate
        self.instr.write('PGENB:CH1:PRATE NORM')
        self.instr.write('PGENB:CH2:PRATE NORM')
        self.instr.write('PGENB:CH3:PRATE NORM')
        
        # Set the signal names
        self.instr.write('PGENB:CH1:SIGN "SCLK"')
        self.instr.write('PGENB:CH2:SIGN "SDIO"')
        self.instr.write('PGENB:CH3:SIGN "CSB"')
        
        # 50 percent duty cycle
        self.instr.write('PGENB:CH1:DCYC 50')
        self.instr.write('PGENB:CH2:DCYC 50')
        self.instr.write('PGENB:CH3:DCYC 50')
        
        # Setup delays for each channel
        SCLK_delay = 1/SCLK_freq
        SDIO_delay = 1/(4*SCLK_freq)
        CSB_delay = 0
        self.instr.write('PGENB:CH1:LDELAY %s' %str(SCLK_delay))
        self.instr.write('PGENB:CH2:LDELAY %s' %str(SDIO_delay))
        self.instr.write('PGENB:CH3:LDELAY %s' %str(CSB_delay))
        
        # Set each channel's radix to binary
        self.instr.write('PGENB:CH1:DRAD BIN')
        self.instr.write('PGENB:CH2:DRAD BIN')
        self.instr.write('PGENB:CH3:DRAD BIN')
        
        
        # Set frequency of time base
        freq = SCLK_freq*2
        self.instr.write('TBAS:FREQ %s' %str(freq))

        # Use burst mode
        self.instr.write('TBAS:MODE BURST')
              
        # Setup trigger for only 1 time
        self.instr.write('TBAS:TOUT:PER 1')
        
        # Setup the time base count........may not need this
        self.instr.write('TBAS:COUNT 24')
        
        # Put PG in running mode (waiting for next trigger)
        self.instr.write('TBAS:RUN ON')
                
        
        # Set the vector radix to decimal
        self.instr.write('FPAN:VRAD DEC')
         
        # Set the vector start, loop, and end fields
        self.instr.write('VECT:START 0')
        self.instr.write('VECT:LOOP 0')
        self.instr.write('VECT:END 51')
        
        # Setup SCLK and CSB channel vectors
        self.instr.write('VECT:IOFORMAT "SCLK", BIN')
        self.instr.write('VECT:DATA 0,52, "1010101010101011010101010101010110101010101010101000"')
        self.instr.write('VECT:IOFORMAT "CSB", BIN')
        self.instr.write('VECT:DATA 0,52, "1000000000000000000000000000000000000000000000000001"')
        
        # Enable channels
        self.__EnableOutputs__()
                
        
        
    def __SetupSDIO__(self,address=0x120,data=0x00):
        '''This function sets up the data on SDIO for a SPI transfer.  The SPI interface on the PG 
        should have already been setup.  A 16 bit address is setup, followed by 8 bits of data'''
        address_bin = self.dectobin_SDIO(address,16)
        data_bin = self.dectobin_SDIO(data,8)
        
        self.instr.write('VECT:IOFORMAT "SDIO", BIN')
        self.instr.write('VECT:DATA 0,1,"1"')
        self.instr.write('VECT:DATA 1,16,"%s"' %str(address_bin[0:16]))
        self.instr.write('VECT:DATA 17,1,"%s"' %str(address_bin[15]))
        self.instr.write('VECT:DATA 18,16,"%s"' %str(address_bin[16:32]))
        self.instr.write('VECT:DATA 34,1,"%s"' %str(address_bin[31]))
        self.instr.write('VECT:DATA 35,16,"%s"' %str(data_bin))
        self.instr.write('VECT:DATA 51,1,"1"')
            