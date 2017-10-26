# Author: Tom MacLeod and Marc Barnet
# Date: 04/15/2010 (Tax Day!)
# Purpose: This module is a generic GPIB wrapper for:
# Keithley 3706
#------------------------------------------------------------------------
# Status: Alpha!

from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import isscalar
import time

TRIGGER_FALLING = 1
TRIGGER_RISING = 2
BREAK_BEFORE_MAKE = 1
POLE_ONE = 1
POLE_TWO = 2
DEFAULT_BACKPLANE_CONFIG = [1913, 1923, 2913, 2923, 4914, 4924, 5914, 5924]

class fake_instr:
    def write(self, x):
        print x

class Keithley3706(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1, mode=TRIGGER_FALLING):
        GPIBObjectBaseClass.__init__(self, 'TSP>', addr)
      
##        self.instr = fake_instr()
    
        # Initialization of Keithley box
        #self.Reset()
        #time.sleep(2)
        
        self.images_dict = None
        
        self.SetPole('slot1', POLE_ONE)
        self.SetPole('slot4', POLE_ONE)
        self.ExclusiveClose(DEFAULT_BACKPLANE_CONFIG)
        
        self.SetTriggerMode(1, mode)
        self.SetTriggerMode(2, mode)
        
        self.SetConnectionRule(BREAK_BEFORE_MAKE)
        
        self.trigger_wait = 40
        self.channel_wait = 0.1
        self.delay = 0.6
    
    def Beep(self):
        self.instr.write('beeper.beep(1,980)')
                
    def Close(self, relays):
        '''Inclusively closes the relays provided.  Relays can be a scalar or list'''
        #try:
        if isscalar(relays):
            parameter = str(relays)
        else:
            explicit_list = []
            for relay in relays:
                if (self.images_dict):
                    if (relay in self.images_dict):
                        value = self.images_dict[relay]
                        if (isscalar(value)):
                            explicit_list += [value]
                        else:
                            explicit_list += value
                    else:
                        explicit_list += [relay]
                else:
                    explicit_list += [relay]
            parameter = str(explicit_list)[1:-1]
        self.instr.write('channel.close("%s")' % (parameter))
        #except:
        #   print 'ERROR: Unable to close relay(s)', relays
    
    def DisplayClear(self):
        '''Clears the display text'''
        self.instr.write('display.clear()')
    
    def ExclusiveClose(self, relays=None):
        '''Exclusively closes only the relays provided.  If none are provided, 
           it will open all relays.'''
        try:
            if (relays is None):
                parameter = ''
            elif (isscalar(relays)):
                if (self.images_dict):
                    if (relays in self.images_dict):
                        value = self.images_dict[relays]
                        if (isscalar(value)):
                            parameter = str(value)
                        else:
                            parameter = str(value)[1:-1]
                    else:
                        parameter = str(relays)
                else:
                    parameter = str(relays)
            else:
                explicit_list = []
                for relay in relays:
                    if (self.images_dict):
                        if (relay in self.images_dict):
                            value = self.images_dict[relay]
                            if (isscalar(value)):
                                explicit_list += [value]
                            else:
                                explicit_list += value
                        else:
                            explicit_list += [relay]
                    else:
                        explicit_list += [relay]
                parameter = str(explicit_list)[1:-1]
            self.instr.write('channel.exclusiveclose("%s")' % (parameter)) 
        except:
            print 'ERROR: Unable to ExclusiveClose(', relays, ')'
    
    def ExternalTrigger(self, chan_assert=2, chan_wait=1):
        '''Asserts the external trigger'''
        self.TriggerAssert(chan_assert)
        self.TriggerClear(chan_assert)
        
        time.sleep(self.delay)
        
        self.TriggerWait(chan_wait)
        self.TriggerClear(chan_wait)
        
        time.sleep(self.channel_wait)
                    
    def Open(self, relays):
        '''Inclusively closes the relays provided.  Relays can be a scalar or list'''
        try:
            if isscalar(relays):
                parameter = str(relays)
            else:
                explicit_list = []
                for relay in relays:
                    if (self.images_dict):
                        if (relay in self.images_dict):
                            value = self.images_dict[relay]
                            if (isscalar(value)):
                                explicit_list += [value]
                            else:
                                explicit_list += value
                        else:
                            explicit_list += [relay]
                    else:
                        explicit_list += [relay]
                parameter = str(explicit_list)[1:-1]
            self.instr.write('channel.open("%s")' % (parameter))
        except:
            print 'ERROR: Unable to open relay(s)', relays
    
    def Reset(self):
        '''Master Reset for the Keithley'''
        self.instr.write('reset()')
        
    def SetConnectionRule(self, rule):
        '''Sets the connection rule'''
        try:
            self.instr.write('channel.connectrule = %i' % (rule))
        except:
            print 'ERROR: Unable to set connection rule ', rule
    
    def SetImages(self, images_dict):
        '''Sets images (aliases) for relays from an images dictionary.  Each
           key is tied to either a relay or list of relays associated with 
           that particular key'''
        try:
            self.images_dict = images_dict
            for key in images_dict:
                value = images_dict[key]
                if isscalar(value):
                    parameter = str(value)
                else:
                    parameter = str(value)[1:-1]
                self.instr.write('channel.pattern.setimage("%s", "%s")' % (parameter, key))
        except:
            print 'ERROR: Unable to write image(s)', images_dict
    
    def SetPole(self, slot, pole_setting):
        '''Sets the pole setting for the specified slot'''
        try:
            self.instr.write('channel.setpole("%s", %i)' % (slot, pole_setting))
        except:
            print 'ERROR: Unable to set the pole setting for slot %s, value %i' % (slot, pole_setting)
        
    def SetPulseWidth(self, index, pulse_width):
        '''Sets the Trigger pulse width for index-th channel'''
        try:
            self.instr.write('digio.trigger[%i].pulsewidth(%f)' % (index, pulse_width))
        except:
            print 'ERROR: Unable to set pulse_width ', pulse_width
    
    def SetText(self, text):
        '''Sets the text to be shown on the LCD'''
        self.instr.write('display.settext("%s")' % (text))
    
    def SetTriggerMode(self, index, mode=TRIGGER_FALLING):
        '''Sets the Trigger pulse width for index-th channel'''
        try:
            self.instr.write('digio.trigger[%i].mode = %i' % (index, mode))
            self.TriggerClear(index)
        except:
            print 'ERROR: Unable to set trigger mode ', mode
                    
    def TriggerAssert(self, index):
        '''Asserts the index-th trigger'''
        try:
            self.instr.write('digio.trigger[%i].assert()' % (index))
        except:
            print 'ERROR: Unable to assert trigger ', index
                    
    def TriggerClear(self, index):
        '''Clears the index-th trigger'''
        try:
            self.instr.write('digio.trigger[%i].clear()' % (index))
        except:
            print 'ERROR: Unable to clear trigger ', index
    
    def TriggerWait(self, index):
        '''Waits the index-th trigger'''
        try:
            self.instr.write('digio.trigger[%i].wait(%i)' % (index, self.trigger_wait))
        except:
            print 'ERROR: Unable to wait for trigger ', index
            
# Test Code
if __name__ == '__main__':
    
    Keithley = Keithley3706(27)
    #kb.DisplayClear()
    Keithley.Beep()
    
    
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