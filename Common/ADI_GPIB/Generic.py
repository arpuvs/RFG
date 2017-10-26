# Author: Tom MacLeod
# Date: 10/22/2008
# Version: 0.1 Beta!
# Purpose: This module is a generic GPIB wrapper for:
# Any Generic device.  This helps a programmer issue commands without
# the need for work arounds.
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
import string

class Generic(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, '', addr)
        self.__delay__ = delay

    def Register(self, name, command, n_of_vars=0):
        '''This function registers a function call and binds it to this class.
           
           Parameters:
               name      > (str) - the name of the function
               command   > (str) - the GPIB command to be sent (this includes any type
                                   conversions necessary on the vars parameter)
                                   this can also end in a '?' for Ask() requests
               n_of_vars > (int) - the number of variables to be passed
               
            Example:
                Inst.Register('Frequency', 'FREQ %fMHz', 1)
                --later in code--
                Instr.Frequency(2.3)
        '''
        try:
            if name == 'Write' or name == 'Ask' or name == 'Register':
                raise Exception("'name' parameter not valid")
            
            if n_of_vars < 0:
                raise Exception("'n_of_vars' must be positive")
            
            if command[-1] == '?':
                exec "class C:\n def __init__(self,f):\n  self.f=f\n def func(self):\n  return self.f('%s')" % (command)
                c = C(self.Ask)
            else:
                if n_of_vars == 0:
                    exec "class C:\n def __init__(self,f):\n  self.f=f\n def func(self):\n  self.f('%s')" % (command)
                    c = C(self.Write)
                else:
                    param_lst = [chr(x + 65) for x in xrange(n_of_vars)]
                    param_str = string.join(param_lst, ',')
                    
                    exec "class C:\n def __init__(self,f):\n  self.f=f\n def func(self,%s):\n  self.f('%s' %% (%s))" % (param_str, command, param_str)
                    c = C(self.Write)

            # Execute st and create a 'local' function
            exec "%s = c.func" % (name)
                        
            # Make the local function an attribute of this class
            sa = "setattr(self, '%s', %s)" % (name, name)
            exec sa
            
        except Exception, inst:
            print 'ERROR: ' + str(inst)

    def Write(self, command):
        '''This function writes to the host GPIB instrument "command"'''
        self.instr.write(command)
        time.sleep(self.__delay__)
                
    def Ask(self, command):
        '''This function asks the host GPIB instrument "command" and returns
           the response'''
        return self.instr.ask(command)
        
#This code is used to debug this module
if __name__ == '__main__':
    G = Generic(12)
        
    G.Register('SetFreq', 'FREQ %fMHz', 1)
    G.Register('GetFreq', 'FREQ?')
    
    G.SetFreq(2.3)
    
    print G.GetFreq()
    
        