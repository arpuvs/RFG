'''
Created on Mar 22, 2016

@author: lweida
Status:   created for Advantest D3186 Pattern Genertor

'''
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time

class ADV_D3186(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=30):
        GPIBObjectBaseClass.__init__(self, '', addr)        
        self.instr.term_chars = '\n'
        
        self.__delay__ = 0.1

        
        #Continue with normal operation        
        self.__delay__   = delay
        
        #write commands       
    def __Set_word_pat_length__(self,length): # set the length of the patter words when the d3186 is in "WORD" mode
        self.instr.write("BL " +str(length))
        time.sleep(0.1)
        
        #read Commands
    def __GetwordLength__ ( self ) :
        '''This function returns the WORD pattern length '''
        len= self.instr.ask( "BL?" ) 
        return len
        