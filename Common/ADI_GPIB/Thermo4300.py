# Author: Tom MacLeod
#
# Date: 05/20/2014 L.Magaldi
# changed low end set point to -60 from -50C   
#
# Date: 12/28/2007 (Dave Shoudy)
#       Debugged an error with the __init__ function
#
# Date: 8/7/2007
# Status: Several mods by Dave Shoudy:
#   - Debugged SetIdleMode and SetAirFlow functions
#   - Added FlowON and OFF functions
#   - Added high/low temp parameters for initializing the class
#   - Debugged SetTemp function to properly select the setpoint based on the desired temp.
#   - Added EnableDUTMode function
# Date: 11/11/2006
# Status: Added arm control functions and idlemode control
# ----------------------------------------------------------------
# Date: 11/09/2006
# Status: Debugged!
# Purpose: This module is a generic GPIB wrapper for:
# Thermo4300

from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time

AF_MAX = 8
AF_MED = 5
AF_MIN = 0

class Thermo4300(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=30, HighTemp=140, LowTemp=-60):    # Added paramters to this
        GPIBObjectBaseClass.__init__(self, '', addr)
        #This code is to fix some odd bug in writing to the 
        #temp machine the first time
        self.__delay__   = 0.1
        self.__airflow__ = AF_MAX
        
        #Reset Thermo4300
        #self.instr.write( '*RST' )
        #self.instr.write( 'RSTO' )
        
        #Set Air Mode by default
        self.__SetupAirMode__(HighTemp,LowTemp)

        #Continue with normal operation        
        self.__delay__   = delay
        self.__airflow__ = AF_MAX
    
    def __SetupAirMode__(self, HighTemp=90, LowTemp=-60, TestTime=230):
        '''This function sets up the Thermo4300 fir Air Mode'''
        #Set air mode
        self.instr.write( 'DUTM 0' )
        
        #Trickle keeps flexline hose cold
        #self.instr.write( 'TRKL 1' )
        
        #Turn compressor on
        #self.instr.write( 'COOL 1' )
        
        #Set main airflow at head output nozzle
        self.instr.write( 'FLSE %s' % str(self.__airflow__) )
        
        #Set air temp high limit
        self.instr.write( 'ULIM %s' % str(HighTemp) ) 
        
        #Set air temp lower limit
        self.instr.write( 'LLIM %s' % str(LowTemp) )
        
        #Set DUT sensor to None
        self.instr.write( 'DSNS 0' )
        
        #Set max test time
        self.instr.write( 'TTIM %s' % str(TestTime) )
    
    def __EnableDUTMode__(self,SensorType='T'):
        #Set DUT sensor (no RTD/diode support in this code yet)
        if SensorType == 'T':
            self.instr.write( 'DSNS 1' )
        elif SensorType == 'K':
            self.instr.write( 'DSNS 2' )
        else:
            self.instr.write( 'DSNS 0' )
        
        #Set DUT mode
        self.instr.write( 'DUTM 1' )
        
    def __SetupDUTMode__(self, HighTemp=90, LowTemp=-60, SensorType='T', TestTime=230):
        '''This function sets up the Thermo4300 fir Air Mode'''
        #Set DUT mode
        self.instr.write( 'DUTM 1' )
        
        #Trickle keeps flexline hose cold
        self.instr.write( 'TRKL 0' )
        
        #Turn compressor on
        #self.instr.write( 'COOL 1' )
        
        #Set main airflow at head output nozzle
        self.instr.write( 'FLSE %s' % str(self.__airflow__) )
        
        #Set air temp high limit
        self.instr.write( 'ULIM %s' % str(HighTemp) )
        
        #Set air temp lower limit
        self.instr.write( 'LLIM %s' % str(LowTemp) )
        
        #Set DUT sensor to None
        if SensorType == 'T':
            self.instr.write( 'DSNS 1' )
        elif SensorType == 'K':
            self.instr.write( 'DSNS 2' )
        else:
            self.instr.write( 'DSNS 0' )
        
        #Set max test time'  
        self.instr.write( 'TTIM %s' % str(TestTime) )
        
    def __MoveArmUp__(self):
        '''This function moves the Thermo4300 arm up'''
        self.instr.write('HEAD 0')
        time.sleep(4)
    
    def __MoveArmDown__(self):
        '''This function moves the Thermo4300 arm down'''
        self.instr.write('HEAD 1')
        time.sleep(4)
    
    def __SetIdleMode__(self):
        '''This function puts the Thermo4300 into idle mode''' 
        self.instr.write('FLOW 0')
        self.instr.write('TRKL 0')
        #self.instr.write('COOL 0')   
     
    def __FlowOFF__(self):
        self.instr.write('FLOW 0')
        self.instr.write('TRKL 0')
    
    def __FlowON__(self):
        self.instr.write('FLOW 1')
           
    def __SetTemp__(self, Temp):
        '''This function sets the Thermo4300 temperature'''
        Temp = clip(Temp, -60, 140)
        if(Temp <= 15):                         
            self.instr.write('SETN 2')  # Cold setpoint
        elif ((Temp > 15) and (Temp < 35)):     
            self.instr.write('SETN 1')  # Ambient setpoint
        else:                                   
            self.instr.write('SETN 0')  # Hot setpoint
        
        self.instr.write('SETP %s' % str(Temp)) # Set temp
        time.sleep(self.__delay__)
    
    def __SetAirFlow__(self, AirFlow):
        '''This function sets the Thermo4300 airflow'''
        self.__airflow__ = AirFlow
        self.instr.write('FLSE %s' % str(self.__airflow__))
        time.sleep(0.1)
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    def __GetTemperature__(self):
        '''This function gets the Thermostream Temperature'''
        return float(self.instr.ask('TMPA?'))
 
    def __GetDutTemperature__(self):
        '''This function gets the Thermostream Temperature'''
        return float(self.instr.ask('TMPD?'))

    def __SetDutThermalConst__(self, Const):
        '''This function sets the DUT thermal Constant'''
        self.instr.write('DUTC %s' % str(Const)) # Set temp

    def __SetDutDtype__(self, Dtype):
        '''This function sets the DUT thermal Constant'''
        self.instr.write('DTYP %s' % str(Dtype)) # Set temp

    Temp    = property(None,         __SetTemp__,     None, "Sets the Thermo4300 temperature")
    AirFlow = property(None,         __SetAirFlow__,  None, "Sets the Thermo4300 airflow")
    Delay   = property(__GetDelay__, __SetDelay__,    None, "Delay")