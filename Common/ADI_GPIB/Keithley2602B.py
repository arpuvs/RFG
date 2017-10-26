# Author: TMarc Barnett
# Date: 03/1/2013 
# Purpose: This module is a generic GPIB wrapper for:
# Keithley 2602B
#------------------------------------------------------------------------
# Status: Alpha!
import ADI_GPIB
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import isscalar
import time
from ADI_GPIB.Keithley3706 import *
import os, sys, re

class Keithley2602B(GPIBObjectBaseClass):
    def __init__(self, addr=-1,  delay = 0.1):
        GPIBObjectBaseClass.__init__(self, 'TSP>', addr)
        self.__config_done__ = False        
        self.__vrange__ = 6             # 6V default range        
        self.__nplc__ = 1               # nplc to 1
        self.__curr_compliance__ = 2e-3 # 2mA as current compliance
        self.__num_points__ = 101       # 101 No. of data points
        self.Reset()
    
    def Set_Num_Points(self, value):
        assert(value > 0)
        self.__num_points__ = value

    def Reset(self):
        self.instr.clear()
        self.instr.write("reset()")        
        self.Reset_SMUA()
        self.Reset_SMUB()

    def Reset_SMUA(self):
        self.instr.write('smua.reset()')
        
    def Reset_SMUB(self):
        self.instr.write('smub.reset()')
        
    def WaitComplete(self):
        self.instr.write('waitcomplete()')
 
    def Beep(self, mode):
        self.instr.write('beeper.enable = %i' % (mode))
        self.instr.write('beeper.beep(1,980)')
        
    def DisplayScreen(self, mode):
        self.instr.write('display.screen = %i' % (mode))

##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxx  Auto Range Features  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def EnableSMUA_I_AutoRange(self, state): # 0 = OFF ; 1 = ON        
        self.instr.write('smua.measure.autorangei = %i' % (state))
            
    def EnableSMUB_I_AutoRange(self, state): # 0 = OFF ; 1 = ON
        self.instr.write('smub.measure.autorangei = %i' % (state))
    
    def EnableSMUA_V_AutoRange(self, state): # 0 = OFF ; 1 = ON
        self.instr.write('smua.measure.autorangev = %i' % (state))
        
    def EnableSMUA_V_AutoRange(self, state): # 0 = OFF ; 1 = ON
        self.instr.write('smub.measure.autorangev = %i' % (state))

##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        
##xxxxxxxxxxxxxxxxxxxxxxxxx  Turns SMUA & SMUB ON/OFF xxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        
    def SMUA_On(self, state):
        self.instr.write('smua.source.output = %i' % (state))
        
    def SMUB_On(self, state):
       self.instr.write('smub.source.output = %i' % (state))
        
    def SMUAB_On(self, state):
        self.instr.write('smua.source.output = %i' % (state))
        self.instr.write('smub.source.output = %i' % (state))

    def SMUA_Trigger(self):
        self.instr.write('smua.trigger.initiate()')

##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        
##xxxxxxxxxxxxxxxxxxxxxxx  Current & Voltage Compliance  xxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    
    def SMUA_I_Compliance(self, ilimit):   
        ilimit = float(ilimit)
        if ilimit > 5e-3 and ilimit < 0:
            raise "Outside the limits of :"         
        self.instr.write('smua.source.limiti = %f' % (ilimit))
        
    def SMUB_I_Compliance(self, ilimit):   
        ilimit = float(ilimit)
        if ilimit > 5e-3 and ilimit < 0:
            raise "Outside the limits of :"
        self.instr.write('smub.source.limiti = %f' % (ilimit))
        
    def SMUA_V_Compliance(self, vlimit):   
        vlimit = float(vlimit)
        if vlimit > 40 and vlimit < -40:
            raise "Outside the limits of :"         
        self.instr.write('smua.source.limitv = %f' % (vlimit))
        
    def SMUB_V_Compliance(self, vlimit):   
        vlimit = float(vlimit)
        if vlimit > 40 and vlimit < -40:
            raise "Outside the limits of :"         
        self.instr.write('smuv.source.limitv = %f' % (vlimit))

##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                
##xxxxxxxxxxxxxxxxxxxx  Current & Voltage Ranges  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        
    def Set_SMUA_I_Range(self, irange): # 100nA, 1uA, 10uA, 100uA, 1mA, 10mA, 100mA, 1A, 3A, 10A(pulsed only)
        self.instr.write('smua.source.rangei = %i' % (irange))
        
    def Set_SMUB_I_Range(self, irange): # 100nA, 1uA, 10uA, 100uA, 1mA, 10mA, 100mA, 1A, 3A, 10A(pulsed only)
        self.instr.write('smub.source.rangei = %i' % (irange))        
       
    def Set_SMUA_V_Range(self, vrange): # 100mV, 1v, 6v, 40v
        self.instr.write('smua.source.rangev = %i' % (vrange))
               
    def Set_SMUB_V_Range(self, vrange): # 100mV, 1v, 6v, 40v
        self.instr.write('smub.source.rangev = %i' % (vrange))

##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                
##xxxxxxxxxxxxxxxxxxxx  Data Buffer Functions  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def Clear_SMUA_nvbuffer1(self):
        self.instr.write('smua.nvbuffer1.clear()')
        
    def Clear_SMUB_nvbuffer1(self):
        self.instr.write('smub.nvbuffer1.clear()')
        
    def Clear_SMUA_nvbuffer2(self):
        self.instr.write('smua.nvbuffer2.clear()')

    def Clear_SMUB_nvbuffer2(self):
        self.instr.write('smub.nvbuffer2.clear()')
        
    def PrintBuffer(self):        
        self.instr.write('printbuffer(1,%d, smua.nvbuffer2, smua.nvbuffer1)' % self.__num_points__)
        self.WaitComplete()    

##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        
##    def xxxx(self):
##        self.instr.write('') 
##
##    def xxxx(self):
##        self.instr.write('')
##
##    def xxxx(self):
##        self.instr.write('') 
##    def xxxx(self):
##        self.instr.write('')
##
##    def xxxx(self):
##        self.instr.write('') 
##        
##    def xxxx(self):
##        self.instr.write('')
##
##    def xxxx(self):
##        self.instr.write('')
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxx  Linear  VSweep Parameters  xxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        
    def Set_Measurement_Delay(self, delay = 5e-3):
        self.__delay__ = delay
        self.instr.write('smua.source.delay = %f' % delay)
        
    def Set_Measurement_Integration_Interval(self, value):
        self.__nplc__ = value # Ranges are .001 to 25 ; 1 PLC for 60Hz is 16.67mS (1/60)
        self.instr.write('smua.measure.nplc = %f' % (value))
                
    def Set_Linear_VSweep_Config(self, start_voltage, stop_voltage):
        start_voltage = float(start_voltage)
        stop_voltage = float(stop_voltage)        
        
        self.instr.write('smua.source.func = smua.OUTPUT_DCVOLTS')
        self.instr.write('smua.source.levelv = 0')
        
        self.Set_SMUA_V_Range(self.__vrange__)        
        self.SMUA_I_Compliance(self.__curr_compliance__)        
        self.EnableSMUA_I_AutoRange(0) # Disable Autorange
        self.Set_Measurement_Integration_Interval(self.__nplc__)
        self.Set_Measurement_Delay()
        self.Clear_SMUA_nvbuffer1()
        self.Clear_SMUA_nvbuffer2()
        
        self.instr.write('smua.trigger.measure.action = smua.ENABLE')
        self.instr.write('smua.trigger.measure.iv(smua.nvbuffer1, smua.nvbuffer2)')        
        
        self.instr.write('smua.trigger.count = %d' % self.__num_points__)
        self.instr.write('smua.trigger.endpulse.action = smua.SOURCE_HOLD')
        self.instr.write('smua.trigger.endsweep.action = smua.SOURCE_IDLE')
        self.instr.write('smua.trigger.source.action = smua.ENABLE')
        self.instr.write('smua.trigger.source.linearv(%f, %f, %d)' % (start_voltage, stop_voltage, self.__num_points__))
        self.instr.write('smua.trigger.source.limiti = %f' % self.__curr_compliance__)
        
        #self.instr.write('smua.source.delay = 0.005')        
        
        self.__config_done__ = True
        
    def Start_Linear_VSweep(self):
        if (self.__config_done__ == False):
            raise Exception("Set_Linear_VSweep_Config needs to be called first")
        self.SMUA_On(1)	        
        self.SMUA_Trigger()
        self.WaitComplete()
        self.SMUA_On(0)        

    def SaveCSV( self, filename, mode = 'a' ):
        '''
        Saves a CSV spreadsheet of the current graph in the format we want
        
        mode = 'w' or 'a', write will overwrite the file, and append will append
               to the csv file
        '''         
        f_dest = open(filename, mode)
        read_values = self.instr.read_values()    
        step = len(read_values)/self.__num_points__
        
        header_line = "NO.,VSWEEP(V),ISWEEP(A)\n"
        f_dest.write(header_line)
        
        for i in range(0, len(read_values), step):
            v, c = read_values[i:i+step]
            line = "%d,%+1.6f,%+1.6f\n" % ((i/step)+1,v, c)
            f_dest.write(line)
            #print line.strip()
        f_dest.close()

tsp_script = """
	reset()
	
	-- Configure the SMU
	smua.reset()
	smua.source.func					= smua.OUTPUT_DCVOLTS
	smua.source.rangev                  = 4
	smua.source.limiti					= %f
	smua.measure.nplc					= %d
	smua.measure.delay					= smua.DELAY_AUTO

	-- Prepare the Reading Buffers
	smua.nvbuffer1.clear()
	smua.nvbuffer1.collecttimestamps	= 1
	smua.nvbuffer2.clear()
	smua.nvbuffer2.collecttimestamps	= 1

	-- Configure SMU Trigger Model for Sweep
	smua.trigger.source.linearv(%f, %f, %d)
	smua.trigger.source.limiti			= %f
	smua.trigger.measure.action			= smua.ENABLE
	smua.trigger.measure.iv(smua.nvbuffer1, smua.nvbuffer2)
	smua.trigger.endpulse.action		= smua.SOURCE_HOLD
	-- By setting the endsweep action to SOURCE_IDLE, the output will return
	-- to the bias level at the end of the sweep.
	smua.trigger.endsweep.action		= smua.SOURCE_IDLE
	smua.trigger.count					= numPoints
	smua.trigger.source.action			= smua.ENABLE
	-- Ready to begin the test

	smua.source.output					= smua.OUTPUT_ON
	-- Start the trigger model execution
	smua.trigger.initiate()
	-- Wait until the sweep has completed
	waitcomplete()
	smua.source.output					= smua.OUTPUT_OFF
	
	-- Print the data back to the Console in tabular format
	-- print("Time\tVoltage\tCurrent")
	-- Voltage readings are in nvbuffer2. Current readings are in nvbuffer1.
	printbuffer(1,smua.nvbuffer1.n, smua.nvbuffer1.timestamps, smua.nvbuffer2, smua.nvbuffer1)
""" % (.5, 1, 0, 2.4, 101, .5)

if __name__ == '__main__':    
    Keithley2602 = Keithley2602B(26)
    ##Keithley2602.instr.clear()
##    Keithley2602.instr.write("reset()")
##    Keithley2602.instr.write("start = 0")
##    Keithley2602.instr.write("stop  = 2.4")
##    Keithley2602.instr.write("numPoints = 101")
##    Keithley2602.instr.write("limitI = 0.5")
##    Keithley2602.instr.write("nplc = 1")
##    #-- Configure the SMU    
##    Keithley2602.instr.write("smua.reset()")
##    Keithley2602.instr.write("smua.source.func = smua.OUTPUT_DCVOLTS")
##    Keithley2602.instr.write("smua.source.rangev = 4")
##    Keithley2602.instr.write("smua.source.limiti = limitI")
##    Keithley2602.instr.write("smua.measure.nplc = nplc")
##    Keithley2602.instr.write("smua.measure.delay = smua.DELAY_AUTO")
##    #-- Prepare the Reading Buffers
##    Keithley2602.instr.write("smua.nvbuffer1.clear()")
##    Keithley2602.instr.write("smua.nvbuffer1.collecttimestamps	= 1")
##    Keithley2602.instr.write("smua.nvbuffer2.clear()")
##    Keithley2602.instr.write("smua.nvbuffer2.collecttimestamps	= 1")
##    #-- Configure SMU Trigger Model for Sweep
##    Keithley2602.instr.write("smua.trigger.source.linearv(start, stop, numPoints)")
##    Keithley2602.instr.write("smua.trigger.source.limiti = limitI")
##    Keithley2602.instr.write("smua.trigger.measure.action = smua.ENABLE")
##    Keithley2602.instr.write("smua.trigger.measure.iv(smua.nvbuffer1, smua.nvbuffer2)")
##    Keithley2602.instr.write("smua.trigger.endpulse.action = smua.SOURCE_HOLD")
##    #-- By setting the endsweep action to SOURCE_IDLE, the output will return
##    #-- to the bias level at the end of the sweep.
##    Keithley2602.instr.write("smua.trigger.endsweep.action = smua.SOURCE_IDLE")
##    Keithley2602.instr.write("smua.trigger.count = numPoints")
##    Keithley2602.instr.write("smua.trigger.source.action = smua.ENABLE")
##    #-- Ready to begin the test
##    Keithley2602.instr.write("smua.source.output = smua.OUTPUT_ON")
##    #-- Start the trigger model execution
##    Keithley2602.instr.write("smua.trigger.initiate()")
##    #-- Wait until the sweep has completed
##    Keithley2602.instr.write("waitcomplete()")    
##    #Keithley2602.instr.write("printbuffer(1, 1, smua.nvbuffer1.timestamps, smua.nvbuffer1)")
##    #Keithley2602.instr.write('savebuffer(smua.nvbuffer1, "csv", "mybuffer.csv")')
##    Keithley2602.instr.write("for x=1,smua.nvbuffer1.n do print(smua.nvbuffer1.timestamps[x], smua.nvbuffer2[x], smua.nvbuffer1[x]) end")
##    
##    for line in tsp_script.split('\n'):
##        line = line.strip()
##        while (line.count("  ") or line.count('\t')):
##            line = line.replace('\t', " ")
##            line = line.replace("  ", " ")
##        if (line == '' or line.startswith('--')):continue
##        print line
##        Keithley2602.instr.write(line)
    
##    Keithley2602.instr.write(tsp_script)    
##    read_values = Keithley2602.instr.read_values()    
##    for i in range(0, len(read_values), 3):
##        t, v, c = read_values[i:i+3]
##        print "%+1.3f, %+1.3f, %+1.6f" % (t, v, c)

##    Keithley = Keithley3706(27)
##    start_voltage = 0
##    stop_voltage = 2.6
##    number_of_datapoints = 101
##    I_comp = .03
##    #
##    Keithley2602.Reset_SMUA()
##    time.sleep(1)
##    Keithley2602.MakeDataBuffer()
##    for i in range(1,101,1):
##       Keithley2602.GetData( i)
##    print TestBuffer
##    Keithley2602.AutoRange(1)
##    time.sleep(1)
##    Keithley2602.Set_VSweep_Enable(1)
##    time.sleep(1)
##    Keithley2602.DisplayScreen(0)
##    time.sleep(1)
##    #Keithley2602.V_Range(40)
##    Keithley2602.I_Compliance(I_comp)
##    time.sleep(1)
##    Keithley2602.Linear_VSweep_Config(start_voltage,stop_voltage,number_of_datapoints)
##    time.sleep(1)
##    Keithley2602.SMUA_On(1)
##    time.sleep(1)
##    Keithley2602.Start_Linear_VSweep()
##    time.sleep(1)
##    #kb.DisplayClear()
##    Keithley2602.Beep(1)
##    time.sleep(1)
##    Keithley2602.Beep(980)
##    #mode = 0
##    Keithley2602.SMUA_On(0)
##    Keithley2602.SMUAB_On(0)
##    kb.SetTriggerMode(2, TRIGGER_RISING)
##    
##    images = {}
##    images["PD0m"] = 1006
##    images["PD0p"] = 1007
##    images["DRGND"] = [4013, 4039, 4083]
##    images["DRVDD"] = [4012, 4040, 4082]
##    
##    kb.SetImages(images)
##    
##    #kb.ExclusiveClose(["DRGND", "DRVDD", 1003] + DEFAULT_BACKPLANE_CONFIG)
##    
##    kb.Close("DRGND")
##    kb.Close(1003)
##    kb.Close(["DRGND", 1003, 1004])
##    
##    kb.Open("DRGND")
##    kb.Open(["DRGND", 1003])