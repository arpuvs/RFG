# Author: Lloyd Weida

# Purpose: This module is a generic GPIB wrapper for:
# HP8116A HP Pulse/Function Generator 50MHz

#list of commands used:

# FRQ 400000.00 HZ
# HIL 2 V
# LOL 0 V
# DTY 50 %
# M1    (normal mode)
# W3    (select sq wave)


from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class HP8116A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'HP8116A', addr)
        self.instr.write('D1')  #disable output
 
        self.__delay__ = delay
              
                  
    def __SetHILV__(self,V1):       
        '''This function sets the Hi level Voltage'''        
        self.instr.write( 'HIL ' + str(V1) + ' V' )
        time.sleep(self.__delay__)

    def __SetLOLV__(self,V1):       
        '''This function sets the Lo level Voltage'''        
        self.instr.write( 'LOL ' + str(V1) + ' V' )
        time.sleep(self.__delay__)
		
    def __SetFreq__(self,Freq,CH=0):
        '''This function sets the frequency'''
        self.instr.write( 'FRQ ' + str(Freq) + ' Hz' )
        time.sleep(self.__delay__)       
               
    def __SetDTY__(self,duty,CH=0):
        '''This function sets the duty cycle'''
        self.instr.write( 'DTY ' + str(duty) + ' %' )
        time.sleep(self.__delay__)       
                           
    def __SetEnable__(self,  Enabled):
        '''This function enables the On/Off for the Pulse generator'''
        if Enabled:
            self.instr.write('D0')
        else:
            self.instr.write('D1')
    
    def __SetNorm__(self):
        '''This function sets the normal mode'''
        self.instr.write( 'M1' )
        time.sleep(self.__delay__)                                       

    def __SetSqWave__(self):  #set sq wave
        self.instr.write( 'W3' )
        time.sleep(self.__delay__)   
		
    # def __GetI__(self):
        # '''This function gets the I Current'''
        # if CH == 1:   
            # return float( self.instr.ask('IOUT? 1') )  
        # if CH == 2:
            # return float( self.instr.ask('IOUT? 2') )          
        # if CH == 3:
            # return float( self.instr.ask('IOUT? 3') ) 
        # if CH == 4:
            # return float( self.instr.ask('IOUT? 4') )           
    
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
   