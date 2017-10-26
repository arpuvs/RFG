# Author: Snehal Prabhu
# Date: 08/29/2012
# Status: Implemented Command set for TJ -4 ( Thermojet)
# Derived from Turbojet Code
# ---------------------------------------------------------------


from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time

AF_MAX = 15
AF_MED = 10
AF_MIN = 5

class ThermoJet(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=30):
        GPIBObjectBaseClass.__init__(self, '', addr)        
        self.instr.term_chars = '\n'
        
        #This code is to fix some odd bug in writing to the 
        #temp machine the first time
        self.__delay__ = 0.1
        self.__SetTemp__(25)
        self.__SetTemp__(25)
        
        #Continue with normal operation        
        self.__delay__   = delay
        
#Arm Movement Functions       
    def MoveArmUp(self):
        '''This function moves the ThermoJet arm up'''
        self.instr.write('AU')
        time.sleep(4)
    
    def MoveArmDown(self):
        '''This function moves the ThermoJet arm down'''
        self.instr.write('AD')
        time.sleep(4)
    
    def MoveArmIn(self):
        '''This function is not supported in the ThermoJet'''
        print('This function - MoveArmIn is not supported in the ThermoJet')
    
    def MoveArmOut(self):
        ''''This function is not supported in the ThermoJet'''
        print('This function - MoveArmOut is not supported in the ThermoJet')
        
#Status/ Read Functions
    def __GetTemp__ ( self ) :
        '''This function returns the Thermojet system DUT/Nozzle temperature'''
        #Temp_sys = self.instr.ask( '?PV' )
        return float( self.instr.ask( '?PV' ) )
    
    def __GetDUTTemp__ ( self ) :
        '''This function returns the Thermojet DUT temperature'''
        #Temp_DUT = self.instr.ask( '?TD' )
        return float( self.instr.ask( '?TD' ) )
    
    def __GetNozzleTemp__ ( self ) :
        '''This function returns the Thermojet Nozzle temperature'''
        #Temp_Nozzle = self.instr.ask( '?TA' )
        return float ( self.instr.ask( '?TA' ) )
    
    def __GetAirFlow__ ( self ) :
        '''This function returns the Thermojet Airflow Set Point'''
        #AirFlow = self.instr.ask( '?AF' )
        return float( self.instr.ask( '?AF' ) )
   
# Idle Mode / Proram Mode Functions
    def SetIdleMode(self):
        '''This function puts the ThermoJet into idle mode'''
        self.instr.write('ID')
        
    def SetProgramRun(self):
        '''This function puts the ThermoJet into Program mode'''
        self.instr.write('RP')
        
    def SetProgramHalt(self):
        '''This function halts the ThermoJet in Program mode'''
        self.instr.write('HL')
        
    def SetProgramContinue(self):
        '''This function continues the ThermoJet in Program mode'''
        self.instr.write('CN')
        
# Temperature / Airflow Functions           
    def __SetTemp__(self,Temp,Mode=2):
        '''This function sets the ThermoJet temperature'''
        
        Temp = clip(Temp, -60, 140)
        #self.instr.write('WI,10')
        #time.sleep(0.1)
        self.instr.write('RM' + str(Mode))
        time.sleep(0.1)
        self.instr.write('SP' + str (Mode) + str(Temp))
        time.sleep(self.__delay__)
    
    def __SetAirFlow__(self, AirFlow):
        '''This function sets the TurboJet airflow'''
        self.__airflow__ = AirFlow
        self.instr.write('AF' + str(self.__airflow__))
        time.sleep(0.1)
    
    def BeginDeFrost(self):
        '''This function befins the defrost operation'''
        self.instr.write('DF')
 
 # General Functions   
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    Temp    = property( __GetTemp__, __SetTemp__,     None, "Gets the ThermoJet temperature")
    AirFlow = property(__GetAirFlow__,__SetAirFlow__,  None, "Sets the ThermoJet airflow")
    Delay   = property(__GetDelay__, __SetDelay__,    None, "Delay")