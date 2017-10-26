# Author: Tom MacLeod
# Rev History --------------------
# Date: 08/08/2008
# Created Debugged! (Thanks Eric)
# --------------------------------
# Date: 07/30/2008
# Created (Not Debugged!)
# --------------------------------
# Purpose: This module is a generic GPIB wrapper for:
# Agilent Technologies 11713A Attenuator / Switch
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class Agilent11713A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1, y_attn_val=110):
        GPIBObjectBaseClass.__init__(self, '--(unknown)--', addr)

        if (y_attn_val != 90 or y_attn_val != 110):
            assert('Unknown attn attached.')

        self._lut_x = [ 'B1234',  'A1B234', 'A2B134',  'A12B34', 'A4B123',
                        'A14B23', 'A24B13', 'A124B3', 'A34B12', 'A134B2' ]

        if y_attn_val == 110:
            self._lut_y = [ 'B5678',  'A5B678', 'A6B578', 'A56B78', 'A8B567', 'A58B67',
                            'A68B57', 'A568B7', 'A78B56', 'A578B6', 'A678B5', 'A5678' ]
        elif y_attn_val == 90:
            self._lut_y = [ 'B5678', 'A5B678', 'A6B578', 'A7B568', 'A57B68', 'A67B58',
                            'A78B56', 'A578B6', 'A678B5', 'A5678' ]

        self.__delay__ = delay
        
    def _atten_to_str(self, atten):
        '''Converts atten to a string'''
        try:
            if atten < 0:
                return ''
        
            x = int(atten) % 10
            y = int(atten) / 10
            
            #print x, y
            
            st_x = self._lut_x[x]
            st_y = self._lut_y[y]
            
            return st_x + st_y
        
        except:
            return ''
        
    def __SetAtten__(self, atten):
        '''This function sets the 11713A attenuation'''
        st = self._atten_to_str( atten )
        if st:
            self.instr.write( st )
            time.sleep(self.__delay__)
        else:
            print 'Error: Invalid attenuation request'
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    Atten       = property(None, __SetAtten__,   None, "Sets the 11713A Attenuation")
    Attenuation = property(None, __SetAtten__,   None, "Sets the 11713A Attenuation")
    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")
    
if __name__ == '__main__':
    at = Agilent11713A(29, y_attn_val=90)
        
    at.Atten = 93
