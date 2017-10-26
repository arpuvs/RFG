# Author: Lloyd Weida
# Date: 12/18/2013
# ---------------------------------------------------------------------
# Purpose: This module is a generic GPIB wrapper for:
# Keithley 2700 Multimeter
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass

class Keithley2700(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        GPIBObjectBaseClass.__init__(self, 'Keithley2700', addr)

    
    def __SetMeasContinuous__(self):
        '''This function gets the Keithley2700 in continuous read mode'''
        self.instr.write( ':initiate:continuous on '  )
    
    def __Config2wireResistance__(self):
        '''This function gets the Keithley2700 in continuous read mode'''
        self.instr.write( 'CONFigure:RESistance '  )    
    
    def __GetVoltage__(self):
        '''This function gets the Keithley2700 Voltage'''
        return float(self.instr.ask(':measure:voltage:dc?'))
    
    def __GetCurrent__(self):
        '''This function gets the Keithley2700 Current'''
        return float(self.instr.ask(':measure:current:dc?'))
    
    def __GetResistance__(self):
        '''This function gets the Keithley2700 Resistance'''
        return float(self.instr.ask('MEAS:RES?'))
    
    def __Get4wireResistance__(self):
        '''This function gets the Keithley2700 4 Wire Resistance'''
        return float(self.instr.ask('MEAS:FRES?'))
    
    
    
    def __Set_Voltage_NPLC__(self, NPLC): 
        '''This function sets the number of power line cycles for the voltage measurement'''
        self.instr.write( ':VOLTage:NPLCycles ' + str(NPLC) )
    def __Get_Voltage_NPLC__(self, NPLC): 
        '''This function gets the number of power line cycles for the voltage measurement'''
        return float(self.instr.ask(':VOLTage:NPLCycles?'))           

    def __Set_Current_NPLC__(self, NPLC): 
        '''This function sets the number of power line cycles for the current measurement'''
        self.instr.write( ':CURRent:NPLCycles ' + str(NPLC) )
    def __Get_Current_NPLC__(self, NPLC): 
        '''This function gets the number of power line cycles for the current measurement'''
        return float(self.instr.ask(':CURRent:NPLCycles?'))   

    def __Set_2wire_NPLC__(self, NPLC): 
        '''This function sets the number of power line cycles for the 2wire measurement'''
        self.instr.write( ':RES:NPLCycles ' + str(NPLC) )
    def __Get_2wire_NPLC__(self, NPLC): 
        '''This function gets the number of power line cycles for the 2wire measurement'''
        return float(self.instr.ask(':RES:NPLCycles?'))   

    def __Set_4wire_NPLC__(self, NPLC): 
        '''This function sets the number of power line cycles for the 4wire measurement'''
        self.instr.write( ':FRES:NPLCycles ' + str(NPLC) )
    def __Get_4wire_NPLC__(self, NPLC): 
        '''This function gets the number of power line cycles for the 4wire measurement'''
        return float(self.instr.ask(':FRES:NPLCycles?'))   
       
     
       
    Voltage         = property(__GetVoltage__,      None, None, "Gets the Keithley2700 Voltage")
    Current         = property(__GetCurrent__,      None, None, "Gets the Keithley2700 Current")
    Resistance      = property(__GetResistance__,   None, None, "Gets the Keithley2700 2-Wire Resistance")
    FourWireResistance      = property(__Get4wireResistance__,   None, None, "Gets the Keithley2700 4-Wire Resistance")
