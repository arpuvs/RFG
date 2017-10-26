# Author: Lloyd Weida
#
# Date: 01/26/14
#      
#
# ----------------------------------------------------------------
# Date: 11/09/2006
# Status: Debugged!
# Purpose: This module is a generic GPIB wrapper for:
# Agilent 3499 Switch/Control System

from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time


class Agilent3499(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):   
        GPIBObjectBaseClass.__init__(self, 'Agilent3499', addr)
        self.__delay__ = delay  
        #Reset Agilent3499
        self.instr.write( 'RESET' )
        
    def __reset_relays__(self, addr=-1, delay=0.1):   
        self.instr.write( 'RESET' )
                
    def __select_red_rack_relay__(self, p_relays,n_relays):
         self.instr.write( 'dwrite 100, ' + str(p_relays))
         self.instr.write( 'dwrite 101, ' + str(n_relays))
        
    def __select_green_rack_relay__(self, p_relays,n_relays):
         self.instr.write( 'dwrite 200, ' + str(p_relays))
         self.instr.write( 'dwrite 201, ' + str(n_relays))

    def __select_blue_rack_relay__(self, p_relays,n_relays):
         self.instr.write( 'dwrite 300, ' + str(p_relays))
         self.instr.write( 'dwrite 301, ' + str(n_relays))

    def __select_formC_rack_relay__(self, all_relays):
         self.instr.write( 'dwrite 502, ' + str(all_relays))
         
##        FORM C switches :
##
##        RED (R8-R15 side-on)    dwrite 502,254 (0xfe)  (11111110)
##        Green (G8-G15 side-on)  dwrite 502,251 (0xfb)  (11111011)
##        Blue  (B8-B15 side-on)  dwrite 502,239 (0xef)  (11101111)

   
                   
       
    