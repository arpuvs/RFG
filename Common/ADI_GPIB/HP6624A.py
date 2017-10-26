# Author: Lloyd Weida

# Purpose: This module is a generic GPIB wrapper for:
# HP6624A Power Supply
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class HP6624A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'HP6624A', addr)
        self.__delay__ = delay
              
    def __SetV__(self,V1,CH=0):       
        '''This function sets the V Voltage of selected CH '''        
        if CH == 1: 
            self.instr.write( 'VSET 1, ' + str(V1) )
        time.sleep(self.__delay__)
        if CH == 2: 
            self.instr.write( 'VSET 2, ' + str(V1) )
        time.sleep(self.__delay__)
        if CH == 3: 
            self.instr.write( 'VSET 3, ' + str(V1) )
        time.sleep(self.__delay__)       
        if CH == 4: 
            self.instr.write( 'VSET 4, ' + str(V1) )
        time.sleep(self.__delay__)
                                       
    def __SetI__(self,I1,CH=0):
        '''This function sets the I Current of selected CH '''
        if CH == 1:
            self.instr.write( 'ISET 1, ' + str(I1) )
        time.sleep(self.__delay__)
        if CH == 2:
            self.instr.write( 'ISET 2, ' + str(I1) )
        time.sleep(self.__delay__)
        if CH == 3:
            self.instr.write( 'ISET 3, ' + str(I1) )
        time.sleep(self.__delay__)                
        if CH == 4:
            self.instr.write( 'ISET 4, ' + str(I1) )
        time.sleep(self.__delay__)        
               
            
    def __SetEnable_a__(self,  Enabled):
        '''This function enables the On/Off for the power supply'''
        if Enabled:
            self.instr.write('OUT 1,1')
        else:
            self.instr.write('OUT 1,0')
    
    def __SetEnable__(self,Enabled,CH=0):
        '''This function enables the On/Off for the power supply'''
        if CH == 1:
            if Enabled:
                self.instr.write('OUT 1,1')
            else:
                self.instr.write('OUT 1,0')    
        if CH == 2:
            if Enabled:
                self.instr.write('OUT 2,1')
            else:
                self.instr.write('OUT 2,0')   
        if CH == 3:
            if Enabled:
                self.instr.write('OUT 3,1')
            else:
                self.instr.write('OUT 3,0')   
        if CH == 4:
            if Enabled:
                self.instr.write('OUT 4,1')
            else:
                self.instr.write('OUT 4,0')   
            
    def __GetV__(self,CH=0):
        '''This function gets the V Voltage'''
        if CH == 1:  
            return float( self.instr.ask('VOUT? 1') )
        if CH == 2:
            return float( self.instr.ask('VOUT? 2') )    
        if CH == 3:
            return float( self.instr.ask('VOUT? 3') )                
        if CH == 4:
            return float( self.instr.ask('VOUT? 4') )                                       

    def __GetI__(self):
        '''This function gets the I Current'''
        if CH == 1:   
            return float( self.instr.ask('IOUT? 1') )  
        if CH == 2:
            return float( self.instr.ask('IOUT? 2') )          
        if CH == 3:
            return float( self.instr.ask('IOUT? 3') ) 
        if CH == 4:
            return float( self.instr.ask('IOUT? 4') )           
    
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
   